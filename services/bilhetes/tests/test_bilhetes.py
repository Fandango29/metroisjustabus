from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)

CAMPOS_RF20 = {"id", "nome", "preco_centimos", "validade_minutos", "viagens", "condicoes"}


def test_rnf12_health_responde_ok():
    resposta = cliente.get("/health")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_rnf17_version_identifica_servico_e_commit(monkeypatch):
    monkeypatch.setenv("APP_COMMIT_SHA", "abc1234")
    resposta = cliente.get("/version")
    assert resposta.json() == {"servico": "bilhetes", "commit": "abc1234"}


def test_rf20_tipos_bilhete_tem_todos_os_campos():
    resposta = cliente.get("/tipos-bilhete")
    assert resposta.status_code == 200
    tipos = resposta.json()
    assert len(tipos) > 0
    assert all(CAMPOS_RF20 <= set(tipo) for tipo in tipos)


def test_rf20_precos_sao_inteiros_positivos_em_centimos():
    for tipo in cliente.get("/tipos-bilhete").json():
        assert isinstance(tipo["preco_centimos"], int)
        assert tipo["preco_centimos"] > 0
