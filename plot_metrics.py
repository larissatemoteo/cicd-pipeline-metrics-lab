"""Gera os quatro graficos obrigatorios a partir das bases coletadas.

Le data/metrics.csv (e data/steps.csv quando disponivel) e salva PNGs em
reports/charts/. Todos os graficos saem dos dados reais coletados; nada e
digitado a mao.

Uso:
    python scripts/plot_metrics.py
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

DATA_DIR = "data"
OUT_DIR = os.path.join("reports", "charts")


def _runs_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Reduz para uma linha por execucao (workflow), preservando duracao e contagem."""
    cols = ["run_id", "workflow_duration", "status", "test_count", "timestamp", "commit_sha"]
    runs = df[cols].drop_duplicates(subset="run_id").copy()
    runs["workflow_duration"] = pd.to_numeric(runs["workflow_duration"], errors="coerce")
    runs["test_count"] = pd.to_numeric(runs["test_count"], errors="coerce")
    runs["timestamp"] = pd.to_datetime(runs["timestamp"], errors="coerce")
    return runs.sort_values("timestamp").reset_index(drop=True)


def chart_total_time(df: pd.DataFrame) -> None:
    runs = _runs_frame(df)
    labels = [f"#{i+1}\n{sha}" for i, sha in enumerate(runs["commit_sha"])]
    colors = ["#2e7d32" if s == "success" else "#c62828" for s in runs["status"]]
    plt.figure(figsize=(11, 5))
    plt.bar(labels, runs["workflow_duration"], color=colors)
    plt.ylabel("Duracao total (s)")
    plt.title("Tempo total do pipeline por execucao")
    plt.xticks(rotation=0, fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "01_tempo_total_por_execucao.png"), dpi=130)
    plt.close()


def chart_time_by_job(df: pd.DataFrame) -> None:
    d = df.copy()
    d["job_duration"] = pd.to_numeric(d["job_duration"], errors="coerce")
    by_job = d.groupby("job_name")["job_duration"].mean().sort_values(ascending=False)
    plt.figure(figsize=(9, 5))
    plt.barh(by_job.index, by_job.values, color="#1565c0")
    plt.xlabel("Duracao media (s)")
    plt.title("Tempo medio por job")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "02_tempo_por_job.png"), dpi=130)
    plt.close()


def chart_success_failure(df: pd.DataFrame) -> None:
    runs = _runs_frame(df)
    counts = runs["status"].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(counts.values, labels=list(counts.index), autopct="%1.0f%%", startangle=90)
    plt.title("Taxa de sucesso e falha das execucoes")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "03_taxa_sucesso_falha.png"), dpi=130)
    plt.close()


def chart_tests_vs_duration(df: pd.DataFrame) -> None:
    runs = _runs_frame(df).dropna(subset=["test_count", "workflow_duration"])
    plt.figure(figsize=(8, 6))
    plt.scatter(runs["test_count"], runs["workflow_duration"], s=70, color="#6a1b9a")
    plt.xlabel("Quantidade de testes")
    plt.ylabel("Duracao total do pipeline (s)")
    plt.title("Relacao entre quantidade de testes e duracao do pipeline")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "04_testes_vs_duracao.png"), dpi=130)
    plt.close()


def main() -> int:
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, "metrics.csv")
    if not os.path.exists(path):
        print(f"ERRO: {path} nao encontrado. Rode collect_metrics.py primeiro.")
        return 1
    df = pd.read_csv(path)
    if df.empty:
        print("ERRO: base vazia.")
        return 1

    chart_total_time(df)
    chart_time_by_job(df)
    chart_success_failure(df)
    chart_tests_vs_duration(df)
    print(f"OK: 4 graficos salvos em {OUT_DIR}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
