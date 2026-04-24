"""
Leitor e análise dos dados de correlação HW × Internações/Óbitos.
Fontes: bd_analise_cardio_total.csv e bd_analise_respirat_total.csv
"""
import logging
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import json

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

_BASE = Path(__file__).parent / "ANALISE_CORRELAÇÃO"

_AGRAVO_FILE = {
    "CARDIOVASCULAR": "bd_analise_cardio_total.csv",
    "RESPIRATORIAS":  "bd_analise_respirat_total.csv",
}

_NUM_COLS = [
    "tempMax", "tempMed", "tempMin", "UmidadeMed",
    "EHF", "thermalRange", "tempAnom",
]

# Cache bruto por agravo
_raw_cache: Dict[str, pd.DataFrame] = {}

# Resultados pré-computados DLNM (R: glm.nb + crossbasis, lag=7)
_DLNM_FILE = _BASE / "dlnm_results.json"
_dlnm_cache: Optional[Dict] = None


def _load_dlnm() -> Dict:
    global _dlnm_cache
    if _dlnm_cache is not None:
        return _dlnm_cache
    if not _DLNM_FILE.exists():
        logger.warning("dlnm_results.json não encontrado em %s", _BASE)
        _dlnm_cache = {}
        return _dlnm_cache
    with open(_DLNM_FILE, encoding="utf-8") as f:
        _dlnm_cache = json.load(f)
    return _dlnm_cache


def _fix_text(s: object) -> str:
    if not isinstance(s, str):
        return str(s) if s is not None else ""
    try:
        return s.encode("latin-1").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return s


def _load_raw(agravo: str) -> pd.DataFrame:
    if agravo in _raw_cache:
        return _raw_cache[agravo]

    fname = _AGRAVO_FILE.get(agravo.upper())
    if not fname:
        logger.error("Agravo desconhecido: %s", agravo)
        return pd.DataFrame()

    path = _BASE / fname
    if not path.exists():
        logger.warning("CSV não encontrado: %s", path)
        return pd.DataFrame()

    try:
        df = pd.read_csv(path, sep=";", index_col=0,
                         encoding="latin-1", low_memory=False)

        # Fix mojibake em colunas de texto
        for col in ["NOME_REGMETROP", "cidade", "HWDay_Intensity", "HW_Intensity"]:
            if col in df.columns:
                df[col] = df[col].apply(_fix_text)

        # Converte numéricos com vírgula decimal
        for col in _NUM_COLS:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace(",", ".", regex=False),
                    errors="coerce",
                )

        df["isHW"] = df["isHW"].astype(str).str.strip().str.upper().isin(["TRUE"])
        df["DT_INTER"] = pd.to_datetime(df["DT_INTER"], errors="coerce")
        df["year"] = pd.to_numeric(df["year"], errors="coerce")
        df["MES_OC"] = pd.to_numeric(df["MES_OC"], errors="coerce")
        df["N_TOTAL"] = pd.to_numeric(df["N_TOTAL"], errors="coerce")

        _raw_cache[agravo] = df
        logger.info("CSV carregado: %s (%d linhas)", fname, len(df))
    except Exception as exc:
        logger.error("Erro ao carregar %s: %s", fname, exc)
        _raw_cache[agravo] = pd.DataFrame()

    return _raw_cache[agravo]


# ── API pública ─────────────────────────────────────────────────────────────

@lru_cache(maxsize=8)
def rms_disponiveis(agravo: str) -> List[str]:
    df = _load_raw(agravo)
    if df.empty or "NOME_REGMETROP" not in df.columns:
        return []
    return sorted(df["NOME_REGMETROP"].dropna().unique().tolist())


@lru_cache(maxsize=32)
def anos_disponiveis(agravo: str, rm: str) -> List[int]:
    df = _load_raw(agravo)
    if df.empty:
        return []
    sub = df.loc[df["NOME_REGMETROP"] == rm, "year"].dropna()
    return sorted(sub.astype(int).unique().tolist())


def _subset(agravo: str, rm: str, ano_ini: int, ano_fim: int) -> pd.DataFrame:
    df = _load_raw(agravo)
    if df.empty:
        return pd.DataFrame()
    mask = (
        (df["NOME_REGMETROP"] == rm)
        & (df["year"] >= ano_ini)
        & (df["year"] <= ano_fim)
    )
    return df.loc[mask].sort_values("DT_INTER").reset_index(drop=True)


# ── KPIs ────────────────────────────────────────────────────────────────────

