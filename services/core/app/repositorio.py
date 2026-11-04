"""Acesso aos dados da rede.

Usa o PostgreSQL quando a variável DATABASE_URL está definida (ambientes dev e prod).
Sem ela, usa os dados de exemplo de app/dados.py (testes unitários e pipeline).
"""

import os

import psycopg
from psycopg.rows import dict_row

from app import dados


def _url_base_dados():
    return os.getenv("DATABASE_URL")


def obter_linhas():
    url = _url_base_dados()
    if not url:
        return dados.LINHAS
    with psycopg.connect(url, row_factory=dict_row) as ligacao:
        return ligacao.execute("SELECT id, nome FROM linhas ORDER BY id").fetchall()


def obter_paragens(linha_id: str):
    """Devolve as paragens da linha pela ordem do percurso, ou None se a linha não existir."""
    url = _url_base_dados()
    if not url:
        return dados.PARAGENS_POR_LINHA.get(linha_id)
    with psycopg.connect(url, row_factory=dict_row) as ligacao:
        linha = ligacao.execute("SELECT 1 FROM linhas WHERE id = %s", (linha_id,)).fetchone()
        if linha is None:
            return None
        return ligacao.execute(
            """
            SELECT p.id, p.nome, lp.ordem
            FROM linha_paragens lp
            JOIN paragens p ON p.id = lp.paragem_id
            WHERE lp.linha_id = %s
            ORDER BY lp.ordem
            """,
            (linha_id,),
        ).fetchall()
