# Métricas do processo

Registo das tarefas feitas na entrega final, para a análise crítica do relatório (critério "Measurement & Critical Analysis", 30% da nota). Cada tarefa é registada **no dia em que fecha**: estes dados não se reconstroem no fim.

## `tarefas.csv`

Uma linha por tarefa (uma tarefa = uma issue = um pull request).

| Coluna | O que escrever | Exemplo |
| --- | --- | --- |
| `tarefa` | Número da issue | `14` |
| `requisitos` | IDs cobertos, separados por `;` | `RF-22;RF-23` |
| `responsavel` | Quem supervisionou a tarefa | `Tomás` |
| `agente` | Ferramenta usada, ou `nenhum` | `Claude Code` |
| `inicio` / `fim` | Data e hora, `AAAA-MM-DD HH:MM` | `2026-11-20 14:00` |
| `iteracoes` | Número de prompts ou pedidos de correção ao agente | `6` |
| `autonomia` | `alta` (o agente fez tudo), `media` (correções pontuais), `baixa` (reescrito à mão) | `media` |
| `defeitos_pipeline` | Defeitos apanhados pela pipeline (lint, testes) | `1` |
| `defeitos_revisao` | Defeitos apanhados na revisão do pull request | `1` |
| `retrabalho` | O que foi refeito e porquê, numa frase | `Consulta SQL sem índice; reescrita` |
| `notas` | Qualquer erro típico da IA, decisão humana ou observação | `Agente inventou um campo inexistente` |

Se um texto tiver vírgulas, escrevê-lo entre aspas: `"lento, refeito"`.

## Métricas da pipeline

Não se registam à mão: o GitHub guarda o histórico das execuções. No fim, extraem-se com:

```bash
gh run list --limit 500 --json name,conclusion,createdAt,updatedAt,headBranch,event > metricas/execucoes.json
```
