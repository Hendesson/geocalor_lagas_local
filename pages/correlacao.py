"""
Análise de Correlação — Risco Relativo por Defasagem (OC × Internações/Óbitos).
Fonte: dlnm_results.json (pré-computado em R: glm.nb + DLNM crossbasis).
"""
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

import data_correlacao as dc
from components import chart_card, info_card, kpi_box, dd, dl_btn


def chart_note(texto: str) -> html.P:
    return html.P(texto, className="chart-note text-muted small mt-2")


# ── Plotly base ───────────────────────────────────────────────────────────────

_LAYOUT_BASE = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Segoe UI, sans-serif", color="#333"),
    margin=dict(l=55, r=35, t=50, b=55),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

_EMPTY = go.Figure(layout=go.Layout(
    **_LAYOUT_BASE,
    annotations=[dict(text="Dados não disponíveis para esta seleção",
                      x=0.5, y=0.5, showarrow=False,
                      font=dict(size=14, color="#aaa"))],
))


# ── Figura RR × lag ───────────────────────────────────────────────────────────

def _fig_rr_lag(df_rr, rm_label: str = ""):
    if df_rr.empty:
        return _EMPTY

    has_ic = "ic_low" in df_rr.columns and df_rr["ic_low"].notna().any()
    lag_max = int(df_rr["lag"].max()) if not df_rr.empty else 7
    fig = go.Figure()

    if has_ic:
        x_fwd = df_rr["lag"].tolist()
        y_hi  = df_rr["ic_high"].tolist()
        y_lo  = df_rr["ic_low"].tolist()[::-1]
        fig.add_trace(go.Scatter(
            x=x_fwd + x_fwd[::-1],
            y=y_hi + y_lo,
            fill="toself",
            fillcolor="rgba(23,97,160,0.15)",
            line=dict(width=0),
            hoverinfo="skip",
            showlegend=True,
            name="IC 95%",
        ))

    fig.add_trace(go.Scatter(
        x=df_rr["lag"],
        y=df_rr["rr"],
        mode="lines+markers",
        line=dict(color="#1761a0", width=2.5),
        marker=dict(size=7, color="#1761a0"),
        name="RR",
        hovertemplate=(
            "<b>Lag %{x} dias</b><br>"
            "RR = %{y:.3f}"
            + ("<br>IC95%: [%{customdata[0]:.3f}, %{customdata[1]:.3f}]" if has_ic else "")
            + "<extra></extra>"
        ),
        customdata=df_rr[["ic_low", "ic_high"]].values if has_ic else None,
        connectgaps=False,
    ))

    fig.add_hline(y=1, line_dash="dash", line_color="#e63946", line_width=1.5,
                  annotation_text="RR = 1",
                  annotation_position="bottom right",
                  annotation_font=dict(color="#e63946", size=11))

    fig.update_layout(
        **_LAYOUT_BASE,
        xaxis=dict(title="Lag (dias)", dtick=1, gridcolor="#eee",
                   tick0=0, range=[-0.4, lag_max + 0.4]),
        yaxis=dict(title="RR (IC 95%)", gridcolor="#eee", zeroline=False),
        title=dict(text=rm_label, font=dict(size=13), x=0.5) if rm_label else {},
    )
    return fig


# ── Nota técnica (padrão GeoCalor) ───────────────────────────────────────────

