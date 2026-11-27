"""Coerência dos dados de exemplo de app/dados.py (os mesmos do 02-horarios-perturbacoes.sql)."""

from collections import Counter
from datetime import UTC, datetime

from app import dados

TIPOS_PERTURBACAO = {"atraso", "cancelamento", "desvio", "outro"}


def _ativas():
    agora = datetime.now(UTC)
    return [p for p in dados.PERTURBACOES if p["inicio"] <= agora and p["encerrada_em"] is None]


def test_a17_horas_das_viagens_seguem_a_ordem_da_linha_e_crescem():
    for viagem in dados.VIAGENS:
        paragens = dados.PARAGENS_POR_LINHA[viagem["linha_id"]]
        assert [(h["paragem_id"], h["ordem"]) for h in viagem["horas"]] == [
            (p["id"], p["ordem"]) for p in paragens
        ]
        minutos = [h["minutos"] for h in viagem["horas"]]
        assert minutos[0] == viagem["partida_min"]
        assert all(a < b for a, b in zip(minutos, minutos[1:], strict=False))


def test_a17_existe_viagem_depois_da_meia_noite():
    assert any(v["partida_min"] >= 24 * 60 for v in dados.VIAGENS)


def test_a05_capacidade_por_omissao_80():
    assert all(v["capacidade"] == 80 for v in dados.VIAGENS)


def test_rf04_viagens_por_tipo_de_dia_em_cada_linha():
    tipos_validos = {t["id"] for t in dados.TIPOS_DIA}
    assert tipos_validos == {"util", "sabado", "domingo_feriado"}
    for linha in dados.LINHAS:
        contagem = Counter(v["tipo_dia_id"] for v in dados.VIAGENS if v["linha_id"] == linha["id"])
        assert set(contagem) <= tipos_validos
        assert contagem["util"] >= 3
        assert contagem["sabado"] >= 2
        assert contagem["domingo_feriado"] >= 1


def test_a07_excecoes_do_calendario_usam_tipos_de_dia_existentes():
    tipos_validos = {t["id"] for t in dados.TIPOS_DIA}
    assert dados.CALENDARIO_EXCECOES
    assert set(dados.CALENDARIO_EXCECOES.values()) <= tipos_validos


def test_rf10_uma_perturbacao_ativa_de_cada_tipo():
    assert Counter(p["tipo"] for p in _ativas()) == dict.fromkeys(TIPOS_PERTURBACAO, 1)


def test_rf10_existe_perturbacao_planeada():
    agora = datetime.now(UTC)
    assert any(p["inicio"] > agora and p["encerrada_em"] is None for p in dados.PERTURBACOES)


def test_rf10_atraso_tem_minutos_e_os_outros_tipos_nao():
    for p in dados.PERTURBACOES:
        if p["tipo"] == "atraso":
            assert p["atraso_min"] > 0
        else:
            assert p["atraso_min"] is None


def test_rf05_cada_linha_tem_viagem_sem_perturbacoes():
    ativas = _ativas()
    assert not any(p["ambito"] == "periodo" for p in ativas)
    afetadas = {p["elemento_id"] for p in ativas if p["ambito"] in ("viagem", "linha")}
    for linha in dados.LINHAS:
        assert linha["id"] not in afetadas, f"a linha {linha['id']} está toda afetada"
        viagens_da_linha = [v["id"] for v in dados.VIAGENS if v["linha_id"] == linha["id"]]
        assert set(viagens_da_linha) - afetadas, f"todas as viagens de {linha['id']} afetadas"


def test_a08_desvio_tem_paragens_nao_servidas_da_linha_da_viagem():
    viagens = {v["id"]: v for v in dados.VIAGENS}
    desvios = [p for p in dados.PERTURBACOES if p["tipo"] == "desvio"]
    assert desvios
    for p in desvios:
        assert p["paragens_nao_servidas"]
        viagem = viagens[p["elemento_id"]]
        paragens_da_linha = {par["id"] for par in dados.PARAGENS_POR_LINHA[viagem["linha_id"]]}
        assert set(p["paragens_nao_servidas"]) <= paragens_da_linha
    assert all(not p["paragens_nao_servidas"] for p in dados.PERTURBACOES if p["tipo"] != "desvio")
