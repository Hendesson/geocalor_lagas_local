"""
Mortalidade por Ondas de Calor — Razão Observado/Esperado e Fatores de Risco.
Fonte: ondas_de_calor_OER.xlsx, ResultadosFatoresDeRisco_dashboard.xlsx,
       tabela_resumo_ondas_de_calor_mortalidade.xlsx
"""
from dash import dcc, html, Input, Output, State, dash_table, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd

import data_mortalidade as dm
from components import chart_card, info_card, dd, dl_btn


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


# ── Figura OER × tempo ────────────────────────────────────────────────────────

def _fig_oer(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _EMPTY

    def _hover(sub: pd.DataFrame) -> list:
        rows = []
        for _, r in sub.iterrows():
            fim = r["fim_onda"].strftime("%d/%m/%Y") if pd.notna(r.get("fim_onda")) else "?"
            dur = int(r["duracao_dias"]) if pd.notna(r.get("duracao_dias")) else "?"
            pct = f"{r['excesso_percentual']:+.1f}%" if pd.notna(r.get("excesso_percentual")) else "?"
            obs = f"{int(r['OBITOS_OBS'])}" if pd.notna(r.get("OBITOS_OBS")) else "?"
            esp = f"{r['OBITOS_ESP']:.1f}" if pd.notna(r.get("OBITOS_ESP")) else "?"
            ic_l = f"{r['IC_95_inf']:.3f}" if pd.notna(r.get("IC_95_inf")) else "?"
            ic_h = f"{r['IC_95_sup']:.3f}" if pd.notna(r.get("IC_95_sup")) else "?"
            rows.append(
                f"Fim: {fim} · Duração: {dur} dias<br>"
                f"O/E: {r['OER']:.3f} [IC 95%: {ic_l} – {ic_h}]<br>"
                f"Excesso: {pct} · Obs: {obs} | Esp: {esp}"
            )
        return rows

    sig  = df["OER_isSIG"].astype(bool)
    nsig = df[~sig]
    ssig = df[sig]

    # Faixa Y automática com margem
    y_vals = df["OER"].dropna()
    y_min = max(0, y_vals.min() - 0.15)
    y_max = y_vals.max() + 0.15

    fig = go.Figure()

    for sub, color, name in [
        (nsig, "gray",    "Não Significativo"),
        (ssig, "red",     "Significativo"),
    ]:
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["inicio_onda"],
            y=sub["OER"],
            mode="markers",
            marker=dict(
                color=color,
                size=9,
                opacity=0.5,
                line=dict(width=0.5, color="black"),
            ),
            name=name,
            customdata=[[t] for t in _hover(sub)],
            hovertemplate="<b>%{x|%d/%m/%Y}</b><br>%{customdata[0]}<extra></extra>",
        ))

    fig.add_hline(y=1.0, line_dash="dash", line_color="black", line_width=1.2)

    layout = {
        **_LAYOUT_BASE,
        "legend": dict(
            title="Significância Estatística (IC 95%)",
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
        ),
        "xaxis": dict(title="", gridcolor="#eee",
                      range=["1999-07-01", "2024-01-01"]),
        "yaxis": dict(title="O/E ratio", gridcolor="#eee",
                      zeroline=False, range=[y_min, y_max]),
    }
    fig.update_layout(**layout)
    return fig


# ── Figura Fatores de Risco ───────────────────────────────────────────────────

_FATORES_MAP = [
    ("Duração",              "Duração alta",                   "duracao_sig"),
    ("Amplitude Térmica",    "Amplitude térmica alta",          "amplitude_sig"),
    ("Umidade",              "Umidade alta",                    "umidade_sig"),
    ("Anomalia de Temp.",    "Anomailia de temperatura alta",   "anomalia_sig"),
    ("Dias p/ Última OC",   "Distância para última onda",      "distancia_sig"),
    ("EHF",                  "EHF alto",                        "ehf_sig"),
]


