from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_rnf12_health_responde_ok():
    resposta = cliente.get("/health")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_rnf17_version_identifica_servico_e_commit(monkeypatch):
    monkeypatch.setenv("APP_COMMIT_SHA", "abc1234")
    resposta = cliente.get("/version")
    assert resposta.status_code == 200
    assert resposta.json() == {"servico": "notificacoes", "commit": "abc1234"}


def test_rnf17_version_sem_sha_devolve_desconhecido(monkeypatch):
    monkeypatch.delenv("APP_COMMIT_SHA", raising=False)
    resposta = cliente.get("/version")
    assert resposta.json() == {"servico": "notificacoes", "commit": "desconhecido"}
