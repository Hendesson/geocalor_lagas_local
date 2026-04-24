"""
Leitor dos parquets pré-agregados SIH/SIM.
Execute prepare_sih_sim_data.py UMA VEZ antes de usar o dashboard.
"""
import json
import logging
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from db import execute as db_execute
from config_paths import ASSETS_DIR

logger = logging.getLogger(__name__)

PROCESSED = Path(__file__).parent / "processed" / "sih_sim"
_GEOJSON_PATH = Path(ASSETS_DIR) / "geojson_rmb.json"

_ANO_COL = {"SIH": "ANO_INTERNACAO", "SIM": "ANO_OBITO"}
_MES_COL = {"SIH": "MES_INTERNACAO", "SIM": "MES_OBITO"}
_MUN_COL = {"SIH": "MUNIC_MOV", "SIM": "CODMUNOCOR"}

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

# Cache do GeoJSON (lido uma vez do disco)
_geojson_all_cache: Optional[dict] = None
# Cache por RM: {norm_rm → {geojson, lat_c, lon_c, n_feat}} — computado uma vez por RM
_geojson_rm_cache: Dict[str, Optional[dict]] = {}
# Cache de mapa_data por (sistema, causa, rm, ano)
_mapa_data_cache: Dict[tuple, Optional[dict]] = {}
# Cache de mapa_data_all_years por (sistema, causa, rm)
_mapa_all_years_cache: Dict[tuple, Optional[dict]] = {}
# Cache de DataFrames das funções de agregação (evita re-filtrar/re-agregar por callback)
_df_agg_cache: Dict[tuple, pd.DataFrame] = {}


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
    """Mapeia códigos para rótulos de forma vetorizada (sem apply por elemento)."""
    fixed  = _fix_column(series)
    mapped = fixed.map(mapping)
    return mapped.where(mapped.notna(), fixed)  # preserva valores não mapeados


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
    return df[df["NOME_RM"] == rm]


def _add_pct(df: pd.DataFrame, n_col: str = "N") -> pd.DataFrame:
    total = df[n_col].sum()
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

@lru_cache(maxsize=16)
def rms_disponiveis(sistema: str, causa: str) -> List[str]:
    df = _load(f"{_prefix(sistema, causa)}_taxa_anual.parquet")
    if df.empty or "NOME_RM" not in df.columns:
        return []
    return sorted(df["NOME_RM"].dropna().unique().tolist())


@lru_cache(maxsize=64)
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
    key = ("serie_mensal", sistema, causa, rm)
    if key not in _df_agg_cache:
        df = _load(f"{_prefix(sistema, causa)}_serie_mensal.parquet")
        _df_agg_cache[key] = _filter_rm(df, rm)
    return _df_agg_cache[key]


def serie_mensal_taxa(sistema: str, causa: str, rm: str) -> pd.DataFrame:
    """Taxa mensal por 10.000 hab.: (ANO_*, MES_*, N, taxa). taxa=NaN se pop indisponível."""
    key = ("serie_mensal_taxa", sistema, causa, rm)
    if key in _df_agg_cache:
        return _df_agg_cache[key]

    df_serie = serie_mensal(sistema, causa, rm)
    ano_col  = _ANO_COL[sistema]
    mes_col  = _MES_COL[sistema]
    if df_serie.empty:
        _df_agg_cache[key] = pd.DataFrame(columns=[ano_col, mes_col, "N", "taxa"])
        return _df_agg_cache[key]

    pop = _load("populacao_RM.parquet")
    pop_por_ano: Dict[int, float] = {}
    if not pop.empty and "NOME_RM" in pop.columns:
        norm_rm = _norm(rm)
        if "NOME_RM_NORM" not in pop.columns:
            pop = pop.copy()
            pop["NOME_RM_NORM"] = pop["NOME_RM"].apply(_norm)
        pop_rm = pop[pop["NOME_RM_NORM"] == norm_rm]
        p_cols = {int(c.replace("pop_", "")): c
                  for c in pop_rm.columns
                  if c.startswith("pop_") and c.replace("pop_", "").isdigit()}
        pop_por_ano = {yr: float(pop_rm[col].sum()) for yr, col in p_cols.items()
                       if pop_rm[col].sum() > 0}

    def _get_pop(ano: int) -> Optional[float]:
        if not pop_por_ano:
            return None
        if ano in pop_por_ano:
            return pop_por_ano[ano]
        return pop_por_ano[min(pop_por_ano, key=lambda a: abs(a - ano))]

    out = df_serie[[ano_col, mes_col, "N"]].copy()
    out[ano_col] = pd.to_numeric(out[ano_col], errors="coerce")
    pop_vals = out[ano_col].map(lambda a: _get_pop(int(a)) if pd.notna(a) else None)
    out["taxa"] = np.where(pop_vals.notna() & (pop_vals > 0),
                           out["N"] / pop_vals * 10000.0, np.nan)
    _df_agg_cache[key] = out.sort_values([ano_col, mes_col])
    return _df_agg_cache[key]