def _fig_fatores(row_df: pd.DataFrame) -> go.Figure:
    if row_df.empty:
        return _EMPTY

    row = row_df.iloc[0]
    labels, values, colors, hovers = [], [], [], []

    for label, col, sig_col in _FATORES_MAP:
        val = row.get(col)
        sig = str(row.get(sig_col, "N")).strip().upper()
        if val is None or (isinstance(val, float) and pd.isna(val)):
            continue
        labels.append(label)
        values.append(float(val))
        sig_txt = "Significativo" if sig == "S" else "Não significativo"
        hovers.append(f"RP = {float(val):.3f}<br>{sig_txt}")
        if sig == "S":
            colors.append("#e63946" if float(val) > 1 else "#1761a0")
        else:
            colors.append("#aaaaaa")

    if not values:
        return _EMPTY

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker_color=colors,
        customdata=[[h] for h in hovers],
        hovertemplate="%{y}<br>%{customdata[0]}<extra></extra>",
        width=0.55,
    ))

    fig.add_vline(x=1, line_dash="dash", line_color="#333", line_width=1.5,
                  annotation_text="RP = 1",
                  annotation_position="top right",
                  annotation_font=dict(size=11))

    x_max = max(values + [1.0]) * 1.25 if values else 4
    x_min = min(values + [1.0]) * 0.8  if values else 0

    layout = {**_LAYOUT_BASE,
              "margin": dict(l=160, r=40, t=50, b=55),
              "xaxis": dict(title="Razão de Prevalência (RP)", gridcolor="#eee",
                            range=[max(0, x_min), x_max]),
              "yaxis": dict(gridcolor="#eee", autorange="reversed")}
    fig.update_layout(**layout)
    return fig


# ── Tabela resumo (HTML estático — todas as RMs) ──────────────────────────────

def _build_tabela() -> html.Div:
    df = dm.tabela_resumo()
    if df.empty:
        return html.P("Dados não disponíveis.", className="text-muted small")

    ncols = min(len(df.columns), 8)
    headers_short = [
        "Região Metropolitana",
        "Nº de Ondas",
        "Ondas c/ Excesso",
        "Ondas c/ Baixa Mort.",
        "% Excesso",
        "% Baixa",
        "Óbitos Atribuíveis",
        "Óbitos / 1M hab.",
    ][:ncols]

    def _br(val, dec=1):
        """Formata número no padrão brasileiro: ponto milhar, vírgula decimal."""
        s = f"{float(val):,.{dec}f}"          # "30,421.9"
        return s.replace(".", "X").replace(",", ".").replace("X", ",")  # "30.421,9"

    def _fmt(val, col_idx):
        try:
            if pd.isna(val):
                return "—"
        except Exception:
            pass
        if val is None:
            return "—"
        if col_idx in (4, 5):
            try:
                return f"{float(val):.1f}%".replace(".", ",")
            except Exception:
                return str(val)
        if col_idx in (6, 7):
            try:
                return _br(val)
            except Exception:
                return str(val)
        if col_idx in (1, 2, 3):
            try:
                return f"{int(float(val)):,}".replace(",", ".")
            except Exception:
                return str(val)
        return str(val)

    rows = []
    for _, r in df.iterrows():
        rm_raw = r.iloc[0]
        # Detecta linha TOTAL: string "TOTAL"/"TOTAIS" OU célula NaN do Excel
        try:
            nan_cell = pd.isna(rm_raw)
        except Exception:
            nan_cell = False
        is_total = nan_cell or str(rm_raw).strip().upper() in ("TOTAL", "TOTAIS")
        rm_label = "TOTAL" if is_total else str(rm_raw).strip()

        tds = [html.Td(rm_label,
                       style={"fontWeight": "bold"} if is_total else {})]
        for i in range(1, ncols):
            tds.append(html.Td(
                _fmt(r.iloc[i], i),
                style={"fontWeight": "bold"} if is_total else {},
                className="text-end",
            ))
        rows.append(html.Tr(
            tds,
            style={"background": "#ddeef8", "borderTop": "2px solid #1761a0"}
            if is_total else {},
        ))

    return html.Div([
        html.Div([
            html.Button(
                [html.I(className="fas fa-download me-1"), "Baixar tabela (CSV)"],
                id="mort-tabela-btn",
                className="btn btn-outline-secondary btn-sm mb-3",
                n_clicks=0,
            ),
            dcc.Download(id="mort-tabela-download"),
        ]),
        html.Div(style={"overflowX": "auto"}, children=[
            html.Table(
                className="table table-sm table-hover table-bordered mb-0",
                style={"fontSize": "0.82rem", "minWidth": "700px"},
                children=[
                    html.Thead(html.Tr([
                        html.Th(h,
                                className="text-end" if i > 0 else "",
                                style={"background": "#1761a0", "color": "white",
                                       "whiteSpace": "nowrap", "fontSize": "0.78rem"})
                        for i, h in enumerate(headers_short)
                    ])),
                    html.Tbody(rows),
                ],
            )
        ]),
        html.P(
            "* Curitiba: proporções quase iguais de ondas com excesso (47,6%) e com "
            "baixa mortalidade (50,0%), resultando em efeito líquido muito pequeno — "
            "interprete com cautela.",
            className="chart-note text-muted small mt-2",
        ),
    ])


