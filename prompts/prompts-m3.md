# Prompts — Entrega final

- **Ferramenta:** Claude Opus 5.5 (claude.ai), na mesma conversa da Milestone 1 e da Milestone 2
- **Autor dos prompts:** Diogo Santos
- **Contexto dado:** repositório do projeto (zip), enunciado, especificação da M1, email do docente sobre as VMs do DEI, capturas de ecrã do portal my.dei
- **Artefactos produzidos com apoio da IA:** plano da entrega final (documento), lista de tarefas por pessoa, texto do pedido das VMs, `CLAUDE.md`, modelos de issue e de pull request, registo de métricas

Os prompts estão transcritos tal como foram enviados, pela ordem em que foram enviados, incluindo os erros de escrita. Quando o prompt era texto colado de uma resposta anterior, fica só a indicação *[texto colado]*. Cada sessão acrescenta-se ao fim deste ficheiro.

Em cada entrada, a linha **Ação da equipa** regista o que foi feito com a resposta: aceite, corrigido ou rejeitado.

---

## Sessão 1 — 17/11/2026: planeamento da entrega final e pedido das VMs

### P-01 — O que falta para a entrega final

- **Hora:** 10:34 · **Contexto:** zip do repositório no fim da M2

**Prompt:**
> isto é o meu projeto ate a milestone 2, diz o que tem de ser feito na milestone 3

**Resposta (resumo):** Esclareceu que o enunciado não tem Milestone 3: depois da M2 vem a entrega final (11/12, 90% da nota). Comparou o que o enunciado exige com o estado do projeto: 45 dos 48 requisitos funcionais por fazer, faltam a Web App, o Keycloak, o RabbitMQ, o serviço de Notificações, o ambiente de produção, os testes de integração e de sistema, a monitorização, o processo com agentes, as métricas, o relatório e o vídeo. Assinalou que o `prompts-m2.md` não estava no repositório.

**Ação da equipa:** Aceite. Confirmado no enunciado que não existe Milestone 3.

### P-02 — Aplicação web

- **Hora:** 10:35

**Prompt:**
> vamos ter uma aplicação certo ?

**Resposta (resumo):** Sim: uma aplicação web (SPA), prevista na arquitetura da M1, sem lógica de negócio, que chama as APIs dos serviços; tem de funcionar em telemóvel (RNF-19).

**Ação da equipa:** Compreensão.

### P-03 — Decisões para o plano

- **Hora:** 10:58

**Prompt:**
> ajuda me a fazer a milestone 3

**Resposta (resumo):** Antes de planear, perguntou quatro decisões: onde corre a produção, a tecnologia da Web App, o agente de IA e por onde começar.

**Ação da equipa:** **Decisões humanas:**
- Produção nas VMs do DEI, com base num email do docente recebido nesse dia, colado como resposta.
- Web App em React.
- Agente: Claude Code.
- Começar por um plano completo.

A IA criou o documento "Plano da entrega final", com o calendário, a infraestrutura, o processo com agentes e as métricas, as funcionalidades em três ondas, a Web App, os testes, a pipeline até produção, a monitorização, o relatório e a divisão do trabalho.

### P-04, P-05 — Uma VM ou duas

- **Hora:** 11:30 · **Contexto:** comentário no plano

**Prompts:**
> o que é que recomendas de acordo com o meu projeto ate agora?

> Pedir as duas *(resposta a um comentário no plano)*

**Resposta (resumo):** Recomendou pedir duas VMs (dev e produção). Razões: o runner no portátil já tinha ficado offline; quase todos os problemas da M2 vieram do Windows; com dev e produção em Linux há um só script de deploy.

**Ação da equipa:** Aceite. O plano foi atualizado.

### P-06, P-07 — Pull requests

- **Hora:** 11:32 · **Contexto:** comentário no plano

**Prompts:**
> o que recomendas ?

> Passar a pull requests *(resposta a um comentário no plano)*

**Resposta (resumo):** Recomendou passar a pull requests com 1 aprovação: há trabalho em paralelo, a pipeline verifica antes do merge, há revisão humana do trabalho do agente e rastreabilidade.

