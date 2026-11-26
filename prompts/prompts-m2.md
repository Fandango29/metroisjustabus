# Prompts — Milestone 2

- **Ferramenta:** Claude Opus 5.5 (claude.ai), numa só conversa, continuação da Milestone 1
- **Autor dos prompts:** Diogo Santos
- **Datas:** 04/11/2026 e 05/11/2026
- **Contexto dado:** repositório do projeto (zip), enunciado, especificação da M1, resumos das aulas teóricas, e o output do terminal e da pipeline ao longo do trabalho
- **Artefactos produzidos com apoio da IA:** plano da M2, serviços Core e Bilhetes, testes, Dockerfile, docker-compose, workflows do GitHub Actions, script de deploy, README

Os prompts estão transcritos tal como foram enviados, pela ordem em que foram enviados, incluindo os erros de escrita. Quando o prompt era o output do terminal, fica só o início, com a indicação *[output omitido]*. Tokens e passwords foram retirados.

Em cada entrada, a linha **Ação da equipa** regista o que foi feito com a resposta: aceite, corrigido ou rejeitado. No fim, há um resumo dos erros e problemas encontrados.

---

## Parte 1 — Planeamento

### P-01 — O que é pedido na Milestone 2

- **Data:** [confirmar data] · **Contexto:** zip do repositório e PDF do enunciado

**Prompt:**
> @Projeto.zip @enunciado-v1.0.pdf esta parte do projeto corresponde a Mileston 1, com base no enunciado explica me o que tem de ser feito na Milestone 2

**Resposta (resumo):** Explicou os seis requisitos da M2 (build automático, testes, verificações de qualidade, contentores, artefacto versionado e deploy automático em dev) e as restrições do enunciado (runner self-hosted, ambientes separados, segredos).

**Ação da equipa:** Aceite. Comparado com o enunciado.

### P-02 — Plano completo da Milestone 2

- **Data:** [confirmar data]

**Prompt:**
> por onde me aconselhavas começar? Dá-me uma lista completa do que fazer por ondem de modo a ter a Milestone 2 completamente concluida

**Resposta (resumo):** Plano com 8 fases e 26 passos, cada um com um critério de "está feito quando": decisões, máquina e runner, código mínimo do Core, contentores, pipeline de CI, deploy em dev, melhorias, documentação e apresentação.

**Ação da equipa:** Aceite como plano de trabalho.

### P-03 — Ter em conta os resumos das aulas

- **Data:** 2026-11-04 · **Contexto:** `Resumos_Aulas.docx`

**Prompt:**
> @Resumos_Aulas.docx isto são os resumos dos pdfs teoricos dados nas aulas, todas as decisões que tomares tem sempre em conta isto

**Resposta (resumo):** Propôs um plano revisto com 10 alterações (trabalho com pull requests, mais ferramentas de verificação, ficheiros de especificação por funcionalidade, entre outras).

**Ação da equipa:** Ver P-05.

### P-04 — Diferenças em relação ao plano inicial

- **Data:** 2026-11-04 19:16

**Prompt:**
> quais são as diferencas para o que tinhas proposto inicialmente ?

**Resposta (resumo):** Listou as 10 diferenças e indicou as que davam mais trabalho.

**Ação da equipa:** Analisado. Levou à decisão do P-05.

### P-05 — Rejeição das alterações, exceto o rollback

- **Data:** 2026-11-04 19:21

**Prompt:**
> esquece todas estas alterações (aproveitando apenas esta: Rollback. No plano inicial, o smoke test ao `/health` só mostrava se o deploy tinha corrido bem. Agora, se o teste falhar, a pipeline volta automaticamente à imagem anterior. Isto também cumpre um RNF vosso da M1.) e continua com o que me disseste primeiro:
>
> *[o prompt continuava com o texto completo do plano original, colado da resposta ao P-02]*

**Resposta (resumo):** Voltou ao plano original e acrescentou o rollback ao passo 17.

**Ação da equipa:** **Decisão humana.** A equipa rejeitou 9 das 10 alterações propostas pela IA, para manter o âmbito da M2 controlado, e aceitou só o rollback, que cumpre o RNF-16 da especificação.

---

## Parte 2 — Fase 0: decisões