# ── Nota técnica ──────────────────────────────────────────────────────────────

def _nota_tecnica_card() -> dbc.Card:
    return dbc.Card([
        dbc.CardBody([
            html.H5([html.I(className="fas fa-file-alt me-2"), "Nota Técnica"],
                    className="card-title mb-3"),
            html.Div([
                html.Div([
                    html.Strong("Excesso de mortalidade por onda (O/E)"),
                    html.P(
                        "A razão O/E de cada onda é calculada dividindo a mortalidade "
                        "observada durante o evento pela média do mesmo período nos demais "
                        "anos (excluindo anos que também tiveram onda no período). "
                        "IC 95% identifica ondas com excesso ou déficit significativo.",
                        className="small text-muted mb-2",
                    ),
                ]),
                html.Div([
                    html.Strong("Fatores de risco (Razão de Prevalência)"),
                    html.P(
                        "Para cada RM, indicadores climáticos de cada onda são "
                        "dicotomizados pela mediana (alto/baixo). Tabelas 2×2 geram "
                        "razões de prevalência + IC 95%. RP > 1 significativa = fator de "
                        "risco; RP < 1 significativa = fator protetor.",
                        className="small text-muted mb-3",
                    ),
                ]),
            ]),
            html.Div([
                html.A(
                    [html.I(className="fas fa-external-link-alt me-1"), " Visualizar completo"],
                    href="/nota-tecnica-mortalidade", target="_blank",
                    className="btn btn-info btn-sm me-2",
                ),
                html.A(
                    [html.I(className="fas fa-print me-1"), " Baixar PDF"],
                    href="/nota-tecnica-mortalidade", target="_blank",
                    className="btn btn-outline-secondary btn-sm",
                    title="Ctrl+P para salvar como PDF",
                ),
            ], className="d-flex flex-wrap gap-2"),
        ])
    ], className="nota-tecnica-card mb-3")


# ── Layout ────────────────────────────────────────────────────────────────────

