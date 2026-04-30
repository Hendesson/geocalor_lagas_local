"""
Temperaturas diárias — ex-dashboard-temperaturas.
"""
import json
import os

import folium
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go

from config import YEAR_MIN, YEAR_MAX
from config_paths import ASSETS_DIR
from components import chart_card, info_card, dd, dl_btn

_mapa_estacoes_html: str | None = None
_GEOJSON_PATH = os.path.join(ASSETS_DIR, "geojson_rmb.json")


def _popup_estacao(cidade, lat, lon, n_reg, y_min, y_max):
    return f"""
    <div style="font-family:Arial,sans-serif;min-width:220px;">
      <div style="background:linear-gradient(90deg,#1761a0,#2b9eb3);color:#fff;
                  font-weight:700;padding:8px 12px;border-radius:6px 6px 0 0;font-size:13px;">
        {cidade}
      </div>
      <div style="padding:8px 12px;font-size:12px;line-height:1.7;">
        <b>Coordenadas:</b> {lat:.4f}°, {lon:.4f}°<br>
        <b>Registros:</b> {n_reg:,} observações diárias<br>
        <b>Período:</b> {y_min} – {y_max}
      </div>
    </div>"""


def build_mapa_estacoes(df: pd.DataFrame) -> str:
    global _mapa_estacoes_html
    if _mapa_estacoes_html is not None:
        return _mapa_estacoes_html

    m = folium.Map(location=[-15.78, -47.93], zoom_start=4)

    # Limites das RMBs
    if os.path.exists(_GEOJSON_PATH):
        with open(_GEOJSON_PATH, encoding="utf-8") as f:
            geojson_data = json.load(f)
        folium.GeoJson(
            geojson_data,
            name="RMBs",
            style_function=lambda _: {
                "fillColor": "#ffb347",
                "color": "#333333",
                "weight": 1.0,
                "fillOpacity": 0.18,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["NM_MUN"],
                aliases=["Município:"],
                sticky=False,
            ),
        ).add_to(m)

    # Marcadores das estações — suporta variações de nome de coluna lat/lon
    lat_col = next((c for c in ["Lat", "Latitude", "lat", "latitude"] if c in df.columns), None)
    lon_col = next((c for c in ["Long", "Longitude", "lon", "longitude"] if c in df.columns), None)
    if not df.empty and lat_col and lon_col:
        meta = df.drop_duplicates("cidade").dropna(subset=[lat_col, lon_col])
        stats = df.groupby("cidade")["year"].agg(y_min="min", y_max="max", n_reg="count").to_dict("index")
        for _, row in meta.iterrows():
            cidade = str(row["cidade"])
            lat, lon = float(row[lat_col]), float(row[lon_col])
            s = stats.get(cidade, {})
            folium.Marker(
                location=[lat, lon],
                tooltip=cidade,
                popup=folium.Popup(_popup_estacao(cidade, lat, lon,
                                                  int(s.get("n_reg", 0)),
                                                  int(s.get("y_min", YEAR_MIN)),
                                                  int(s.get("y_max", YEAR_MAX))),
                                   max_width=300),
            ).add_to(m)

    _mapa_estacoes_html = m._repr_html_()
    return _mapa_estacoes_html


def chart_note(texto: str) -> html.P:
    return html.P(texto, className="chart-note text-muted small mt-2")


