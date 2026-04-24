"""
Leitor dos dados de Mortalidade por Ondas de Calor.
Fontes: processed/ (parquet)
"""
import logging
from functools import lru_cache
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

_PROCESSED = Path(__file__).parent / "processed"

_OER_FILE    = _PROCESSED / "ondas_de_calor_OER.parquet"
_FATORES_FILE = _PROCESSED / "ResultadosFatoresDeRisco_dashboard.parquet"
_RESUMO_FILE  = _PROCESSED / "tabela_resumo_ondas_de_calor_mortalidade.parquet"

_oer_cache: pd.DataFrame | None = None
_fatores_cache: pd.DataFrame | None = None
_resumo_cache: pd.DataFrame | None = None


def _load_oer() -> pd.DataFrame:
    global _oer_cache
    if _oer_cache is not None:
        return _oer_cache
    if not _OER_FILE.exists():
        logger.warning("OER não encontrado: %s", _OER_FILE)
        _oer_cache = pd.DataFrame()
        return _oer_cache
    try:
        df = pd.read_parquet(_OER_FILE)
        df["inicio_onda"] = pd.to_datetime(df["inicio_onda"], errors="coerce")
        df["fim_onda"]    = pd.to_datetime(df["fim_onda"],    errors="coerce")
        df["OER_isSIG"]   = df["OER_isSIG"].astype(bool)
        for col in ["OER", "IC_95_inf", "IC_95_sup", "excesso_percentual",
                    "OBITOS_OBS", "OBITOS_ESP", "OBITOS_EXCESSO",
                    "MTR", "Mean_HW_Humidity", "mean_temp_anom",
                    "days_since_HW", "EHF_mean"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        _oer_cache = df
        logger.info("OER carregado: %d ondas", len(df))
    except Exception as e:
        logger.error("Erro ao carregar OER: %s", e)
        _oer_cache = pd.DataFrame()
    return _oer_cache


def _load_fatores() -> pd.DataFrame:
    global _fatores_cache
    if _fatores_cache is not None:
        return _fatores_cache
    if not _FATORES_FILE.exists():
        logger.warning("Fatores não encontrado: %s", _FATORES_FILE)
        _fatores_cache = pd.DataFrame()
        return _fatores_cache
    try:
        df = pd.read_parquet(_FATORES_FILE)
        df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
        rm_col = df.columns[0]
        df[rm_col] = df[rm_col].astype(str).str.replace("RIDE/DF", "Brasília", regex=False)
        _fatores_cache = df
        logger.info("Fatores carregado: %d RMs", len(df))
    except Exception as e:
        logger.error("Erro ao carregar Fatores: %s", e)
        _fatores_cache = pd.DataFrame()
    return _fatores_cache


def _load_resumo() -> pd.DataFrame:
    global _resumo_cache
    if _resumo_cache is not None:
        return _resumo_cache
    if not _RESUMO_FILE.exists():
        logger.warning("Resumo não encontrado: %s", _RESUMO_FILE)
        _resumo_cache = pd.DataFrame()
        return _resumo_cache
    try:
        df = pd.read_parquet(_RESUMO_FILE)
        # Limpar RM: remover asterisco e strip — preserva NaN real (linha TOTAL)
        col0 = df.iloc[:, 0]
        df.iloc[:, 0] = col0.where(
            col0.isna(),
            col0.astype(str).str.replace("*", "", regex=False).str.strip(),
        )
        _resumo_cache = df
        logger.info("Resumo carregado: %d linhas", len(df))
    except Exception as e:
        logger.error("Erro ao carregar Resumo: %s", e)
        _resumo_cache = pd.DataFrame()
    return _resumo_cache


# ── API pública ──────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def cidades_disponiveis() -> List[str]:
    df = _load_oer()
    if df.empty or "Cidade" not in df.columns:
        return []
    return sorted(df["Cidade"].dropna().unique().tolist())


def oer_por_cidade(cidade: str) -> pd.DataFrame:
    df = _load_oer()
    if df.empty:
        return pd.DataFrame()
    return df[df["Cidade"] == cidade].copy().sort_values("inicio_onda").reset_index(drop=True)


def fatores_risco_cidade(cidade: str) -> pd.DataFrame:
    df = _load_fatores()
    if df.empty or len(df.columns) == 0:
        return pd.DataFrame()
    rm_col = df.columns[0]
    return df[df[rm_col] == cidade].copy()


def kpis_cidade(cidade: str) -> dict:
    """Retorna KPIs da cidade a partir da tabela resumo."""
    df = _load_resumo()
    empty = dict(n_ondas="-", n_excesso="-", pct_excesso="-", obitos="-", obitos_pm="-")
    if df.empty:
        return empty
    row = df[df.iloc[:, 0] == cidade]
    if row.empty:
        # fallback: tenta match parcial
        row = df[df.iloc[:, 0].str.contains(cidade.split()[0], case=False, na=False)]
    if row.empty:
        return empty
    r = row.iloc[0]
    cols = list(df.columns)
    try:
        return dict(
            n_ondas   = int(r[cols[1]]) if pd.notna(r[cols[1]]) else "-",
            n_excesso = int(r[cols[2]]) if pd.notna(r[cols[2]]) else "-",
            pct_excesso = f"{float(r[cols[4]]):.1f}%" if pd.notna(r[cols[4]]) else "-",
            obitos    = f"{float(r[cols[6]]):.1f}" if pd.notna(r[cols[6]]) else "-",
            obitos_pm = f"{float(r[cols[7]]):.1f}" if pd.notna(r[cols[7]]) else "-",
        )
    except Exception:
        return empty


def tabela_resumo() -> pd.DataFrame:
    return _load_resumo()
