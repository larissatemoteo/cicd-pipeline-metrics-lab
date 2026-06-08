"""Funcoes estatisticas descritivas sobre Series e DataFrames."""

from __future__ import annotations

import pandas as pd
from scipy import stats as sps


def describe(series: pd.Series) -> dict[str, float]:
    """Resumo estatistico de uma Series (ignora NaN)."""
    s = series.dropna()
    if len(s) == 0:
        raise ValueError("series vazia")
    return {
        "mean": float(s.mean()),
        "std": float(s.std(ddof=1)) if len(s) > 1 else 0.0,
        "min": float(s.min()),
        "max": float(s.max()),
        "median": float(s.median()),
    }


def zscore(series: pd.Series) -> pd.Series:
    """Padroniza uma Series (media 0, desvio 1)."""
    return pd.Series(sps.zscore(series, nan_policy="omit"), index=series.index)


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Matriz de correlacao das colunas numericas."""
    return df.select_dtypes(include="number").corr()

import os  # falha de lint proposital