def kpis(agravo: str, rm: str, ano_ini: int, ano_fim: int) -> Dict:
    sub = _subset(agravo, rm, ano_ini, ano_fim)
    empty = dict(total_dias=0, dias_hw=0, total_intern=0, rr=None, pct_hw=0.0)
    if sub.empty:
        return empty

    n = sub["N_TOTAL"].values.astype(float)
    hw = sub["isHW"].values.astype(bool)

    dias_hw    = int(hw.sum())
    total_dias = len(sub)
    total_int  = int(n.sum())
    pct_hw     = round(dias_hw / total_dias * 100, 1) if total_dias else 0.0

    hw_mean  = float(n[hw].mean()) if hw.any() else np.nan
    nhw_mean = float(n[~hw].mean()) if (~hw).any() else np.nan
    rr = round(hw_mean / nhw_mean, 3) if (nhw_mean and nhw_mean > 0) else None

    return dict(
        total_dias=total_dias,
        dias_hw=dias_hw,
        total_intern=total_int,
        rr=rr,
        pct_hw=pct_hw,
    )


# ── Correlação por defasagem ─────────────────────────────────────────────────

def lag_correlation(agravo: str, rm: str, ano_ini: int, ano_fim: int,
                    max_lag: int = 14) -> pd.DataFrame:
    """
    Pearson r entre isHW(t-lag) e N_TOTAL(t), para lag 0..max_lag.
    Retorna DataFrame com colunas: lag, r, label.
    """
    sub = _subset(agravo, rm, ano_ini, ano_fim)
    if sub.empty:
        return pd.DataFrame(columns=["lag", "r"])

    n  = sub["N_TOTAL"].astype(float)
    hw = sub["isHW"].astype(float)

    rows = []
    for lag in range(max_lag + 1):
        if lag == 0:
            r = hw.corr(n)
        else:
            r = hw.iloc[:-lag].reset_index(drop=True).corr(
                n.iloc[lag:].reset_index(drop=True)
            )
        rows.append({"lag": lag, "r": round(float(r), 4) if not np.isnan(r) else 0.0})

    return pd.DataFrame(rows)


# ── RR por defasagem ─────────────────────────────────────────────────────────

def rr_por_lag(agravo: str, rm: str, ano_ini: int, ano_fim: int,
               max_lag: int = 14) -> pd.DataFrame:
    """
    Risco Relativo por defasagem com IC 95% (método delta, escala log).

    RR(lag) = μ_hw(lag) / μ_ref
    SE[log RR] = sqrt( s²_hw/(n_hw·μ_hw²) + s²_ref/(n_ref·μ_ref²) )
    IC = exp( log(RR) ± 1.96·SE )

    Retorna: lag, rr, ic_low, ic_high, n_hw, n_ref.
    """
    sub = _subset(agravo, rm, ano_ini, ano_fim)
    if sub.empty:
        return pd.DataFrame(columns=["lag", "rr", "ic_low", "ic_high", "n_hw", "n_ref"])

    n   = sub["N_TOTAL"].values.astype(float)
    hw  = sub["isHW"].values.astype(bool)
    ref = n[~hw]

    if len(ref) == 0:
        return pd.DataFrame(columns=["lag", "rr", "ic_low", "ic_high", "n_hw", "n_ref"])

    ref_mean = float(ref.mean())
    ref_var  = float(ref.var(ddof=1)) if len(ref) > 1 else 0.0
    n_ref    = len(ref)

    rows = []
    for lag in range(max_lag + 1):
        if lag == 0:
            idx = np.where(hw)[0]
        else:
            hw_shifted = np.zeros(len(hw), dtype=bool)
            for i in np.where(hw)[0]:
                if i + lag < len(hw):
                    hw_shifted[i + lag] = True
            idx = np.where(hw_shifted)[0]

        if len(idx) > 0 and ref_mean > 0:
            vals    = n[idx]
            hw_mean = float(vals.mean())
            hw_var  = float(vals.var(ddof=1)) if len(vals) > 1 else 0.0
            n_hw    = len(vals)

            rr = hw_mean / ref_mean

            # SE de log(RR) pelo método delta
            term_hw  = hw_var  / (n_hw  * hw_mean ** 2) if hw_mean  != 0 else 0.0
            term_ref = ref_var / (n_ref * ref_mean ** 2) if ref_mean != 0 else 0.0
            se_log   = float(np.sqrt(term_hw + term_ref))

            log_rr   = float(np.log(rr)) if rr > 0 else np.nan
            ic_low   = float(np.exp(log_rr - 1.96 * se_log)) if not np.isnan(log_rr) else np.nan
            ic_high  = float(np.exp(log_rr + 1.96 * se_log)) if not np.isnan(log_rr) else np.nan
        else:
            rr = hw_mean = ic_low = ic_high = np.nan
            n_hw = 0

        rows.append({
            "lag":    lag,
            "rr":     round(rr,      4) if not np.isnan(rr)      else None,
            "ic_low": round(ic_low,  4) if not np.isnan(ic_low)  else None,
            "ic_high":round(ic_high, 4) if not np.isnan(ic_high) else None,
            "n_hw":   round(float(hw_mean), 2) if not np.isnan(hw_mean) else None,
            "n_ref":  round(ref_mean, 2),
        })

    return pd.DataFrame(rows)