### P-06, P-07 — Explicação e comandos da Fase 0

- **Datas:** 2026-11-04 19:22 e 19:27

**Prompts:**
> vamos começar pelo inicio, pelo fase 0

> da me esses comandos aqui

**Resposta (resumo):** Explicou cada decisão (stack, máquina do runner, divisão do trabalho) e deu os comandos para registar as decisões no README.

**Ação da equipa:** Aceite. Decidido usar o portátil do Diogo como runner e ambiente de dev. Decisões registadas no README.

---

## Parte 3 — Fase 1: Docker e runner self-hosted

### P-08 — Início da Fase 1

- **Data:** 2026-11-04 19:45

**Prompt:**
> Segue para a fase 1

**Resposta (resumo):** Passos para instalar o WSL 2 e o Docker Desktop, registar o runner como serviço do Windows e testá-lo com um workflow mínimo.

**Ação da equipa:** Aceite. Executado passo a passo (P-09 a P-21).

### P-09 — Instalação do WSL

- **Data:** 2026-11-04 20:07

**Prompt:**
> eu ainda não reniciei o computador
>
> isto foi o que apareceu depois de eu ter usado o comando
>
> PS C:\WINDOWS\system32> wsl --install
> A transferir: Ubuntu
> *[output omitido]*

**Resposta (resumo):** Confirmou que a instalação correu bem; o primeiro nome de utilizador foi recusado só por ter maiúsculas.

**Ação da equipa:** Aceite.

### P-10 a P-13 — Docker Desktop já instalado

- **Datas:** 2026-11-04 20:16, 20:19, 20:23 e 20:25

**Prompts:**
> eu ja tinha o Docker Desktop instalado mas nao sei se marquei esta opção durante a intalação "Use WSL 2 instead of Hyper-V"

> *[texto do passo 4.2 colado da resposta anterior]* então explica me esta parte tendo em conta que eu ja tinha o docker desktop instalado

> isto é o menu principal ? *(com captura de ecrã)*

> ja esta selecionado ? *(com captura de ecrã)*

**Resposta (resumo):** Adaptou o passo à instalação existente; explicou que a página aberta era o site da Docker e não a aplicação; confirmou que o motor WSL 2 já estava ativo.

**Ação da equipa:** Aceite.

### P-14 — Ligar o Git Bash ao repositório

- **Data:** 2026-11-04 20:31

**Prompt:**
> como ligar o gitbash ao meu repositorio no git hub?

**Resposta (resumo):** Explicou como confirmar a ligação com `git remote -v` e o que fazer em cada caso.

**Ação da equipa:** Compreensão. A pasta já estava ligada.

### P-15 — Teste do Docker

- **Data:** 2026-11-04 20:33

**Prompt:**
> $ docker --version
> Docker version 29.9.2, build a82e528
> *[output omitido]*
> $ docker run Projeto ADS
> docker: invalid reference format: repository name (library/Projeto) must be lowercase

**Resposta (resumo):** Explicou que `hello-world` é o nome literal de uma imagem de teste e não um nome a substituir.

**Ação da equipa:** **Engano humano** na leitura da instrução, corrigido. O teste com `docker run hello-world` passou.

### P-16 — PowerShell sem administrador

- **Data:** 2026-11-04 20:41

**Prompt:**
> *[instrução do passo 4.1 colada da resposta anterior]* eu nao executei como administrador

**Resposta (resumo):** Mostrou, pelo output enviado antes (`PS C:\WINDOWS\system32>`), que o PowerShell estava como administrador e que não era preciso repetir nada.

**Ação da equipa:** Aceite.

### P-17 — Download do runner

- **Data:** 2026-11-04 20:45

**Prompt:**
> PS C:\WINDOWS\system32> mkdir actions-runner; cd actions-runner
> *[output omitido]*
> esta certo ?

**Resposta (resumo):** Os downloads estavam certos, mas a pasta tinha ficado dentro de `C:\WINDOWS\system32`, porque o comando da página do GitHub foi corrido a partir da pasta onde o PowerShell de administrador começa. Deu o comando para a mover para `C:\actions-runner`.

**Ação da equipa:** **Problema detetado pela IA** na revisão do output. Corrigido.

