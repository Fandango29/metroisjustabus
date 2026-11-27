"""Dados de exemplo da rede, usados quando não há base de dados configurada (testes e pipeline).

São os mesmos dados de deploy/dev/init-db/01-rede.sql e 02-horarios-perturbacoes.sql.
"""

from datetime import UTC, date, datetime

LINHAS = [
    {"id": "L1", "nome": "Estação Central - Hospital"},
    {"id": "L2", "nome": "Universidade - Praia"},
]

PARAGENS_POR_LINHA = {
    "L1": [
        {"id": "P01", "nome": "Estação Central", "ordem": 1},
        {"id": "P02", "nome": "Praça da República", "ordem": 2},
        {"id": "P03", "nome": "Hospital", "ordem": 3},
    ],
    "L2": [
        {"id": "P04", "nome": "Universidade", "ordem": 1},
        {"id": "P02", "nome": "Praça da República", "ordem": 2},
        {"id": "P05", "nome": "Praia", "ordem": 3},
    ],
}

TIPOS_DIA = [
    {"id": "util", "nome": "Dia útil"},
    {"id": "sabado", "nome": "Sábado"},
    {"id": "domingo_feriado", "nome": "Domingo ou feriado"},
]

# Datas em que o tipo de dia não é o do dia da semana (A-07)
CALENDARIO_EXCECOES = {
    date(2026, 12, 1): "domingo_feriado",
    date(2026, 12, 8): "domingo_feriado",
    date(2026, 12, 25): "domingo_feriado",
    date(2027, 1, 1): "domingo_feriado",
}

# Minutos de cada paragem desde a partida, pela ordem da linha
_DESVIOS_MIN = {"L1": [0, 10, 25], "L2": [0, 12, 20]}


def _viagem(viagem_id, linha_id, tipo_dia_id, partida_min):
    """Viagem planeada; horas em minutos desde o início do dia de serviço (A-17)."""
    paragens = PARAGENS_POR_LINHA[linha_id]
    return {
        "id": viagem_id,
        "linha_id": linha_id,
        "tipo_dia_id": tipo_dia_id,
        "partida_min": partida_min,
        "capacidade": 80,
        "ativa": True,
        "horas": [
            {"paragem_id": p["id"], "ordem": p["ordem"], "minutos": partida_min + desvio}
            for p, desvio in zip(paragens, _DESVIOS_MIN[linha_id], strict=True)
        ],
    }


VIAGENS = [
    _viagem("L1-U-0700", "L1", "util", 420),
    _viagem("L1-U-1230", "L1", "util", 750),
    _viagem("L1-U-2430", "L1", "util", 1470),
    _viagem("L1-S-0900", "L1", "sabado", 540),
    _viagem("L1-S-1800", "L1", "sabado", 1080),
    _viagem("L1-D-1000", "L1", "domingo_feriado", 600),
    _viagem("L2-U-0730", "L2", "util", 450),
    _viagem("L2-U-1300", "L2", "util", 780),
    _viagem("L2-U-1830", "L2", "util", 1110),
    _viagem("L2-S-0930", "L2", "sabado", 570),
    _viagem("L2-S-1730", "L2", "sabado", 1050),
    _viagem("L2-D-1100", "L2", "domingo_feriado", 660),
]


def _instante(ano, mes, dia, hora, minuto=0):
    return datetime(ano, mes, dia, hora, minuto, tzinfo=UTC)


# Uma perturbação ativa de cada tipo (1 a 4) e uma planeada (5)
PERTURBACOES = [
    {
        "id": 1,
        "tipo": "atraso",
        "ambito": "viagem",
        "elemento_id": "L1-U-0700",
        "descricao": "Atraso por trânsito intenso na Estação Central",
        "inicio": _instante(2026, 11, 20, 7),
        "fim_previsto": None,
        "encerrada_em": None,
        "atraso_min": 10,
        "criada_em": _instante(2026, 11, 20, 6, 45),
        "alterada_em": _instante(2026, 11, 20, 6, 45),
        "paragens_nao_servidas": [],
    },
    {
        "id": 2,
        "tipo": "cancelamento",
        "ambito": "viagem",
        "elemento_id": "L2-U-1300",
        "descricao": "Viagem cancelada por avaria do autocarro",
        "inicio": _instante(2026, 11, 20, 12),
        "fim_previsto": None,
        "encerrada_em": None,
        "atraso_min": None,
        "criada_em": _instante(2026, 11, 20, 11, 30),
        "alterada_em": _instante(2026, 11, 20, 11, 30),
        "paragens_nao_servidas": [],
    },
    {
        "id": 3,
        "tipo": "desvio",
        "ambito": "viagem",
        "elemento_id": "L2-U-0730",
        "descricao": "Desvio por obras na Praça da República",
        "inicio": _instante(2026, 11, 20, 7),
        "fim_previsto": None,
        "encerrada_em": None,
        "atraso_min": None,
        "criada_em": _instante(2026, 11, 20, 6, 30),
        "alterada_em": _instante(2026, 11, 20, 6, 30),
        "paragens_nao_servidas": ["P02"],
    },
    {
        "id": 4,
        "tipo": "outro",
        "ambito": "paragem",
        "elemento_id": "P03",
        "descricao": "Obras no abrigo da paragem do Hospital",
        "inicio": _instante(2026, 11, 20, 8),
        "fim_previsto": None,
        "encerrada_em": None,
        "atraso_min": None,
        "criada_em": _instante(2026, 11, 20, 7, 30),
        "alterada_em": _instante(2026, 11, 20, 7, 30),
        "paragens_nao_servidas": [],
    },
    {
        "id": 5,
        "tipo": "outro",
        "ambito": "periodo",
        "elemento_id": None,
        "descricao": "Greve dos motoristas: serviço mínimo em toda a rede",
        "inicio": _instante(2030, 3, 15, 0),
        "fim_previsto": _instante(2030, 3, 16, 0),
        "encerrada_em": None,
        "atraso_min": None,
        "criada_em": _instante(2026, 11, 20, 9),
        "alterada_em": _instante(2026, 11, 20, 9),
        "paragens_nao_servidas": [],
    },
]

# Eventos por publicar (padrão outbox, RF-13); começa vazia
OUTBOX = []
