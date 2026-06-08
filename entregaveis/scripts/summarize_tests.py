"""Resume um relatorio JUnit XML do pytest em um JSON de metricas de teste.

Uso:
    python scripts/summarize_tests.py reports/junit.xml reports/pipeline-metrics.json

Gera um JSON com: test_count, test_failures, test_errors, test_skipped,
total_test_time e avg_test_time. Esse arquivo entra no artefato do pipeline
e e lido depois pelo coletor de metricas.
"""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET


def summarize(junit_path: str) -> dict[str, float | int]:
    root = ET.parse(junit_path).getroot()
    suites = root.findall("testsuite") if root.tag == "testsuites" else [root]

    tests = failures = errors = skipped = 0
    total_time = 0.0
    for s in suites:
        tests += int(s.get("tests", 0))
        failures += int(s.get("failures", 0))
        errors += int(s.get("errors", 0))
        skipped += int(s.get("skipped", 0))
        total_time += float(s.get("time", 0.0))

    executed = max(tests - skipped, 0)
    avg = total_time / executed if executed else 0.0
    return {
        "test_count": tests,
        "test_failures": failures,
        "test_errors": errors,
        "test_skipped": skipped,
        "total_test_time": round(total_time, 4),
        "avg_test_time": round(avg, 6),
    }


def main() -> int:
    if len(sys.argv) != 3:
        print("uso: summarize_tests.py <junit.xml> <saida.json>", file=sys.stderr)
        return 2
    junit_path, out_path = sys.argv[1], sys.argv[2]
    metrics = summarize(junit_path)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(metrics, fh, indent=2)
    print(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
