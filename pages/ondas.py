"""
Análise de ondas de calor — ex-dashboard-ondas-calor.
"""
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import calendar
from datetime import date

from components import chart_card, dd


def chart_note(texto: str) -> html.P:
    return html.P(texto, className="chart-note text-muted small mt-2")


def nota_tecnica_card() -> dbc.Card:
    return dbc.Card([
        dbc.CardBody([
            html.H5([html.I(className="fas fa-file-alt me-2"), "Nota Técnica"],
                    className="card-title mb-3"),
            html.Div([
                html.Div([
                    html.Strong("Metodologia EHF"),
                    html.P("Excess Heat Factor (Nairn & Fawcett, 2015): "
                           "combina a significância do calor em relação ao "
                           "percentil 95 histórico com a capacidade de "
                           "aclimatação humana (baseada nos 30 dias anteriores).",
                           className="small text-muted mb-2")
                ]),
                html.Div([
                    html.Strong("Classificação"),
                    html.P("Baixa Intensidade • Severa • Extrema — "
                           "definidas por desvios-padrão (σ) do EHF histórico.",
                           className="small text-muted mb-3")
                ]),
            ]),
            html.Div([
                html.A(
                    [html.I(className="fas fa-external-link-alt me-1"), " Visualizar completo"],
                    href="/nota-tecnica-ondas", target="_blank",
                    className="btn btn-info btn-sm me-2"
                ),
                html.A(
                    [html.I(className="fas fa-print me-1"), " Baixar PDF"],
                    href="/nota-tecnica-ondas", target="_blank",
                    className="btn btn-outline-secondary btn-sm",
                    title="Ctrl+P para salvar como PDF"
                ),
            ], className="d-flex flex-wrap gap-2")
        ])
    ], className="nota-tecnica-card mb-3")


