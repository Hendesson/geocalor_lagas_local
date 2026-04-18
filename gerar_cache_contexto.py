"""
Gera cache/geocalor_context.json com estatísticas pré-computadas do dataset.
Executar sempre que os dados em processed/ forem atualizados.

Uso:
    python gerar_cache_contexto.py
"""
import json
import os
from datetime import date

import pandas as pd

PARQUET = os.path.join("processed", "banco_dados_climaticos_consolidado (2).parquet")
OUTPUT  = os.path.join("cache", "geocalor_context.json")


def main():
    print(f"Lendo {PARQUET}...")
    df = pd.read_parquet(PARQUET)
    hw = df[df["isHW"] == True].copy()

    cidades = sorted(df["cidade"].unique().tolist())
    anos    = sorted(df["year"].unique().tolist())

    city_stats = {}
    for cidade in cidades:
        c = df[df["cidade"] == cidade]
        h = hw[hw["cidade"] == cidade]
        events = h.drop_duplicates(subset=["group"]) if not h.empty else h

        by_intensity = {}
        for intens in ["Low Intensity", "Severe", "Extreme"]:
            sub = h[h["HW_Intensity"] == intens]
            ev  = sub.drop_duplicates(subset=["group"]) if not sub.empty else sub
            by_intensity[intens] = {
                "n_events": len(ev),
                "n_days":   len(sub),
                "dur_mean": round(float(ev["HW_duration"].mean()), 1) if len(ev) > 0 else 0,
                "dur_max":  int(ev["HW_duration"].max())              if len(ev) > 0 else 0,
                "temp_max": round(float(sub["tempMax"].max()), 1)     if len(sub) > 0 else None,
                "ehf_max":  round(float(sub["EHF"].max()), 2)         if len(sub) > 0 else None,
            }

        city_stats[cidade] = {
            "lat":               round(float(c["Lat"].iloc[0]), 4),
            "lon":               round(float(c["Long"].iloc[0]), 4),
            "years":             [int(c["year"].min()), int(c["year"].max())],
            "n_rows":            len(c),
            "hw_total_events":   len(events),
            "hw_total_days":     len(h),
            "by_intensity":      by_intensity,
        }

    cache = {
        "generated":    str(date.today()),
        "parquet_file": os.path.basename(PARQUET),
        "shape":        list(df.shape),
        "cidades":      cidades,
        "anos":         [anos[0], anos[-1]],
        "columns":      list(df.columns),
        "city_stats":   city_stats,
    }

    os.makedirs("cache", exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

    print(f"Salvo em {OUTPUT}")
    print(f"  {len(cidades)} cidades | {anos[0]}–{anos[-1]} | {df.shape[0]:,} linhas")


if __name__ == "__main__":
    main()
