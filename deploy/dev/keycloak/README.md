# Keycloak: realm `metroisjustabus`

Configuração do serviço de identidade em dev (issue #22; base de RF-50, RF-51, A-18, A-19, RNF-10, RNF-20).

| Ficheiro | O que é |
| --- | --- |
| `realm-metroisjustabus.json` | Realm importado automaticamente no arranque (`start-dev --import-realm`) |
| `criar-utilizadores-teste.sh` | Cria um passageiro e um staff de teste, com passwords vindas de variáveis de ambiente |

O `docker-compose.yml` monta esta pasta em `/opt/keycloak/data/import` (só leitura). Se o realm já existir, o import é ignorado.

## O que o realm tem

- Papéis do realm: `passageiro`, `staff` e `administrador`. O `administrador` inclui `view-users`, `query-users` e `manage-users` do `realm-management`, para gerir as contas de staff (A-18).
- Registo de contas ativo (RF-50). O formulário só pede nome, email e password (A-19), e o email é o nome de utilizador. Toda a conta nova recebe `passageiro` pelo papel por omissão `default-roles-metroisjustabus`.
- Cliente `web`: público, Authorization Code com PKCE obrigatório (`S256`). Redirect URIs `http://localhost:5173/*` (Vite) e `http://10.17.0.189:8003/*` (nginx na metro-dev).
- Os papéis do realm vão no access token em `realm_access.roles` (client scope `roles`).

O ficheiro foi escrito à mão, não exportado com `kc.sh export`. Uma exportação completa traz as chaves privadas do realm e segredos de clientes internos (RNF-10). O Keycloak gera-os no import. O ficheiro não tem utilizadores, passwords nem segredos.

**Para mudar a configuração**, edita-se o JSON. O import só acontece quando o realm não existe, por isso a seguir é preciso recriar o contentor: `docker compose up -d --force-recreate keycloak`.

## Arranque em dev local

```bash
cd deploy/dev
docker compose up -d keycloak     # credenciais de admin vêm do .env (ver .env.example)
docker compose logs keycloak | grep "Realm 'metroisjustabus' imported"
```

Arranque limpo, como pede a issue: `docker compose down -v && docker compose up keycloak`. Atenção: o `down -v` também apaga os volumes das bases de dados. Para recomeçar só o Keycloak, basta `docker compose up -d --force-recreate keycloak`, porque o Keycloak não tem volume.

## Arranque na metro-dev

A pipeline nunca sobe o Keycloak. O `deploy.sh` só faz `compose up` do serviço que está a implantar, e o Keycloak não é dependência de nenhum. Arranca-se à mão, uma vez, numa shell da VM, no diretório `deploy/dev` do checkout do runner (o mesmo onde corre o `deploy.sh`):

```bash
read -rp  "Utilizador admin: " KEYCLOAK_ADMIN_USER
read -rsp "Password admin: "   KEYCLOAK_ADMIN_PASSWORD; echo
export KEYCLOAK_ADMIN_USER KEYCLOAK_ADMIN_PASSWORD
docker compose up -d keycloak
unset KEYCLOAK_ADMIN_PASSWORD
```

- **De onde vêm as credenciais de admin:** a equipa escolhe-as e guarda-as fora do repositório (gestor de passwords da equipa). Só passam pela shell de quem arranca o Keycloak. O Compose dá prioridade às variáveis da shell sobre o `.env`. O `.env` da VM é reescrito pelo `deploy.sh` e não as tem. O `read -s` não as mostra nem as guarda no histórico.
- **Ciclo de vida (sem volume):** o administrador só é criado quando a base interna do Keycloak está vazia. `docker restart` e os reboots da VM (`restart: unless-stopped`) mantêm o contentor, e com ele o admin e os utilizadores de teste. Se o contentor for recriado (`down`, `--force-recreate`, mudança da configuração do serviço), o realm volta do JSON mas o admin e os utilizadores perdem-se. Nesse caso repetem-se os comandos acima e o script de utilizadores.
- O Keycloak 26 marca este administrador como temporário e mostra um aviso na consola. Em dev é aceitável.

## Utilizadores de teste

Com o Keycloak a correr, em `deploy/dev`:

```bash
read -rp  "Admin Keycloak: " KEYCLOAK_ADMIN_USER
read -rsp "Password admin: " KEYCLOAK_ADMIN_PASSWORD; echo
read -rsp "Password passageiro de teste: " TESTE_PASSAGEIRO_PASSWORD; echo
read -rsp "Password staff de teste: "      TESTE_STAFF_PASSWORD; echo
export KEYCLOAK_ADMIN_USER KEYCLOAK_ADMIN_PASSWORD TESTE_PASSAGEIRO_PASSWORD TESTE_STAFF_PASSWORD
./keycloak/criar-utilizadores-teste.sh
unset KEYCLOAK_ADMIN_PASSWORD TESTE_PASSAGEIRO_PASSWORD TESTE_STAFF_PASSWORD
```

São criados `passageiro@teste.local` (papel `passageiro`) e `staff@teste.local` (papéis `passageiro` e `staff`). Os emails mudam-se com `TESTE_PASSAGEIRO_EMAIL` e `TESTE_STAFF_EMAIL`. O script pode correr várias vezes: não duplica utilizadores, só volta a definir as passwords.

## Verificar o realm

Com as variáveis `KEYCLOAK_ADMIN_*` exportadas como acima:

```bash
kc() { docker compose exec -T -e KEYCLOAK_ADMIN_USER -e KEYCLOAK_ADMIN_PASSWORD keycloak sh -c \
  '/opt/keycloak/bin/kcadm.sh config credentials --config /tmp/kc.cfg --server http://localhost:8080 --realm master --user "$KEYCLOAK_ADMIN_USER" --password "$KEYCLOAK_ADMIN_PASSWORD" >/dev/null && /opt/keycloak/bin/kcadm.sh "$@" --config /tmp/kc.cfg; r=$?; rm -f /tmp/kc.cfg; exit $r' sh "$@"; }

kc get roles -r metroisjustabus --fields name
kc get realms/metroisjustabus --fields registrationAllowed,registrationEmailAsUsername,defaultRole
kc get clients -r metroisjustabus -q clientId=web --fields clientId,publicClient,redirectUris,webOrigins,attributes
kc get users -r metroisjustabus --fields username
kc get-roles -r metroisjustabus --uusername staff@teste.local --effective --fields name

# Access token de exemplo do staff: realm_access.roles tem de conter passageiro e staff
CID=$(kc get clients -r metroisjustabus -q clientId=web --fields id --format csv --noquotes | tr -d '\r')
UID_STAFF=$(kc get users -r metroisjustabus -q username=staff@teste.local --fields id --format csv --noquotes | tr -d '\r')
kc get "clients/$CID/evaluate-scopes/generate-example-access-token" -r metroisjustabus -q userId="$UID_STAFF" | grep -A4 realm_access
```

Registo manual: em `http://localhost:8080/realms/metroisjustabus/account` → "Register". A conta nova aparece com o papel `passageiro`.
