import pytest
from fastapi.testclient import TestClient

from app import dados
from app.main import app

cliente = TestClient(app)

CAMPOS_RF20 = {"id", "nome", "preco_centimos", "validade_minutos", "viagens", "condicoes"}


@pytest.fixture(autouse=True)
def sem_base_de_dados(monkeypatch):
    """Os testes unitários usam sempre os dados de app/dados.py, mesmo que DATABASE_URL exista."""
    monkeypatch.delenv("DATABASE_URL", raising=False)


def _tipo_inativo():
    return {
        "id": "ANTIGO",
        "nome": "Bilhete retirado de venda",
        "preco_centimos": 100,
        "validade_tipo": "minutos",
        "validade_minutos": 60,
        "viagens": 1,
        "condicoes": "Já não se vende.",
        "ativo": False,
    }


def _tipos_por_id():
    return {tipo["id"]: tipo for tipo in cliente.get("/tipos-bilhete").json()}


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


def test_rf20_tipos_bilhete_tem_os_quatro_tipos_do_a01():
    assert set(_tipos_por_id()) == {"SIMPLES", "DEZ_VIAGENS", "DIARIO", "MENSAL"}


def test_rf20_simples_tem_uma_viagem_e_dez_viagens_tem_dez():
    tipos = _tipos_por_id()
    assert tipos["SIMPLES"]["viagens"] == 1
    assert tipos["DEZ_VIAGENS"]["viagens"] == 10


def test_rf20_passes_diario_e_mensal_tem_viagens_ilimitadas():
    tipos = _tipos_por_id()
    assert tipos["DIARIO"]["viagens"] is None
    assert tipos["MENSAL"]["viagens"] is None


def test_rf20_passe_diario_vale_24_horas():
    diario = _tipos_por_id()["DIARIO"]
    assert diario["validade_tipo"] == "minutos"
    assert diario["validade_minutos"] == 24 * 60


def test_rf20_passe_mensal_vale_no_mes_civil():
    mensal = _tipos_por_id()["MENSAL"]
    assert mensal["validade_tipo"] == "mes_civil"
    assert mensal["validade_minutos"] is None
    assert mensal["preco_centimos"] == 4000


def test_rf20_tipos_bilhete_nao_devolve_tipos_inativos(monkeypatch):
    monkeypatch.setattr(dados, "TIPOS_BILHETE", [*dados.TIPOS_BILHETE, _tipo_inativo()])
    tipos = _tipos_por_id()
    assert "ANTIGO" not in tipos
    assert len(tipos) == 4


def test_rf20_tipos_bilhete_sem_tipos_ativos_devolve_lista_vazia(monkeypatch):
    monkeypatch.setattr(dados, "TIPOS_BILHETE", [_tipo_inativo()])
    resposta = cliente.get("/tipos-bilhete")
    assert resposta.status_code == 200
    assert resposta.json() == []