# ── Série temporal ───────────────────────────────────────────────────────────

def serie_temporal(agravo: str, rm: str, ano_ini: int, ano_fim: int) -> pd.DataFrame:
    """Retorna série diária com N_TOTAL, isHW, tempMax, tempMed para o período."""
    sub = _subset(agravo, rm, ano_ini, ano_fim)
    cols = ["DT_INTER", "N_TOTAL", "isHW", "tempMax", "tempMed", "tempMin",
            "UmidadeMed", "HW_Intensity", "year", "MES_OC"]
    cols_ok = [c for c in cols if c in sub.columns]
    return sub[cols_ok]


# ── Mensal HW vs não-HW ──────────────────────────────────────────────────────

def mensal_hw_vs_nhw(agravo: str, rm: str, ano_ini: int, ano_fim: int) -> pd.DataFrame:
    """Média mensal de N_TOTAL separada em HW e não-HW."""
    sub = _subset(agravo, rm, ano_ini, ano_fim)
    if sub.empty or "MES_OC" not in sub.columns:
        return pd.DataFrame()

    MESES = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
              7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}

    grp = (
        sub.groupby(["MES_OC", "isHW"])["N_TOTAL"]
        .mean()
        .reset_index()
        .rename(columns={"N_TOTAL": "media", "isHW": "hw", "MES_OC": "mes"})
    )
    grp["mes_nome"] = grp["mes"].map(MESES)
    return grp.sort_values("mes")


# ── Scatter temperatura × internações ───────────────────────────────────────

def scatter_temp_intern(agravo: str, rm: str, ano_ini: int, ano_fim: int,
                        var: str = "tempMax") -> pd.DataFrame:
    """Retorna par (var, N_TOTAL, isHW) para scatter plot."""
    sub = _subset(agravo, rm, ano_ini, ano_fim)
    if sub.empty or var not in sub.columns:
        return pd.DataFrame()
    cols = [var, "N_TOTAL", "isHW", "DT_INTER"]
    return sub[[c for c in cols if c in sub.columns]].dropna(subset=[var, "N_TOTAL"])


# ── Boxplot HW vs não-HW ─────────────────────────────────────────────────────

def boxplot_data(agravo: str, rm: str, ano_ini: int, ano_fim: int) -> Tuple[pd.Series, pd.Series]:
    """Retorna (serie_hw, serie_nao_hw) de N_TOTAL para boxplot."""
    sub = _subset(agravo, rm, ano_ini, ano_fim)
    if sub.empty:
        return pd.Series(dtype=float), pd.Series(dtype=float)
    hw  = sub.loc[sub["isHW"],  "N_TOTAL"].astype(float)
    nhw = sub.loc[~sub["isHW"], "N_TOTAL"].astype(float)
    return hw, nhw


# ── RR DLNM pré-computado (R: glm.nb + crossbasis) ──────────────────────────

def rr_por_lag_dlnm(agravo: str, rm: str) -> pd.DataFrame:
    """
    Retorna tabela de RR × lag pré-computada pelo R (DLNM + glm.nb, lag=7).
    Período fixo: 2010-2019, sem COVID (exceto Recife 2010-2022).
    Colunas: lag, rr, ic_low, ic_high.
    Retorna DataFrame vazio se agravo/RM não disponível.
    """
    data = _load_dlnm()
    tabela = data.get(agravo.upper(), {}).get(rm)
    if not tabela:
        return pd.DataFrame(columns=["lag", "rr", "ic_low", "ic_high"])
    return pd.DataFrame(tabela)


def dlnm_disponivel(agravo: str, rm: str) -> bool:
    """True se há resultado DLNM pré-computado para este agravo/RM."""
    data = _load_dlnm()
    return bool(data.get(agravo.upper(), {}).get(rm))
