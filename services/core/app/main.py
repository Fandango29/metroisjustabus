"""Serviço Core: rede, linhas, paragens e horários."""

import os

from fastapi import FastAPI, HTTPException

from app.dados import LINHAS, PARAGENS_POR_LINHA

app = FastAPI(title="MetroIsJustABus - Core", version="0.1.0")


@app.get("/health")
def health():
    """RNF-12: verificação de saúde do serviço."""
    return {"status": "ok"}


@app.get("/version")
def version():
    """RNF-17: versão em execução, identificada pelo SHA do commit."""
    return {"servico": "core", "commit": os.getenv("APP_COMMIT_SHA", "desconhecido")}


@app.get("/linhas")
def listar_linhas():
    """RF-01: lista as linhas da rede."""
    return LINHAS


@app.get("/linhas/{linha_id}/paragens")
def listar_paragens(linha_id: str):
    """RF-02: lista as paragens de uma linha, pela ordem do percurso."""
    if linha_id not in PARAGENS_POR_LINHA:
        raise HTTPException(status_code=404, detail="Linha não encontrada")
    return PARAGENS_POR_LINHA[linha_id]
