"""
Regenera os mapas Folium em mapa_eventos/.

    mapa_geral.html     → todas as intensidades (Baixa, Severa, Extrema)
    mapa_interativo.html → apenas Severa + Extrema (ondas de maior intensidade)

Uso:
    python gerar_mapas.py
    python gerar_mapas.py --apenas-geral
    python gerar_mapas.py --apenas-interativo

NOTA: usa HW_Intensity (intensidade do evento) para calcular duração —
nunca usar HWDay_Intensity para isso.
"""
import argparse
import os

import folium
import pandas as pd

PARQUET  = os.path.join("processed", "banco_dados_climaticos_consolidado (2).parquet")
OUT_DIR  = "mapa_eventos"

INTENSITIES_GERAL = [
    ("Low Intensity", "Baixa Intensidade", "#ff9f1c"),
    ("Severe",        "Severa",            "#e63946"),
    ("Extreme",       "Extrema",           "#dc2f3d"),
]

INTENSITIES_MAJOR = [
    ("Severe",  "Severa",  "#e63946"),
    ("Extreme", "Extrema", "#dc2f3d"),
]


def _popup_html(cidade, lat, lon, total_events, rows):
    tbody = ""
    for label, color, n_ev, dur_med, dur_max, max_temp, max_ehf in rows:
        tbody += f"""
            <tr>
              <td style="padding:7px 10px;border-bottom:1px solid #eee;white-space:nowrap;">
                <span style="display:inline-block;width:11px;height:11px;border-radius:50%;
                             background:{color};margin-right:6px;vertical-align:middle;"></span>
                <b>{label}</b>
              </td>
              <td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;">{n_ev}</td>
              <td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;">{dur_med}</td>
              <td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;">{dur_max}</td>
              <td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;">{max_temp}</td>
              <td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;">{max_ehf}</td>
            </tr>"""

    return f"""
    <div style="font-family:Arial,sans-serif;min-width:360px;">
      <div style="background:linear-gradient(90deg,#1761a0,#2b9eb3);color:#fff;
                  font-weight:700;padding:9px 14px;border-radius:7px 7px 0 0;font-size:14px;">
        {cidade}
        <span style="float:right;font-size:11px;font-weight:400;opacity:0.85;">
          Estação: {lat:.2f}°, {lon:.2f}°
        </span>
      </div>
      <div style="padding:8px 10px 4px;font-size:12px;color:#555;">
        <b>Total de eventos registrados:</b> {total_events}
      </div>
      <table style="width:100%;border-collapse:collapse;font-size:12px;">
        <thead>
          <tr style="background:#f5f8fb;color:#1761a0;">
            <th style="padding:6px 10px;text-align:left;">Classificação</th>
            <th style="padding:6px 10px;">Eventos</th>
            <th style="padding:6px 10px;">Dur. média</th>
            <th style="padding:6px 10px;">Dur. máx.</th>
            <th style="padding:6px 10px;">T máx.</th>
            <th style="padding:6px 10px;">EHF máx.</th>
          </tr>
        </thead>
        <tbody>{tbody}</tbody>
      </table>
      <div style="padding:6px 10px 8px;font-size:11px;color:#888;font-style:italic;">
        Dados: 1981–2023 · EHF (Nairn &amp; Fawcett, 2015)
      </div>
    </div>"""


def build_map(df_hw, intensities, title=None):
    m = folium.Map(location=[-15.77972, -47.92972], zoom_start=4)

    if title:
        folium.Element(
            f'<h3 style="position:absolute;z-index:100000;left:50px;top:10px;'
            f'background-color:white;padding:10px;border-radius:5px;'
            f'box-shadow:0 0 5px rgba(0,0,0,0.2);">{title}</h3>'
        )

    for cidade in sorted(df_hw["cidade"].unique()):
        city_hw = df_hw[df_hw["cidade"] == cidade]
        lat = float(city_hw["Lat"].iloc[0])
        lon = float(city_hw["Long"].iloc[0])
        total = city_hw.drop_duplicates(subset=["group"]).shape[0]

        rows = []
        marker_color = "#ff9f1c"
        for hw_int, label, color in intensities:
            sub = city_hw[city_hw["HW_Intensity"] == hw_int]
            ev  = sub.drop_duplicates(subset=["group"]) if not sub.empty else sub
            n_ev    = len(ev)
            dur_med = f"{ev['HW_duration'].mean():.1f}d" if n_ev > 0 else "-"
            dur_max = f"{int(ev['HW_duration'].max())}d"  if n_ev > 0 else "-"
            max_t   = f"{sub['tempMax'].max():.1f}°C"     if n_ev > 0 else "-"
            max_e   = f"{sub['EHF'].max():.2f}"           if n_ev > 0 else "-"
            rows.append((label, color, n_ev, dur_med, dur_max, max_t, max_e))
            if n_ev > 0:
                marker_color = color  # usa cor da intensidade mais alta

        popup_html = _popup_html(cidade, lat, lon, total, rows)
        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.8,
            tooltip=cidade,
            popup=folium.Popup(popup_html, max_width=420),
        ).add_to(m)

    return m


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apenas-geral",      action="store_true")
    parser.add_argument("--apenas-interativo", action="store_true")
    args = parser.parse_args()

    print(f"Lendo {PARQUET}...")
    df = pd.read_parquet(PARQUET)
    hw = df[df["isHW"] == True].copy()
    os.makedirs(OUT_DIR, exist_ok=True)

    if not args.apenas_interativo:
        print("Gerando mapa_geral.html (todas as intensidades)...")
        m = build_map(hw, INTENSITIES_GERAL)
        m.save(os.path.join(OUT_DIR, "mapa_geral.html"))
        print("  → mapa_eventos/mapa_geral.html salvo")

    if not args.apenas_geral:
        print("Gerando mapa_interativo.html (Severa + Extrema)...")
        hw_major = hw[hw["HW_Intensity"].isin(["Severe", "Extreme"])]
        m2 = build_map(hw_major, INTENSITIES_MAJOR)
        # Injeta título no HTML gerado
        html_str = m2._repr_html_()
        out_path = os.path.join(OUT_DIR, "mapa_interativo.html")
        m2.save(out_path)
        # Adiciona título ao arquivo salvo
        with open(out_path, "r", encoding="utf-8") as f:
            content = f.read()
        title_tag = (
            '\n    <h3 style="position:absolute;z-index:100000;left:50px;top:10px;'
            'background-color:white;padding:10px;border-radius:5px;'
            'box-shadow:0 0 5px rgba(0,0,0,0.2);">\n'
            '        Mapa interativo das ondas de calor de maior intensidade\n'
            '    </h3>\n    '
        )
        content = content.replace("<body>\n    \n    \n    ", f"<body>\n    {title_tag}")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  → mapa_eventos/mapa_interativo.html salvo")

    print("Concluído.")


if __name__ == "__main__":
    main()