def _nota_tecnica_card() -> dbc.Card:
    return dbc.Card([
        dbc.CardBody([
            html.H5([html.I(className="fas fa-file-alt me-2"), "Nota Técnica"],
                    className="card-title mb-3"),
            html.Div([
                html.Div([
                    html.Strong("Modelo estatístico"),
                    html.P(
                        "Regressão Binomial Negativa com DLNM (crossbasis, lag=7, "
                        "spline natural 3 df), ajustada por sazonalidade (spline natural "
                        "7 df/ano), umidade relativa, amplitude térmica e dia da semana.",
                        className="small text-muted mb-2",
                    ),
                ]),
                html.Div([
                    html.Strong("Período e referência"),
                    html.P(
                        "2010–2019 (sem COVID 2020–2022; exceção: Recife 2010–2022). "
                        "Categoria de referência: dias sem onda de calor (isHW = 0).",
                        className="small text-muted mb-3",
                    ),
                ]),
            ]),
            html.Div([
                html.A(
                    [html.I(className="fas fa-external-link-alt me-1"), " Visualizar completo"],
                    href="/nota-tecnica-correlacao", target="_blank",
                    className="btn btn-info btn-sm me-2",
                ),
                html.A(
                    [html.I(className="fas fa-print me-1"), " Baixar PDF"],
                    href="/nota-tecnica-correlacao", target="_blank",
                    className="btn btn-outline-secondary btn-sm",
                    title="Ctrl+P para salvar como PDF",
                ),
            ], className="d-flex flex-wrap gap-2"),
        ])
    ], className="nota-tecnica-card mb-3")


# ── Layout ────────────────────────────────────────────────────────────────────

def layout_correlacao(app):
    agravos = [
        {"label": "Respiratórias",  "value": "RESPIRATORIAS"},
        {"label": "Cardiovascular", "value": "CARDIOVASCULAR"},
    ]
    rms_ini = dc.rms_disponiveis("RESPIRATORIAS")
    rm_default = rms_ini[0] if rms_ini else None

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Img(src=app.get_asset_url("geocalor.png"), className="logo-img"),
                html.H2("Internações associadas a ondas de calor",
                        className="text-center my-4"),
            ], width=12),
        ], className="text-center"),

        dcc.Store(id="corr-modo", data="single"),

        # ── Filtros ──────────────────────────────────────────────────────────
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(dd("corr-agravo", agravos, "RESPIRATORIAS",
                               label="Agravo"), xs=12, md=4),
                    dbc.Col(dd("corr-rm",
                               [{"label": r, "value": r} for r in rms_ini],
                               rm_default, label="Região Metropolitana"), xs=12, md=5),
                    dbc.Col([
                        html.Label("\u00a0", className="filter-label d-block mb-1"),
                        html.Button(
                            [html.I(className="fas fa-th me-2"), "Ver todas as RMs"],
                            id="corr-all-btn",
                            className="btn btn-outline-primary fw-bold w-100",
                            n_clicks=0,
                        ),
                    ], xs=12, md=3),
                ], className="g-2 align-items-end"),
            ])
        ], className="shadow-sm border-0 mb-4"),

        # ── Info metodológica ─────────────────────────────────────────────────
        info_card(
            "Sobre o modelo",
            html.P([
                "RR estimado por ",
                html.Strong("glm.nb + DLNM crossbasis"),
                " (lag=7, spline natural 3 df), ajustado por sazonalidade, "
                "umidade, amplitude térmica e dia da semana. "
                "Período 2010–2019 (sem COVID). Referência: dias sem OC.",
            ], className="mb-0 text-muted small"),
            fa_icon="fas fa-flask",
        ),

        # ── Vista única ───────────────────────────────────────────────────────
        html.Div(id="corr-single-view", children=[
            chart_card("Risco Relativo por Defasagem (IC 95%)", [
                dcc.Graph(
                    id="corr-rr-graph",
                    style={"height": "clamp(300px, 55vw, 460px)"},
                    config={"displayModeBar": False},
                ),
                html.Div(id="corr-rr-note"),
                dl_btn("corr-rr-graph", "rr_por_lag"),
            ], fa_icon="fas fa-chart-line"),
        ]),

        # ── Vista todas as RMs ────────────────────────────────────────────────
        html.Div(id="corr-all-view", style={"display": "none"}, children=[
            dbc.Row([
                dbc.Col([
                    html.Button(
                        [html.I(className="fas fa-download me-2"), "Baixar todos (PNG)"],
                        className="btn btn-outline-secondary btn-sm mb-3",
                        **{
                            "data-mapa-download": "corr-all-container",
                            "data-mapa-filename": "rr_por_lag_todas_rms",
                        },
                    ),
                ], xs=12),
            ]),
            html.Div(id="corr-all-container"),
        ]),

        # ── Nota técnica ──────────────────────────────────────────────────────
        _nota_tecnica_card(),

    ], fluid=True)