**Ação da equipa:** **Decisão humana que altera a da M2,** onde não se usaram pull requests. O plano foi atualizado.

### P-08 — Divisão do trabalho

- **Hora:** 11:33 · **Contexto:** comentário no plano

**Prompt:**
> Aceite como está *(resposta a um comentário no plano)*

**Resposta (resumo):** Marcou a divisão do trabalho como aceite, faltando a confirmação do Bernardo e do Tomás.

**Ação da equipa:** Aceite pelo Diogo; por confirmar com o grupo.

### P-09 — Início do trabalho

- **Hora:** 11:39

**Prompt:**
> comeca a realização da milestone 3

**Resposta (resumo):** Criou o `CLAUDE.md`, os modelos de issue e de pull request e a pasta `metricas/`, e redigiu um texto para pedir as VMs ao DEI Helpdesk.

**Ação da equipa:** Ficheiros aceites. O texto do pedido foi adaptado no passo seguinte (ver P-10).

### P-10 a P-14 — Pedido das VMs no portal my.dei

- **Horas:** 11:42 a 11:52 · **Contexto:** capturas de ecrã de cada passo do formulário

**Prompts:**
> *(captura de ecrã da página Virtual Machines do my.dei, sem texto)*

> *(captura de ecrã do passo "Type", sem texto)*

> *(captura de ecrã do passo "Details", sem texto)*

> *[texto do campo Objective colado]* com estas VM so conseguimos correr o codigo no dei ou consigo correr em casa ?

> *(captura de ecrã do passo "Resources", sem texto)*

> da me este texto todo ja corrigido

> *(captura de ecrã do passo "Review", sem texto)*

**Resposta (resumo):**
- Indicou o tipo "resource group", para pedir as duas VMs num só pedido.
- Indicou o docente como responsável e os colegas como utilizadores adicionais.
- Indicou o período até 28/02/2027.
- Explicou que a pipeline funciona de casa sem alterações e que o acesso às VMs de fora do DEI provavelmente exige VPN.
- Ajustou os recursos ao limite do perfil de estudante.

**Ação da equipa:** Pedido submetido a 17/11. **Erros da IA corrigidos:**
- A IA propôs primeiro um texto para o Helpdesk, mas o pedido faz-se por um formulário próprio no my.dei.
- A IA propôs 6 vCPU, 12 GB de RAM e 100 GB no total, acima do limite do perfil de estudante (4 vCPU, 8 GB, 100 GB), que o formulário mostrou. Foi corrigido para 2 vCPU e 4 GB por VM.

### P-15 a P-19 — Próximos passos e pull requests

- **Horas:** 11:54 a 12:13

**Prompts:**
> depois de fazer  o Request das VMs o que tenho de fazer

> para que serve o zip ? que ficheiros contem ?

> relativamente ao ponto 2 como é que vai funcionar ?

> a revisão nao pode ser feita por mim ?

> se eu optasse por nao fazer pull requests o que poderia acontecer ao meu projeto ?

**Resposta (resumo):**
- Lista de tarefas sem dependência das VMs.
- Explicação de cada ficheiro do zip.
- O fluxo issue → branch → pull request → revisão → merge.
- O GitHub não deixa o autor aprovar o próprio pull request.
- As consequências de não usar pull requests: menos evidência de supervisão, `main` partida mais vezes, mais conflitos.

**Ação da equipa:** Compreensão. Mantida a decisão de usar pull requests com 1 aprovação.

---

## Sessão 2 — 19/11/2026: lista de tarefas e trabalho em equipa

### P-20 — Lista de tarefas por pessoa

- **Hora:** 12:50

**Prompt:**
> *[lista dos passos 2 a 7 colada da resposta anterior]* da me uma lista de tudo o que tem de ser feito, nao so por mim como tambem pelos meus colegas, para termos a milestone 3 toda toda feitae pronta a entregar

**Resposta (resumo):** Separador "Lista de tarefas" no plano, por semana (19/11 a 11/12) e por pessoa, com a lista do que se entrega a 11/12.

**Ação da equipa:** Aceite.

### P-21 a P-23 — Usar só o computador do Diogo

- **Horas:** 12:54, 13:00 e 13:03