def nota_tecnica_card() -> dbc.Card:
    return dbc.Card([
        dbc.CardBody([
            html.H5([html.I(className="fas fa-file-alt me-2"), "Nota Técnica"],
                    className="card-title mb-3"),
            html.P(
                "Acesse a documentação completa da metodologia utilizada "
                "nesta página do dashboard, incluindo cálculos de amplitude "
                "térmica e anomalias de temperatura.",
                className="card-text text-muted small mb-3"
            ),
            html.Div([
                html.A(
                    [html.I(className="fas fa-external-link-alt me-1"), " Visualizar"],
                    href="/nota-tecnica-temperaturas",
                    target="_blank",
                    className="btn btn-info btn-sm me-2"
                ),
                html.A(
                    [html.I(className="fas fa-print me-1"), " Baixar PDF"],
                    href="/nota-tecnica-temperaturas",
                    target="_blank",
                    className="btn btn-outline-secondary btn-sm",
                    title="Abrirá em nova aba — use Ctrl+P para salvar como PDF"
                ),
            ], className="d-flex flex-wrap gap-2")
        ])
    ], className="mt-3 nota-tecnica-card")


def _marks_periodo():
    m = {y: str(y) for y in range(YEAR_MIN, YEAR_MAX + 1, 4)}
    m[YEAR_MIN] = str(YEAR_MIN)
    m[YEAR_MAX] = str(YEAR_MAX)
    return m




