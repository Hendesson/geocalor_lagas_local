"""
Leitor dos parquets pré-agregados SIH/SIM.
Execute prepare_sih_sim_data.py UMA VEZ antes de usar o dashboard.
"""
import json
import logging
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from db import execute as db_execute

logger = logging.getLogger(__name__)

PROCESSED = Path(__file__).parent / "processed" / "sih_sim"

_ANO_COL = {"SIH": "ANO_INTERNACAO", "SIM": "ANO_OBITO"}
_MES_COL = {"SIH": "MES_INTERNACAO", "SIM": "MES_OBITO"}
_MUN_COL = {"SIH": "MUNIC_MOV",      "SIM": "CODMUNRES"}

FAIXA_ORDER = [
    "<1", "1-5", "6-10", "11-19", "20-29", "30-39",
    "40-49", "50-59", "60-69", "70-79", ">80", "Ignorado",
]
MESES_PTBR = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
}

# Tabelas de decodificação para colunas SIM
_RACA_MAP = {
    "1": "Branca",  "01": "Branca",
    "2": "Preta",   "02": "Preta",
    "3": "Parda",   "03": "Parda",
    "4": "Amarela", "04": "Amarela",
    "5": "Indígena","05": "Indígena",
    "9": "Ignorado","99": "Ignorado",
}
_ESTCIV_MAP = {
    "1": "Solteiro",
    "2": "Casado",
    "3": "Viúvo",
    "4": "Separado judicialmente",
    "5": "União consensual",
    "9": "Ignorado",
}
_LOCOCOR_MAP = {
    "1": "Hospital",
    "2": "Outro estabelecimento de saúde",
    "3": "Domicílio",
    "4": "Via pública",
    "5": "Outros",
    "6": "Aldeia indígena",
    "9": "Ignorado",
    # Formas abreviadas / variantes encontradas nos dados
    "Outro estab. de saúde": "Outro estabelecimento de saúde",
    "Domic\xedlio": "Domicílio",          # Latin-1 'í' = U+00ED
    "Via p\xfablica": "Via pública",       # Latin-1 'ú' = U+00FA
}

_cache: Dict[str, pd.DataFrame] = {}


# ── normalização e decodificação ────────────────────────────────────────────

def _norm(s: object) -> str:
    """Remove acentos e coloca em maiúsculas para comparação robusta."""
    if not isinstance(s, str):
        s = "" if s is None else str(s)
    s = s.strip()
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c) and ord(c) < 128).upper()


def _fix_mojibake(s: object) -> str:
    """Corrige mojibake: UTF-8 bytes lidos como latin-1 (ex: 'RegiÃ£o' → 'Região')."""
    if not isinstance(s, str):
        return str(s) if s is not None else ""
    try:
        return s.encode("latin-1").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return s


def _fix_column(series: pd.Series) -> pd.Series:
    """Aplica _fix_mojibake a toda uma coluna de strings."""
    return series.astype(str).apply(_fix_mojibake)


def _decode_cat(series: pd.Series, mapping: dict) -> pd.Series:
    """
    Normaliza coluna categórica:
    1. Corrige mojibake em strings existentes
    2. Mapeia códigos numéricos para rótulos
    3. Agrupa duplicatas geradas pelo mesmo rótulo
    """
    fixed = _fix_column(series)
    return fixed.apply(lambda v: mapping.get(v, v))


def _prefix(sistema: str, causa: str) -> str:
    return f"{sistema.lower()}_{causa.lower()}"


# ── leitura e cache ─────────────────────────────────────────────────────────

def _load(filename: str) -> pd.DataFrame:
    """Carrega um parquet SIH/SIM via DuckDB (MotherDuck ou arquivo local)."""
    if filename not in _cache:
        table_name = Path(filename).stem  # ex.: sih_cardiovascular_car_int
        try:
            df = db_execute(f'SELECT * FROM "{table_name}"').df()
            if "NOME_RM" in df.columns:
                df["NOME_RM"] = _fix_column(df["NOME_RM"])
            _cache[filename] = df
            logger.debug("_load DuckDB OK: %s (%d linhas)", table_name, len(df))
        except Exception as e:
            logger.warning("_load DuckDB falhou para '%s': %s — tentando parquet local.", table_name, e)
            path = PROCESSED / filename
            if path.exists():
                df = pd.read_parquet(path)
                if "NOME_RM" in df.columns:
                    df["NOME_RM"] = _fix_column(df["NOME_RM"])
                _cache[filename] = df
            else:
                logger.warning("Parquet não encontrado: %s", path.name)
                _cache[filename] = pd.DataFrame()
    return _cache[filename]


