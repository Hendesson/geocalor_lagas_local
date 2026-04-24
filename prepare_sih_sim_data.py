"""
Pré-processamento dos dados SIH/SIM → parquets agregados.

Execute UMA VEZ antes de subir o dashboard:
  cd C:\\pibic_dash\\dashboard_unico
  python prepare_sih_sim_data.py

Lê:
  C:/pibic_dash/sih_banco/SIH_CARDIOVASCULAR.csv
  C:/pibic_dash/sih_banco/SIH_RESPIRATORIAS.csv
  C:/pibic_dash/sim_banco/SIM_CARDIOVASCULAR_2010-2023.csv
  C:/pibic_dash/sim_banco/SIM_RESPIRATORIAS_2010-2023.csv
  C:/pibic_dash/Shapefiles_e_Dados_População/populacao_RM.xlsx
  C:/pibic_dash/Shapefiles_e_Dados_População/shapefile_RM.shp

Grava em:
  dashboard_unico/processed/sih_sim/*.parquet
  dashboard_unico/processed/sih_sim/geojson_rm.json
"""

import json
import logging
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ── Paths ──────────────────────────────────────────────────────────────────
BASE     = Path(__file__).parent
OUT      = BASE / "processed" / "sih_sim"
OUT.mkdir(parents=True, exist_ok=True)

SIH_CARDIO = Path("C:/pibic_dash/sih_banco/SIH_CARDIOVASCULAR.csv")
SIH_RESP   = Path("C:/pibic_dash/sih_banco/SIH_RESPIRATORIAS.csv")
SIM_CARDIO = Path("C:/pibic_dash/sim_banco/SIM_CARDIOVASCULAR_2010-2023.csv")
SIM_RESP   = Path("C:/pibic_dash/sim_banco/SIM_RESPIRATORIAS_2010-2023.csv")
POP_XLSX   = Path("C:/pibic_dash/Shapefiles_e_Dados_Populacao/populacao_RM.xlsx")
# Fallback com acento
if not POP_XLSX.exists():
    POP_XLSX = Path("C:/pibic_dash/Shapefiles_e_Dados_População/populacao_RM.xlsx")
SHAPES_DIR = POP_XLSX.parent


# ── Helpers ────────────────────────────────────────────────────────────────

def norm(s) -> str:
    if not isinstance(s, str):
        s = "" if s is None else str(s)
    s = s.strip()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c) and ord(c) < 128)
    return s.upper()


FAIXA_ORDER = ["<1", "1-5", "6-10", "11-19", "20-29", "30-39",
               "40-49", "50-59", "60-69", "70-79", ">80", "Ignorado"]

def _faixa_from_idade(idade_series: pd.Series) -> pd.Series:
    """Calcula faixa etária a partir de IDADE numérica."""
    x = pd.to_numeric(idade_series, errors="coerce")
    cats = np.where(x >= 120, "Ignorado",
           np.where(x <  1,   "<1",
           np.where(x <= 5,   "1-5",
           np.where(x <= 10,  "6-10",
           np.where(x <= 19,  "11-19",
           np.where(x <= 29,  "20-29",
           np.where(x <= 39,  "30-39",
           np.where(x <= 49,  "40-49",
           np.where(x <= 59,  "50-59",
           np.where(x <= 69,  "60-69",
           np.where(x <= 79,  "70-79",
           np.where(x >= 80,  ">80", "Ignorado"))))))))))))
    return pd.Series(cats, index=idade_series.index, dtype="str")


RACA_SIH = {"01": "Branca", "02": "Preta", "03": "Parda",
             "04": "Amarela", "05": "Indígena", "99": "Ignorado"}
