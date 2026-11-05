"""Tipos de bilhete de exemplo (RF-20), usados até o serviço ter base de dados própria."""

# Preços em cêntimos (inteiros), para evitar erros de arredondamento.
# "viagens": None significa viagens ilimitadas durante a validade.
TIPOS_BILHETE = [
    {
        "id": "SIMPLES",
        "nome": "Bilhete simples",
        "preco_centimos": 150,
        "validade_minutos": 60,
        "viagens": 1,
        "condicoes": "Válido para uma viagem numa linha, até 60 minutos após a compra.",
    },
    {
        "id": "DIARIO",
        "nome": "Passe diário",
        "preco_centimos": 450,
        "validade_minutos": 1440,
        "viagens": None,
        "condicoes": "Viagens ilimitadas durante 24 horas após a primeira validação.",
    },
    {
        "id": "DEZ_VIAGENS",
        "nome": "Cartão de 10 viagens",
        "preco_centimos": 1200,
        "validade_minutos": 43200,
        "viagens": 10,
        "condicoes": "Dez viagens a usar no prazo de 30 dias.",
    },
]