def _filter_rm(df: pd.DataFrame, rm: str) -> pd.DataFrame:
    if df.empty or "NOME_RM" not in df.columns:
        return pd.DataFrame()
    return df[df["NOME_RM"] == rm].copy()


def _add_pct(df: pd.DataFrame, n_col: str = "N") -> pd.DataFrame:
    total = df[n_col].sum()
    df = df.copy()
    df["pct"] = df[n_col] * 100.0 / total if total > 0 else 0.0
    return df


def _pop_total_rm(rm: str, ano: int) -> Optional[float]:
    """Retorna população total da RM no ano (ou no mais próximo disponível)."""
    pop = _load("populacao_RM.parquet")
    if pop.empty:
        return None
    # garante NOME_RM_NORM existe; usa _norm do rm decodificado
    norm_rm = _norm(rm)
    if "NOME_RM_NORM" not in pop.columns:
        pop["NOME_RM_NORM"] = pop["NOME_RM"].apply(_norm) if "NOME_RM" in pop.columns else pd.Series()
    pop_rm = pop[pop["NOME_RM_NORM"] == norm_rm]
    if pop_rm.empty:
        logger.warning("_pop_total_rm: RM '%s' (norm=%s) não encontrada na tabela de população", rm, norm_rm)
        return None
    p_cols = [c for c in pop_rm.columns if c.startswith("pop_") and c.replace("pop_", "").isdigit()]
    if not p_cols:
        return None
    pcol = f"pop_{ano}"
    if pcol not in p_cols:
        anos_pop = [int(c.replace("pop_", "")) for c in p_cols]
        pcol = f"pop_{min(anos_pop, key=lambda a: abs(a - ano))}"
    val = pop_rm[pcol].sum()
    return float(val) if val > 0 else None


# ── API pública ─────────────────────────────────────────────────────────────

def rms_disponiveis(sistema: str, causa: str) -> List[str]:
    df = _load(f"{_prefix(sistema, causa)}_taxa_anual.parquet")
    if df.empty or "NOME_RM" not in df.columns:
        return []
    return sorted(df["NOME_RM"].dropna().unique().tolist())


def anos_disponiveis(sistema: str, causa: str, rm: str) -> List[int]:
    df = _load(f"{_prefix(sistema, causa)}_taxa_anual.parquet")
    if df.empty:
        return []
    ano_col = _ANO_COL[sistema]
    dff = _filter_rm(df, rm)
    if dff.empty or ano_col not in dff.columns:
        return []
    return sorted(dff[ano_col].dropna().unique().astype(int).tolist())


def serie_mensal(sistema: str, causa: str, rm: str) -> pd.DataFrame:
    """Retorna serie temporal mensal: colunas NOME_RM, ANO_*, MES_*, N."""
    df = _load(f"{_prefix(sistema, causa)}_serie_mensal.parquet")
    return _filter_rm(df, rm)


def taxa_anual(sistema: str, causa: str, rm: str) -> pd.DataFrame:
    """Taxa anual por 1.000 hab.: (ANO_*, N, taxa). taxa=NaN se pop indisponível."""
    df = _load(f"{_prefix(sistema, causa)}_taxa_anual.parquet")
    ano_col = _ANO_COL[sistema]
    dff = _filter_rm(df, rm)
    if dff.empty or ano_col not in dff.columns:
        return pd.DataFrame(columns=[ano_col, "N", "taxa"])
    rows = []
    for _, row in dff.iterrows():
        ano = int(row[ano_col])
        pop = _pop_total_rm(rm, ano)
        taxa_val = row["N"] / pop * 1000.0 if pop else None
        rows.append({ano_col: ano, "N": int(row["N"]), "taxa": taxa_val})
    return pd.DataFrame(rows).sort_values(ano_col)


