# Relatorio tecnico: experimento de CI/CD

> Esqueleto do relatorio. Cada secao traz uma orientacao do que preencher.
> Regra de integridade: nenhum numero, ID de run ou SHA pode ser digitado a mao.
> Todos os valores citados devem vir de `data/metrics.csv` e dos graficos gerados,
> e toda evidencia visual deve apontar para execucoes reais do GitHub Actions.

## 1. Visao geral do experimento

<!-- Descreva o projeto-alvo, o pipeline (5 etapas), os dois workflows e o objetivo. -->

## 2. Evidencias de execucao real (obrigatorio)

<!-- Cole prints e/ou links das execucoes. Liste os Run IDs reais e os commits usados.
     Pode colar a tabela preenchida do EXPERIMENT_LOG.md aqui. -->

- Repositorio: <!-- link -->
- Workflow YAML: <!-- link para ci-parallel.yml -->
- Run IDs reais: <!-- lista -->
- Commits reais: <!-- lista de SHAs -->

## 3. Variacoes realizadas entre execucoes

<!-- Explique cada variacao (cache on/off, paralelo/sequencial, scale, slow, fail)
     e por que ela foi feita. Referencie os numeros do diario. -->

## 4. Metodo de coleta

<!-- Explique que o coletor consulta a API do GitHub Actions, calcula duracoes de
     workflow/jobs/steps e le o resumo de testes do artefato. Cite os arquivos
     gerados: data/metrics.csv e data/steps.csv. -->

## 5. Graficos

<!-- Embuta os 4 graficos de reports/charts/. -->

![Tempo total por execucao](reports/charts/01_tempo_total_por_execucao.png)
![Tempo por job](reports/charts/02_tempo_por_job.png)
![Taxa de sucesso e falha](reports/charts/03_taxa_sucesso_falha.png)
![Testes vs duracao](reports/charts/04_testes_vs_duracao.png)

## 6. Analise (responder com base nos dados)

1. Qual etapa mais contribuiu para o tempo total do pipeline?
2. Houve diferenca significativa entre execucoes com e sem cache?
3. O paralelismo reduziu o tempo total? Em que condicoes?
4. Quais falhas foram mais frequentes?
5. O pipeline fornece feedback rapido o suficiente para o desenvolvedor?
6. Que melhorias poderiam ser feitas no pipeline?
7. Quais limitacoes existem nos dados coletados?
8. Como essa analise poderia apoiar decisoes de engenharia?

<!-- Dica p/ Q2 e Q3: compare medias entre os grupos de runs. Para paralelismo,
     compare a duracao de parede do workflow contra a soma das duracoes dos jobs. -->

## 7. Resultados inesperados (pelo menos dois)

<!-- Descreva dois resultados que divergiram da expectativa. Nao invente: use o que
     os dados realmente mostraram (ex.: cache com efeito menor que o esperado,
     variancia alta entre runs identicas, paralelismo limitado pela subida do runner). -->

## 8. Hipotese inicial x resultado observado

<!-- Para cada variacao, compare a hipotese registrada no diario com o medido. -->

## 9. Limitacoes do experimento

<!-- Ruido de medicao do runner, diferenca entre tempo de parede e tempo faturado,
     amostra pequena, metricas de teste repetidas por linha de job, etc. -->
