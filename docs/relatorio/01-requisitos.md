# 1. Análise do problema e requisitos

> Responsável: Diogo. Rascunho feito a partir da especificação da M1 (`docs/requisitos/especificacao-requisitos-m1.pdf`). Rever e completar a secção 1.7 no fim do projeto.

O MetroIsJustABus foi especificado com 48 requisitos funcionais, 20 não-funcionais e 22 pressupostos para as ambiguidades do enunciado. Cada requisito está ligado ao excerto do enunciado (E-01 a E-18) ou ao pressuposto (A-xx) que o justifica, e todos os 18 excertos relevantes do enunciado estão cobertos por pelo menos um requisito.

## 1.1 O problema

O sistema apoia uma rede urbana de autocarros: consulta da rede e dos horários, gestão de perturbações, venda e validação de bilhetes, lotação das viagens, subscrições e notificações, e o backoffice do staff.

Ficaram fora do âmbito, por decisão documentada nos pressupostos: pagamentos reais (A-10), localização GPS dos autocarros (A-09) e validadores físicos (A-11).

## 1.2 Como analisámos o enunciado

1. **Divisão do enunciado em excertos.** O enunciado foi dividido em 18 excertos identificados (E-01 a E-18), para cada requisito poder apontar para a sua origem sem transcrever o texto.
2. **Extração dos requisitos.** Os requisitos foram extraídos dos excertos, agrupados por área, com um ID e uma prioridade MoSCoW (Must, Should, Could).
3. **Identificação das ambiguidades.** Cada ponto vago, incompleto ou com várias leituras ficou registado com um pressuposto proposto e o seu impacto.
4. **Rastreabilidade nos dois sentidos.** De cada requisito para a sua origem, e de cada excerto para os requisitos que o cobrem.
5. **Revisão pela equipa.** Os pressupostos, as prioridades e a decomposição em componentes foram revistos e decididos em grupo.

A análise teve apoio de um LLM (Claude). O processo, os erros da IA detetados pela equipa e as correções estão descritos na secção 8 da especificação da M1 e em `prompts/prompts.md`.

## 1.3 Atores

| Ator | O que faz no sistema | Origem |
| --- | --- | --- |
| Visitante | Consulta a rede, as linhas, as paragens, os horários e as perturbações, sem conta | E-03, A-22 |
| Passageiro | Tudo o que o visitante faz; compra e consulta bilhetes, gere subscrições e preferências, recebe notificações | E-05, E-09 |
| Staff operacional | Mantém a rede e os horários, gere os tipos de bilhete e as perturbações, consulta as validações e a lotação | E-07, E-08, E-10 |
| Administrador | Cria e gere as contas de staff | A-18 |
| Validador (simulado) | Sistema externo que submete validações de bilhetes a bordo | E-06, A-11 |
| Serviço de envio (simulado) | Entrega os emails de notificação, por exemplo um servidor SMTP de teste | A-12 |

## 1.4 Requisitos funcionais

48 requisitos em 8 áreas: 40 obrigatórios (M), 7 desejáveis (S) e 1 opcional (C). A lista completa, com a origem de cada um, está na secção 3 da especificação da M1.

| Área | Requisitos | Total | Exemplos |
| --- | --- | --- | --- |
| Consulta da rede e dos horários | RF-01 a RF-08 | 8 | lista de linhas; paragens de uma linha pela ordem; próximas passagens numa paragem |
| Perturbações | RF-10 a RF-14 | 5 | o staff regista e encerra perturbações; cada alteração gera um evento |
| Gestão da rede e dos horários (staff) | RF-15 a RF-19 | 5 | criar e alterar paragens, linhas e horários; uma alteração não apaga o histórico |
| Bilhetes | RF-20 a RF-26 | 7 | tipos de bilhete com preço e condições; compra idempotente; código único |
| Validação | RF-30 a RF-36 | 7 | aceitar ou recusar uma validação; só as aceites contam; simulador de validador |
| Lotação | RF-40 a RF-44 | 5 | cada validação aceite aumenta a ocupação; validações duplicadas não contam |
| Contas e subscrições | RF-50 a RF-55 | 6 | conta de passageiro; login do staff com outro papel; subscrever linhas e paragens |
| Notificações | RF-60 a RF-64 | 5 | notificar os subscritores de um evento relevante, no máximo uma vez por evento |