def sexo_por_ano(sistema: str, causa: str, rm: str) -> pd.DataFrame:
    """Contagem por sexo e ano: (ANO_*, SEXO, N)."""
    df = _load(f"{_prefix(sistema, causa)}_sexo_ano.parquet")
    ano_col = _ANO_COL[sistema]
    dff = _filter_rm(df, rm)
    if dff.empty or "SEXO" not in dff.columns:
        return pd.DataFrame(columns=[ano_col, "SEXO", "N"])
    return dff[[ano_col, "SEXO", "N"]].sort_values([ano_col, "SEXO"])


def raca_cor(sistema: str, causa: str, rm: str) -> pd.DataFrame:
    """Distribuição por raça/cor: (RACA_COR, N, pct)."""
    df = _load(f"{_prefix(sistema, causa)}_raca.parquet")
    dff = _filter_rm(df, rm)
    if dff.empty:
        return pd.DataFrame(columns=["RACA_COR", "N", "pct"])
    dff["RACA_COR"] = _decode_cat(dff["RACA_COR"], _RACA_MAP)
    tab = dff.groupby("RACA_COR", dropna=False)["N"].sum().reset_index()
    return _add_pct(tab).sort_values("pct", ascending=False)


def faixa_etaria(sistema: str, causa: str, rm: str) -> pd.DataFrame:
    """Distribuição por faixa etária: (FAIXA_ETARIA, N, pct)."""
    df = _load(f"{_prefix(sistema, causa)}_faixa_etaria.parquet")
    dff = _filter_rm(df, rm)
    if dff.empty:
        return pd.DataFrame(columns=["FAIXA_ETARIA", "N", "pct"])
    tab = dff.groupby("FAIXA_ETARIA", dropna=False)["N"].sum().reset_index()
    tab["_ord"] = tab["FAIXA_ETARIA"].apply(
        lambda x: FAIXA_ORDER.index(x) if x in FAIXA_ORDER else 99
    )
    return _add_pct(tab.sort_values("_ord").drop(columns="_ord")).sort_values(
        "pct", ascending=False
    )


# ── SIH-específico ──────────────────────────────────────────────────────────

def car_int(causa: str, rm: str) -> pd.DataFrame:
    """Caráter de internação: (CAR_INT, N, pct)."""
    df = _load(f"sih_{causa.lower()}_car_int.parquet")
    dff = _filter_rm(df, rm)
    if dff.empty:
        return pd.DataFrame(columns=["CAR_INT", "N", "pct"])
    tab = dff.groupby("CAR_INT", dropna=False)["N"].sum().reset_index()
    return _add_pct(tab).sort_values("pct", ascending=False)


def espec(causa: str, rm: str) -> pd.DataFrame:
    """Especialidade do leito — top 12: (ESPEC, N, pct)."""
    df = _load(f"sih_{causa.lower()}_espec.parquet")
    dff = _filter_rm(df, rm)
    if dff.empty:
        return pd.DataFrame(columns=["ESPEC", "N", "pct"])
    tab = dff.groupby("ESPEC", dropna=False)["N"].sum().reset_index()
    return _add_pct(tab).sort_values("pct", ascending=False).head(12)


# ── SIM-específico ──────────────────────────────────────────────────────────

def lococor(causa: str, rm: str) -> pd.DataFrame:
    """Local do óbito: (LOCOCOR, N, pct)."""
    df = _load(f"sim_{causa.lower()}_lococor.parquet")
    dff = _filter_rm(df, rm)
    if dff.empty:
        return pd.DataFrame(columns=["LOCOCOR", "N", "pct"])
    dff["LOCOCOR"] = _decode_cat(dff["LOCOCOR"], _LOCOCOR_MAP)
    tab = dff.groupby("LOCOCOR", dropna=False)["N"].sum().reset_index()
    return _add_pct(tab).sort_values("pct", ascending=False)


