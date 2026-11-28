#!/usr/bin/env bash
# Cria (ou atualiza) os utilizadores de teste do realm metroisjustabus (issue #22):
#   - um passageiro (fica com o papel passageiro, que é o papel por omissão do realm);
#   - um staff (fica com os papéis passageiro e staff).
#
# As passwords vêm só de variáveis de ambiente, nunca do repositório (RNF-10).
# O script é idempotente: se o utilizador já existe, só volta a definir a password e os papéis.
# Usa o kcadm.sh de dentro do contentor do Keycloak, por isso não precisa de curl nem de jq.
#
# Variáveis obrigatórias:
#   KEYCLOAK_ADMIN_USER          administrador do Keycloak (realm master)
#   KEYCLOAK_ADMIN_PASSWORD      password desse administrador
#   TESTE_PASSAGEIRO_PASSWORD    password do passageiro de teste
#   TESTE_STAFF_PASSWORD         password do staff de teste
# Variáveis opcionais:
#   TESTE_PASSAGEIRO_EMAIL       por omissão passageiro@teste.local
#   TESTE_STAFF_EMAIL            por omissão staff@teste.local
#
# Uso (em deploy/dev, com o Keycloak a correr; as passwords são lidas sem eco nem histórico):
#   read -rp  "Admin Keycloak: " KEYCLOAK_ADMIN_USER
#   read -rsp "Password admin: " KEYCLOAK_ADMIN_PASSWORD; echo
#   read -rsp "Password passageiro de teste: " TESTE_PASSAGEIRO_PASSWORD; echo
#   read -rsp "Password staff de teste: " TESTE_STAFF_PASSWORD; echo
#   export KEYCLOAK_ADMIN_USER KEYCLOAK_ADMIN_PASSWORD TESTE_PASSAGEIRO_PASSWORD TESTE_STAFF_PASSWORD
#   ./keycloak/criar-utilizadores-teste.sh
#   unset KEYCLOAK_ADMIN_PASSWORD TESTE_PASSAGEIRO_PASSWORD TESTE_STAFF_PASSWORD
#
# As variáveis passam para o contentor com "docker compose exec -e NOME" (sem valor), por isso
# as passwords não aparecem na linha de comandos do anfitrião.

set -euo pipefail

erro() {
    echo "$*" >&2
    exit 1
}

for variavel in KEYCLOAK_ADMIN_USER KEYCLOAK_ADMIN_PASSWORD TESTE_PASSAGEIRO_PASSWORD TESTE_STAFF_PASSWORD; do
    [[ -n "${!variavel:-}" ]] || erro "Falta a variável de ambiente ${variavel}."
done

export TESTE_PASSAGEIRO_EMAIL="${TESTE_PASSAGEIRO_EMAIL:-passageiro@teste.local}"
export TESTE_STAFF_EMAIL="${TESTE_STAFF_EMAIL:-staff@teste.local}"
export KEYCLOAK_ADMIN_USER KEYCLOAK_ADMIN_PASSWORD TESTE_PASSAGEIRO_PASSWORD TESTE_STAFF_PASSWORD

# O docker-compose.yml está na pasta acima deste script
cd "$(dirname "${BASH_SOURCE[0]}")/.."

if [[ -z "$(docker compose ps -q --status running keycloak)" ]]; then
    erro "O Keycloak não está a correr. Arranca-o primeiro com: docker compose up -d keycloak"
fi

# O script abaixo corre dentro do contentor. Lê as variáveis do ambiente, nunca de argumentos.
docker compose exec -T \
    -e KEYCLOAK_ADMIN_USER -e KEYCLOAK_ADMIN_PASSWORD \
    -e TESTE_PASSAGEIRO_EMAIL -e TESTE_PASSAGEIRO_PASSWORD \
    -e TESTE_STAFF_EMAIL -e TESTE_STAFF_PASSWORD \
    keycloak bash -s <<'DENTRO_DO_CONTENTOR'
set -euo pipefail
KCADM=/opt/keycloak/bin/kcadm.sh
REALM=metroisjustabus
CONFIG="/tmp/kcadm-$$.config"
# A config do kcadm guarda o token de admin: apagá-la sempre no fim
trap 'rm -f "$CONFIG"' EXIT

kc() {
    "$KCADM" "$@" --config "$CONFIG"
}

# Esperar que o Keycloak aceite o login (pode estar ainda a arrancar)
for tentativa in $(seq 1 30); do
    if "$KCADM" config credentials --config "$CONFIG" --server http://localhost:8080 \
        --realm master --user "$KEYCLOAK_ADMIN_USER" --password "$KEYCLOAK_ADMIN_PASSWORD" \
        >/dev/null 2>&1; then
        break
    fi
    if [[ "$tentativa" -eq 30 ]]; then
        echo "Não foi possível entrar como administrador (o Keycloak não responde ou as credenciais estão erradas)." >&2
        exit 1
    fi
    sleep 2
done

# Cria o utilizador se não existir e define a password (não temporária)
garantir_utilizador() {
    local email="$1" nome="$2" password="$3" id
    id=$(kc get users -r "$REALM" -q username="$email" -q exact=true --fields id --format csv --noquotes)
    if [[ -z "$id" ]]; then
        kc create users -r "$REALM" -s username="$email" -s email="$email" -s firstName="$nome" \
            -s enabled=true -s emailVerified=true >/dev/null 2>&1
        echo "Criado: $email"
    else
        echo "Já existia: $email"
    fi
    kc set-password -r "$REALM" --username "$email" --new-password "$password"
}

garantir_utilizador "$TESTE_PASSAGEIRO_EMAIL" "Passageiro de Teste" "$TESTE_PASSAGEIRO_PASSWORD"
garantir_utilizador "$TESTE_STAFF_EMAIL" "Staff de Teste" "$TESTE_STAFF_PASSWORD"

# O passageiro já tem o papel passageiro pelo papel por omissão do realm; o staff precisa de staff
kc add-roles -r "$REALM" --uusername "$TESTE_STAFF_EMAIL" --rolename staff
echo "Papel staff atribuído a $TESTE_STAFF_EMAIL"
echo "Utilizadores de teste prontos."
DENTRO_DO_CONTENTOR