def taxa_anual(sistema: str, causa: str, rm: str) -> pd.DataFrame:
    """Taxa anual por 1.000 hab.: (ANO_*, N, taxa). taxa=NaN se pop indisponível."""
    key = ("taxa_anual", sistema, causa, rm)
    if key in _df_agg_cache:
        return _df_agg_cache[key]
    df = _load(f"{_prefix(sistema, causa)}_taxa_anual.parquet")
    ano_col = _ANO_COL[sistema]
    dff = _filter_rm(df, rm)
    if dff.empty or ano_col not in dff.columns:
        return pd.DataFrame(columns=[ano_col, "N", "taxa"])

    # Pré-carrega populações da RM uma única vez (em vez de 1 chamada por linha)
    pop = _load("populacao_RM.parquet")
    pop_por_ano: Dict[int, float] = {}
    if not pop.empty and "NOME_RM" in pop.columns:
        norm_rm = _norm(rm)
        if "NOME_RM_NORM" not in pop.columns:
            pop = pop.copy()
            pop["NOME_RM_NORM"] = pop["NOME_RM"].apply(_norm)
        pop_rm  = pop[pop["NOME_RM_NORM"] == norm_rm]
        p_cols  = {int(c.replace("pop_", "")): c
                   for c in pop_rm.columns
                   if c.startswith("pop_") and c.replace("pop_", "").isdigit()}
        pop_por_ano = {yr: float(pop_rm[col].sum()) for yr, col in p_cols.items()
                       if pop_rm[col].sum() > 0}

    def _get_pop(ano: int) -> Optional[float]:
        if not pop_por_ano:
            return None
        if ano in pop_por_ano:
            return pop_por_ano[ano]
        return pop_por_ano[min(pop_por_ano, key=lambda a: abs(a - ano))]

    out = dff[[ano_col, "N"]].copy()
    out[ano_col] = out[ano_col].astype(int)
    pop_vals = out[ano_col].map(_get_pop)
    out["taxa"] = np.where(pop_vals.notna() & (pop_vals > 0),
                           out["N"] / pop_vals * 1000.0, np.nan)
    result = out.sort_values(ano_col)
    _df_agg_cache[key] = result
    return result


def sexo_por_ano(sistema: str, causa: str, rm: str) -> pd.DataFrame:
    """Contagem por sexo e ano: (ANO_*, SEXO, N)."""
    key = ("sexo_por_ano", sistema, causa, rm)
    if key not in _df_agg_cache:
        df = _load(f"{_prefix(sistema, causa)}_sexo_ano.parquet")
        ano_col = _ANO_COL[sistema]
        dff = _filter_rm(df, rm)
        if dff.empty or "SEXO" not in dff.columns:
            _df_agg_cache[key] = pd.DataFrame(columns=[ano_col, "SEXO", "N"])
        else:
            _df_agg_cache[key] = dff[[ano_col, "SEXO", "N"]].sort_values([ano_col, "SEXO"])
    return _df_agg_cache[key]


