# Contexto do projeto para o agente (Claude Code)

Este ficheiro é lido pelo agente no início de cada sessão. Mantém-no atualizado: quando uma decisão muda, muda aqui também.

## O projeto

MetroIsJustABus: sistema distribuído para uma rede urbana de autocarros (consulta da rede e horários, perturbações, bilhetes e validação, lotação, subscrições e notificações). Projeto da unidade curricular Engenharia de Software Automatizada, 2026/2027.

- Requisitos: `docs/requisitos/especificacao-requisitos-m1.pdf` (RF-xx funcionais, RNF-xx não funcionais, A-xx pressupostos).
- Enunciado: `docs/enunciado/enunciado-v1.0.pdf`.

## Arquitetura

| Componente | Pasta | Porta em dev | Responsabilidade |
| --- | --- | --- | --- |
| Core | `services/core/` | 8000 | Rede, linhas, paragens, horários, viagens, perturbações, lotação |
| Bilhetes | `services/bilhetes/` | 8001 | Tipos de bilhete, compra, estados, validação |
| Notificações | `services/notificacoes/` | 8002 | Subscrições, preferências, envio de notificações |
| Web App | `services/web/` | 8003 (nginx no contentor; 5173 com `npm run dev`) | React (SPA). Sem lógica de negócio: só chama as APIs |
| Identidade | Keycloak | 8080 | Contas, login, papéis `passageiro`, `staff` e `administrador`. Realm em `deploy/dev/keycloak/` |
| Broker | RabbitMQ | 5672 / 15672 | Eventos entre serviços |

Regras da arquitetura:

- Cada serviço tem a sua própria base de dados PostgreSQL. Nenhum serviço lê a base de dados de outro.
- REST quando quem chama precisa da resposta; eventos (RabbitMQ) nos restantes casos.
- Eventos: `PerturbaçãoAlterada`, `HorárioAlterado`, `ViagemCancelada` (Core); `BilheteEmitido`, `BilheteValidado` (Bilhetes).
- Publicação de eventos pelo padrão outbox; entrega pelo menos uma vez; consumidores idempotentes.
- Pedidos de compra com chave de idempotência (RF-23).
- Os serviços validam o token JWT emitido pelo Keycloak nos endpoints protegidos.
- Todos os serviços expõem `GET /health` (RNF-12) e `GET /version` com o SHA do commit (RNF-17).

## Stack

- Python 3.13, FastAPI, pytest, ruff, psycopg 3, PostgreSQL 16.
- Web App: React com Vite, ESLint, Playwright.
- Docker com Dockerfile em três etapas (`base`, `teste`, `final`) e Docker Compose.
- GitHub Actions com runners self-hosted; imagens no GHCR (`ghcr.io/fandango29/metroisjustabus-<serviço>`).
- Web App: imagem final com nginx (`/health` e `/version` servidos pelo nginx); a pipeline usa os inputs `comando_lint` e `comando_testes` do `servico.yml` (`npm run lint`, `npm test`); os serviços Python usam os valores por omissão (`ruff check .`, `pytest -v`).
- A pipeline (`servico.yml`) corre na VM Linux `metro-dev` (runner `[self-hosted, dev]`, `shell: bash`); o deploy de dev usa `deploy/dev/deploy.sh`. O `deploy/dev/deploy.ps1` mantém-se para uso em Windows.

## Comandos

Testes e lint de um serviço Python (exemplo para o Core), tal como a pipeline os corre:

```bash
docker build --target teste -t core-testes services/core
docker run --rm core-testes ruff check .
docker run --rm core-testes pytest -v
```

Ambiente de dev completo:

```bash
cd deploy/dev
docker compose up -d --build
```

## Convenções

- Cada teste tem o ID do requisito no nome: `test_rf22_compra_bilhete_com_chave_repetida_nao_duplica`.
- Cada endpoint tem um docstring que começa pelo ID do requisito: `"""RF-22: ..."""`.
- Código, nomes, comentários e mensagens de commit em português de Portugal.
- Commits pequenos, um por alteração lógica, com mensagens que dizem o que muda e porquê.
- Uma tarefa = um branch (`feat/<n.º da issue>-<descrição-curta>`) = um pull request.
- Valores de dinheiro em cêntimos inteiros; nunca `float`.
- Consultas SQL sempre com parâmetros (`%s`), nunca com texto colado.
- Novas dependências: acrescentar a `requirements.txt` (para correr) ou a `requirements-dev.txt` (só para testes).

## Regras que o agente nunca pode quebrar

1. Nunca escrever passwords, tokens ou chaves em ficheiros do repositório. Segredos só em `.env` (ignorado pelo Git) ou nos GitHub Secrets.
2. Nunca editar ou ler o conteúdo de ficheiros `.env`.
3. Nunca reescrever o histórico (`git push --force`, `git rebase` de commits publicados).
4. Nunca fazer push diretamente para a `main`: trabalhar sempre num branch.
5. Nunca apagar ou desativar testes para fazer a pipeline passar.
6. Não acrescentar funcionalidades que a tarefa não pede.

## Quando uma tarefa está feita

- Os critérios de aceitação da issue estão cumpridos.
- Há testes novos para o comportamento novo, incluindo os casos de erro.
- `ruff check .` e `pytest` passam no contentor de testes.
- O pull request diz que requisitos cobre e o que foi testado.
- Se uma decisão de arquitetura mudou, este ficheiro foi atualizado.