### P-18 a P-20 — Refazer a configuração do runner

- **Datas:** 2026-11-04 20:49, 20:52 e 20:53

**Prompts:**
> eu enganei me a configurar o runner como é que eu volto a fazer a configuração?

> PS C:\actions-runner> ./config.sh remove --token *[token retirado]*
> ./config.sh : The term './config.sh' is not recognized *[output omitido]*

> nao preciso de fazer o download outra vez ?

**Resposta (resumo):** Explicou como remover e voltar a configurar o runner. O `config.sh` é a versão para Linux, mostrada na página do GitHub; no Windows é o `config.cmd`. Não era preciso descarregar o runner outra vez.

**Ação da equipa:** Aceite. Runner removido e configurado de novo.

### P-21 — Password recusada na configuração do serviço

- **Data:** 2026-11-04 20:58

**Prompt:**
> Password for the account fandango\diogo **********
> Invalid windows credentials entered. Try again or ctrl-c to quit

**Resposta (resumo):** A conta do Windows é uma conta Microsoft, que muitas vezes não é aceite em serviços. Propôs usar a conta de serviço de rede do Windows e adicioná-la ao grupo `docker-users`.

**Ação da equipa:** **Pressuposto da IA corrigido:** as instruções anteriores assumiam uma conta local do Windows. Aceite a solução alternativa.

### P-22 — Nome da conta de sistema em português

- **Data:** 2026-11-04 21:05

**Prompt:**
> PS C:\actions-runner> net localgroup docker-users "NT AUTHORITY\NETWORK SERVICE" /add
> Não existe nenhum utilizador ou grupo global NT AUTHORITY\NETWORK SERVICE.
> *[output omitido]*

**Resposta (resumo):** O Windows está em português e o nome da conta é traduzido. Deu um comando que usa o identificador interno da conta (`S-1-5-20`), igual em todas as línguas.

**Ação da equipa:** **Erro da IA:** o comando assumia um Windows em inglês. Corrigido e confirmado com `Get-LocalGroupMember`.

### P-23 — Runner ativo e primeiro workflow falhado

- **Data:** 2026-11-04 21:07 a 21:14 *(capturas de ecrã do GitHub)*

**Prompts:** confirmação do serviço do runner (output do PowerShell), captura de ecrã do runner "Idle" e capturas de ecrã do workflow de teste falhado.

**Resposta (resumo):** O workflow de teste falhou porque o Windows bloqueia scripts de PowerShell por defeito. Propôs mudar a política de execução para `RemoteSigned`.

**Ação da equipa:** **Problema não previsto pela IA**, detetado no log da pipeline. Corrigido.

---

## Parte 4 — Fase 2: código mínimo do Core

### P-24 — Início da Fase 2

- **Data:** 2026-11-04 21:19

**Prompt:**
> segue para a fase 2

**Resposta (resumo):** Estrutura do serviço Core, quatro endpoints (`/health`, `/version`, `/linhas`, `/linhas/{id}/paragens`), seis testes com o ID do requisito no nome e a configuração do ruff.

**Ação da equipa:** Aceite. Os IDs dos requisitos (RF-01, RF-02, RNF-12, RNF-17) foram confirmados na especificação da M1.

### P-25 a P-28 — Compreensão da Fase 2

- **Datas:** 2026-11-04 21:27, 21:28, 21:29 e 21:31

**Prompts:**
> explica me o passo 8

> mas isto vai fazer parte do trabalho ou corresponde apenas a uma simulação da miestone 2

> explica me o que é que esta a fazer na fase 2 para que serve esta fase

> *[texto dos passos 8 a 10 colado da resposta anterior]* esta parte ainda nao esta completa certo? vai ser completada na entrega final do projeto?

**Resposta (resumo):** Explicou o código linha a linha; que o código faz parte do trabalho final (só os dados de exemplo são temporários); para que serve cada passo; e que a fase fica completa para a M2 e vai crescendo até à entrega final.

**Ação da equipa:** Compreensão.

### P-29, P-30 — Commit sem o código do serviço

- **Datas:** 2026-11-04 21:41 e 21:42

**Prompts:**
> diogo@Fandango MINGW64 /c/Universidade/Mestrado/1ºAno/ADS/Projeto/services/core (main)
> *[output do git status, git add, git commit e git push omitido]*

