"""Testes de datalab.cleaning. Parametrizados e escalaveis via TEST_SCALE."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from util import scale

from datalab import cleaning

_rng = np.random.default_rng(7)
_N = 5 * scale()
_IDS = [f"frame-{i}" for i in range(_N)]


def _make_frame(seed: int) -> pd.DataFrame:
    r = np.random.default_rng(seed)
    return pd.DataFrame(
        {
            "x": r.normal(size=200),
            "y": r.normal(size=200),
            "z": r.normal(size=200),
        }
    )


@pytest.mark.parametrize("idx", range(_N), ids=_IDS)
def test_fill_missing_removes_nans(idx: int) -> None:
    df = _make_frame(idx)
    df.loc[df.index[:10], "x"] = np.nan
    filled = cleaning.fill_missing(df, strategy="mean")
    assert filled["x"].isna().sum() == 0


@pytest.mark.parametrize("idx", range(_N), ids=_IDS)
def test_remove_outliers_keeps_most_rows(idx: int) -> None:
    df = _make_frame(idx)
    out = cleaning.remove_outliers_zscore(df, "x", z=3.0)
    assert len(out) <= len(df)
    assert len(out) >= 0.9 * len(df)


def test_normalize_column_names() -> None:
    df = pd.DataFrame({" Nome Completo ": [1], "Idade": [2]})
    out = cleaning.normalize_column_names(df)
    assert list(out.columns) == ["nome_completo", "idade"]


def test_drop_high_missing() -> None:
    df = pd.DataFrame({"keep": [1, 2, 3, 4], "drop": [np.nan, np.nan, np.nan, 1]})
    out = cleaning.drop_high_missing(df, threshold=0.5)
    assert "keep" in out.columns
    assert "drop" not in out.columns


def test_fill_missing_invalid_strategy() -> None:
    with pytest.raises(ValueError):
        cleaning.fill_missing(pd.DataFrame({"a": [1.0, np.nan]}), strategy="banana")
