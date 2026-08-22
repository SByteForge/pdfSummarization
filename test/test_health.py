import json
import urllib.error

from src.health import check_ollama


class _FakeResponse:
    def __init__(self, payload):
        self._payload = json.dumps(payload).encode()

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_check_ollama_reachable(monkeypatch):
    monkeypatch.setattr(
        "src.health.urllib.request.urlopen",
        lambda url, timeout: _FakeResponse({"models": [{"name": "llama3.2:1b"}, {"name": "mistral"}]}),
    )

    result = check_ollama(url="http://fake:11434")

    assert result["reachable"] is True
    assert result["models"] == ["llama3.2:1b", "mistral"]
    assert result["error"] is None


def test_check_ollama_unreachable(monkeypatch):
    def _raise(url, timeout):
        raise urllib.error.URLError("connection refused")

    monkeypatch.setattr("src.health.urllib.request.urlopen", _raise)

    result = check_ollama(url="http://fake:11434")

    assert result["reachable"] is False
    assert result["models"] == []
    assert result["error"] is not None
