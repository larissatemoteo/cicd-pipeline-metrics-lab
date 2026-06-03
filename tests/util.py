"""Auxiliares para as variacoes controladas do experimento, lidas de variaveis de ambiente.

- TEST_SCALE: multiplica a quantidade de casos parametrizados (default 1).
- ENABLE_SLOW_TEST: habilita um teste lento (sleep).
- INTRODUCE_FAILURE: forca uma falha de teste controlada.
"""

from __future__ import annotations

import os


def flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def scale() -> int:
    try:
        return max(1, int(os.environ.get("TEST_SCALE", "1")))
    except ValueError:
        return 1