def estciv(causa: str, rm: str) -> pd.DataFrame:
    """Estado civil: (ESTCIV, N, pct)."""
    df = _load(f"sim_{causa.lower()}_estciv.parquet")
    dff = _filter_rm(df, rm)
    if dff.empty:
        return pd.DataFrame(columns=["ESTCIV", "N", "pct"])
    dff["ESTCIV"] = _decode_cat(dff["ESTCIV"], _ESTCIV_MAP)
    tab = dff.groupby("ESTCIV", dropna=False)["N"].sum().reset_index()
    return _add_pct(tab).sort_values("pct", ascending=False)


# ── Mapa ─────────────────────────────────────────────────────────────────────

def mapa_data(sistema: str, causa: str, rm: str, ano: int):
    """
    Retorna dict {"geojson": GeoJSON apenas da RM, "taxa_df": DataFrame(COD_MUN6, NM_MUN, N, taxa)}
    ou None se dados indisponíveis.
    """
    mun_col = _MUN_COL[sistema]
    ano_col = _ANO_COL[sistema]
    geo_path = PROCESSED / "geojson_rm.json"

    df_mapa = _load(f"{_prefix(sistema, causa)}_mapa_mun.parquet")
    pop = _load("populacao_RM.parquet")

    if df_mapa.empty:
        logger.warning("mapa_data: parquet de mapa vazio para %s/%s", sistema, causa)
        return None

    # Verifica disponibilidade do GeoJSON local
    if not geo_path.exists():
        logger.warning("GeoJSON não encontrado: %s", geo_path)
        return None

    # Filtra parquet pela RM e ano selecionados
    dff = _filter_rm(df_mapa, rm)
    if dff.empty or ano_col not in dff.columns:
        return None
    dff = dff[dff[ano_col] == ano].copy()
    if dff.empty:
        return None

    dff = dff.rename(columns={mun_col: "COD_MUN6"})
    dff["COD_MUN6"] = dff["COD_MUN6"].astype(str).str.strip()

    # Merge com população municipal
    if not pop.empty and "COD_MUN6" in pop.columns:
        p_cols = [c for c in pop.columns if c.startswith("pop_") and c.replace("pop_", "").isdigit()]
        pcol = f"pop_{ano}"
        if pcol not in p_cols:
            anos_pop = [int(c.replace("pop_", "")) for c in p_cols]
            pcol = f"pop_{min(anos_pop, key=lambda a: abs(a - ano))}" if anos_pop else None
        if pcol:
            pop_mun = pop[["COD_MUN6", pcol]].copy()
            pop_mun["COD_MUN6"] = pop_mun["COD_MUN6"].astype(str).str.strip()
            dff = dff.merge(pop_mun, on="COD_MUN6", how="left")
            dff["taxa"] = np.where(
                dff[pcol].notna() & (dff[pcol] > 0),
                dff["N"] / dff[pcol] * 1000.0,
                np.nan,
            )
        else:
            dff["taxa"] = dff["N"].astype(float)
    else:
        dff["taxa"] = dff["N"].astype(float)

    # Carrega GeoJSON do arquivo local
    try:
        with open(geo_path, encoding="utf-8") as f:
            geojson_all = json.load(f)
    except Exception as e:
        logger.error("Erro ao ler GeoJSON: %s", e)
        return None

    norm_rm = _norm(rm)
    features_rm = [
        feat for feat in geojson_all.get("features", [])
        if _norm(feat.get("properties", {}).get("NOME_CA_NORM", "")) == norm_rm
        or _norm(feat.get("properties", {}).get("NOME_CA", "")) == norm_rm
    ]

    if not features_rm:
        logger.warning("mapa_data: nenhuma feature GeoJSON para RM '%s' (norm=%s)", rm, norm_rm)
        return None

    geojson_rm = {"type": "FeatureCollection", "features": features_rm}

    # Adiciona COD_MUN6 como id em cada feature para plotly
    for feat in geojson_rm["features"]:
        cod = str(feat["properties"].get("COD_MUN6", "")).strip()
        feat["id"] = cod

    return {"geojson": geojson_rm, "taxa_df": dff}
