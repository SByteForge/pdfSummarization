"""Governance: audit logging and policy enforcement for retrieval and generation.

Every retrieval (what chunks were pulled from the document) and every
generation (what the model produced) is logged to a local SQLite file, along
with simple enforced policies (query length limits, per-session rate
limiting). This is the audit trail the Cost Dashboard page reads from.

Honest limitation: this persists inside the running container's filesystem.
Without a mounted volume, it's lost if the container is recreated — fine for
a local demo, but a real deployment would point this at a durable, shared
store instead.
"""

import sqlite3
import time
import uuid
from contextlib import contextmanager

from src.config import Config

# Illustrative pricing only. Ollama runs locally and is free — there is no
# real bill. This exists purely to show what an equivalent call would have
# cost on a typical paid API, for cost-avoidance visibility.
ILLUSTRATIVE_PRICE_PER_1K_TOKENS = 0.002

MAX_QUERY_CHARS = 4000
MAX_GENERATIONS_PER_SESSION_PER_MINUTE = 10


class GovernanceError(Exception):
    """Raised when a request is blocked by a governance policy."""


def estimate_tokens(text: str) -> int:
    """Rough token estimate (~4 characters/token).

    Not exact: different Ollama models use different tokenizers, and there's
    no single correct count across models without loading each one's actual
    tokenizer. This is a transparent approximation, not a precise measurement.
    """
    return max(1, len(text) // 4)


@contextmanager
def _connection():
    conn = sqlite3.connect(Config.GOVERNANCE_DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    """Create the events table if it doesn't exist. Safe to call repeatedly."""
    with _connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                timestamp REAL NOT NULL,
                event_type TEXT NOT NULL,
                session_id TEXT,
                model TEXT,
                query TEXT,
                num_chunks INTEGER,
                input_tokens INTEGER,
                output_tokens INTEGER,
                latency_s REAL,
                estimated_cost_usd REAL,
                success INTEGER,
                error TEXT
            )
            """
        )


def check_query_policy(query: str) -> None:
    """Reject empty or excessively long queries before any pipeline work runs."""
    if not query or not query.strip():
        raise GovernanceError("Query is empty — refusing to process.")
    if len(query) > MAX_QUERY_CHARS:
        raise GovernanceError(f"Query exceeds the maximum allowed length ({MAX_QUERY_CHARS} chars).")


def check_rate_limit(session_id: str) -> None:
    """Reject requests once a session exceeds the per-minute generation limit."""
    cutoff = time.time() - 60
    with _connection() as conn:
        (count,) = conn.execute(
            "SELECT COUNT(*) FROM events "
            "WHERE session_id = ? AND event_type = 'generation' AND timestamp > ?",
            (session_id, cutoff),
        ).fetchone()
    if count >= MAX_GENERATIONS_PER_SESSION_PER_MINUTE:
        raise GovernanceError(
            f"Rate limit exceeded: max {MAX_GENERATIONS_PER_SESSION_PER_MINUTE} "
            "generations per minute per session."
        )


def log_retrieval(session_id: str, query: str, num_chunks: int, latency_s: float) -> None:
    with _connection() as conn:
        conn.execute(
            "INSERT INTO events (id, timestamp, event_type, session_id, query, num_chunks, latency_s, success)"
            " VALUES (?, ?, 'retrieval', ?, ?, ?, ?, 1)",
            (str(uuid.uuid4()), time.time(), session_id, query, num_chunks, latency_s),
        )


def log_generation(
    session_id: str,
    query: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    latency_s: float,
    success: bool,
    error: str | None = None,
) -> None:
    cost = (input_tokens + output_tokens) / 1000 * ILLUSTRATIVE_PRICE_PER_1K_TOKENS
    with _connection() as conn:
        conn.execute(
            "INSERT INTO events (id, timestamp, event_type, session_id, model, query, input_tokens,"
            " output_tokens, latency_s, estimated_cost_usd, success, error)"
            " VALUES (?, ?, 'generation', ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                str(uuid.uuid4()),
                time.time(),
                session_id,
                model,
                query,
                input_tokens,
                output_tokens,
                latency_s,
                cost,
                int(success),
                error,
            ),
        )


def get_events(event_type: str | None = None, limit: int = 200) -> list[dict]:
    sql = "SELECT * FROM events"
    params: list = []
    if event_type:
        sql += " WHERE event_type = ?"
        params.append(event_type)
    sql += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    with _connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]