Os requisitos "Should" são RF-07, RF-14, RF-19, RF-36, RF-43, RF-63 e RF-64. O único "Could" é o RF-55 (apagar a conta).

## 1.5 Requisitos não-funcionais

20 requisitos, cada um com um critério de verificação que possa ser testado na pipeline.

| Categoria | Requisitos | O que garantem |
| --- | --- | --- |
| Disponibilidade | RNF-01, RNF-02 | a falha de um componente não derruba funcionalidades que não dependem dele |
| Fiabilidade | RNF-03 a RNF-05 | operações idempotentes; eventos que não se perdem; timeouts e tentativas nas chamadas entre serviços |
| Consistência | RNF-06 | a ocupação reflete uma validação aceite em 5 s ou menos |
| Desempenho | RNF-07, RNF-08 | p95 abaixo de 500 ms nas consultas de horários (50 utilizadores) e de 300 ms por validação |
| Segurança e privacidade | RNF-09 a RNF-11 | autorização por papel em cada endpoint; segredos fora do repositório; dados pessoais mínimos (RGPD) |
| Observabilidade | RNF-12 | health check, métricas e logs com ID de correlação em cada serviço |
| Histórico | RNF-13 | validações, perturbações e notificações conservadas depois de um redeploy |
| Interoperabilidade | RNF-14 | contratos OpenAPI e AsyncAPI ou JSON Schema entre componentes |
| Deploy | RNF-15, RNF-16 | cada componente implantado sozinho; rollback automático de um deploy falhado |
| Rastreabilidade | RNF-17 | cada versão em execução ligada ao commit que a gerou |
| Manutenibilidade | RNF-18 | lint sem erros e cobertura de testes de pelo menos 70% por serviço |
| Usabilidade | RNF-19 | a aplicação web funciona num ecrã de 360 px |
| Portabilidade | RNF-20 | os ambientes de dev e produção recriam-se só a partir do repositório |

Os valores numéricos (500 ms, 300 ms, 50 utilizadores, 360 px) não vêm do enunciado: foram propostos pela equipa (A-21).

## 1.6 Ambiguidades e pressupostos

Foram identificadas 22 ambiguidades ou lacunas, cada uma com um pressuposto proposto: 4 de impacto alto, 10 de impacto médio e 8 de impacto baixo. A lista completa está na secção 5 da especificação da M1. As de impacto alto foram as que mais condicionaram o design:

| ID | Ambiguidade | Pressuposto adotado |
| --- | --- | --- |
| A-01 | As "condições de uso" e a "validade" dos bilhetes não são definidas | Sem zonas; quatro tipos iniciais (simples, 10 viagens, passe de 24 h, passe mensal); sem transbordo gratuito |
| A-02 | O enunciado usa "journey" (deslocação do passageiro) e "trip" (viagem planeada) com sentidos diferentes | "Viagem planeada" = trip; uma utilização = uma validação aceite numa viagem planeada |
| A-04 | Só há validação à entrada, por isso não se sabe quando o passageiro sai | A ocupação é estimada pelas entradas e reposta a zero no fim da viagem; limitação documentada |
| A-13 | "Quando algo relevante muda" não é definido | Notificam-se perturbações (criadas, alteradas, encerradas), viagens canceladas e alterações de horário; a lotação não gera notificações |

## 1.7 Conflitos e alterações aos requisitos durante o projeto

**Conflitos identificados.** O enunciado pede que só as validações aceites sejam registadas, mas o staff quer consultar a "atividade de validação". O pressuposto A-20 resolve-o: as recusas ficam num registo separado, só para métricas e auditoria, e não contam como validações.

**Alterações depois da M1.**

| Data | Requisito ou pressuposto | Alteração | Porquê |
| --- | --- | --- | --- |
| 2026-11-26 | A-01 | O serviço Bilhetes tem 3 dos 4 tipos de bilhete previstos (falta o passe mensal) | A acrescentar nas tarefas RF-21 a RF-26 |

<!-- Registar aqui qualquer requisito que mude, seja adiado ou fique por implementar, com a razão. -->
