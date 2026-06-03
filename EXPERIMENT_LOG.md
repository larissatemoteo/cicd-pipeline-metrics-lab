# Diario do experimento

Preencha uma linha por execucao no momento em que ela acontece. A hipotese deve
ser escrita ANTES de olhar o resultado, para sustentar a comparacao hipotese x
observado exigida no relatorio. Os campos de ID, SHA e URL saem do GitHub Actions.

| # | Data/hora | Workflow | Inputs (scale/slow/fail/cache) | Commit SHA | Run ID | URL | Hipotese | Resultado observado |
|---|-----------|----------|-------------------------------|------------|--------|-----|----------|---------------------|
| 1 |           | Parallel | 1 / no / no / on              |            |        |     |          |                     |
| 2 |           | Parallel | 1 / no / no / on              |            |        |     |          |                     |
| 3 |           | Parallel | 1 / no / no / on              |            |        |     |          |                     |
| 4 |           | Parallel | 1 / no / no / OFF             |            |        |     |          |                     |
| 5 |           | Parallel | 1 / no / no / OFF             |            |        |     |          |                     |
| 6 |           | Parallel | 1 / no / YES / on             |            |        |     |          |                     |
| 7 |           | Parallel | lint quebrado (commit)        |            |        |     |          |                     |
| 8 |           | Parallel | 2 / no / no / on              |            |        |     |          |                     |
| 9 |           | Parallel | 4 / no / no / on              |            |        |     |          |                     |
| 10|           | Parallel | 1 / YES / no / on             |            |        |     |          |                     |
| 11|           | Sequential | 1 / no / no / on            |            |        |     |          |                     |
| 12|           | Sequential | 1 / no / no / on            |            |        |     |          |                     |
| 13|           | Parallel | 1 / no / no / on              |            |        |     |          |                     |
| 14|           | Parallel | 1 / no / no / on              |            |        |     |          |                     |
