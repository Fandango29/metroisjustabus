# MetroIsJustABus

Sistema distribuído de apoio a uma rede urbana de autocarros: consulta de rede e horários, perturbações, bilhetes e validação, lotação das viagens, subscrições e notificações.

Projeto da unidade curricular **Engenharia de Software Automatizada** (2026/2027), Departamento de Engenharia Informática.


## Estado do projeto

| Marco | Data | Estado | Onde está |
| --- | --- | --- | --- |
| Milestone 1 — Requisitos | 27/10/2026 | Entregue | `docs/requisitos/`, `prompts/prompts.md` |
| Milestone 2 — Pipeline CI/CDE/CD | 17/11/2026 | Implementada | `.github/workflows/`, `services/`, `deploy/`, `prompts/prompts-m2.md` |
| Entrega final | 11/12/2026 | Por iniciar | — |

## Estrutura do repositório

```
├── README.md                          este ficheiro
├── .gitignore                         ficheiros excluídos do repositório (segredos, builds, dependências)
├── .gitattributes                     fins de linha consistentes entre Windows e Linux
├── .github/workflows/
│   ├── servico.yml                    pipeline comum a todos os serviços (workflow reutilizável)
│   ├── ci-cd-core.yml                 pipeline do Core
│   └── ci-cd-bilhetes.yml             pipeline do Bilhetes
├── deploy/dev/
│   ├── docker-compose.yml             ambiente de desenvolvimento: Core, Bilhetes e PostgreSQL
│   ├── deploy.ps1                     deploy de um serviço, com smoke test e rollback
│   ├── init-db/01-rede.sql            estrutura e dados iniciais da base de dados do Core
│   └── .env.example                   modelo das variáveis de ambiente (sem valores reais)
├── docs/
│   ├── enunciado/                     enunciado original do projeto
│   └── requisitos/                    especificação de requisitos (Milestone 1)
├── prompts/
│   ├── prompts.md                     prompts usados na Milestone 1
│   └── prompts-m2.md                  prompts usados na Milestone 2, com erros e correções
└── services/
    ├── core/                          serviço Core: rede, linhas e paragens
    └── bilhetes/                      serviço Bilhetes e Validação: tipos de bilhete
```

Cada serviço tem a mesma organização: `app/` (código), `tests/` (testes), `Dockerfile`, `requirements.txt`, `requirements-dev.txt` e `pyproject.toml` (configuração do pytest e do ruff).

## Milestone 1 — o que está entregue

| O enunciado pede | Onde encontrar |
| --- | --- |
| Requisitos funcionais e não-funcionais | Especificação, secções 3 e 4 |
| Ambiguidades, informação em falta e pressupostos | Especificação, secção 5 |
| Rastreabilidade ao enunciado | Especificação, secção 6, e coluna "Origem" de cada requisito |
| Decomposição inicial em componentes | Especificação, secção 7 |
| Evidência do uso de LLMs na análise, refinamento e validação | Especificação, secção 8, e `prompts/prompts.md` |

## Milestone 2 — pipeline CI/CDE/CD

### Decisões

| Decisão | Escolha |
| --- | --- |
| Linguagem e framework | Python 3.13 + FastAPI |
| Testes | pytest |
| Lint | ruff |
| Base de dados | PostgreSQL 16 |
| Contentores | Docker + Docker Compose |
| Registo de imagens | GitHub Container Registry (GHCR) |
| CI/CD | GitHub Actions com runner self-hosted |
| Máquina do runner e do ambiente de dev | Portátil do Diogo (Windows, Docker Desktop com WSL 2) |
| Onde correm o lint e os testes | Dentro de um contentor (etapa `teste` do Dockerfile), com o mesmo Python e as mesmas bibliotecas da imagem final |
| Uma pipeline por serviço | Workflow reutilizável (`servico.yml`) e filtros `paths:`, para cada serviço ser construído e implantado sozinho (RNF-15) |
| Segredos | GitHub Secrets na pipeline; ficheiro `.env` local, fora do repositório (RNF-10) |
| Deploy em dev | Automático após pipeline verde, com smoke test e rollback para a versão anterior se falhar |
| Proteção da `main` | Ruleset que impede apagar o branch e fazer force push |

### Serviços e endpoints

| Serviço | Porta em dev | Endpoint | Requisito |
| --- | --- | --- | --- |
| Core | 8000 | `GET /health` | RNF-12 (health check) |
| Core | 8000 | `GET /version` | RNF-17 |
| Core | 8000 | `GET /linhas` | RF-01 |
| Core | 8000 | `GET /linhas/{id}/paragens` | RF-02 |
| Bilhetes | 8001 | `GET /health` | RNF-12 (health check) |
| Bilhetes | 8001 | `GET /version` | RNF-17 |
| Bilhetes | 8001 | `GET /tipos-bilhete` | RF-20 |

Cada serviço tem também a documentação da API gerada automaticamente em `/docs`.

O Core lê as linhas e as paragens do PostgreSQL quando a variável `DATABASE_URL` está definida, como acontece no ambiente de dev. Sem ela, como nos testes, usa os dados de exemplo de `app/dados.py`. O Bilhetes ainda usa só dados de exemplo.

### Como funciona a pipeline

A cada push, corre a pipeline do serviço cujo código mudou:

| Alteração em | Pipeline que corre |
| --- | --- |
| `services/core/` | CI/CD Core |
| `services/bilhetes/` | CI/CD Bilhetes |
| `deploy/dev/` ou `.github/workflows/servico.yml` | as duas |
| documentação, `prompts/` ou `README.md` | nenhuma |

Cada pipeline tem três jobs, e cada um só corre se o anterior passar (`needs:`):

