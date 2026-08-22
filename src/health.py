"""Lightweight Ollama connectivity check, used by the UI's pre-flight status indicator."""

import json
import urllib.error
import urllib.request

from src.config import Config

TIMEOUT_SECONDS = 2.0


def check_ollama(url: str | None = None, timeout: float = TIMEOUT_SECONDS) -> dict:
    """Check whether Ollama is reachable and list the models it has pulled.

    Returns a dict with keys: reachable (bool), models (list[str]), error (str | None).
    Never raises — this is a best-effort UI status check, not a hard dependency.
    """
    target = url or Config.OLLAMA_URL
    try:
        with urllib.request.urlopen(f"{target}/api/tags", timeout=timeout) as resp:
            payload = json.loads(resp.read())
        models = [m["name"] for m in payload.get("models", [])]
        return {"reachable": True, "models": models, "error": None}
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        return {"reachable": False, "models": [], "error": str(exc)}
