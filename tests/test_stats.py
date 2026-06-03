"""Testes de datalab.stats. Parametrizados e escalaveis via TEST_SCALE."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from util import scale

from datalab import stats

_rng = np.random.default_rng(42)
_CASES = [_rng.normal(loc=0.0, scale=1.0, size=300) for _ in range(5 * scale())]
_IDS = [f"sample-{i}" for i in range(len(_CASES))]


@pytest.mark.parametrize("idx", range(len(_CASES)), ids=_IDS)
def test_zscore_is_standardized(idx: int) -> None:
    s = pd.Series(_CASES[idx])
    z = stats.zscore(s)
    assert abs(float(z.mean())) < 1e-6
    assert abs(float(z.std(ddof=0)) - 1.0) < 1e-2


@pytest.mark.parametrize("idx", range(len(_CASES)), ids=_IDS)
def test_describe_bounds(idx: int) -> None:
    s = pd.Series(_CASES[idx])
    d = stats.describe(s)
    assert d["min"] <= d["median"] <= d["max"]
    assert d["std"] >= 0.0


def test_describe_empty_raises() -> None:
    with pytest.raises(ValueError):
        stats.describe(pd.Series([], dtype="float64"))


def test_correlation_is_symmetric() -> None:
    df = pd.DataFrame({"a": _CASES[0], "b": _CASES[0] * 2 + 1})
    corr = stats.correlation_matrix(df)
    assert abs(corr.loc["a", "b"] - corr.loc["b", "a"]) < 1e-9