CAR_INT_MAP = {"01": "Eletivo", "02": "Urgência"}
ESPEC_MAP = {
    "01": "Cirúrgico", "02": "Obstétrico", "03": "Clínico", "04": "Crônicos",
    "05": "Psiquiatria", "06": "Pneumologia Sanitária", "07": "Pediátrico",
    "08": "Reabilitação", "74": "UTI I", "75": "UTI Adulto II", "76": "UTI Adulto III",
    "83": "UTI Queimados", "85": "UTI Coronariana II", "86": "UTI Coronariana III",
}
LOCOCOR_MAP = {
    "1": "Hospital",
    "2": "Outro estab. de saúde",
    "3": "Domicílio",
    "4": "Via pública",
    "5": "Outros",
    "9": "Ignorado",
}

ANOS_VALIDOS = set(range(2010, 2024))


# ── Processamento SIH ──────────────────────────────────────────────────────

def _processa_sih(csv_path: Path, prefixo: str) -> None:
    log.info("Lendo SIH: %s", csv_path.name)
    cols_needed = [
        "NOME_REGMETROP", "ANO_INTERNACAO", "MES_INTERNACAO",
        "SEXO", "RACA_COR", "MUNIC_MOV",
        "CAR_INT", "ESPEC",
    ]
    # lê com todas as colunas e seleciona as disponíveis
    df = pd.read_csv(csv_path, sep=";", encoding="latin1", dtype=str, low_memory=True)
    if "" in df.columns:
        df = df.drop(columns=[""])
    avail = [c for c in cols_needed if c in df.columns]

    # IDADE2 pode não existir em alguns arquivos → calculamos de IDADE
    if "IDADE2" in df.columns:
        df["FAIXA_ETARIA"] = df["IDADE2"].astype(str).str.strip()
    elif "IDADE" in df.columns:
        df["FAIXA_ETARIA"] = _faixa_from_idade(df["IDADE"])
    else:
        df["FAIXA_ETARIA"] = "Ignorado"

    df = df[avail + ["FAIXA_ETARIA"]].copy()

    # Normaliza
    df["ANO_INTERNACAO"]  = pd.to_numeric(df.get("ANO_INTERNACAO", pd.NA), errors="coerce")
    df["MES_INTERNACAO"]  = pd.to_numeric(df.get("MES_INTERNACAO", pd.NA), errors="coerce")
    df["NOME_RM"]         = df["NOME_REGMETROP"].astype(str).str.strip()
    df["NOME_RM_NORM"]    = df["NOME_RM"].apply(norm)
    df = df[df["ANO_INTERNACAO"].isin(ANOS_VALIDOS)]

    # Mapeia categorias
    if "RACA_COR" in df.columns:
        df["RACA_COR"] = df["RACA_COR"].astype(str).str.strip().map(RACA_SIH).fillna("Ignorado")
    if "CAR_INT" in df.columns:
        df["CAR_INT"] = df["CAR_INT"].astype(str).str.strip().map(CAR_INT_MAP).fillna(df["CAR_INT"])
    if "ESPEC" in df.columns:
        df["ESPEC"] = df["ESPEC"].astype(str).str.strip().map(ESPEC_MAP).fillna(df["ESPEC"])

    n = len(df)
    log.info("  %d registros após filtro 2010-2023", n)

    # 1. Série mensal
    g = df.groupby(["NOME_RM", "ANO_INTERNACAO", "MES_INTERNACAO"], dropna=True).size().reset_index(name="N")
    g.to_parquet(OUT / f"{prefixo}_serie_mensal.parquet", index=False)
    log.info("  serie_mensal: %d linhas", len(g))

    # 2. Taxa anual (contagens brutas — taxa calculada no processor com pop)
    g2 = df.groupby(["NOME_RM", "NOME_RM_NORM", "ANO_INTERNACAO"], dropna=True).size().reset_index(name="N")
    g2.to_parquet(OUT / f"{prefixo}_taxa_anual.parquet", index=False)

    # 3. Sexo por ano
    if "SEXO" in df.columns:
        g3 = df.groupby(["NOME_RM", "ANO_INTERNACAO", "SEXO"], dropna=True).size().reset_index(name="N")
        g3.to_parquet(OUT / f"{prefixo}_sexo_ano.parquet", index=False)

    # 4. Raça/cor
    if "RACA_COR" in df.columns:
        g4 = df.groupby(["NOME_RM", "RACA_COR"], dropna=True).size().reset_index(name="N")
        g4.to_parquet(OUT / f"{prefixo}_raca.parquet", index=False)

    # 5. Faixa etária
    g5 = df.groupby(["NOME_RM", "FAIXA_ETARIA"], dropna=True).size().reset_index(name="N")
    g5.to_parquet(OUT / f"{prefixo}_faixa_etaria.parquet", index=False)

    # 5b. Pirâmide etária: sexo × faixa etária
    if "SEXO" in df.columns:
        g_pir = df.groupby(["NOME_RM", "SEXO", "FAIXA_ETARIA"], dropna=True).size().reset_index(name="N")
        g_pir.to_parquet(OUT / f"{prefixo}_sexo_faixa.parquet", index=False)

    # 6. Caráter de internação (SIH específico)
    if "CAR_INT" in df.columns:
        g6 = df.groupby(["NOME_RM", "CAR_INT"], dropna=True).size().reset_index(name="N")
        g6.to_parquet(OUT / f"{prefixo}_car_int.parquet", index=False)

    # 7. Especialidade do leito (SIH específico)
    if "ESPEC" in df.columns:
        g7 = df.groupby(["NOME_RM", "ESPEC"], dropna=True).size().reset_index(name="N")
        g7.to_parquet(OUT / f"{prefixo}_espec.parquet", index=False)

    # 8. Mapa — contagem por município e ano
    if "MUNIC_MOV" in df.columns:
        df["MUNIC_MOV"] = df["MUNIC_MOV"].astype(str).str.strip().str.zfill(6)
        g8 = df.groupby(["NOME_RM", "MUNIC_MOV", "ANO_INTERNACAO"], dropna=True).size().reset_index(name="N")
        g8.to_parquet(OUT / f"{prefixo}_mapa_mun.parquet", index=False)

    log.info("  SIH %s: parquets gravados.", prefixo)


