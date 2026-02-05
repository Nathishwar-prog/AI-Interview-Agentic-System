import importlib
import sys
import types
from pathlib import Path

from fastapi.testclient import TestClient


def test_health_check(monkeypatch):
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test.db")
    fake_openai = types.ModuleType("openai")
    fake_openai.OpenAI = lambda *args, **kwargs: object()
    monkeypatch.setitem(sys.modules, "openai", fake_openai)
    app_module = importlib.import_module("app.main")
    client = TestClient(app_module.app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
