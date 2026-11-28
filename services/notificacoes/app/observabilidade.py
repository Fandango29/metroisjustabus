"""RNF-12: logs estruturados em JSON e ID de correlação por pedido.

Cópia idêntica em services/{core,bilhetes,notificacoes}/app/observabilidade.py: alterar as três.
O nome do serviço não está aqui; é passado a configurar_logs() no main.py de cada serviço.

Nunca registar dados pessoais nem segredos (RNF-10, RNF-11): tokens, passwords, emails,
cabeçalhos, corpos de pedidos ou query strings.
"""

import json
import logging
import re
import sys
import time
import uuid
from contextvars import ContextVar
from datetime import UTC, datetime

CABECALHO = "X-Correlation-ID"
_CABECALHO_ASGI = CABECALHO.lower().encode("ascii")

# Aceita só IDs curtos e sem caracteres estranhos; os restantes são substituídos por um UUID novo
_ID_VALIDO = re.compile(r"[A-Za-z0-9._-]{1,128}")

_correlation_id: ContextVar[str | None] = ContextVar("correlation_id", default=None)

_logger = logging.getLogger(__name__)
_logger_acesso = logging.getLogger("acesso")


def obter_correlation_id() -> str | None:
    """RNF-12: ID de correlação do pedido atual (None fora de um pedido).

    Passar em chamadas HTTP a outros serviços (cabeçalho X-Correlation-ID) e nas mensagens
    do RabbitMQ (campo correlation_id).
    """
    return _correlation_id.get()


class FormatadorJSON(logging.Formatter):
    """RNF-12: uma linha JSON por registo, com os campos obrigatórios e os `dados` explícitos."""

    def __init__(self, servico: str):
        super().__init__()
        self.servico = servico

    def format(self, record: logging.LogRecord) -> str:
        linha = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(
                timespec="milliseconds"
            ),
            "nivel": record.levelname,
            "servico": self.servico,
            "logger": record.name,
            "mensagem": record.getMessage(),
            "correlation_id": obter_correlation_id(),
        }
        # Só entram os campos passados de propósito em extra={"dados": {...}};
        # não se copiam outros atributos do registo nem se sobrepõem os obrigatórios
        dados = getattr(record, "dados", None)
        if isinstance(dados, dict):
            for chave, valor in dados.items():
                linha.setdefault(chave, valor)
        if record.exc_info:
            linha["excecao"] = self.formatException(record.exc_info)
        return json.dumps(linha, ensure_ascii=False, default=str)


class _HandlerJSON(logging.StreamHandler):
    """Handler instalado por configurar_logs(); a classe própria permite não o duplicar."""


def configurar_logs(servico: str, nivel: int = logging.INFO) -> None:
    """RNF-12: todos os logs em JSON no stdout; desliga os logs de acesso em texto do uvicorn."""
    raiz = logging.getLogger()
    for handler in list(raiz.handlers):
        if isinstance(handler, _HandlerJSON):
            raiz.removeHandler(handler)
    handler = _HandlerJSON(sys.stdout)
    handler.setFormatter(FormatadorJSON(servico))
    raiz.addHandler(handler)
    raiz.setLevel(nivel)

    # O uvicorn configura os seus loggers antes de importar a app; aqui passam a usar o handler
    # JSON da raiz. A linha de acesso é a do MiddlewareCorrelacao, para não haver dois formatos.
    for nome in ("uvicorn", "uvicorn.error"):
        logger = logging.getLogger(nome)
        logger.handlers.clear()
        logger.propagate = True
    acesso_uvicorn = logging.getLogger("uvicorn.access")
    acesso_uvicorn.handlers.clear()
    acesso_uvicorn.propagate = False
    acesso_uvicorn.disabled = True

    # O httpx regista em INFO o URL completo de cada chamada, query string incluída (RNF-10)
    for nome in ("httpx", "httpcore"):
        logging.getLogger(nome).setLevel(logging.WARNING)


class MiddlewareCorrelacao:
    """RNF-12: ID de correlação por pedido e uma linha de acesso em JSON.

    Lê o cabeçalho X-Correlation-ID (ou gera um UUID), devolve-o na resposta e regista o
    método, o caminho (sem query string), o código de estado e a duração em milissegundos.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        correlation_id = _ler_ou_gerar_id(scope)
        token = _correlation_id.set(correlation_id)
        inicio = time.perf_counter()
        estado = 500
        resposta_iniciada = False

        async def enviar(mensagem):
            nonlocal estado, resposta_iniciada
            if mensagem["type"] == "http.response.start":
                estado = mensagem["status"]
                resposta_iniciada = True
                cabecalhos = [
                    (nome, valor)
                    for nome, valor in mensagem.get("headers", [])
                    if nome.lower() != _CABECALHO_ASGI
                ]
                cabecalhos.append((_CABECALHO_ASGI, correlation_id.encode("ascii")))
                mensagem = {**mensagem, "headers": cabecalhos}
            await send(mensagem)

        try:
            await self.app(scope, receive, enviar)
        except Exception:
            # Registado aqui, ainda com o ID de correlação; o cliente recebe um 500 com o ID
            _logger.exception("erro não tratado")
            if resposta_iniciada:
                raise
            await _enviar_erro_500(enviar)
        finally:
            _logger_acesso.info(
                "pedido",
                extra={
                    "dados": {
                        "metodo": scope["method"],
                        "caminho": scope["path"],
                        "estado": estado,
                        "duracao_ms": round((time.perf_counter() - inicio) * 1000, 2),
                    }
                },
            )
            _correlation_id.reset(token)


def _ler_ou_gerar_id(scope) -> str:
    for nome, valor in scope.get("headers", []):
        if nome == _CABECALHO_ASGI:
            recebido = valor.decode("latin-1")
            if _ID_VALIDO.fullmatch(recebido):
                return recebido
            break
    return str(uuid.uuid4())


async def _enviar_erro_500(enviar) -> None:
    corpo = json.dumps({"detail": "Erro interno"}).encode("utf-8")
    await enviar(
        {
            "type": "http.response.start",
            "status": 500,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(corpo)).encode("ascii")),
            ],
        }
    )
    await enviar({"type": "http.response.body", "body": corpo})