**Prompts:**
> tenho uma duvida, o trabalhho pode ser todo feito no meu computador ?

> entao nao precisamos dos computadores dos meus colegas, eles podem usar o meu ?

> mas nos vamos trabalhar em branches, se por exemplo o bernardo tiver no meu computador mas tiver na sua branch os commits continuam a ficar em meu nome? se sim como é que eles ficam no nome do bernardo ?

**Resposta (resumo):**
- O código pode ser feito no portátil, mas a produção não: tem de estar sempre disponível e separada de dev.
- Se todos usarem o computador do Diogo, os commits e os pull requests ficam em nome dele, o que tira aos colegas a evidência de contribuição.
- Para isso não acontecer: uma pasta de clone por pessoa, com `user.name` e `user.email` locais e a conta GitHub de cada um no endereço do repositório.

**Ação da equipa:** Compreensão. Decidido que cada um trabalha no seu computador.

### P-24 — Pedido cancelado

- **Hora:** 13:06

**Prompt:**
> faz o mesmo para este *[endereço de uma página externa]*

**Resposta:** Nenhuma. O pedido foi interrompido pelo utilizador antes da resposta.

**Ação da equipa:** Cancelado.

---

## Sessão 3 — 26/11/2026: arranque do trabalho

### P-25, P-26 — Recomeçar pelo princípio

- **Horas:** 13:00 e 14:18

**Prompts:**
> ajuda me a comecar a realizar a milestone 3 desde o inicio

> vamos comecar por aqui *[tarefas da semana 1 do Diogo coladas da lista de tarefas]*

**Resposta (resumo):** Assinalou que, a 26/11, faltam 15 dias e a semana das fundações já passou. Deu os passos para pôr os ficheiros no repositório e ativar os pull requests, e preparou este registo como primeiro pull request.

**Ação da equipa:** [preencher]

---

## Resumo até agora

### Erros e problemas encontrados

| # | Problema | Origem | Detetado por | Correção | Prompt |
| --- | --- | --- | --- | --- | --- |
| 1 | Texto para o Helpdesk, quando o pedido se faz por um formulário no my.dei | IA | Equipa | Pedido feito pelo formulário | P-10 |
| 2 | Recursos pedidos acima do limite do perfil de estudante | IA | Formulário do DEI | Ajustado para 2 vCPU e 4 GB por VM | P-13 |

### Decisões tomadas pela equipa

- Produção nas VMs do DEI (P-03), duas VMs (P-05).
- Web App em React, agente Claude Code (P-03).
- Pull requests com 1 aprovação, ao contrário da M2 (P-07).
- Cada membro trabalha no seu computador (P-23).

---

## Sessão 4 — 26/11/2026: primeira tarefa com o Claude Code (issue #2)

- **Ferramenta:** Claude Code 2.1.332, modelo Opus 5.5, conta Claude Pro, em plan mode e depois com aprovação manual de cada alteração

### P-27 — RabbitMQ e Keycloak no ambiente de dev

**Prompt:**
> Lê o CLAUDE.md. Tarefa: issue #2 — acrescentar o RabbitMQ e o Keycloak ao ambiente de dev em deploy/dev/docker-compose.yml. *[seguido dos requisitos, restrições e verificação, conforme a issue #2]*

**Resposta (resumo):**
- Apresentou um plano: dois serviços novos e um volume no `docker-compose.yml`, e as variáveis novas no `.env.example`.
- Confirmou com `docker manifest inspect` que as versões das imagens existiam antes de as escrever.
- Usou `${VAR:-}` para não partir o `deploy.ps1`, e `hostname: rabbitmq` para os dados persistirem.
- Validou o ficheiro sem imprimir os segredos do `.env`.
- Assinalou que o Keycloak em `start-dev` não guarda dados.

**Ação da equipa:** Aceite. O plano foi lido antes de aprovado, e cada alteração e cada comando foram aprovados um a um. Testes manuais: RabbitMQ healthy, logins no RabbitMQ e no Keycloak, persistência da fila, Core e Bilhetes a responder. O aviso sobre o Keycloak foi aceite sem alterações: o realm vai ser exportado para o repositório (tarefa do Tomás).
