#!/usr/bin/env bash
# Deploy de um serviço no ambiente de desenvolvimento, com smoke test e rollback automático.
# Usado pela pipeline (job "Deploy em desenvolvimento") no runner Linux da VM metro-dev.
# Cada serviço é implantado sozinho, sem mexer nos outros (RNF-15).
# Mesmo comportamento do deploy.ps1 (versão para Windows).
#
# Uso:
#   ./deploy.sh --servico core|bilhetes|notificacoes --porta <n> --imagem <imagem> --sha <sha>
#               [--simular-falha] [--tentativas <n>] [--intervalo <segundos>]

set -euo pipefail

erro() {
    echo "$*" >&2
    exit 1
}

e_inteiro() {
    [[ "$1" =~ ^-?[0-9]+$ ]]
}

# --- Argumentos (validados antes de qualquer outra coisa) ---
SERVICO=""
PORTA=""
IMAGEM=""
SHA=""
SIMULAR_FALHA=false
TENTATIVAS=10
INTERVALO_SEGUNDOS=3

while [[ $# -gt 0 ]]; do
    case "$1" in
        --servico | --porta | --imagem | --sha | --tentativas | --intervalo)
            [[ $# -ge 2 ]] || erro "Falta o valor da opção $1."
            case "$1" in
                --servico) SERVICO="$2" ;;
                --porta) PORTA="$2" ;;
                --imagem) IMAGEM="$2" ;;
                --sha) SHA="$2" ;;
                --tentativas) TENTATIVAS="$2" ;;
                --intervalo) INTERVALO_SEGUNDOS="$2" ;;
            esac
            shift 2
            ;;
        --simular-falha)
            SIMULAR_FALHA=true
            shift
            ;;
        *)
            erro "Opção desconhecida: $1"
            ;;
    esac
done

[[ -n "$SERVICO" ]] || erro "Falta a opção obrigatória --servico."
[[ -n "$PORTA" ]] || erro "Falta a opção obrigatória --porta."
[[ -n "$IMAGEM" ]] || erro "Falta a opção obrigatória --imagem."
[[ -n "$SHA" ]] || erro "Falta a opção obrigatória --sha."
case "$SERVICO" in
    core | bilhetes | notificacoes) ;;
    *) erro "Serviço inválido: '$SERVICO' (valores aceites: core, bilhetes, notificacoes)." ;;
esac
e_inteiro "$PORTA" || erro "Porta inválida: '$PORTA' (tem de ser um número inteiro)."
e_inteiro "$TENTATIVAS" || erro "Número de tentativas inválido: '$TENTATIVAS'."
e_inteiro "$INTERVALO_SEGUNDOS" || erro "Intervalo inválido: '$INTERVALO_SEGUNDOS'."

cd "$(dirname "${BASH_SOURCE[0]}")"

CONTENTOR="metroisjustabus-dev-${SERVICO}-1"
URL_BASE="http://localhost:${PORTA}"
VARIAVEL_IMAGEM="${SERVICO^^}_IMAGE"

# Corre um comando docker e falha o script se o comando falhar
executar_docker() {
    if ! docker "$@"; then
        erro "Falhou o comando: docker $*"
    fi
}