def layout_ondas(app, df, cidades, anos):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Img(src=app.get_asset_url('geocalor.png'), className="logo-img"),
                html.H2("Análise de Ondas de Calor", className="text-center my-4")
            ], width=12)
        ], className="text-center"),

        html.Br(),
        dbc.Row([dbc.Col(nota_tecnica_card(), width=12)]),

        dbc.Row([
            dbc.Col([
                chart_card(
                    "Dias de OC por Mês — Período Completo",
                    [
                        dd("cidade-hw-total",
                           [{"label": c, "value": c} for c in cidades],
                           cidades[0] if cidades else None,
                           label="Cidade"),
                        dcc.Loading(dcc.Graph(id="grafico-polar-total"), type="circle"),
                        chart_note(
                            "Frequência mensal acumulada de dias de Ondas de Calor "
                            "ao longo de todo o período histórico. Cada eixo representa "
                            "um mês; o valor indica o total de dias de OC registrados."
                        ),
                    ],
                    fa_icon="fas fa-chart-pie",
                ),
            ], width=6),

            dbc.Col([
                chart_card(
                    "Dias de OC por Mês — Ano Selecionado",
                    [
                        dbc.Row([
                            dbc.Col(
                                dd("cidade-hw",
                                   [{"label": c, "value": c} for c in cidades],
                                   cidades[0] if cidades else None,
                                   label="Cidade"),
                                width=6,
                            ),
                            dbc.Col(
                                dd("ano-hw",
                                   [{"label": str(a), "value": a} for a in anos if a <= 2023],
                                   min(anos[-1], 2023) if anos else None,
                                   label="Ano"),
                                width=6,
                            ),
                        ]),
                        dcc.Loading(dcc.Graph(id="grafico-polar"), type="circle"),
                        chart_note(
                            "Distribuição mensal das Ondas de Calor para o ano e cidade "
                            "selecionados. Permite identificar os meses de maior ocorrência."
                        ),
                    ],
                    fa_icon="fas fa-calendar-alt",
                ),
            ], width=6),
        ]),

        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Button(
                    [html.I(className="fas fa-calendar-alt me-2"),
                     "Mostrar / Ocultar Calendário de Ondas de Calor"],
                    id="btn-calendario", color="primary", className="mb-3"
                ),
                html.Div(id="calendar-container", style={"display": "none"})
            ], width=12)
        ]),

        html.Br(),

        chart_card(
            "Temperatura Diária e Ondas de Calor",
            [
                dcc.Loading(dcc.Graph(id="grafico-temp-hw"), type="circle"),
                chart_note(
                    "Série temporal de temperaturas máxima, média e mínima diárias. "
                    "As faixas laranjas indicam os dias classificados como Onda de Calor "
                    "(EHF > 0 por ≥ 3 dias consecutivos). Marcadores 'Pico' = Percentil 95."
                ),
            ],
            fa_icon="fas fa-thermometer-full",
        ),

        chart_card(
            "EHF Diário e Limiar de Onda de Calor",
            [
                dcc.Loading(dcc.Graph(id="grafico-ehf-hw"), type="circle"),
                chart_note(
                    "Fator de Excesso de Calor (EHF) diário. "
                    "A linha vermelha representa o limiar zero: valores positivos "
                    "indicam condições de excesso de calor."
                ),
            ],
            fa_icon="fas fa-fire",
        ),

        chart_card(
            "Umidade Diária e Ondas de Calor",
            [
                dcc.Loading(dcc.Graph(id="grafico-umidade-hw"), type="circle"),
                chart_note(
                    "Umidade relativa (%). Faixas laranjas com opacidade proporcional "
                    "à intensidade da OC: baixa, severa e extrema."
                ),
            ],
            fa_icon="fas fa-tint",
        ),

        html.Br(),
        dbc.Card([
            html.Div(
                [html.I(className="fas fa-map me-2"), "Mapa de Temperatura Extrema"],
                className="geo-map-section-header",
            ),
            dbc.CardBody([
                html.P(
                    "Limiares de temperaturas extremas nas Regiões Metropolitanas analisadas. "
                    "Clique na imagem para expandir.",
                    className="text-muted small mb-3",
                ),
                html.Div([
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url('limiares de temperaturas extremas.png'),
                                id="img-mapa-temperatura",
                                style={"width": "160px", "height": "110px", "objectFit": "cover",
                                       "cursor": "zoom-in", "transition": "all 0.3s ease",
                                       "display": "block", "borderRadius": "10px",
                                       "boxShadow": "0 2px 8px rgba(23,97,160,0.18)"}
                            ),
                            html.Div(
                                [html.I(className="fas fa-expand-alt me-1"), "Expandir"],
                                style={
                                    "position": "absolute", "bottom": "6px", "right": "6px",
                                    "background": "rgba(23,97,160,0.75)", "color": "#fff",
                                    "fontSize": "0.72rem", "padding": "2px 7px",
                                    "borderRadius": "6px", "pointerEvents": "none",
                                },
                            ),
                        ],
                        style={"position": "relative", "display": "inline-block"},
                    ),
                    dbc.Tooltip("Clique para expandir / reduzir",
                                target="img-mapa-temperatura",
                                id="mapa-temperatura-tooltip"),
                ]),
            ]),
        ], className="mb-4 shadow-sm border-0"),

        html.Br(),

        chart_card(
            "Frequência de Ondas de Calor por Ano e Cidade",
            [
                dbc.Row([
                    dbc.Col([
                        dbc.ButtonGroup([
                            dbc.Button("Dias",    id="btn-heatmap-dias",    color="primary", active=True),
                            dbc.Button("Eventos", id="btn-heatmap-eventos", color="primary"),
                        ])
                    ], className="text-center mb-3"),
                ]),
                dcc.Loading(dcc.Graph(id="heatmap-oc"), type="circle"),
                chart_note(
                    "Frequência de dias ou eventos de OC por ano (eixo X) e cidade (eixo Y). "
                    "Cores mais intensas indicam maior ocorrência."
                ),
            ],
            fa_icon="fas fa-th",
        ),

        dbc.Card([
            html.Div(
                [html.I(className="fas fa-globe-americas me-2"), "Mapas Anuais de Dias de OC"],
                className="geo-map-section-header",
            ),
            dbc.CardBody([
                html.P(
                    "Distribuição espacial dos dias de Onda de Calor por ano. "
                    "Clique na imagem para expandir e use as setas para navegar entre anos.",
                    className="text-muted small mb-3",
                ),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col(dbc.Button(html.I(className="fas fa-chevron-left"),
                                               id="prev-year-map-button", color="primary"),
                                    width=2, className="d-flex justify-content-end align-items-center"),
                            dbc.Col(html.H4(id="current-map-year", className="text-center mb-0"),
                                    width=8, className="d-flex justify-content-center align-items-center"),
                            dbc.Col(dbc.Button(html.I(className="fas fa-chevron-right"),
                                               id="next-year-map-button", color="primary"),
                                    width=2, className="d-flex justify-content-start align-items-center"),
                        ], className="mb-3 align-items-center"),
                    ], id="year-map-navigation", style={"display": "none", "width": "100%"}),
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url('DIAS 2010.png'),
                                id="heatmap-year-map",
                                style={"width": "160px", "height": "110px", "objectFit": "cover",
                                       "cursor": "zoom-in", "transition": "all 0.3s ease",
                                       "display": "block", "borderRadius": "10px",
                                       "boxShadow": "0 2px 8px rgba(23,97,160,0.18)"}
                            ),
                            html.Div(
                                [html.I(className="fas fa-expand-alt me-1"), "Expandir"],
                                style={
                                    "position": "absolute", "bottom": "6px", "right": "6px",
                                    "background": "rgba(23,97,160,0.75)", "color": "#fff",
                                    "fontSize": "0.72rem", "padding": "2px 7px",
                                    "borderRadius": "6px", "pointerEvents": "none",
                                },
                            ),
                            dbc.Tooltip("", target="heatmap-year-map", id="heatmap-year-tooltip"),
                        ],
                        id="container-heatmap-year-map",
                        style={"position": "relative", "display": "inline-block"},
                    ),
                ]),
                dcc.Store(id='current-year-map-index', data=0),
                dcc.Store(id='year-map-list', data=[str(y) for y in range(2010, 2024)]),
            ]),
        ], className="mb-5 shadow-sm border-0"),

        html.Hr(className="my-5"),

        dbc.Card([
            html.Div(
                [html.I(className="fas fa-map-pin me-2"),
                 "Mapa de Ondas de Calor — Todas as Intensidades"],
                className="geo-map-section-header",
            ),
            dbc.CardBody([
                html.P(
                    "Estações meteorológicas das Regiões Metropolitanas. "
                    "Cada marcador representa uma estação — clique para ver "
                    "estatísticas de Baixa Intensidade, Severa e Extrema "
                    "registradas no período 1981–2023.",
                    className="text-muted small mb-3",
                ),
                html.Iframe(
                    src="/mapa-eventos-geral",
                    style={
                        "width": "100%",
                        "height": "580px",
                        "border": "none",
                        "borderRadius": "12px",
                    },
                ),
            ]),
        ], className="mb-4 shadow-sm border-0"),

        dbc.Card([
            html.Div(
                [
                    html.I(className="fas fa-map-marked-alt me-2"),
                    "Mapa interativo de eventos extremos",
                ],
                className="geo-map-section-header",
            ),
            dbc.CardBody([
                html.P(
                    "Visualização geoespacial dos eventos extremos de temperatura "
                    "nas Regiões Metropolitanas analisadas. Use os controles do mapa "
                    "para explorar diferentes regiões e períodos.",
                    className="text-muted small mb-3",
                ),
                html.Iframe(
                    src="/mapa-eventos-extremos",
                    style={
                        "width": "100%",
                        "height": "620px",
                        "border": "none",
                        "borderRadius": "12px",
                    },
                ),
            ]),
        ], className="mb-5 shadow-sm border-0"),

    ], fluid=True, className="py-4")


