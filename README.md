# cicd-pipeline-metrics-lab

Experimento pratico de instrumentacao e analise de um pipeline CI/CD no GitHub
Actions. O repositorio contem um pequeno projeto Python com testes automatizados,
dois workflows (paralelo e sequencial), um coletor de metricas que consulta a API
do GitHub e um gerador de graficos. O objetivo e medir, com execucoes reais, o
comportamento da esteira sob variacoes controladas (cache, paralelismo, quantidade
de testes, teste lento e falhas).

## Estrutura

```
.github/workflows/   ci-parallel.yml e ci-sequential.yml
src/datalab/         modulo de processamento de dados (pandas, numpy, scipy, sklearn)
tests/               testes pytest parametrizados e escalaveis
scripts/             collect_metrics.py, plot_metrics.py, summarize_tests.py
data/                base de dados gerada (metrics.csv, steps.csv)
reports/charts/      graficos gerados
RELATORIO.md         relatorio tecnico (a preencher com evidencias reais)
EXPERIMENT_LOG.md    diario de execucoes
```

## Pipeline (etapas obrigatorias)

Cada workflow cumpre as cinco etapas exigidas: instalacao de dependencias, analise
estatica (ruff), type check (mypy), testes (pytest com JUnit), geracao de artefato
(`test-results` com `junit.xml` + `pipeline-metrics.json`, e `dist/` no job de build)
e disponibiliza os dados para a coleta de metricas.

## Como rodar localmente

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
mypy
pytest --junitxml=reports/junit.xml
python scripts/summarize_tests.py reports/junit.xml reports/pipeline-metrics.json
```

## Como executar o experimento (variacoes controladas)

Os dois workflows aceitam disparo manual (aba Actions > Run workflow) com inputs:

- `test_scale`: 1, 2, 4 ou 8 (multiplica a quantidade de testes)
- `slow_test`: habilita um teste lento
- `fail_test`: introduz uma falha de teste controlada
- `disable_cache`: desativa o cache de dependencias

Matriz sugerida (no minimo 12 execucoes; aqui 14 para medir variancia):

| #     | Workflow   | Variacao                              | Mede                          |
|-------|------------|---------------------------------------|-------------------------------|
| 1-3   | Parallel   | baseline (scale 1, cache on)          | variancia entre runs iguais   |
| 4-5   | Parallel   | disable_cache = true                  | efeito do cache               |
| 6     | Parallel   | fail_test = true                      | falha de teste                |
| 7     | Parallel   | commit com erro de lint               | falha de analise estatica     |
| 8     | Parallel   | test_scale = 2                        | nº de testes x duracao        |
| 9     | Parallel   | test_scale = 4                        | nº de testes x duracao        |
| 10    | Parallel   | slow_test = true                      | impacto de teste lento        |
| 11-12 | Sequential | baseline (scale 1, cache on)          | sequencial vs paralelo        |
| 13-14 | Parallel   | baseline (confirmacao)                | confirma efeito do paralelismo|

Para o run de falha de lint (#7), introduza uma violacao simples (ex.: variavel nao
usada), faca commit, dispare o workflow e depois reverta. Isso gera um commit real
com falha real, registrado no diario.

## Como coletar as metricas

1. Gere um Personal Access Token do GitHub com leitura de Actions.
2. Exporte as variaveis e rode o coletor:

```bash
export GITHUB_TOKEN=seu_token
python scripts/collect_metrics.py --repo SEU_USUARIO/cicd-pipeline-metrics-lab --limit 50
```

Isso gera `data/metrics.csv` (uma linha por job) e `data/steps.csv` (uma linha por step).

## Como gerar os graficos

```bash
python scripts/plot_metrics.py
```

Gera os quatro graficos em `reports/charts/`.

## Reproducao completa

Clonar o repo, criar o ambiente, disparar os workflows conforme a matriz acima,
rodar o coletor com um token valido e por fim o gerador de graficos. Todos os
numeros do relatorio saem de `data/metrics.csv`; nada e digitado manualmente.
