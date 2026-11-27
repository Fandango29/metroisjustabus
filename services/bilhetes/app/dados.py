"""Tipos de bilhete de exemplo (RF-20, A-01), usados sem base de dados (testes e pipeline).

São os mesmos 4 tipos que o deploy/dev/init-db-bilhetes/01-bilhetes.sql insere na base.
"""

# Preços em cêntimos (inteiros), para evitar erros de arredondamento.
# "validade_tipo": "minutos" usa validade_minutos; "mes_civil" vale até ao fim do mês civil
# e por isso não tem validade_minutos (os meses têm 28 a 31 dias).
# "viagens": None significa viagens ilimitadas durante a validade.
# "ativo": False tira o tipo das novas vendas sem o apagar (A-15).
TIPOS_BILHETE = [
    {
        "id": "SIMPLES",
        "nome": "Bilhete simples",
        "preco_centimos": 150,
        "validade_tipo": "minutos",
        "validade_minutos": 60,
        "viagens": 1,
        "condicoes": "Válido para uma viagem numa linha, até 60 minutos após a compra.",
        "ativo": True,
    },
    {
        "id": "DIARIO",
        "nome": "Passe diário",
        "preco_centimos": 450,
        "validade_tipo": "minutos",
        "validade_minutos": 1440,
        "viagens": None,
        "condicoes": "Viagens ilimitadas durante 24 horas após a primeira validação.",
        "ativo": True,
    },
    {
        "id": "DEZ_VIAGENS",
        "nome": "Cartão de 10 viagens",
        "preco_centimos": 1200,
        "validade_tipo": "minutos",
        "validade_minutos": 43200,
        "viagens": 10,
        "condicoes": "Dez viagens a usar no prazo de 30 dias após a compra.",
        "ativo": True,
    },
    {
        "id": "MENSAL",
        "nome": "Passe mensal",
        "preco_centimos": 4000,
        "validade_tipo": "mes_civil",
        "validade_minutos": None,
        "viagens": None,
        "condicoes": "Viagens ilimitadas até ao fim do mês civil da primeira validação.",
        "ativo": True,
    },
]
