"""
Temperaturas diárias — ex-dashboard-temperaturas.
"""
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import pandas as pd
import plotly.graph_objs as go

from config import YEAR_MIN, YEAR_MAX
from components import chart_card, info_card, dd, dl_btn


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


_estacoes_cache: list | None = None


def _estacoes_map_children(df: pd.DataFrame):
    """Marcadores com tooltip + popup com detalhes ao clicar."""
    global _estacoes_cache
    if _estacoes_cache is not None:
        return _estacoes_cache
    if df.empty or "Lat" not in df.columns or "Long" not in df.columns:
        return []
    meta = df.drop_duplicates(subset=["cidade"], keep="first").dropna(subset=["Lat", "Long"])
    # Pré-computa estatísticas por cidade uma única vez (evita 15 filtros full-df)
    city_stats = (
        df.groupby("cidade")["year"]
        .agg(y_min="min", y_max="max", n_reg="count")
        .to_dict("index")
    )
    out = []
    for _, row in meta.iterrows():
        cidade = str(row["cidade"])
        stats  = city_stats.get(cidade, {})
        y_min  = int(stats.get("y_min", YEAR_MIN))
        y_max  = int(stats.get("y_max", YEAR_MAX))
        n_reg  = int(stats.get("n_reg", 0))
        lat, lon = float(row["Lat"]), float(row["Long"])

        extras = []
        for col, label in [
            ("UF", "UF"),
            ("Estado", "Estado"),
            ("RM", "Região metropolitana"),
            ("Regiao", "Região"),
        ]:
            if col in row.index and pd.notna(row[col]) and str(row[col]).strip():
                extras.append(
                    html.P([html.Strong(f"{label}: "), str(row[col])], className="small mb-1")
                )

        popup_body = html.Div([
            html.H6(cidade, className="text-primary mb-2 fw-bold"),
            html.P([
                html.I(className="fas fa-location-dot me-1 text-muted"),
                html.Span(f"{lat:.4f}°, {lon:.4f}°", className="small"),
            ], className="mb-2"),
            html.P([html.Strong("Registros: "), f"{n_reg:,} observações diárias"], className="small mb-1"),
            html.P([html.Strong("Anos nos dados: "), f"{y_min} – {y_max}"], className="small mb-2"),
        ] + extras + [
            html.Hr(className="my-2"),
            html.P(
                "Use o menu «Cidade» ao lado para carregar os gráficos desta estação.",
                className="small text-muted mb-0",
                style={"fontStyle": "italic"},
            ),
        ], style={"minWidth": "240px", "maxWidth": "320px"})

        out.append(
            dl.Marker(
                position=[lat, lon],
                children=[
                    dl.Tooltip(cidade),
                    dl.Popup(children=popup_body),
                ],
            )
        )
    _estacoes_cache = out
    return out