def sexo_por_faixa(sistema: str, causa: str, rm: str) -> pd.DataFrame:
    """Contagem por sexo e faixa etária para pirâmide: (SEXO, FAIXA_ETARIA, N)."""
    key = ("sexo_por_faixa", sistema, causa, rm)
    if key not in _df_agg_cache:
        df = _load(f"{_prefix(sistema, causa)}_sexo_faixa.parquet")
        dff = _filter_rm(df, rm)
        if dff.empty or "SEXO" not in dff.columns or "FAIXA_ETARIA" not in dff.columns:
            _df_agg_cache[key] = pd.DataFrame(columns=["SEXO", "FAIXA_ETARIA", "N"])
        else:
            result = (dff.groupby(["SEXO", "FAIXA_ETARIA"])["N"]
                        .sum().reset_index())
            _df_agg_cache[key] = result
    return _df_agg_cache[key]


def raca_cor(sistema: str, causa: str, rm: str) -> pd.DataFrame:
    """Distribuição por raça/cor: (RACA_COR, N, pct)."""
    key = ("raca_cor", sistema, causa, rm)
    if key not in _df_agg_cache:
        df = _load(f"{_prefix(sistema, causa)}_raca.parquet")
        dff = _filter_rm(df, rm).copy()
        if dff.empty:
            _df_agg_cache[key] = pd.DataFrame(columns=["RACA_COR", "N", "pct"])
        else:
            dff["RACA_COR"] = _decode_cat(dff["RACA_COR"], _RACA_MAP)
            tab = dff.groupby("RACA_COR", dropna=False)["N"].sum().reset_index()
            _df_agg_cache[key] = _add_pct(tab).sort_values("pct", ascending=False)
    return _df_agg_cache[key]


def faixa_etaria(sistema: str, causa: str, rm: str) -> pd.DataFrame:
    """Distribuição por faixa etária: (FAIXA_ETARIA, N, pct)."""
    key = ("faixa_etaria", sistema, causa, rm)
    if key not in _df_agg_cache:
        df = _load(f"{_prefix(sistema, causa)}_faixa_etaria.parquet")
        dff = _filter_rm(df, rm)
        if dff.empty:
            _df_agg_cache[key] = pd.DataFrame(columns=["FAIXA_ETARIA", "N", "pct"])
        else:
            tab = dff.groupby("FAIXA_ETARIA", dropna=False)["N"].sum().reset_index()
            tab["_ord"] = tab["FAIXA_ETARIA"].apply(
                lambda x: FAIXA_ORDER.index(x) if x in FAIXA_ORDER else 99
            )
            _df_agg_cache[key] = _add_pct(tab.sort_values("_ord").drop(columns="_ord")).sort_values(
                "pct", ascending=False
            )
    return _df_agg_cache[key]


# ── SIH-específico ──────────────────────────────────────────────────────────

def car_int(causa: str, rm: str) -> pd.DataFrame:
    """Caráter de internação: (CAR_INT, N, pct)."""
    key = ("car_int", causa, rm)
    if key not in _df_agg_cache:
        df = _load(f"sih_{causa.lower()}_car_int.parquet")
        dff = _filter_rm(df, rm)
        if dff.empty:
            _df_agg_cache[key] = pd.DataFrame(columns=["CAR_INT", "N", "pct"])
        else:
            tab = dff.groupby("CAR_INT", dropna=False)["N"].sum().reset_index()
            _df_agg_cache[key] = _add_pct(tab).sort_values("pct", ascending=False)
    return _df_agg_cache[key]


def espec(causa: str, rm: str) -> pd.DataFrame:
    """Especialidade do leito — top 12: (ESPEC, N, pct)."""
    key = ("espec", causa, rm)
    if key not in _df_agg_cache:
        df = _load(f"sih_{causa.lower()}_espec.parquet")
        dff = _filter_rm(df, rm)
        if dff.empty:
            _df_agg_cache[key] = pd.DataFrame(columns=["ESPEC", "N", "pct"])
        else:
            tab = dff.groupby("ESPEC", dropna=False)["N"].sum().reset_index()
            _df_agg_cache[key] = _add_pct(tab).sort_values("pct", ascending=False).head(12)
    return _df_agg_cache[key]


# ── SIM-específico ──────────────────────────────────────────────────────────

