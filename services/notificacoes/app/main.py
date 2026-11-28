"""Serviço Notificações: subscrições, preferências e envio de notificações."""

import os

from fastapi import FastAPI

from app.observabilidade import MiddlewareCorrelacao, configurar_logs

configurar_logs("notificacoes")

app = FastAPI(title="MetroIsJustABus - Notificações", version="0.1.0")
app.add_middleware(MiddlewareCorrelacao)


@app.get("/health")
def health():
    """RNF-12: verificação de saúde do serviço."""
    return {"status": "ok"}


@app.get("/version")
def version():
    """RNF-17: versão em execução, identificada pelo SHA do commit."""
    return {"servico": "notificacoes", "commit": os.getenv("APP_COMMIT_SHA", "desconhecido")}
