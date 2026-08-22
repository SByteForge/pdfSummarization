import pytest

from src import governance
from src.governance import GovernanceError


@pytest.fixture(autouse=True)
def _isolated_db(tmp_path, monkeypatch):
    """Point governance at a throwaway SQLite file so tests never share state."""
    monkeypatch.setattr(governance.Config, "GOVERNANCE_DB_PATH", str(tmp_path / "test_governance.db"))
    governance.init_db()


def test_estimate_tokens_is_roughly_char_count_over_four():
    assert governance.estimate_tokens("a" * 40) == 10
    assert governance.estimate_tokens("") == 1  # floor of 1, never zero


def test_check_query_policy_rejects_empty_query():
    with pytest.raises(GovernanceError):
        governance.check_query_policy("   ")


def test_check_query_policy_rejects_oversized_query():
    with pytest.raises(GovernanceError):
        governance.check_query_policy("x" * (governance.MAX_QUERY_CHARS + 1))


def test_check_query_policy_allows_normal_query():
    governance.check_query_policy("Summarize this document.")  # should not raise


def test_rate_limit_blocks_after_threshold():
    session_id = "session-a"
    for _ in range(governance.MAX_GENERATIONS_PER_SESSION_PER_MINUTE):
        governance.check_rate_limit(session_id)  # should not raise yet
        governance.log_generation(session_id, "q", "model", 10, 10, 0.1, success=True)

    with pytest.raises(GovernanceError):
        governance.check_rate_limit(session_id)


def test_rate_limit_is_scoped_per_session():
    for _ in range(governance.MAX_GENERATIONS_PER_SESSION_PER_MINUTE):
        governance.log_generation("session-b", "q", "model", 10, 10, 0.1, success=True)

    governance.check_rate_limit("session-c")  # a different session should not be blocked


def test_log_and_retrieve_generation_event():
    governance.log_generation("session-d", "my query", "llama3.2:1b", 100, 50, 1.23, success=True)

    events = governance.get_events(event_type="generation")

    assert len(events) == 1
    event = events[0]
    assert event["session_id"] == "session-d"
    assert event["model"] == "llama3.2:1b"
    assert event["input_tokens"] == 100
    assert event["output_tokens"] == 50
    assert event["success"] == 1
    assert event["estimated_cost_usd"] == pytest.approx((100 + 50) / 1000 * governance.ILLUSTRATIVE_PRICE_PER_1K_TOKENS)


def test_log_generation_failure_records_error():
    governance.log_generation("session-e", "q", "model", 10, 0, 0.5, success=False, error="ollama unreachable")

    events = governance.get_events(event_type="generation")

    assert events[0]["success"] == 0
    assert events[0]["error"] == "ollama unreachable"


def test_log_and_retrieve_retrieval_event():
    governance.log_retrieval("session-f", "my query", num_chunks=4, latency_s=0.05)

    events = governance.get_events(event_type="retrieval")

    assert len(events) == 1
    assert events[0]["num_chunks"] == 4
    assert events[0]["query"] == "my query"


def test_get_events_filters_by_type():
    governance.log_retrieval("session-g", "q", num_chunks=2, latency_s=0.01)
    governance.log_generation("session-g", "q", "model", 10, 10, 0.1, success=True)

    assert len(governance.get_events(event_type="retrieval")) == 1
    assert len(governance.get_events(event_type="generation")) == 1
    assert len(governance.get_events()) == 2
