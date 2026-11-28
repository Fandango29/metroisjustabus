"""Serviço Bilhetes e Validação: tipos de bilhete, emissão e validação."""

import os

from fastapi import FastAPI

from app import repositorio
from app.observabilidade import MiddlewareCorrelacao, configurar_logs

configurar_logs("bilhetes")

app = FastAPI(title="MetroIsJustABus - Bilhetes", version="0.1.0")
app.add_middleware(MiddlewareCorrelacao)


@app.get("/health")
def health():
    """RNF-12: verificação de saúde do serviço."""
    return {"status": "ok"}


@app.get("/version")
def version():
    """RNF-17: versão em execução, identificada pelo SHA do commit."""
    return {"servico": "bilhetes", "commit": os.getenv("APP_COMMIT_SHA", "desconhecido")}


@app.get("/tipos-bilhete")
def listar_tipos_bilhete():
    """RF-20: lista os tipos de bilhete ativos com preço, validade, condições e n.º de viagens."""
    return repositorio.obter_tipos_bilhete_ativos()