def layout_temperaturas(app, df, cidades, anos):
    build_mapa_estacoes(df)
    cidade_opts = [{"label": c, "value": c} for c in cidades]
    cidade_default = "Brasília" if "Brasília" in cidades else (cidades[0] if cidades else None)

    return dbc.Container([

        # ── Cabeçalho ────────────────────────────────────────────────────────
        dbc.Row(dbc.Col([
            html.Img(src=app.get_asset_url("geocalor.png"), className="logo-img"),
            html.H2("Caracterização climática das RMB", className="text-center my-4"),
            info_card(
                "",
                html.P(
                    "Foi feita uma caracterização climática das regiões metropolitanas estudadas "
                    "no Projeto GeoCalor a partir de duas variáveis principais, a temperatura e "
                    "a umidade. Nós identificamos inicialmente o comportamento geral das temperaturas "
                    "máximas, médias e mínimas, bem como da umidade relativa do ar média. "
                    "Filtre os dados por cidade e período abaixo.",
                    className="mb-0 text-muted",
                ),
                fa_icon="fas fa-info-circle",
            ),
        ], width=12), className="text-center mb-3"),

        # ── Controles: cidade + slider na mesma linha ─────────────────────
        dbc.Row([
            dbc.Col(
                dd("cidade-temp", cidade_opts, cidade_default, label="Cidade"),
                xs=12, md=3, className="mb-2",
            ),
            dbc.Col([
                html.Label("Período:", className="fw-semibold small mb-1"),
                dcc.RangeSlider(
                    id="slider-anos",
                    min=YEAR_MIN, max=YEAR_MAX, step=1,
                    marks=_marks_periodo(),
                    value=[YEAR_MIN, YEAR_MAX],
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
            ], xs=12, md=9, className="mb-2"),
        ], className="align-items-end mb-3"),

        # ── Mapa | Temperaturas diárias (lado a lado) ────────────────────
        dbc.Row([
            dbc.Col(
                chart_card(
                    "Estações meteorológicas",
                    [
                        html.P(
                            "Passe o mouse sobre o marcador para ver o nome da cidade; "
                            "clique para exibir coordenadas, volume de dados e período.",
                            className="small text-muted mb-2",
                        ),
                        html.Iframe(
                            src="/mapa-estacoes",
                            style={"width": "100%", "height": "clamp(240px, 52vw, 420px)",
                                   "border": "none", "borderRadius": "8px"},
                        ),
                    ],
                    fa_icon="fas fa-map-marked-alt",
                ),
                xs=12, lg=5, className="mb-3",
            ),
            dbc.Col(
                chart_card(
                    "Temperaturas diárias",
                    [
                        dcc.Loading(dcc.Graph(id="grafico-temp"), type="circle"),
                        chart_note(
                            "Série temporal das temperaturas máxima (vermelho), média (laranja) "
                            "e mínima (teal) diárias para a cidade e período selecionados."
                        ),
                        dl_btn("grafico-temp", "temperaturas_diarias"),
                    ],
                    fa_icon="fas fa-thermometer-half",
                ),
                xs=12, lg=7, className="mb-3",
            ),
        ], className="align-items-stretch mb-0"),

        # ── Umidade | Amplitude (mesma altura, sem gap) ───────────────────
        dbc.Row([
            dbc.Col(
                chart_card(
                    "Umidade média mensal",
                    [
                        dcc.Loading(dcc.Graph(id="grafico-umidade"), type="circle"),
                        chart_note(
                            "Umidade relativa do ar média por mês. Valores sazonais "
                            "evidenciam a alternância entre estação seca e chuvosa."
                        ),
                        dl_btn("grafico-umidade", "umidade_media_mensal"),
                    ],
                    fa_icon="fas fa-tint",
                ),
                xs=12, lg=5, className="mb-3",
            ),
            dbc.Col(
                chart_card(
                    "Amplitude térmica diária",
                    [
                        dcc.Loading(dcc.Graph(id="grafico-amplitude"), type="circle"),
                        chart_note(
                            "Amplitude térmica diária (tempMax − tempMin). "
                            "A linha tracejada representa a média móvel de 30 dias."
                        ),
                        dl_btn("grafico-amplitude", "amplitude_termica"),
                    ],
                    fa_icon="fas fa-arrows-alt-v",
                ),
                xs=12, lg=7, className="mb-3",
            ),
        ], className="align-items-stretch"),

        # ── Anomalia de temperatura (full width — precisa de largura) ─────
        dbc.Row(dbc.Col(
            chart_card(
                "Anomalia de temperatura",
                [
                    dcc.Loading(dcc.Graph(id="grafico-anomalia"), type="circle"),
                    chart_note(
                        "Anomalia da temperatura média mensal vs. climatologia histórica do período. "
                        "Barras vermelhas: acima da média; barras teal: abaixo da média."
                    ),
                    dl_btn("grafico-anomalia", "anomalia_temperatura"),
                ],
                fa_icon="fas fa-chart-bar",
            ),
            width=12,
        ), className="mb-3"),

        # ── Nota técnica ──────────────────────────────────────────────────
        dbc.Row(dbc.Col(nota_tecnica_card(), width=12)),

    ], fluid=True, className="py-4")


def register_callbacks_temperaturas(app, df, visualizer):
    @app.callback(
        [Output("grafico-temp",      "figure"),
         Output("grafico-umidade",   "figure"),
         Output("grafico-amplitude", "figure"),
         Output("grafico-anomalia",  "figure")],
        [Input("cidade-temp",  "value"),
         Input("slider-anos",  "value")],
    )
    def update_graficos(cidade, anos_selecionados):
        empty = go.Figure()

        def _empty_four():
            return empty, empty, empty, empty

        if not cidade or df.empty or not anos_selecionados or len(anos_selecionados) < 2:
            return _empty_four()

        try:
            a0, a1 = anos_selecionados[0], anos_selecionados[1]
            if a0 is None or a1 is None:
                return _empty_four()
            ano_inicio = int(round(float(a0)))
            ano_fim = int(round(float(a1)))
        except (ValueError, TypeError):
            ano_inicio, ano_fim = YEAR_MIN, YEAR_MAX

        if ano_inicio > ano_fim:
            ano_inicio, ano_fim = ano_fim, ano_inicio
        ano_inicio = max(YEAR_MIN, min(ano_inicio, YEAR_MAX))
        ano_fim = max(YEAR_MIN, min(ano_fim, YEAR_MAX))

        return (
            visualizer.create_temperature_plot(df, cidade, ano_inicio, ano_fim),
            visualizer.create_umidity_plot(df, cidade, ano_inicio, ano_fim),
            visualizer.create_amplitude_plot(df, cidade, ano_inicio, ano_fim),
            visualizer.create_anomaly_plot(df, cidade, ano_inicio, ano_fim),
        )