# ── Processamento SIM ──────────────────────────────────────────────────────

def _processa_sim(csv_path: Path, prefixo: str) -> None:
    log.info("Lendo SIM: %s", csv_path.name)
    cols_needed = [
        "NOME_REGMETROP", "ANO_OBITO", "MES_OBITO",
        "SEXO", "RACACOR", "CODMUNRES", "CODMUNOCOR",
        "LOCOCOR", "ESTCIV",
    ]
    df = pd.read_csv(csv_path, sep=";", encoding="latin1", dtype=str, low_memory=True)
    if "" in df.columns:
        df = df.drop(columns=[""])
    avail = [c for c in cols_needed if c in df.columns]

    if "IDADE2" in df.columns:
        df["FAIXA_ETARIA"] = df["IDADE2"].astype(str).str.strip()
    elif "IDADE" in df.columns:
        df["FAIXA_ETARIA"] = _faixa_from_idade(df["IDADE"])
    else:
        df["FAIXA_ETARIA"] = "Ignorado"

    df = df[avail + ["FAIXA_ETARIA"]].copy()

    df["ANO_OBITO"]    = pd.to_numeric(df.get("ANO_OBITO", pd.NA), errors="coerce")
    df["MES_OBITO"]    = pd.to_numeric(df.get("MES_OBITO", pd.NA), errors="coerce")
    df["NOME_RM"]      = df["NOME_REGMETROP"].astype(str).str.strip()
    df["NOME_RM_NORM"] = df["NOME_RM"].apply(norm)
    df = df[df["ANO_OBITO"].isin(ANOS_VALIDOS)]

    # Mapeia local do óbito
    if "LOCOCOR" in df.columns:
        df["LOCOCOR"] = df["LOCOCOR"].astype(str).str.strip().map(LOCOCOR_MAP).fillna(df["LOCOCOR"])

    n = len(df)
    log.info("  %d registros após filtro 2010-2023", n)

    # 1. Série mensal
    g = df.groupby(["NOME_RM", "ANO_OBITO", "MES_OBITO"], dropna=True).size().reset_index(name="N")
    g.to_parquet(OUT / f"{prefixo}_serie_mensal.parquet", index=False)

    # 2. Taxa anual (contagens brutas)
    g2 = df.groupby(["NOME_RM", "NOME_RM_NORM", "ANO_OBITO"], dropna=True).size().reset_index(name="N")
    g2.to_parquet(OUT / f"{prefixo}_taxa_anual.parquet", index=False)

    # 3. Sexo por ano
    if "SEXO" in df.columns:
        g3 = df.groupby(["NOME_RM", "ANO_OBITO", "SEXO"], dropna=True).size().reset_index(name="N")
        g3.to_parquet(OUT / f"{prefixo}_sexo_ano.parquet", index=False)

    # 4. Raça/cor (SIM já tem string decodificada)
    col_raca = "RACACOR" if "RACACOR" in df.columns else None
    if col_raca:
        g4 = df.groupby(["NOME_RM", col_raca], dropna=True).size().reset_index(name="N")
        g4 = g4.rename(columns={col_raca: "RACA_COR"})
        g4.to_parquet(OUT / f"{prefixo}_raca.parquet", index=False)

    # 5. Faixa etária
    g5 = df.groupby(["NOME_RM", "FAIXA_ETARIA"], dropna=True).size().reset_index(name="N")
    g5.to_parquet(OUT / f"{prefixo}_faixa_etaria.parquet", index=False)

    # 5b. Pirâmide etária: sexo × faixa etária
    if "SEXO" in df.columns:
        g_pir = df.groupby(["NOME_RM", "SEXO", "FAIXA_ETARIA"], dropna=True).size().reset_index(name="N")
        g_pir.to_parquet(OUT / f"{prefixo}_sexo_faixa.parquet", index=False)

    # 6. Local do óbito (SIM específico)
    if "LOCOCOR" in df.columns:
        g6 = df.groupby(["NOME_RM", "LOCOCOR"], dropna=True).size().reset_index(name="N")
        g6.to_parquet(OUT / f"{prefixo}_lococor.parquet", index=False)

    # 7. Estado civil (SIM específico)
    if "ESTCIV" in df.columns:
        g7 = df.groupby(["NOME_RM", "ESTCIV"], dropna=True).size().reset_index(name="N")
        g7.to_parquet(OUT / f"{prefixo}_estciv.parquet", index=False)

    # 8. Mapa — contagem por município de OCORRÊNCIA do óbito e ano
    # CODMUNOCOR = município onde o óbito ocorreu (hospital/domicílio)
    # CODMUNRES  = município de residência — NÃO usar para mapa geográfico da RM
    mun_mapa = next((c for c in ["CODMUNOCOR", "CODMUNRES"] if c in df.columns), None)
    if mun_mapa:
        if mun_mapa == "CODMUNRES":
            log.warning("  CODMUNOCOR ausente — usando CODMUNRES como fallback para mapa_mun "
                        "(pode haver inconsistência geográfica em RMs polo, ex.: Curitiba)")
        df_mapa = df[[c for c in ["NOME_RM", mun_mapa, "ANO_OBITO"] if c in df.columns]].copy()
        df_mapa["CODMUNOCOR"] = df_mapa[mun_mapa].astype(str).str.strip().str[:6].str.zfill(6)
        g8 = df_mapa.groupby(["NOME_RM", "CODMUNOCOR", "ANO_OBITO"], dropna=True).size().reset_index(name="N")
        g8.to_parquet(OUT / f"{prefixo}_mapa_mun.parquet", index=False)
        log.info("  mapa_mun: %d linhas (coluna fonte: %s)", len(g8), mun_mapa)
    else:
        log.warning("  mapa_mun não gerado: CODMUNOCOR e CODMUNRES ausentes")

    log.info("  SIM %s: parquets gravados.", prefixo)