# ── Callbacks ─────────────────────────────────────────────────────────────────

def register_callbacks_correlacao(app):

    # RM options por agravo
    @app.callback(
        Output("corr-rm", "options"),
        Output("corr-rm", "value"),
        Input("corr-agravo", "value"),
    )
    def _update_rms(agravo):
        rms = dc.rms_disponiveis(agravo or "RESPIRATORIAS")
        opts = [{"label": r, "value": r} for r in rms]
        return opts, (rms[0] if rms else None)

    # Toggle single ↔ all
    @app.callback(
        Output("corr-modo", "data"),
        Output("corr-all-btn", "className"),
        Output("corr-single-view", "style"),
        Output("corr-all-view", "style"),
        Output("corr-rm", "disabled"),
        Input("corr-all-btn", "n_clicks"),
        State("corr-modo", "data"),
        prevent_initial_call=True,
    )
    def _toggle_modo(n, modo_atual):
        novo = "all" if modo_atual != "all" else "single"
        btn_cls = ("btn btn-primary fw-bold w-100" if novo == "all"
                   else "btn btn-outline-primary fw-bold w-100")
        show_single = {} if novo == "single" else {"display": "none"}
        show_all    = {} if novo == "all"    else {"display": "none"}
        return novo, btn_cls, show_single, show_all, novo == "all"

    # Gráfico único
    @app.callback(
        Output("corr-rr-graph", "figure"),
        Output("corr-rr-note", "children"),
        Input("corr-agravo", "value"),
        Input("corr-rm", "value"),
    )
    def _update_rr_single(agravo, rm):
        if not agravo or not rm:
            return _EMPTY, ""

        is_dlnm = dc.dlnm_disponivel(agravo, rm)
        if is_dlnm:
            df_rr = dc.rr_por_lag_dlnm(agravo, rm)
            note = chart_note(
                "Modelo: glm.nb + DLNM crossbasis (lag=7) — ajustado por sazonalidade, "
                "umidade, amplitude térmica e dia da semana. Período 2010–2019. "
                "Banda: IC 95%."
            )
        else:
            df_rr = dc.rr_por_lag(agravo, rm, 2010, 2023)
            note = chart_note(
                "Atenção: resultados DLNM não disponíveis para este agravo. "
                "Exibindo RR bruto (razão de médias, sem ajuste por confundidores)."
            )

        return _fig_rr_lag(df_rr, rm_label=rm), note

    # Grade todas as RMs
    @app.callback(
        Output("corr-all-container", "children"),
        Input("corr-agravo", "value"),
        Input("corr-modo", "data"),
    )
    def _update_rr_all(agravo, modo):
        if modo != "all" or not agravo:
            return []

        rms = dc.rms_disponiveis(agravo)
        cols = []
        for i, rm in enumerate(rms):
            graph_id = f"corr-rr-all-{i}"
            is_dlnm  = dc.dlnm_disponivel(agravo, rm)
            df_rr    = dc.rr_por_lag_dlnm(agravo, rm) if is_dlnm \
                       else dc.rr_por_lag(agravo, rm, 2010, 2023)
            fig = _fig_rr_lag(df_rr, rm_label=rm)

            # h6 invisível para download_graphs.js capturar o nome da RM
            card = html.Div([
                html.H6(rm, style={"display": "none"}),
                html.Div(
                    [html.I(className="fas fa-chart-line me-2"), rm],
                    className="geo-map-section-header",
                    style={"fontSize": "0.78rem"},
                ),
                html.Div([
                    dcc.Graph(
                        id=graph_id,
                        figure=fig,
                        style={"height": "clamp(240px, 46vw, 320px)"},
                        config={"displayModeBar": False},
                    ),
                    html.Div([
                        dl_btn(graph_id, f"rr_lag_{i}"),
                    ], className="mt-1"),
                ], className="chart-card-body p-2"),
            ], className="chart-card shadow-sm border-0 mb-3")

            cols.append(dbc.Col(card, xs=12, md=6))

        return dbc.Row(cols, className="g-3")