| Job | O que faz | Requisito da M2 |
| --- | --- | --- |
| **Lint e testes** | Constrói a imagem de testes, corre o `ruff check` e o `pytest`. | 2 e 3 |
| **Build e publicação da imagem** | Constrói a imagem final com o SHA do commit gravado (`/version`). Na `main`, publica-a no GHCR com as etiquetas `<SHA>` e `dev-latest`. | 1, 4 e 5 |
| **Deploy em desenvolvimento** | Só na `main`. Corre o `deploy/dev/deploy.ps1`, que descarrega a imagem do GHCR (sem a reconstruir), substitui só o contentor deste serviço e faz o smoke test. | 6 |

**Smoke test e rollback.** Depois do deploy, o script chama o `/health` e o `/version` até 10 vezes. O deploy só é aceite se o serviço responder "ok" e o `/version` mostrar o serviço e o SHA certos. Se falhar, o script volta a pôr a correr a imagem anterior e a pipeline fica vermelha.

**Nos outros branches**, a pipeline corre o lint, os testes e o build da imagem, mas não publica nem implanta nada.

**Correr à mão.** Em Actions → CI/CD Core (ou Bilhetes) → Run workflow. A opção "Simular falha do smoke test" serve para demonstrar o rollback.

**Segredos usados pela pipeline**

| Segredo | Para quê |
| --- | --- |
| `GITHUB_TOKEN` | Criado automaticamente pelo GitHub em cada execução; usado para publicar e descarregar imagens do GHCR. |
| `POSTGRES_PASSWORD` | Password da base de dados do Core. O script de deploy cria o `.env` a partir deste segredo. |

### Runner self-hosted

- Instalado em `C:\actions-runner`, como serviço do Windows, com o nome `runner-dev`.
- O serviço corre com a conta de serviço de rede do Windows, que pertence ao grupo `docker-users` para poder usar o Docker Desktop.
- A política de execução do PowerShell está em `RemoteSigned`, para o runner poder correr os scripts dos passos e o `deploy.ps1`.
- O Docker Desktop arranca com a sessão do Windows. O portátil tem de estar ligado e com a sessão iniciada para a pipeline correr.

### Como correr localmente

**Testes e lint**, da mesma forma que a pipeline (exemplo para o Core; para o Bilhetes, troca `core` por `bilhetes`):

```bash
docker build --target teste -t core-testes services/core
docker run --rm core-testes ruff check .
docker run --rm core-testes pytest -v
```

**Ambiente de dev completo:**

```bash
cd deploy/dev
cp .env.example .env      # e definir uma password no .env
docker compose up -d --build
```

Depois, `http://localhost:8000/docs` (Core) e `http://localhost:8001/docs` (Bilhetes). Para parar: `docker compose down`.

Na máquina do runner, o ambiente de dev é gerido pela pipeline. Correr lá o `docker compose up --build` substitui a versão implantada pela versão local até ao próximo push.

### Requisitos da M2

| Requisito do enunciado | Como está cumprido |
| --- | --- |
| 1 — Build automático a partir do repositório | `on: push` nos workflows |
| 2 — Testes automáticos | Job "Lint e testes" (pytest); um teste partido bloqueia o build e o deploy |
| 3 — Verificações de qualidade | ruff no job "Lint e testes" |
| 4 — Aplicação em contentor | Dockerfile multi-etapa e docker-compose |
| 5 — Artefacto versionado | Imagens no GHCR com a etiqueta do SHA do commit |
| 6 — Deploy automático em dev | Job de deploy com smoke test e rollback |

A execução de cada pipeline, incluindo as provas do bloqueio de código partido e do rollback, fica registada no separador Actions do repositório.

### Requisitos da especificação cobertos na M2

| Requisito | Estado |
| --- | --- |
| RF-01, RF-02 (linhas e paragens) | Implementados no Core, com dados no PostgreSQL |
| RF-20 (tipos de bilhete) | Implementado no Bilhetes, com dados de exemplo |
| RNF-10 (segredos fora do repositório) | Cumprido: `.env` ignorado, GitHub Secrets na pipeline |
| RNF-12 (observabilidade) | Parcial: health check em cada serviço; métricas e logs com ID de correlação ficam para a entrega final |
| RNF-13 (histórico) | Base preparada: volume persistente do PostgreSQL |
| RNF-15 (deploy independente) | Cumprido: uma pipeline por serviço, deploy só do serviço alterado |
| RNF-16 (rollback automático) | Implementado em dev; o ambiente de produção fica para a entrega final |
| RNF-17 (rastreabilidade da versão) | Cumprido: imagens com o SHA do commit e endpoint `/version` |
| RNF-18 (qualidade e testes) | Parcial: lint sem erros na pipeline; a cobertura de testes ainda não é medida |

### Limitações conhecidas e próximos passos

- Ambiente de produção separado, com aprovação manual antes do deploy (Continuous Delivery).
- Medição da cobertura de testes na pipeline (RNF-18).
- Serviço de Notificações, broker de mensagens (RabbitMQ) e serviço de identidade (Keycloak).
- Base de dados própria para o serviço de Bilhetes.

## Regras do grupo

- **Todos os prompts usados no projeto ficam em `prompts/`**, um ficheiro por milestone.
- **Nenhum segredo** (passwords, chaves, tokens) é colocado no repositório (RNF-10).
- Fazer sempre `git pull` antes de começar a trabalhar.
- Cada alteração relevante é feita num commit próprio, com uma mensagem clara.
- Não se reescreve o histórico da `main`: os erros corrigem-se com commits novos (por exemplo, `git revert`).