def lococor(causa: str, rm: str) -> pd.DataFrame:
    """Local do óbito: (LOCOCOR, N, pct)."""
    key = ("lococor", causa, rm)
    if key not in _df_agg_cache:
        df = _load(f"sim_{causa.lower()}_lococor.parquet")
        dff = _filter_rm(df, rm).copy()
        if dff.empty:
            _df_agg_cache[key] = pd.DataFrame(columns=["LOCOCOR", "N", "pct"])
        else:
            dff["LOCOCOR"] = _decode_cat(dff["LOCOCOR"], _LOCOCOR_MAP)
            tab = dff.groupby("LOCOCOR", dropna=False)["N"].sum().reset_index()
            _df_agg_cache[key] = _add_pct(tab).sort_values("pct", ascending=False)
    return _df_agg_cache[key]


def estciv(causa: str, rm: str) -> pd.DataFrame:
    """Estado civil: (ESTCIV, N, pct)."""
    key = ("estciv", causa, rm)
    if key not in _df_agg_cache:
        df = _load(f"sim_{causa.lower()}_estciv.parquet")
        dff = _filter_rm(df, rm).copy()
        if dff.empty:
            _df_agg_cache[key] = pd.DataFrame(columns=["ESTCIV", "N", "pct"])
        else:
            dff["ESTCIV"] = _decode_cat(dff["ESTCIV"], _ESTCIV_MAP)
            tab = dff.groupby("ESTCIV", dropna=False)["N"].sum().reset_index()
            _df_agg_cache[key] = _add_pct(tab).sort_values("pct", ascending=False)
    return _df_agg_cache[key]


# ── Mapa ─────────────────────────────────────────────────────────────────────

def _load_geojson_all() -> Optional[dict]:
    """Carrega geojson_rmb.json (simplificado, assets) do disco uma única vez por sessão."""
    global _geojson_all_cache
    if _geojson_all_cache is not None:
        return _geojson_all_cache or None
    geo_path = _GEOJSON_PATH
    if not geo_path.exists():
        logger.warning("GeoJSON não encontrado: %s", geo_path)
        _geojson_all_cache = {}
        return None
    try:
        with open(geo_path, encoding="utf-8") as f:
            _geojson_all_cache = json.load(f)
        logger.info("GeoJSON carregado: %d features", len(_geojson_all_cache.get("features", [])))
    except Exception as e:
        logger.error("Erro ao ler GeoJSON: %s", e)
        _geojson_all_cache = {}
    return _geojson_all_cache or None


def _geojson_for_rm(rm: str) -> Optional[dict]:
    """
    Retorna GeoJSON filtrado para a RM com centro e nº de features pré-computados.
    Resultado em cache por RM — computado apenas uma vez por sessão.
    """
    norm_rm = _norm(rm)
    if norm_rm in _geojson_rm_cache:
        return _geojson_rm_cache[norm_rm]

    geojson_all = _load_geojson_all()
    if not geojson_all:
        _geojson_rm_cache[norm_rm] = None
        return None

    def _rm_match(props: dict) -> bool:
        for key in ("NOME_CA_NORM", "NOME_CA", "NOME_RM", "NM_REGIAO"):
            if _norm(props.get(key, "")) == norm_rm:
                return True
        return False

    features_rm = [
        feat for feat in geojson_all.get("features", [])
        if _rm_match(feat.get("properties", {}))
    ]
    if not features_rm:
        disponiveis = list({
            feat.get("properties", {}).get("NOME_CA", feat.get("properties", {}).get("NOME_RM", ""))
            for feat in geojson_all.get("features", [])
        })
        logger.warning("GeoJSON: nenhuma feature para RM '%s' (norm=%s) — disponíveis: %s",
                       rm, norm_rm, sorted(disponiveis)[:20])
        _geojson_rm_cache[norm_rm] = None
        return None

    # Clona features e seta id uma única vez (6 dígitos para parear com DATASUS)
    import copy as _copy
    features_rm = _copy.deepcopy(features_rm)
    for feat in features_rm:
        feat["id"] = str(feat["properties"].get("COD_MUN6", "")).strip()[:6]

    geojson_rm = {"type": "FeatureCollection", "features": features_rm}

    # Calcula centro geográfico (computado uma única vez por RM)
    lats, lons = [], []
    try:
        for feat in features_rm:
            geom   = feat.get("geometry", {})
            coords = geom.get("coordinates", [])
            gtype  = geom.get("type")
            if gtype == "Polygon" and coords:
                ring = coords[0]
                lons += [p[0] for p in ring]
                lats += [p[1] for p in ring]
            elif gtype == "MultiPolygon" and coords:
                for poly in coords:
                    ring = poly[0]
                    lons += [p[0] for p in ring]
                    lats += [p[1] for p in ring]
        lat_c = float(np.mean(lats)) if lats else -15.0
        lon_c = float(np.mean(lons)) if lons else -50.0
    except Exception:
        lat_c, lon_c = -15.0, -50.0

    all_codes = [str(feat["properties"].get("COD_MUN6", "")).strip()[:6] for feat in features_rm]
    result = {
        "geojson":    geojson_rm,
        "lat_c":      lat_c,
        "lon_c":      lon_c,
        "n_feat":     len(features_rm),
        "all_codes":  all_codes,
    }
    _geojson_rm_cache[norm_rm] = result
    return result