def layout_temperaturas(app, df, cidades, anos):
    map_center = (
        (float(df["Lat"].mean()), float(df["Long"].mean()))
        if not df.empty and "Lat" in df.columns and "Long" in df.columns
        else (-15.0, -50.0)
    )
    map_layers = [
        dl.TileLayer(),
        dl.LayerGroup(children=_estacoes_map_children(df)),
    ]

    cidade_opts = [{"label": c, "value": c} for c in cidades]

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Img(src=app.get_asset_url("geocalor.png"), className="logo-img"),
                html.H2("Caracterização Climática das RMB", className="text-center my-4"),
                info_card(
                    "",
                    html.P(
                        "Foi feita uma caracterização climática das regiões metropolitanas estudadas "
                        "no Projeto GeoCalor a partir de duas variáveis principais, a temperatura e "
                        "a umidade. Nós identificamos inicialmente o comportamento geral das temperaturas "
                        "máximas, médias e mínimas, bem como da umidade relativa do ar média. Você pode ver "
                        "isso abaixo e filtrar os dados por ano e por cidade.",
                        className="mb-0 text-muted",
                    ),
                    fa_icon="fas fa-info-circle",
                ),
            ], width=12),
        ], align="center", className="text-center"),

        html.Br(),

        dbc.Row([
            dbc.Col([
                html.Label("Selecione o período:", className="fw-semibold"),
                dcc.RangeSlider(
                    id="slider-anos",
                    min=YEAR_MIN, max=YEAR_MAX, step=1,
                    marks=_marks_periodo(),
                    value=[YEAR_MIN, YEAR_MAX],
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
            ], width=12),
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col([
                chart_card(
                    "Estações meteorológicas",
                    [
                        html.P(
                            "Passe o mouse para o nome da cidade; clique no marcador para "
                            "coordenadas, volume de dados e período disponível.",
                            className="small text-muted mb-2",
                        ),
                        dl.Map(
                            map_layers,
                            id="mapa-estacoes-temp",
                            style={"width": "100%", "height": "clamp(240px, 50vw, 440px)", "borderRadius": "8px"},
                            center=map_center,
                            zoom=4,
                        ),
                    ],
                    fa_icon="fas fa-map-marked-alt",
                ),
            ], xs=12, lg=5),

            dbc.Col([
                dd("cidade-temp", cidade_opts, cidades[0] if cidades else None, label="Cidade"),
                html.Br(),
                chart_card(
                    "Temperaturas diárias",
                    [
                        dcc.Loading(dcc.Graph(id="grafico-temp"), type="circle"),
                        chart_note(
                            "Série temporal das temperaturas máxima (vermelho), média "
                            "(laranja) e mínima (teal) diárias para a cidade e período selecionados."
                        ),
                        dl_btn("grafico-temp", "temperaturas_diarias"),
                    ],
                    fa_icon="fas fa-thermometer-half",
                ),
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
            ], xs=12, lg=7),
        ]),

        dbc.Row([
            dbc.Col(
                info_card(
                    "",
                    html.P(
                        "A partir dos dados base obtidos do INMET ou do ICEA, nós identificamos "
                        "também as amplitudes térmicas e as anomalias de temperatura, pois são "
                        "importantes indicadores climáticos para servirem de base das investigações "
                        "futuras sobre ondas de calor.",
                        className="mb-0 text-muted",
                    ),
                    fa_icon="fas fa-chart-area",
                ),
                width=12,
            ),
        ]),

        dbc.Row([
            dbc.Col([
                chart_card(
                    "Amplitude térmica diária",
                    [
                        dcc.Loading(dcc.Graph(id="grafico-amplitude"), type="circle"),
                        chart_note(
                            "Amplitude térmica diária (tempMax − tempMin). A linha "
                            "tracejada representa a média móvel de 30 dias."
                        ),
                        dl_btn("grafico-amplitude", "amplitude_termica"),
                    ],
                    fa_icon="fas fa-arrows-alt-v",
                ),
            ], xs=12, md=6, className="mb-3"),
            dbc.Col([
                chart_card(
                    "Anomalia de temperatura",
                    [
                        dcc.Loading(dcc.Graph(id="grafico-anomalia"), type="circle"),
                        chart_note(
                            "Anomalia da temperatura média mensal vs. climatologia histórica. "
                            "Barras vermelhas: acima da média; barras teal: abaixo."
                        ),
                        dl_btn("grafico-anomalia", "anomalia_temperatura"),
                    ],
                    fa_icon="fas fa-chart-bar",
                ),
            ], xs=12, md=6, className="mb-3"),
        ], className="align-items-stretch"),

        dbc.Row([
            dbc.Col(nota_tecnica_card(), width=12),
        ]),

    ], fluid=True, className="py-4")


def register_callbacks_temperaturas(app, df, visualizer):
    @app.callback(
        [Output("grafico-temp",      "figure"),
         Output("grafico-umidade",   "figure"),
         Output("grafico-amplitude", "figure"),
         Output("grafico-anomalia",  "figure")],
        [Input("cidade-temp",  "value"),
         Input("slider-anos",  "value")]
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
