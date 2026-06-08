#!/usr/bin/env bash
# Dispara as execucoes controladas do experimento via GitHub CLI (gh).
# Pre-requisitos: gh instalado e autenticado. Rode de dentro do repo.
set -euo pipefail

PARALLEL="ci-parallel.yml"
SEQ="ci-sequential.yml"
GAP="${GAP:-75}"  # segundos entre disparos

run () {
  local wf="$1"; shift
  echo ">> Disparando $wf $*"
  gh workflow run "$wf" "$@"
  sleep "$GAP"
}

echo "== Baselines (cache on) =="
run "$PARALLEL" -f test_scale=1 -f slow_test=false -f fail_test=false -f disable_cache=false
run "$PARALLEL" -f test_scale=1 -f slow_test=false -f fail_test=false -f disable_cache=false
run "$PARALLEL" -f test_scale=1 -f slow_test=false -f fail_test=false -f disable_cache=false

echo "== Sem cache =="
run "$PARALLEL" -f test_scale=1 -f slow_test=false -f fail_test=false -f disable_cache=true
run "$PARALLEL" -f test_scale=1 -f slow_test=false -f fail_test=false -f disable_cache=true

echo "== Falha de teste =="
run "$PARALLEL" -f test_scale=1 -f slow_test=false -f fail_test=true -f disable_cache=false

echo "== Aumento de testes =="
run "$PARALLEL" -f test_scale=2 -f slow_test=false -f fail_test=false -f disable_cache=false
run "$PARALLEL" -f test_scale=4 -f slow_test=false -f fail_test=false -f disable_cache=false

echo "== Teste lento =="
run "$PARALLEL" -f test_scale=1 -f slow_test=true -f fail_test=false -f disable_cache=false

echo "== Sequencial =="
run "$SEQ" -f test_scale=1 -f slow_test=false -f fail_test=false -f disable_cache=false
run "$SEQ" -f test_scale=1 -f slow_test=false -f fail_test=false -f disable_cache=false

echo "== Confirmacao paralelo =="
run "$PARALLEL" -f test_scale=1 -f slow_test=false -f fail_test=false -f disable_cache=false
run "$PARALLEL" -f test_scale=1 -f slow_test=false -f fail_test=false -f disable_cache=false

echo "Pronto. Acompanhe com: gh run list --limit 20"