> $ git add services/core/requirements.txt services/core/requirements-dev.txt services/core/app/
> *[output omitido]*

**Resposta (resumo):** O primeiro `git add` falhou (`pathspec 'services/.gitkeep' did not match`), por isso o código não entrou no commit `a0dff3f`. Deu os comandos para um commit novo com os ficheiros em falta, sem reescrever o histórico já publicado.

**Ação da equipa:** **Erro nas instruções da IA:** o comando incluía um ficheiro já removido num passo anterior. Detetado na revisão do output do terminal e corrigido com um commit novo.

### P-31, P-32 — Revisão das Fases 0 a 2

- **Datas:** 2026-11-04 21:44 e 21:46

**Prompts:**
> explica me tudo o que foi feito ate a fase 2

> como é que eu sei se até aqui esta tudo a funcionar bem

**Resposta (resumo):** Resumo das fases e uma lista de verificações, incluindo clonar o repositório do zero e correr os testes, para confirmar que nada ficou só no computador local.

**Ação da equipa:** Verificações executadas.

---

## Parte 5 — Fase 3: contentores

### P-33 a P-35 — Início da Fase 3

- **Datas:** 2026-11-04 21:48, 22:00 e 22:01

**Prompts:**
> ok segue para a fase 3

> da me o comando para fazer isto *[instrução colada da resposta anterior]*

> era so para veres onde é que estava dados.py *(com captura de ecrã)*

**Resposta (resumo):** `.gitattributes`, o Core a ler do PostgreSQL, o Dockerfile, o docker-compose com o PostgreSQL e o `.env.example`; um comando `sed` para alterar a linha pedida.

**Ação da equipa:** Aceite.

### P-36 — Versão do Python

- **Data:** 2026-11-04 22:05

**Prompt:**
> esta é que é a minha versao do python *(com captura de ecrã: Python 3.13.3)*

**Resposta (resumo):** Propôs alinhar o projeto todo para o Python 3.13: o README, o ruff e a imagem base do Dockerfile.

**Ação da equipa:** **Pressuposto da IA detetado pela equipa:** a IA tinha proposto o Python 3.12, diferente da versão instalada. Corrigido para 3.13.

### P-37 a P-39 — Verificações da Fase 3

- **Datas:** 2026-11-04 22:11, 22:16 e 22:19

**Prompts:**
> *[output do docker build, docker run e curl, em anexo]* esta tudo certo ?

> $ git check-ignore -v .env
> .gitignore:2:.env       .env

> $ docker compose exec core-db psql -U core -d core -c "INSERT INTO linhas (id, nome) VALUES ('L3', 'Linha de teste');"
> *[output omitido]*
> esta correto ?

**Resposta (resumo):** Confirmou que a imagem tem o SHA do commit, que o `.env` é ignorado pelo Git e que o Core lê da base de dados (a linha L3 inserida só na base de dados apareceu no `/linhas`).

**Ação da equipa:** Aceite.

### P-40 a P-43 — Estado do repositório no fim da Fase 3

- **Datas:** 2026-11-04 22:21, 22:24, 22:25 e 22:27

**Prompts:**
> no final da fase 3 como é que devia estar o meu repositorio ?

> o meu repositorio esta assim, esta correto ? *(com capturas de ecrã)*

> *[output do git status e do git grep]*

> este ficheiro esta correto ? *(captura de ecrã do .env.example)*

**Resposta (resumo):** Estrutura esperada e comandos de verificação; confirmou que não havia passwords no repositório; assinalou uma incoerência num comentário do `.env.example`.

**Ação da equipa:** Aceite.

### P-44 — Revisão completa do repositório

- **Data:** 2026-11-04 22:29 · **Contexto:** zip do repositório

**Prompt:**
> isto é o meu repositorio no final da fase 3, analisa todos os ficheiros e diz me se existe algum erro

**Resposta (resumo):** Código, Docker e compose sem erros (ruff e formatação verificados). Erros no README: faltava a tabela da divisão do trabalho, o estado do projeto e a estrutura estavam desatualizados. Notas: o registo de prompts da M2 ainda estava por fazer; o RNF-12 e o RNF-18 estão só parcialmente cobertos.