def layout_mortalidade(app):
    cidades = dm.cidades_disponiveis()
    default = "Brasília" if "Brasília" in cidades else (cidades[0] if cidades else None)
    opts = [{"label": c, "value": c} for c in cidades]

    return dbc.Container([
        # ── Cabeçalho ─────────────────────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                html.Img(src=app.get_asset_url("geocalor.png"), className="logo-img"),
                html.H2("Mortalidade associada a ocorrência de ondas de calor",
                        className="text-center my-4"),
            ], width=12),
        ], className="text-center"),

        # ── Texto introdutório ────────────────────────────────────────────────
        info_card(
            "",
            html.P(
                "Foi investigado o impacto que cada onda de calor individual teve na "
                "mortalidade através do cálculo do índice de mortalidade esperada e "
                "observada de cada evento somando os óbitos por doenças respiratórias "
                "e cardiovasculares.",
                className="mb-0 text-muted small",
            ),
            fa_icon="fas fa-heartbeat",
        ),

        dcc.Store(id="mort-modo", data="single"),

        # ── Filtro ────────────────────────────────────────────────────────────
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(
                        dd("mort-cidade", opts, default, label="Região Metropolitana"),
                        xs=12, md=5,
                    ),
                    dbc.Col([
                        html.Label("\u00a0", className="filter-label d-block mb-1"),
                        html.Button(
                            [html.I(className="fas fa-th me-2"), "Ver todas as RMs"],
                            id="mort-all-btn",
                            className="btn btn-outline-primary fw-bold w-100",
                            n_clicks=0,
                        ),
                    ], xs=12, md=3),
                ], className="g-2 align-items-end"),
            ])
        ], className="shadow-sm border-0 mb-4"),

        # ── Texto antes do gráfico OER ────────────────────────────────────────
        info_card(
            "",
            html.P(
                "Dentre todas as ondas de calor que aconteceram, algumas mostraram "
                "aumento de mortalidade significativo e outras apresentaram diminuição "
                "significativa na mortalidade.",
                className="mb-0 text-muted small",
            ),
            fa_icon="fas fa-chart-line",
        ),

        # ── Vista única ───────────────────────────────────────────────────────
        html.Div(id="mort-single-view", children=[
            chart_card("Razão Observado/Esperado (O/E) por Onda de Calor", [
                dcc.Graph(
                    id="mort-oer-graph",
                    style={"height": "clamp(300px, 55vw, 480px)"},
                    config={"displayModeBar": False},
                ),
                html.Div(id="mort-oer-note"),
                dl_btn("mort-oer-graph", "oer_por_onda"),
            ], fa_icon="fas fa-chart-line"),
        ]),

        # ── Vista todas as RMs ────────────────────────────────────────────────
        html.Div(id="mort-all-view", style={"display": "none"}, children=[
            dbc.Row([
                dbc.Col([
                    html.Button(
                        [html.I(className="fas fa-download me-2"), "Baixar todos (PNG)"],
                        className="btn btn-outline-secondary btn-sm mb-3",
                        **{
                            "data-mapa-download": "mort-all-container",
                            "data-mapa-filename": "oer_todas_rms",
                        },
                    ),
                ], xs=12),
            ]),
            html.Div(id="mort-all-container"),
        ]),

        # ── Texto antes dos fatores de risco ──────────────────────────────────
        info_card(
            "",
            html.P(
                "A partir desse mapeamento, foram testados fatores de risco climáticos "
                "para a ocorrência de excesso de mortalidade nas ondas de calor a partir "
                "de razões de prevalência. Valores significativos acima de 1 indicam "
                "associação direta enquanto valores abaixo de 1 representam relação inversa.",
                className="mb-0 text-muted small",
            ),
            fa_icon="fas fa-exclamation-triangle",
        ),

        # ── Gráfico Fatores de Risco ──────────────────────────────────────────
        chart_card("Fatores de risco para excesso de mortalidade em ondas de calor", [
            dcc.Graph(
                id="mort-fatores-graph",
                style={"height": "clamp(260px, 50vw, 380px)"},
                config={"displayModeBar": False},
            ),
            chart_note(
                "Vermelho = associação significativa (RP > 1, fator de risco). "
                "Azul = associação significativa (RP < 1, fator protetor). "
                "Cinza = não significativo. Referência: RP = 1."
            ),
            dl_btn("mort-fatores-graph", "fatores_risco_mortalidade"),
        ], fa_icon="fas fa-exclamation-triangle"),

        # ── Tabela resumo ─────────────────────────────────────────────────────
        html.H5("Síntese dos resultados para todas as áreas estudadas",
                className="mt-4 mb-3 fw-bold", style={"color": "#1761a0"}),

        chart_card("", [
            _build_tabela(),
        ], fa_icon="fas fa-table"),

        # ── Nota técnica ──────────────────────────────────────────────────────
        _nota_tecnica_card(),

    ], fluid=True)


