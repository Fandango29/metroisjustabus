"""Serviço Bilhetes e Validação: tipos de bilhete, emissão e validação."""

import os

from fastapi import FastAPI

from app.dados import TIPOS_BILHETE

app = FastAPI(title="MetroIsJustABus - Bilhetes", version="0.1.0")


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
    """RF-20: lista os tipos de bilhete com preço, validade, condições e número de viagens."""
    return TIPOS_BILHETE