**Ação da equipa:** **Erros humanos detetados pela IA** no README. Corrigidos.

### P-45 — Para que serve o `.env.example`

- **Data:** 2026-11-04 22:32

**Prompt:**
> para que serve o ficheiro .env.example

**Resposta (resumo):** Modelo das variáveis necessárias, sem valores reais, para quem clona o repositório.

**Ação da equipa:** Compreensão.

---

## Parte 6 — Fase 4: pipeline de integração contínua

### P-46 — Início da Fase 4

- **Data:** 2026-11-05 15:20

**Prompt:**
> avança agora para a parte 4

**Resposta (resumo):** Workflow `ci-cd.yml` com dois jobs (lint e testes → build e publicação no GHCR). Mudou a abordagem do plano: o lint e os testes passam a correr num contentor (etapa `teste` do Dockerfile), porque a conta de serviço do runner não vê o Python instalado para o utilizador.

**Ação da equipa:** Aceite. Pipeline verde à primeira execução; imagem publicada no GHCR.

### P-47 — Avisos na pipeline

- **Data:** 2026-11-05 15:34 *(capturas de ecrã)*

**Prompt:** capturas de ecrã da pipeline verde, com 2 avisos sobre o Node.js 20, e do pacote no GHCR.

**Resposta (resumo):** Os avisos vêm de versões antigas das ações. Propôs `actions/checkout@v5` e `docker/login-action@v4`, depois de confirmar numa pesquisa que a v4 existe e é compatível com a versão do runner.

**Ação da equipa:** **Erro da IA:** tinha proposto versões das ações já descontinuadas. Corrigido.

### P-48 — Segredo da base de dados

- **Data:** 2026-11-05 15:40 *(captura de ecrã do git grep)*

**Resposta (resumo):** Confirmou que a única password no repositório é a de exemplo.

**Ação da equipa:** Segredo `POSTGRES_PASSWORD` criado no GitHub.

---

## Parte 7 — Fase 5: deploy automático em dev

### P-49 — Início da Fase 5

- **Data:** 2026-11-05 15:41

**Prompt:**
> avança para a fase 5

**Resposta (resumo):** Script `deploy/dev/deploy.ps1` (versão anterior, deploy, smoke test e rollback), job de deploy no workflow e duas provas. Mudou o passo 18 do plano: a prova do bloqueio passa a ser feita na `main`, porque num branch o deploy nunca acontece e o teste não provaria nada.

**Ação da equipa:** Aceite. Três jobs verdes; o `/version` em dev mostrou o mesmo SHA que o `git rev-parse HEAD`.

### P-50 — Prova do bloqueio de código partido

- **Data:** 2026-11-05 15:53 *(capturas de ecrã)*

**Resposta (resumo):** Confirmou o resultado: testes vermelhos, build e deploy não executados, `/version` sem alteração. Deu o `git revert` para repor o teste sem reescrever o histórico.

**Ação da equipa:** Prova executada e registada (`docs/evidencias/m2/`).

### P-51, P-52 — Prova do rollback

- **Datas:** 2026-11-05 16:01 e 16:02

**Prompts:**
> Error: O smoke test falhou para ghcr.io/fandango29/metroisjustabus-core:1b269f3…
> A repor a versao anterior: ghcr.io/fandango29/metroisjustabus-core:9e26ba9…
> *[output omitido]*

> era suposto dar erro ?

**Resposta (resumo):** Confirmou que o rollback funcionou (a versão anterior foi reposta e a base de dados não foi mexida) e explicou porque é que a pipeline deve ficar vermelha quando um deploy é revertido.

**Ação da equipa:** Prova executada e registada.

---

## Parte 8 — Fase 6: segundo serviço e proteção da `main`

### P-53 — Início da Fase 6

- **Data:** 2026-11-05 16:41

**Prompt:**
> segue para a fase 6

**Resposta (resumo):** Serviço Bilhetes (RF-20), script de deploy generalizado por serviço, workflow reutilizável com uma pipeline por serviço (RNF-15), regras de proteção da `main`. Recomendou adiar o RabbitMQ e o Keycloak para a entrega final.

**Ação da equipa:** Aceite.

