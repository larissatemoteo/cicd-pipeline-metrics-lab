"""Testes de datalab.features."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from datalab import features

_rng = np.random.default_rng(13)


def _frame() -> pd.DataFrame:
    return pd.DataFrame({"a": _rng.normal(size=100), "b": _rng.normal(size=100)})


def test_scale_features_zero_mean() -> None:
    out = features.scale_features(_frame(), ["a", "b"])
    assert abs(float(out["a"].mean())) < 1e-9
    assert abs(float(out["a"].std(ddof=0)) - 1.0) < 1e-6


def test_scale_features_missing_column() -> None:
    with pytest.raises(KeyError):
        features.scale_features(_frame(), ["a", "inexistente"])


def test_add_interaction() -> None:
    df = pd.DataFrame({"a": [2.0, 3.0], "b": [4.0, 5.0]})
    out = features.add_interaction(df, "a", "b")
    assert list(out["a_x_b"]) == [8.0, 15.0]