# ── População ──────────────────────────────────────────────────────────────

def _processa_populacao() -> None:
    out_path = OUT / "populacao_RM.parquet"
    log.info("Lendo população: %s", POP_XLSX)
    try:
        pop = pd.read_excel(POP_XLSX)
    except Exception as e:
        log.error("Erro ao ler populacao_RM.xlsx: %s", e)
        return

    for col in ["COD_MUN6", "NOME_RM", "NOME_CA"]:
        if col in pop.columns:
            pop[col] = pop[col].astype(str).str.strip()

    # Garante colunas pop_* em minúsculas
    rename = {c: c.lower() for c in pop.columns if c.upper().startswith("POP_") and c != c.lower()}
    if rename:
        pop.rename(columns=rename, inplace=True)

    if "NOME_RM" in pop.columns:
        pop["NOME_RM_NORM"] = pop["NOME_RM"].apply(norm)

    pop.to_parquet(out_path, index=False)
    log.info("  População: %d linhas gravadas.", len(pop))


# ── GeoJSON das RMs ────────────────────────────────────────────────────────

def _processa_geojson() -> None:
    out_path = OUT / "geojson_rm.json"
    shp_main   = SHAPES_DIR / "shapefile_RM.shp"
    shp_cuiaba = SHAPES_DIR / "shapefile_RM_cuiaba.shp"

    try:
        import geopandas as gpd
    except ImportError:
        log.warning("geopandas não instalado — mapa coroplético indisponível. "
                    "Instale com: pip install geopandas")
        return

    gdfs = []
    for shp in [shp_main, shp_cuiaba]:
        if shp.exists():
            try:
                gdf = gpd.read_file(shp)
                gdfs.append(gdf)
                log.info("  Shapefile carregado: %s (%d features)", shp.name, len(gdf))
            except Exception as e:
                log.warning("  Falha ao ler %s: %s", shp.name, e)

    if not gdfs:
        log.warning("Nenhum shapefile encontrado em %s", SHAPES_DIR)
        return

    gdf_all = pd.concat(gdfs, ignore_index=True)

    # Normaliza código municipal (6 dígitos)
    for col_cod in ["COD_MUN", "CD_MUN", "GEOCOD", "CD_GEOCMU"]:
        if col_cod in gdf_all.columns:
            gdf_all["COD_MUN6"] = gdf_all[col_cod].astype(str).str.strip().str[:6].str.zfill(6)
            break

    if "NOME_CA" in gdf_all.columns:
        gdf_all["NOME_CA_NORM"] = gdf_all["NOME_CA"].apply(norm)

    gdf_all = gdf_all.to_crs(epsg=4326)
    geojson = json.loads(gdf_all.to_json())

    # Adiciona COD_MUN6 como id de cada feature para plotly
    for feat, (_, row) in zip(geojson["features"], gdf_all.iterrows()):
        feat["id"] = str(row.get("COD_MUN6", ""))

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False)
    log.info("  GeoJSON gravado: %d features", len(geojson["features"]))


# ── Entry point ────────────────────────────────────────────────────────────

def main() -> None:
    log.info("=== Iniciando pré-processamento SIH/SIM ===")

    _processa_sih(SIH_CARDIO, "sih_cardiovascular")
    _processa_sih(SIH_RESP,   "sih_respiratorias")
    _processa_sim(SIM_CARDIO, "sim_cardiovascular")
    _processa_sim(SIM_RESP,   "sim_respiratorias")
    _processa_populacao()
    _processa_geojson()

    log.info("=== Concluído. Parquets em: %s ===", OUT)


if __name__ == "__main__":
    main()
