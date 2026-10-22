# MetroIsJustABus

Sistema distribuído de apoio a uma rede urbana de autocarros: consulta de rede e horários, perturbações, bilhetes e validação, lotação das viagens, subscrições e notificações.

Projeto da unidade curricular **Engenharia de Software Automatizada** (2026/2027), Departamento de Engenharia Informática.

## Elementos do grupo

| Nome | Número |
| --- | --- |
| Diogo Santos | 2023220279 |
| Bernardo Esperança | 2023233673 |
| Tomás Neto | 2023229944 |

## Estado do projeto

| Marco | Data | Estado | Onde está |
| --- | --- | --- | --- |
| Milestone 1 — Requisitos | 27/10/2026 | Em revisão | `docs/requisitos/`, `prompts/` |
| Milestone 2 — Pipeline CI/CDE/CD | 17/11/2026 | Por iniciar | `.github/workflows/`, `services/` |
| Entrega final | 11/12/2026 | Por iniciar | — |

## Estrutura do repositório

```
├── README.md                         este ficheiro
├── .gitignore                        ficheiros excluídos do repositório (segredos, builds, dependências)
├── .github/workflows/                pipeline CI/CDE/CD (Milestone 2)
├── docs/
│   ├── enunciado/                    enunciado original do projeto
│   └── requisitos/                   especificação de requisitos (Milestone 1)
├── prompts/                          evidência do uso de IA: prompts, respostas e decisões
└── services/                         código dos serviços (a partir da Milestone 2)
```

## Milestone 1 — o que está entregue

| O enunciado pede | Onde encontrar |
| --- | --- |
| Requisitos funcionais e não-funcionais | Especificação, secções 3 e 4 |
| Ambiguidades, informação em falta e pressupostos | Especificação, secção 5 |
| Rastreabilidade ao enunciado | Especificação, secção 6, e coluna "Origem" de cada requisito |
| Decomposição inicial em componentes | Especificação, secção 7 |
| Evidência do uso de LLMs na análise, refinamento e validação | Especificação, secção 8, e pasta `prompts/` |

## Regras do grupo

- **Todos os prompts usados no projeto ficam em `prompts/`**, seguindo o formato descrito em `prompts/README.md`.
- **Nenhum segredo** (passwords, chaves, tokens) é colocado no repositório (RNF-10).
- Fazer sempre `git pull` antes de começar a trabalhar.
- Cada alteração relevante é feita num commit próprio, com uma mensagem clara.
