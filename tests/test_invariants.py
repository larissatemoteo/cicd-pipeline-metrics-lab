"""Testes que servem de gatilho para as variacoes de falha e de teste lento."""

from __future__ import annotations

import os
import time

import pandas as pd
import pytest
from util import flag

from datalab import stats


def test_describe_mean_known_value() -> None:
    """Quando INTRODUCE_FAILURE esta ativo, o valor esperado muda e o teste falha de proposito."""
    s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    expected = 99.0 if flag("INTRODUCE_FAILURE") else 3.0
    assert stats.describe(s)["mean"] == expected


@pytest.mark.skipif(not flag("ENABLE_SLOW_TEST"), reason="teste lento desabilitado")
def test_slow_pipeline_step() -> None:
    seconds = float(os.environ.get("SLOW_TEST_SECONDS", "12"))
    time.sleep(seconds)
    assert True
