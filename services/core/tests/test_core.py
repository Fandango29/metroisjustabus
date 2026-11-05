from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_rnf12_health_responde_ok():
    resposta = cliente.get("/health")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_rnf17_version_devolve_sha_do_commit(monkeypatch):
    monkeypatch.setenv("APP_COMMIT_SHA", "abc1234")
    resposta = cliente.get("/version")
    assert resposta.status_code == 200
    assert resposta.json()["commit"] == "abc1234"


def test_rnf17_version_sem_sha_devolve_desconhecido(monkeypatch):
    monkeypatch.delenv("APP_COMMIT_SHA", raising=False)
    resposta = cliente.get("/version")
    assert resposta.json()["commit"] == "desconhecido"


def test_rf01_lista_linhas():
    resposta = cliente.get("/linhas")
    assert resposta.status_code == 200
    linhas = resposta.json()
    assert len(linhas) > 0
    assert all("id" in linha and "nome" in linha for linha in linhas)


def test_rf02_lista_paragens_de_uma_linha():
    resposta = cliente.get("/linhas/L1/paragens")
    assert resposta.status_code == 200
    ordens = [paragem["ordem"] for paragem in resposta.json()]
    assert ordens == sorted(ordens)


def test_rf02_linha_inexistente_devolve_404():
    resposta = cliente.get("/linhas/NAO-EXISTE/paragens")
    assert resposta.status_code == 404
