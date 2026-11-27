"""Acesso aos dados dos bilhetes.

Usa o PostgreSQL quando a variável DATABASE_URL está definida (ambientes dev e prod).
Sem ela, usa os dados de exemplo de app/dados.py (testes unitários e pipeline).
"""

import os

import psycopg
from psycopg.rows import dict_row

from app import dados


def _url_base_dados():
    return os.getenv("DATABASE_URL")


def obter_tipos_bilhete_ativos():
    """Devolve os tipos de bilhete ativos para venda, do mais barato para o mais caro."""
    url = _url_base_dados()
    if not url:
        ativos = [tipo for tipo in dados.TIPOS_BILHETE if tipo["ativo"]]
        return sorted(ativos, key=lambda tipo: (tipo["preco_centimos"], tipo["id"]))
    with psycopg.connect(url, row_factory=dict_row) as ligacao:
        return ligacao.execute(
            """
            SELECT id, nome, preco_centimos, validade_tipo, validade_minutos,
                   viagens, condicoes, ativo
            FROM tipos_bilhete
            WHERE ativo
            ORDER BY preco_centimos, id
            """
        ).fetchall()