def mapa_data(sistema: str, causa: str, rm: str, ano: int) -> Optional[dict]:
    """
    Retorna dict {geojson, taxa_df, lat_c, lon_c, n_feat} ou None.
    Resultado em cache por (sistema, causa, rm, ano).
    """
    cache_key = (sistema, causa, rm, ano)
    if cache_key in _mapa_data_cache:
        return _mapa_data_cache[cache_key]

    mun_col = _MUN_COL[sistema]
    ano_col = _ANO_COL[sistema]

    df_mapa = _load(f"{_prefix(sistema, causa)}_mapa_mun.parquet")
    if df_mapa.empty:
        logger.warning("mapa_data: parquet de mapa vazio para %s/%s", sistema, causa)
        _mapa_data_cache[cache_key] = None
        return None

    # GeoJSON por RM (cached — leitura de disco e filtro de features feitos apenas 1× por RM)
    geo_data = _geojson_for_rm(rm)
    if geo_data is None:
        _mapa_data_cache[cache_key] = None
        return None

    # Filtro único: RM + ano em uma operação só (evita double-copy)
    if "NOME_RM" not in df_mapa.columns or ano_col not in df_mapa.columns:
        _mapa_data_cache[cache_key] = None
        return None
    mask = (df_mapa["NOME_RM"] == rm) & (df_mapa[ano_col] == ano)
    dff  = df_mapa[mask].copy()
    if dff.empty:
        # Fallback: comparação normalizada (sem acentos, maiúsculas)
        norm_rm  = _norm(rm)
        rm_norms = df_mapa["NOME_RM"].apply(_norm)
        mask2    = (rm_norms == norm_rm) & (df_mapa[ano_col] == ano)
        dff      = df_mapa[mask2].copy()
        if not dff.empty:
            logger.info("mapa_data: RM '%s' encontrada via normalização (raw: '%s')",
                        rm, dff["NOME_RM"].iloc[0])
    if dff.empty:
        disponiveis = df_mapa["NOME_RM"].dropna().unique().tolist()
        logger.warning("mapa_data: sem dados para RM='%s' ano=%s — NOME_RM disponíveis: %s",
                       rm, ano, disponiveis[:15])
        _mapa_data_cache[cache_key] = None
        return None

    if mun_col not in dff.columns:
        logger.warning("mapa_data: coluna '%s' ausente no parquet %s/%s. Colunas: %s",
                       mun_col, sistema, causa, dff.columns.tolist())
        _mapa_data_cache[cache_key] = None
        return None

    dff = dff.rename(columns={mun_col: "COD_MUN6"})
    # Normaliza para 6 dígitos (DATASUS às vezes usa 7 com dígito verificador)
    dff["COD_MUN6"] = dff["COD_MUN6"].astype(str).str.strip().str[:6]

    # Verifica overlap com GeoJSON — avisa se parquet foi gerado com coluna errada
    geo_ids = set(geo_data.get("all_codes", []))
    if not (set(dff["COD_MUN6"].tolist()) & geo_ids):
        logger.warning(
            "mapa_data [%s/%s RM='%s' ano=%s]: overlap=0 com GeoJSON — "
            "verifique se prepare_sih_sim_data.py foi re-executado com CODMUNOCOR",
            sistema, causa, rm, ano,
        )
        _mapa_data_cache[cache_key] = {"no_overlap": True}
        return {"no_overlap": True}

    # Merge com população municipal
    pop = _load("populacao_RM.parquet")
    if not pop.empty and "COD_MUN6" in pop.columns:
        p_cols = [c for c in pop.columns if c.startswith("pop_") and c.replace("pop_", "").isdigit()]
        pcol   = f"pop_{ano}"
        if pcol not in p_cols:
            anos_pop = [int(c.replace("pop_", "")) for c in p_cols]
            pcol = f"pop_{min(anos_pop, key=lambda a: abs(a - ano))}" if anos_pop else None
        if pcol:
            pop_mun = pop[["COD_MUN6", pcol]].copy()
            # Normaliza para 6 dígitos — mesma regra do dado principal
            pop_mun["COD_MUN6"] = pop_mun["COD_MUN6"].astype(str).str.strip().str[:6]
            dff = dff.merge(pop_mun, on="COD_MUN6", how="left")
            dff["taxa"] = np.where(
                dff[pcol].notna() & (dff[pcol] > 0),
                dff["N"] / dff[pcol] * 1000.0,
                np.nan,
            )
            if dff["taxa"].isna().all():
                # Merge não encontrou população: usa contagem bruta como fallback
                logger.warning(
                    "mapa_data: merge população falhou para RM='%s' ano=%s — "
                    "usando N absoluto. COD_MUN6 amostra dados=%s pop=%s",
                    rm, ano,
                    dff["COD_MUN6"].head(3).tolist(),
                    pop_mun["COD_MUN6"].head(3).tolist(),
                )
                dff["taxa"] = dff["N"].astype(float)
        else:
            dff["taxa"] = dff["N"].astype(float)
    else:
        dff["taxa"] = dff["N"].astype(float)

    result = {
        "geojson":   geo_data["geojson"],
        "taxa_df":   dff,
        "lat_c":     geo_data["lat_c"],
        "lon_c":     geo_data["lon_c"],
        "n_feat":    geo_data["n_feat"],
        "all_codes": geo_data.get("all_codes", []),
    }
    _mapa_data_cache[cache_key] = result
    return result