# ── Callbacks ─────────────────────────────────────────────────────────────────

def register_callbacks_mortalidade(app):

    @app.callback(
        Output("mort-oer-graph", "figure"),
        Output("mort-oer-note", "children"),
        Input("mort-cidade", "value"),
    )
    def _update_oer(cidade):
        if not cidade:
            return _EMPTY, ""
        df = dm.oer_por_cidade(cidade)
        n_sig = int(df["OER_isSIG"].sum()) if not df.empty else 0
        n_exc = int((df["OER_isSIG"] & (df["OER"] >= 1)).sum()) if not df.empty else 0
        note = chart_note(
            f"{len(df)} ondas analisadas · {n_sig} significativas "
            f"({n_exc} com excesso, {n_sig - n_exc} com déficit). "
            "IC 95% calculado com base na variabilidade histórica do mesmo período."
        )
        return _fig_oer(df), note

    @app.callback(
        Output("mort-fatores-graph", "figure"),
        Input("mort-cidade", "value"),
    )
    def _update_fatores(cidade):
        if not cidade:
            return _EMPTY
        row_df = dm.fatores_risco_cidade(cidade)
        return _fig_fatores(row_df)

    # Toggle single ↔ all
    @app.callback(
        Output("mort-modo",        "data"),
        Output("mort-all-btn",     "className"),
        Output("mort-single-view", "style"),
        Output("mort-all-view",    "style"),
        Output("mort-cidade",      "disabled"),
        Input("mort-all-btn",      "n_clicks"),
        State("mort-modo",         "data"),
        prevent_initial_call=True,
    )
    def _toggle_modo(n, modo_atual):
        novo = "all" if modo_atual != "all" else "single"
        btn_cls = ("btn btn-primary fw-bold w-100" if novo == "all"
                   else "btn btn-outline-primary fw-bold w-100")
        show_single = {} if novo == "single" else {"display": "none"}
        show_all    = {} if novo == "all"    else {"display": "none"}
        return novo, btn_cls, show_single, show_all, novo == "all"

    # Grade todas as RMs
    @app.callback(
        Output("mort-all-container", "children"),
        Input("mort-modo",           "data"),
    )
    def _update_all(modo):
        if modo != "all":
            return []
        cidades = dm.cidades_disponiveis()
        cols = []
        for i, cidade in enumerate(cidades):
            graph_id = f"mort-oer-all-{i}"
            df = dm.oer_por_cidade(cidade)
            fig = _fig_oer(df)
            card = html.Div([
                html.H6(cidade, style={"display": "none"}),
                html.Div(
                    [html.I(className="fas fa-chart-line me-2"), cidade],
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
                    html.Div(dl_btn(graph_id, f"oer_{i}"), className="mt-1"),
                ], className="chart-card-body p-2"),
            ], className="chart-card shadow-sm border-0 mb-3")
            cols.append(dbc.Col(card, xs=12, md=6))
        return dbc.Row(cols, className="g-3")

    @app.callback(
        Output("mort-tabela-download", "data"),
        Input("mort-tabela-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def _download_tabela(n):
        import io
        df = dm.tabela_resumo().copy()
        # Nomear linha TOTAL
        try:
            import pandas as _pd
            mask = df.iloc[:, 0].apply(lambda v: bool(_pd.isna(v)))
            df.iloc[mask.values, 0] = "TOTAL"
        except Exception:
            pass
        buf = io.StringIO()
        df.to_csv(buf, index=False, sep=";", decimal=",", encoding="utf-8-sig")
        return dcc.send_bytes(buf.getvalue().encode("utf-8-sig"),
                              "resumo_mortalidade_oc.csv")

