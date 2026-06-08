"""Coletor de metricas do GitHub Actions.

Consulta a API REST do GitHub para cada execucao de workflow, calcula duracoes
de workflow, jobs e steps, baixa o artefato com o resumo dos testes e grava duas
bases de dados:

    data/metrics.csv  -> uma linha por job (formato pedido no enunciado)
    data/steps.csv    -> uma linha por step (para a analise de gargalo por etapa)

Requer a variavel de ambiente GITHUB_TOKEN (Personal Access Token com leitura de
Actions). O repositorio pode vir de --repo owner/nome ou da variavel
GITHUB_REPOSITORY.

Uso:
    export GITHUB_TOKEN=ghp_xxx
    python scripts/collect_metrics.py --repo larissa/cicd-pipeline-metrics-lab --limit 50
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
import zipfile
from datetime import datetime
from typing import Any

import requests

API = "https://api.github.com"
TIMEOUT = 30


def _headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _duration(start: str | None, end: str | None) -> float | None:
    a, b = _parse_ts(start), _parse_ts(end)
    if a is None or b is None:
        return None
    return round((b - a).total_seconds(), 3)


def list_runs(session: requests.Session, repo: str, limit: int) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    page = 1
    while len(runs) < limit:
        resp = session.get(
            f"{API}/repos/{repo}/actions/runs",
            params={"per_page": 100, "page": page},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        batch = resp.json().get("workflow_runs", [])
        if not batch:
            break
        runs.extend(batch)
        page += 1
    return runs[:limit]


def get_jobs(session: requests.Session, repo: str, run_id: int) -> list[dict[str, Any]]:
    resp = session.get(
        f"{API}/repos/{repo}/actions/runs/{run_id}/jobs",
        params={"per_page": 100},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json().get("jobs", [])


def get_test_metrics(
    session: requests.Session, repo: str, run_id: int
) -> dict[str, Any]:
    """Baixa o artefato e le pipeline-metrics.json, se existir."""
    empty = {"test_count": "", "test_failures": "", "avg_test_time": ""}
    resp = session.get(
        f"{API}/repos/{repo}/actions/runs/{run_id}/artifacts", timeout=TIMEOUT
    )
    resp.raise_for_status()
    artifacts = [a for a in resp.json().get("artifacts", []) if not a.get("expired")]
    artifacts.sort(key=lambda a: 0 if a.get("name") == "test-results" else 1)
    for art in artifacts:
        dl = session.get(art["archive_download_url"], timeout=TIMEOUT)
        if dl.status_code != 200:
            continue
        try:
            with zipfile.ZipFile(io.BytesIO(dl.content)) as zf:
                name = next(
                    (n for n in zf.namelist() if n.endswith("pipeline-metrics.json")),
                    None,
                )
                if name is None:
                    continue
                data = json.loads(zf.read(name))
            return {
                "test_count": data.get("test_count", ""),
                "test_failures": data.get("test_failures", ""),
                "avg_test_time": data.get("avg_test_time", ""),
            }
        except (zipfile.BadZipFile, json.JSONDecodeError, KeyError):
            continue
    return empty


def main() -> int:
    parser = argparse.ArgumentParser(description="Coleta metricas do GitHub Actions")
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"))
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--out-dir", default="data")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("ERRO: defina GITHUB_TOKEN no ambiente.", file=sys.stderr)
        return 2
    if not args.repo:
        print("ERRO: informe --repo owner/nome ou GITHUB_REPOSITORY.", file=sys.stderr)
        return 2

    session = requests.Session()
    session.headers.update(_headers(token))

    os.makedirs(args.out_dir, exist_ok=True)
    metrics_path = os.path.join(args.out_dir, "metrics.csv")
    steps_path = os.path.join(args.out_dir, "steps.csv")

    job_rows: list[dict[str, Any]] = []
    step_rows: list[dict[str, Any]] = []

    runs = list_runs(session, args.repo, args.limit)
    print(f"Encontradas {len(runs)} execucoes. Processando...")

    for run in runs:
        if run.get("status") != "completed":
            continue
        run_id = run["id"]
        wf_duration = _duration(run.get("run_started_at"), run.get("updated_at"))
        commit_msg = (run.get("head_commit") or {}).get("message", "").splitlines()[:1]
        commit_msg = commit_msg[0] if commit_msg else ""
        test_metrics = get_test_metrics(session, args.repo, run_id)

        for job in get_jobs(session, args.repo, run_id):
            job_duration = _duration(job.get("started_at"), job.get("completed_at"))
            job_rows.append(
                {
                    "run_id": run_id,
                    "commit_sha": run.get("head_sha", "")[:10],
                    "commit_message": commit_msg,
                    "status": run.get("conclusion", ""),
                    "workflow_duration": wf_duration if wf_duration is not None else "",
                    "job_name": job.get("name", ""),
                    "job_duration": job_duration if job_duration is not None else "",
                    "test_count": test_metrics["test_count"],
                    "test_failures": test_metrics["test_failures"],
                    "timestamp": run.get("run_started_at", ""),
                    "workflow_name": run.get("name", ""),
                    "event": run.get("event", ""),
                    "job_conclusion": job.get("conclusion", ""),
                    "avg_test_time": test_metrics["avg_test_time"],
                    "run_attempt": run.get("run_attempt", ""),
                    "html_url": run.get("html_url", ""),
                }
            )
            for step in job.get("steps", []):
                step_rows.append(
                    {
                        "run_id": run_id,
                        "job_name": job.get("name", ""),
                        "step_name": step.get("name", ""),
                        "step_number": step.get("number", ""),
                        "step_duration": _duration(
                            step.get("started_at"), step.get("completed_at")
                        ),
                        "conclusion": step.get("conclusion", ""),
                    }
                )

    _write_csv(metrics_path, job_rows)
    _write_csv(steps_path, step_rows)
    print(f"OK: {len(job_rows)} linhas de job em {metrics_path}")
    print(f"OK: {len(step_rows)} linhas de step em {steps_path}")
    return 0


def _write_csv(path: str, rows: list[dict[str, Any]]) -> None:
    if not rows:
        print(f"AVISO: nenhuma linha para gravar em {path}")
        return
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
