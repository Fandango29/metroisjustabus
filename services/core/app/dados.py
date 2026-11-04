"""Dados de exemplo da rede, usados quando não há base de dados configurada (testes e pipeline)."""

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
