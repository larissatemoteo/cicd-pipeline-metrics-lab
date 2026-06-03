"""Engenharia de atributos. Usa scikit-learn para justificar a dependencia pesada."""

from __future__ import annotations

import pandas as pd
from sklearn.preprocessing import StandardScaler


def scale_features(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Aplica padronizacao (StandardScaler) nas colunas indicadas."""
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise KeyError(f"colunas inexistentes: {missing}")
    out = df.copy()
    scaler = StandardScaler()
    out[columns] = scaler.fit_transform(out[columns])
    return out


def add_interaction(df: pd.DataFrame, a: str, b: str, name: str | None = None) -> pd.DataFrame:
    """Cria uma coluna de interacao (produto) entre duas colunas."""
    out = df.copy()
    col = name or f"{a}_x_{b}"
    out[col] = out[a] * out[b]
    return out
