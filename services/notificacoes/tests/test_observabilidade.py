"""RNF-12: logs em JSON e ID de correlação (testes iguais nos três serviços, salvo SERVICO)."""

import io
import json
import logging
import logging.config
import uuid
from datetime import datetime, timedelta

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from uvicorn.config import LOGGING_CONFIG

from app import observabilidade
from app.main import app

SERVICO = "notificacoes"
CAMPOS_OBRIGATORIOS = {"timestamp", "nivel", "servico", "mensagem", "correlation_id"}

cliente = TestClient(app)


@pytest.fixture
def linhas_de_log():
    """Redireciona o handler JSON instalado pelo serviço e devolve as linhas já interpretadas."""
    handler = next(
        h for h in logging.getLogger().handlers if isinstance(h, observabilidade._HandlerJSON)
    )
    destino = io.StringIO()
    original = handler.setStream(destino)

    def ler():
        return [json.loads(linha) for linha in destino.getvalue().splitlines()]

    yield ler
    handler.setStream(original)


def _linhas_de_acesso(linhas):
    return [linha for linha in linhas if linha["logger"] == "acesso"]


def _app_de_teste():
    """App mínima com o mesmo middleware, para testar sem acrescentar rotas à app real."""
    mini = FastAPI()
    mini.add_middleware(observabilidade.MiddlewareCorrelacao)

    @mini.get("/id")
    def devolver_id():
        return {"correlation_id": observabilidade.obter_correlation_id()}

    @mini.get("/rebenta")
    def rebentar():
        raise RuntimeError("falha de teste")

    return mini


def test_rnf12_devolve_correlation_id_recebido():
    resposta = cliente.get("/health", headers={"X-Correlation-ID": "pedido-abc.123"})
    assert resposta.status_code == 200
    assert resposta.headers["X-Correlation-ID"] == "pedido-abc.123"


def test_rnf12_sem_cabecalho_gera_uuid():
    resposta = cliente.get("/health")
    gerado = resposta.headers["X-Correlation-ID"]
    assert str(uuid.UUID(gerado)) == gerado


def test_rnf12_sem_cabecalho_cada_pedido_tem_id_diferente():
    primeiro = cliente.get("/health").headers["X-Correlation-ID"]
    segundo = cliente.get("/health").headers["X-Correlation-ID"]
    assert primeiro != segundo


@pytest.mark.parametrize("invalido", ["a" * 129, "tem espacos", "<script>", ""])
def test_rnf12_correlation_id_invalido_e_substituido(invalido):
    resposta = cliente.get("/health", headers={"X-Correlation-ID": invalido})
    devolvido = resposta.headers["X-Correlation-ID"]
    assert devolvido != invalido
    uuid.UUID(devolvido)


def test_rnf12_linha_de_acesso_e_json_com_campos_obrigatorios(linhas_de_log):
    cliente.get("/health", headers={"X-Correlation-ID": "pedido-acesso"})
    acessos = _linhas_de_acesso(linhas_de_log())
    assert len(acessos) == 1
    linha = acessos[0]
    assert CAMPOS_OBRIGATORIOS <= linha.keys()
    assert linha["servico"] == SERVICO
    assert linha["nivel"] == "INFO"
    assert linha["correlation_id"] == "pedido-acesso"
    assert linha["metodo"] == "GET"
    assert linha["caminho"] == "/health"
    assert linha["estado"] == 200
    assert isinstance(linha["duracao_ms"], int | float) and linha["duracao_ms"] >= 0
    assert datetime.fromisoformat(linha["timestamp"]).utcoffset() == timedelta(0)


def test_rnf12_linha_de_acesso_regista_estado_de_erro(linhas_de_log):
    cliente.get("/rota-que-nao-existe")
    (linha,) = _linhas_de_acesso(linhas_de_log())
    assert linha["estado"] == 404


def test_rnf12_caminho_registado_sem_query_string(linhas_de_log):
    cliente.get("/health?email=passageiro@exemplo.pt&token=segredo")
    texto = json.dumps(linhas_de_log())
    (linha,) = _linhas_de_acesso(linhas_de_log())
    assert linha["caminho"] == "/health"
    assert "passageiro@exemplo.pt" not in texto
    assert "segredo" not in texto


def test_rnf12_cabecalho_authorization_nao_e_registado(linhas_de_log):
    cliente.get("/health", headers={"Authorization": "Bearer token-secreto"})
    assert "token-secreto" not in json.dumps(linhas_de_log())


def test_rnf12_obter_correlation_id_dentro_do_pedido():
    resposta = TestClient(_app_de_teste()).get("/id", headers={"X-Correlation-ID": "id-interno"})
    assert resposta.json() == {"correlation_id": "id-interno"}


def test_rnf12_obter_correlation_id_fora_de_um_pedido_e_none():
    TestClient(_app_de_teste()).get("/id", headers={"X-Correlation-ID": "id-anterior"})
    assert observabilidade.obter_correlation_id() is None


def test_rnf12_log_da_aplicacao_leva_o_correlation_id_e_os_dados(linhas_de_log):
    mini = FastAPI()
    mini.add_middleware(observabilidade.MiddlewareCorrelacao)

    @mini.get("/regista")
    def registar():
        logging.getLogger("app.teste").warning("aviso de teste", extra={"dados": {"linha": "L1"}})
        return {}

    TestClient(mini).get("/regista", headers={"X-Correlation-ID": "id-app"})
    (linha,) = [linha for linha in linhas_de_log() if linha["logger"] == "app.teste"]
    assert linha["mensagem"] == "aviso de teste"
    assert linha["nivel"] == "WARNING"
    assert linha["correlation_id"] == "id-app"
    assert linha["linha"] == "L1"


def test_rnf12_dados_nao_sobrepoem_campos_obrigatorios(linhas_de_log):
    logging.getLogger("app.teste").info("mensagem real", extra={"dados": {"mensagem": "falsa"}})
    (linha,) = linhas_de_log()
    assert linha["mensagem"] == "mensagem real"


def test_rnf12_erro_regista_estado_500_e_excecao(linhas_de_log):
    resposta = TestClient(_app_de_teste()).get("/rebenta", headers={"X-Correlation-ID": "id-erro"})
    assert resposta.status_code == 500
    assert resposta.headers["X-Correlation-ID"] == "id-erro"
    linhas = linhas_de_log()
    (erro,) = [linha for linha in linhas if linha["nivel"] == "ERROR"]
    assert erro["correlation_id"] == "id-erro"
    assert "falha de teste" in erro["excecao"]
    (acesso,) = _linhas_de_acesso(linhas)
    assert acesso["estado"] == 500


def test_rnf12_logs_de_acesso_do_uvicorn_desligados():
    # Simula o arranque real: o uvicorn aplica a sua configuração e depois importa a app
    logging.config.dictConfig(LOGGING_CONFIG)
    observabilidade.configurar_logs(SERVICO)
    acesso = logging.getLogger("uvicorn.access")
    assert acesso.disabled
    assert acesso.handlers == []
    assert not acesso.propagate
    assert logging.getLogger("uvicorn").handlers == []
    assert logging.getLogger("uvicorn.error").handlers == []


def test_rnf12_configurar_logs_nao_duplica_handler():
    observabilidade.configurar_logs(SERVICO)
    observabilidade.configurar_logs(SERVICO)
    handlers = [
        h for h in logging.getLogger().handlers if isinstance(h, observabilidade._HandlerJSON)
    ]
    assert len(handlers) == 1