### P-54, P-55 — Falha na publicação da imagem do Bilhetes

- **Datas:** 2026-11-05 16:56 a 17:00

**Prompts:**
> o que esta em vermelho é publicar a imagem (etiquetaSHA)

> ok ja deu tudo a verde

**Resposta (resumo):** Sugeriu repetir o job, por ser provavelmente uma falha temporária na primeira publicação de um pacote novo.

**Ação da equipa:** Re-run do job falhado; passou. Prova do RNF-15 executada (só a pipeline do Bilhetes correu, e o Core manteve a versão).

### P-56, P-57 — Proteção da `main`

- **Datas:** 2026-11-05 17:06 e 17:10

**Prompts:**
> *[texto do passo 20 colado da resposta anterior]* aconcelhas a fazer isto ?

> *[texto colado da resposta anterior]* nos ainda nao queremos trabalhar ja com Pull Requests o qeu temos de fazer para acabar a fase 6

**Resposta (resumo):** Recomendou ativar já as regras que protegem o histórico e deixar os pull requests obrigatórios para quando o grupo trabalhar em paralelo.

**Ação da equipa:** **Decisão humana:** não usar pull requests obrigatórios por agora. Ativadas só as regras "Restrict deletions" e "Block force pushes".

### P-58 — Início da Fase 7

- **Data:** 2026-11-05 17:19

**Prompt:**
> segue para a fase 7

**Resposta (resumo):** README atualizado, este registo de prompts e o índice das evidências.

**Ação da equipa:** [rever estes três ficheiros antes do commit e registar aqui o que foi alterado]

---

## Resumo

### Erros e problemas encontrados

| # | Problema | Origem | Detetado por | Correção | Prompt |
| --- | --- | --- | --- | --- | --- |
| 1 | Plano revisto com 10 alterações fora do âmbito pretendido | IA | Equipa | Rejeitadas 9 das 10 alterações | P-05 |
| 2 | Leitura errada da instrução `docker run hello-world` | Humana | IA | Comando corrigido | P-15 |
| 3 | Pasta do runner criada dentro de `C:\WINDOWS\system32` | Ambiente (comando do GitHub corrido na pasta por defeito) | IA | Pasta movida para `C:\actions-runner` | P-17 |
| 4 | Instruções assumiam uma conta local do Windows; a conta é Microsoft | IA | Erro no configurador do runner | Conta de serviço de rede no grupo `docker-users` | P-21 |
| 5 | Comando com nome de conta em inglês num Windows em português | IA | Erro do comando | Uso do identificador `S-1-5-20` | P-22 |
| 6 | Política do PowerShell bloqueou o runner | Ambiente (não previsto pela IA) | Log da pipeline | Política `RemoteSigned` | P-23 |
| 7 | `git add` com um ficheiro já removido; commit sem o código | IA | Revisão do output | Commit novo, sem reescrever o histórico | P-29 |
| 8 | Python 3.12 proposto; instalado 3.13 | IA | Equipa | Projeto alinhado para 3.13 | P-36 |
| 9 | README sem a divisão do trabalho e desatualizado | Humana | IA | README corrigido | P-44 |
| 10 | Versões de ações do GitHub descontinuadas (Node.js 20) | IA | Avisos da pipeline | Ações atualizadas | P-47 |
| 11 | Prova do passo 18 num branch não provaria o bloqueio | IA (no plano inicial) | IA | Prova feita na `main`, com `git revert` | P-49 |
| 12 | Falha temporária na publicação de uma imagem nova | Ambiente | Log da pipeline | Re-run do job | P-54 |

### Decisões tomadas pela equipa

- Rejeição das alterações ao plano propostas no P-03, exceto o rollback (P-05).
- Portátil do Diogo como runner self-hosted e ambiente de dev (P-06).
- Alinhamento do projeto com o Python 3.13 instalado (P-36).
- Pull requests não obrigatórios por agora; só as regras de proteção do histórico (P-57).

### Métricas

| Métrica | Valor |
| --- | --- |
| Sessões com IA | 2 (04/11 e 05/11) |
| Prompts registados | 58 |
| Erros e problemas registados | 12 (7 com origem na IA, 2 humanos, 3 do ambiente) |
| Tempo total de trabalho | [preencher] |