def register_callbacks_ondas(app, df, _cidades, _anos, data_processor, visualizer):

    def create_calendar_component(dias_calor, ano, mes, cidade):
        cal = calendar.monthcalendar(ano, mes)
        month_name = calendar.month_name[mes]

        # Mapeamento com chave normalizada (lower + espaços → hífen)
        # O dataset armazena "Low Intensity", "Severe", "Extreme" —
        # a normalização abaixo cobre ambos os formatos.
        INTENSITY_LABEL = {
            "low-intensity":  "Baixa Intensidade",
            "low intensity":  "Baixa Intensidade",
            "severe":         "Severa",
            "extreme":        "Extrema",
        }
        INTENSITY_COLOR = {
            "low-intensity":  "#ff9f1c",
            "low intensity":  "#ff9f1c",
            "severe":         "#e63946",
            "extreme":        "#dc2f3d",
        }
        INTENSITY_ABBR = {
            "low-intensity":  "BI",
            "low intensity":  "BI",
            "severe":         "S",
            "extreme":        "E",
        }

        header = html.Div([
            html.H4(f"{month_name} {ano}", className="text-center mb-3"),
            html.Div([
                html.Div(d, className="text-center fw-bold")
                for d in ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
            ], className="d-flex justify-content-between mb-2")
        ])

        def get_intensity_info(intensity):
            """Returns (color, label, abbr) for a given HWDay_Intensity value."""
            if pd.isna(intensity):
                return "#e63946", "Severa", "S"
            # Normaliza: minúsculas + sem espaços extras; mantém espaço para
            # cobrir "low intensity" (formato real do dataset)
            key = str(intensity).strip().lower()
            color = INTENSITY_COLOR.get(key, "#e63946")
            label = INTENSITY_LABEL.get(key, str(intensity).strip())
            abbr  = INTENSITY_ABBR.get(key, "OC")
            return color, label, abbr

        def get_intensity_color(intensity):
            return get_intensity_info(intensity)[0]

        weeks = []
        for week in cal:
            week_divs = []
            for day in week:
                if day == 0:
                    week_divs.append(html.Div("", className="calendar-day"))
                else:
                    current_date = date(ano, mes, day)
                    is_hw = current_date in dias_calor
                    if is_hw:
                        try:
                            row_data = df[
                                (df["cidade"] == cidade) &
                                (df["index"].dt.date == current_date)
                            ].iloc[0]
                            raw_intensity = row_data.get("HWDay_Intensity", None)
                            color, intensity_label, abbr = get_intensity_info(raw_intensity)
                            btn = dbc.Button(
                                # Número do dia em cima + abreviação da classe embaixo
                                html.Div([
                                    html.Span(str(day),
                                              style={"fontSize": "0.85rem",
                                                     "fontWeight": "700",
                                                     "lineHeight": "1"}),
                                    html.Span(abbr,
                                              style={"fontSize": "0.52rem",
                                                     "fontWeight": "600",
                                                     "lineHeight": "1",
                                                     "opacity": "0.9",
                                                     "letterSpacing": "0.03em"}),
                                ], style={"display": "flex", "flexDirection": "column",
                                          "alignItems": "center", "gap": "1px"}),
                                id={"type": "calendar-day", "index": f"{ano}-{mes}-{day}"},
                                className="calendar-day heat-wave",
                                style={"backgroundColor": color, "color": "white",
                                       "borderRadius": "50%", "width": "40px",
                                       "height": "40px", "border": "none",
                                       "display": "flex", "alignItems": "center",
                                       "justifyContent": "center", "margin": "2px",
                                       "padding": "0"}
                            )
                            popup = dbc.Popover(
                                html.Div([
                                    html.Div(
                                        f"Dia {day}/{mes}/{ano}",
                                        style={
                                            "backgroundColor": color,
                                            "color": "white",
                                            "fontWeight": "700",
                                            "padding": "8px 14px",
                                            "borderRadius": "8px 8px 0 0",
                                            "fontSize": "0.9rem",
                                        },
                                    ),
                                    html.Div([
                                        html.Div([
                                            html.Span("Classificação: ", style={"fontWeight": "600"}),
                                            html.Span(intensity_label,
                                                      style={"color": color, "fontWeight": "700"}),
                                        ], className="mb-1"),
                                        html.Div(f"Temp. Máxima: {row_data.get('tempMax','N/A')} °C"),
                                        html.Div(f"Temp. Média:  {row_data.get('tempMed','N/A')} °C"),
                                        html.Div(f"Temp. Mínima: {row_data.get('tempMin','N/A')} °C"),
                                    ], style={"padding": "10px 14px", "fontSize": "0.83rem"}),
                                ]),
                                target={"type": "calendar-day", "index": f"{ano}-{mes}-{day}"},
                                trigger="click", placement="top",
                                style={"minWidth": "200px"},
                            )
                            day_div = html.Div([btn, popup])
                        except Exception:
                            day_div = html.Div(str(day), className="calendar-day",
                                               style={"backgroundColor": "#e63946", "color": "white",
                                                      "borderRadius": "50%", "width": "40px",
                                                      "height": "40px", "display": "flex",
                                                      "alignItems": "center",
                                                      "justifyContent": "center", "margin": "2px"})
                    else:
                        day_div = html.Div(str(day), className="calendar-day",
                                           style={"backgroundColor": "transparent",
                                                  "borderRadius": "50%", "width": "40px",
                                                  "height": "40px", "display": "flex",
                                                  "alignItems": "center",
                                                  "justifyContent": "center", "margin": "2px"})
                    week_divs.append(day_div)
            weeks.append(html.Div(week_divs, className="d-flex justify-content-between mb-2"))

        return html.Div([header, html.Div(weeks, className="calendar-body")],
                        className="calendar-container p-3")

    def create_calendar_grid(dias_calor, ano, cidade):
        legend = html.Div([
            html.Strong("Legenda: ", className="me-2", style={"fontSize": "0.85rem"}),
            html.Span([
                html.Span(className="calendar-legend-dot me-1",
                          style={"backgroundColor": "#ff9f1c", "display": "inline-block",
                                 "width": "14px", "height": "14px", "borderRadius": "50%",
                                 "verticalAlign": "middle"}),
                "Baixa Intensidade",
            ], className="me-3", style={"fontSize": "0.82rem"}),
            html.Span([
                html.Span(className="calendar-legend-dot me-1",
                          style={"backgroundColor": "#e63946", "display": "inline-block",
                                 "width": "14px", "height": "14px", "borderRadius": "50%",
                                 "verticalAlign": "middle"}),
                "Severa",
            ], className="me-3", style={"fontSize": "0.82rem"}),
            html.Span([
                html.Span(className="calendar-legend-dot me-1",
                          style={"backgroundColor": "#dc2f3d", "display": "inline-block",
                                 "width": "14px", "height": "14px", "borderRadius": "50%",
                                 "verticalAlign": "middle",
                                 "border": "2px solid #b02030"}),
                "Extrema",
            ], style={"fontSize": "0.82rem"}),
        ], className="calendar-legend mb-3 ms-1",
           style={"display": "flex", "alignItems": "center", "flexWrap": "wrap",
                  "gap": "0.5rem"})

        return html.Div([
            legend,
            dbc.Row([
                dbc.Col(create_calendar_component(dias_calor, ano, mes, cidade),
                        width=4, className="mb-4")
                for mes in range(1, 13)
            ])
        ])

    @app.callback(
        Output("grafico-polar-total", "figure"),
        Input("cidade-hw-total", "value")
    )
    def update_hw_total(cidade_total):
        if not cidade_total or df.empty or data_processor is None:
            return visualizer.create_polar_plot(pd.DataFrame(), "", None)
        df_polar = data_processor.calculate_hw_monthly_all_years(cidade_total)
        return visualizer.create_polar_plot(df_polar, cidade_total, None)

    @app.callback(
        [Output("grafico-polar", "figure"),
         Output("calendar-container", "children")],
        [Input("cidade-hw", "value"), Input("ano-hw", "value")]
    )
    def update_hw_annual(cidade, ano):
        if df.empty or not cidade or not ano or data_processor is None:
            return visualizer.create_polar_plot(pd.DataFrame(), "", 0), []
        df_polar = data_processor.calculate_hw_monthly(cidade, ano)
        dias_calor = data_processor.get_heat_wave_days(cidade)
        return (visualizer.create_polar_plot(df_polar, cidade, ano),
                create_calendar_grid(dias_calor, ano, cidade))

    @app.callback(
        Output("calendar-container", "style"),
        Input("btn-calendario", "n_clicks"),
        State("calendar-container", "style")
    )
    def toggle_calendar(n_clicks, current_style):
        n = n_clicks or 0
        return {"display": "none"} if n % 2 == 0 else {"display": "block"}

    @app.callback(
        Output("grafico-temp-hw", "figure"),
        [Input("cidade-hw", "value"), Input("ano-hw", "value")]
    )
    def update_temp_hw(cidade, ano):
        if df.empty or not cidade or not ano:
            return go.Figure()
        return visualizer.create_temperature_hw_plot(df, cidade, ano)

    @app.callback(
        Output("grafico-ehf-hw", "figure"),
        [Input("cidade-hw", "value"), Input("ano-hw", "value")]
    )
    def update_ehf_hw(cidade, ano):
        if df.empty or not cidade or not ano:
            return go.Figure()
        dff = df[(df["cidade"] == cidade) & (df["year"] == ano)].copy()
        if dff.empty:
            return go.Figure()
        dff["index"] = pd.to_datetime(dff["index"])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dff["index"], y=dff["EHF"], mode="lines",
                                 name="EHF", line=dict(color="black")))
        fig.add_trace(go.Scatter(x=dff["index"], y=[0] * len(dff), mode="lines",
                                 name="Limiar OC", line=dict(color="red", dash="dash")))
        max_abs = max(abs(dff["EHF"].max()), abs(dff["EHF"].min()), 12)
        step = 6 if max_abs > 12 else 4
        ticks = list(range(int(-(max_abs // step + 1) * step),
                           int((max_abs // step + 2) * step), step))
        fig.update_layout(
            title=f"EHF Diário — {cidade}, {ano}",
            xaxis_title="Data", yaxis_title="EHF (°C²)",
            yaxis=dict(tickvals=ticks, zeroline=True, zerolinecolor="red"),
            legend=dict(orientation="h"),
            plot_bgcolor="white", paper_bgcolor="white", font=dict(size=12)
        )
        return fig

    @app.callback(
        Output("grafico-umidade-hw", "figure"),
        [Input("cidade-hw", "value"), Input("ano-hw", "value")]
    )
    def update_umidade_hw(cidade, ano):
        if df.empty or not cidade or not ano:
            return go.Figure()
        return visualizer.create_umidity_hw_plot(df, cidade, ano)

    @app.callback(
        [Output("heatmap-oc",          "figure"),
         Output("btn-heatmap-dias",    "active"),
         Output("btn-heatmap-eventos", "active")],
        [Input("btn-heatmap-dias",    "n_clicks"),
         Input("btn-heatmap-eventos", "n_clicks")]
    )
    def update_heatmap(dias_clicks, eventos_clicks):
        if df.empty or data_processor is None:
            return go.Figure(), True, False
        ctx = dash.callback_context
        btn = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

        if btn == "btn-heatmap-eventos":
            data_hm = data_processor.prepare_heatmap_events_data()
            is_dias = False
            is_ev = True
            title = "Frequência de Eventos de Ondas de Calor por Ano e Cidade"
            cb_title = "Nº de Eventos"
            cscale = "Oranges"
        else:
            data_hm = data_processor.prepare_heatmap_data()
            is_dias = True
            is_ev = False
            title = "Frequência de Dias de Ondas de Calor por Ano e Cidade"
            cb_title = "Nº de Dias"
            cscale = "Reds"

        if data_hm.empty:
            return go.Figure(), is_dias, is_ev

        try:
            mat = data_hm.pivot(index="cidade", columns="year", values="count").fillna(0)
            fig = px.imshow(
                mat,
                labels=dict(x="Ano", y="Cidade", color=cb_title),
                color_continuous_scale=cscale, aspect="auto",
            )
            fig.update_layout(title=title, xaxis_title="Ano", yaxis_title="Cidade",
                              height=500)
            return fig, is_dias, is_ev
        except Exception:
            return go.Figure(), is_dias, is_ev

    _THUMB_STYLE = {
        "width": "160px", "height": "110px", "objectFit": "cover",
        "cursor": "zoom-in", "transition": "all 0.3s ease",
        "display": "block", "borderRadius": "10px",
        "boxShadow": "0 2px 8px rgba(23,97,160,0.18)",
    }
    _FULL_STYLE = {
        "width": "90%", "height": "auto", "objectFit": "contain",
        "cursor": "zoom-out", "transition": "all 0.3s ease",
        "display": "block", "margin": "0 auto", "borderRadius": "12px",
        "boxShadow": "0 4px 24px rgba(23,97,160,0.22)",
    }

    @app.callback(
        [Output('img-mapa-temperatura', 'style'),
         Output('mapa-temperatura-tooltip', 'children')],
        Input('img-mapa-temperatura', 'n_clicks'),
        State('img-mapa-temperatura', 'style')
    )
    def toggle_mapa_temperatura(n_clicks, _style):
        n = n_clicks or 0
        if n % 2 == 0:
            return _THUMB_STYLE, "Clique para expandir"
        return _FULL_STYLE, "Clique para reduzir"

    @app.callback(
        [Output('heatmap-year-map',   'style'),
         Output('year-map-navigation', 'style')],
        Input('heatmap-year-map', 'n_clicks'),
        State('heatmap-year-map', 'style')
    )
    def toggle_heatmap_map(n_clicks, _style):
        n = n_clicks or 0
        if n % 2 == 0:
            return _THUMB_STYLE, {"display": "none"}
        return _FULL_STYLE, {"display": "flex", "justifyContent": "center", "width": "100%"}

    @app.callback(
        Output('current-year-map-index', 'data'),
        [Input('prev-year-map-button', 'n_clicks'),
         Input('next-year-map-button', 'n_clicks')],
        [State('current-year-map-index', 'data'),
         State('year-map-list',          'data')]
    )
    def update_year_index(prev, nxt, idx, year_list):
        if not year_list:
            return 0
        i = 0 if idx is None else int(idx)
        ctx = dash.callback_context
        if not ctx.triggered:
            return i
        trig = ctx.triggered[0]
        if trig.get("value") is None:
            return i
        btn = trig["prop_id"].split(".")[0]
        n = len(year_list)
        if btn == "prev-year-map-button":
            return (i - 1 + n) % n
        if btn == "next-year-map-button":
            return (i + 1) % n
        return i

    @app.callback(
        [Output('heatmap-year-map',      'src'),
         Output('current-map-year',      'children'),
         Output('heatmap-year-tooltip',  'children')],
        [Input('current-year-map-index', 'data'),
         Input('year-map-list',          'data')]
    )
    def update_heatmap_year(idx, year_list):
        if not year_list:
            return "", "", ""
        i = 0 if idx is None else int(idx) % len(year_list)
        yr = year_list[i]
        return app.get_asset_url(f"DIAS {yr}.png"), f"Ano: {yr}", f"Mapa do Ano {yr}"