def mapa_data_all_years(sistema: str, causa: str, rm: str) -> Optional[dict]:
    """
    Agrega dados de todos os anos disponíveis para a RM.
    Retorna {yearly: [(ano, taxa_df), ...], global_min, global_max, geo_data} ou None.
    Computa escala global (min/max) compartilhada para comparação entre anos.
    """
    cache_key = (sistema, causa, rm)
    if cache_key in _mapa_all_years_cache:
        return _mapa_all_years_cache[cache_key]

    anos = anos_disponiveis(sistema, causa, rm)
    if not anos:
        _mapa_all_years_cache[cache_key] = None
        return None

    geo_data = _geojson_for_rm(rm)
    if geo_data is None:
        _mapa_all_years_cache[cache_key] = None
        return None

    yearly: List[tuple] = []
    all_taxa_vals: List[float] = []

    no_overlap_count = 0
    for ano in anos:
        data = mapa_data(sistema, causa, rm, int(ano))
        if data is None:
            continue
        if data.get("no_overlap"):
            no_overlap_count += 1
            continue
        t_df = data["taxa_df"]
        if t_df.empty or "taxa" not in t_df.columns:
            continue
        yearly.append((ano, t_df))
        vals = t_df["taxa"].dropna()
        if not vals.empty:
            all_taxa_vals.extend(vals.tolist())

    if not yearly:
        result = {"no_overlap": True} if no_overlap_count > 0 else None
        _mapa_all_years_cache[cache_key] = result
        return result

    global_min = float(min(all_taxa_vals)) if all_taxa_vals else 0.0
    global_max = float(max(all_taxa_vals)) if all_taxa_vals else 1.0
    if global_min == global_max:
        global_max = global_min + 1.0

    result = {
        "yearly":     yearly,
        "global_min": global_min,
        "global_max": global_max,
        "geo_data":   geo_data,
    }
    _mapa_all_years_cache[cache_key] = result
    return result