# Smoke test: /health responde ok e /version mostra o serviço e o SHA esperados.
# As comparações não distinguem maiúsculas de minúsculas, como o -eq do PowerShell.
testar_servico() {
    local sha_esperado="$1" caminho_health="$2"
    local i health versao estado servico commit
    for ((i = 1; i <= TENTATIVAS; i++)); do
        if health=$(curl -fsS --max-time 5 "${URL_BASE}${caminho_health}" 2>&1) &&
            versao=$(curl -fsS --max-time 5 "${URL_BASE}/version" 2>&1); then
            estado=$(jq -r '.status // empty' <<<"$health" 2>/dev/null || true)
            servico=$(jq -r '.servico // empty' <<<"$versao" 2>/dev/null || true)
            commit=$(jq -r '.commit // empty' <<<"$versao" 2>/dev/null || true)
            if [[ "${estado,,}" == "ok" && "${servico,,}" == "${SERVICO,,}" && "${commit,,}" == "${sha_esperado,,}" ]]; then
                echo "Smoke test OK (tentativa ${i}): ${SERVICO} na versão ${commit}"
                return 0
            fi
            echo "Tentativa ${i}: resposta inesperada (${servico}, ${commit})"
        else
            # Quando o curl falha, $health ou $versao contém a mensagem de erro do curl
            local mensagem="${versao:-$health}"
            echo "Tentativa ${i}: o serviço ainda não responde (${mensagem})"
        fi
        versao=""
        sleep "$INTERVALO_SEGUNDOS"
    done
    return 1
}

# 1. Guardar a versão que está a correr agora, para o rollback
IMAGEM_ANTERIOR=$(docker ps -a --filter "name=^${CONTENTOR}\$" --format "{{.Image}}" || true)
if [[ -n "$IMAGEM_ANTERIOR" ]]; then
    echo "Versão atualmente em execução: ${IMAGEM_ANTERIOR}"
else
    echo "Não há nenhuma versão de ${SERVICO} em execução (primeiro deploy)."
fi

# 2. Criar o .env a partir do segredo da pipeline (nunca vem do repositório)
if [[ -z "${POSTGRES_PASSWORD:-}" ]]; then
    erro "O segredo POSTGRES_PASSWORD não está definido."
fi
if [[ "$SERVICO" == notificacoes && -z "${NOTIFICACOES_DB_PASSWORD:-}" ]]; then
    erro "O segredo NOTIFICACOES_DB_PASSWORD não está definido."
fi
printf '%s\n' \
    "POSTGRES_USER=core" \
    "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" \
    "POSTGRES_DB=core" >.env
# A password da base das Notificações é escrita sempre que o segredo existe, para que o
# deploy de outro serviço não a apague do .env
if [[ -n "${NOTIFICACOES_DB_PASSWORD:-}" ]]; then
    printf '%s\n' \
        "NOTIFICACOES_DB_USER=notificacoes" \
        "NOTIFICACOES_DB_PASSWORD=${NOTIFICACOES_DB_PASSWORD}" \
        "NOTIFICACOES_DB_NAME=notificacoes" >>.env
fi
# Só o utilizador do runner pode ler o .env, porque contém a password
chmod 600 .env

# 3. Implantar só este serviço, com a imagem publicada no GHCR (sem a reconstruir)
IMAGEM_NOVA="${IMAGEM}:${SHA}"
export "${VARIAVEL_IMAGEM}=${IMAGEM_NOVA}"
echo "A implantar ${IMAGEM_NOVA}"
executar_docker compose pull "$SERVICO"
executar_docker compose up -d --no-build "$SERVICO"

# 4. Smoke test
CAMINHO_HEALTH="/health"
if [[ "$SIMULAR_FALHA" == true ]]; then
    echo "ATENÇÃO: falha do smoke test simulada (demonstração do rollback)"
    CAMINHO_HEALTH="/health-simulacao-de-falha"
fi

if testar_servico "$SHA" "$CAMINHO_HEALTH"; then
    echo "Deploy concluído: ${IMAGEM_NOVA}"
    exit 0
fi

# 5. Rollback para a versão anterior deste serviço
echo "::error::O smoke test falhou para ${IMAGEM_NOVA}"
if [[ -z "$IMAGEM_ANTERIOR" ]]; then
    echo "::error::Não há versão anterior de ${SERVICO} para repor."
    exit 1
fi
echo "A repor a versão anterior: ${IMAGEM_ANTERIOR}"
export "${VARIAVEL_IMAGEM}=${IMAGEM_ANTERIOR}"
executar_docker compose up -d --no-build "$SERVICO"
echo "::warning::Rollback concluído. Em execução: ${IMAGEM_ANTERIOR}"
exit 1
