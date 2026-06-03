"""Funcoes de limpeza de dados. Usam pandas, numpy e scipy de proposito,
para que a instalacao de dependencias tenha custo real e o efeito do cache
seja mensuravel na esteira."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Padroniza nomes de colunas: minusculas, sem espacos nas pontas, espacos -> underscore."""
    out = df.copy()
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]
    return out


def drop_high_missing(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """Remove colunas cuja fracao de valores ausentes excede o threshold."""
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold deve estar entre 0 e 1")
    keep = [c for c in df.columns if float(df[c].isna().mean()) <= threshold]
    return df.loc[:, keep]


def fill_missing(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """Preenche valores ausentes das colunas numericas com a estrategia escolhida."""
    out = df.copy()
    numeric = out.select_dtypes(include="number").columns
    for col in numeric:
        if strategy == "mean":
            out[col] = out[col].fillna(out[col].mean())
        elif strategy == "median":
            out[col] = out[col].fillna(out[col].median())
        elif strategy == "zero":
            out[col] = out[col].fillna(0)
        else:
            raise ValueError(f"strategy invalida: {strategy}")
    return out


def remove_outliers_zscore(df: pd.DataFrame, column: str, z: float = 3.0) -> pd.DataFrame:
    """Remove linhas em que o z-score absoluto da coluna excede z."""
    scores = np.abs(stats.zscore(df[column], nan_policy="omit"))
    mask = scores <= z
    return df.loc[mask]
