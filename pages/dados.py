"""
Página de download de dados — GeoCalor.
"""
import io

import pandas as pd
from dash import ctx, dash_table, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

from components import chart_card, info_card

try:
    import data_sih_sim as ds
    _SIH_SIM_OK = True
except Exception:
    _SIH_SIM_OK = False

# ── Constantes ───────────────────────────────────────────────────────────────

_REGIOES = {
    "Norte":        ["Belém", "Manaus", "Porto Velho"],
    "Nordeste":     ["Fortaleza", "Recife", "Salvador"],
    "Centro-Oeste": ["Brasília", "Campo Grande", "Goiânia"],
    "Sudeste":      ["Belo Horizonte", "Rio de Janeiro", "São Paulo"],
    "Sul":          ["Curitiba", "Florianópolis", "Porto Alegre"],
}

_COR_REGIAO = {
    "Norte": "#6ec1a6",
    "Nordeste": "#e63946",
    "Centro-Oeste": "#ff9f1c",
    "Sudeste": "#9b59b6",
    "Sul": "#2b9eb3",
}

# label exibido → nome interno da coluna no DataFrame
_COLUNAS_CLIMA = {
    "Data":                  "index",
    "Cidade":                "cidade",
    "Ano":                   "year",
    "Temp. Máxima (°C)":     "tempMax",
    "Temp. Média (°C)":      "tempMed",
    "Temp. Mínima (°C)":     "tempMin",
    "Umidade Relativa (%)":  "HumidadeMed",
    "EHF":                   "EHF",
    "Onda de Calor":         "isHW",
    "Intensidade do Evento": "HW_Intensity",
    "Duração do Evento (d)": "HW_duration",
    "Amplitude Térmica":     "thermalRange",
    "Anomalia Térmica":      "tempAnom",
}
_COL_INTERNO_LABEL = {v: k for k, v in _COLUNAS_CLIMA.items()}

_CAUSAS = [
    {"label": "Doenças cardiovasculares", "value": "CARDIOVASCULAR"},
    {"label": "Doenças respiratórias",    "value": "RESPIRATORIAS"},
]

_TIPOS_DADO = [
    {"label": "Série mensal",     "value": "serie_mensal"},
    {"label": "Taxa anual",       "value": "taxa_anual"},
    {"label": "Por faixa etária", "value": "faixa_etaria"},
    {"label": "Por sexo e ano",   "value": "sexo_por_ano"},
    {"label": "Por raça/cor",     "value": "raca_cor"},
]

_PREVIEW_ROWS = 100


# ── Utilitários ──────────────────────────────────────────────────────────────

def _cidades_from_regioes(regioes):
    cidades = []
    for r in (regioes or []):
        cidades.extend(_REGIOES.get(r, []))
    return sorted(cidades)


def _prep_clima(df, cidades, ano_min, ano_max):
    """Filtra df climático e retorna com coluna 'Data' no lugar do índice."""
    dff = df.copy()
    if cidades:
        dff = dff[dff["cidade"].isin(cidades)]
    if "year" in dff.columns:
        dff = dff[(dff["year"] >= ano_min) & (dff["year"] <= ano_max)]
    dff = dff.reset_index()
    idx_col = dff.columns[0]          # nome do índice após reset (geralmente 'index')
    dff = dff.rename(columns={idx_col: "Data"})
    if "Data" in dff.columns and hasattr(dff["Data"], "dt"):
        dff["Data"] = dff["Data"].dt.strftime("%Y-%m-%d")
    return dff


def _select_cols(dff, col_labels):
    """Retorna df apenas com as colunas selecionadas, renomeadas para labels legíveis."""
    mapa = {}
    for label in (col_labels or []):
        interno = _COLUNAS_CLIMA.get(label, "")
        if interno == "index":
            interno = "Data"
        if interno in dff.columns:
            mapa[interno] = label
    if not mapa:
        return dff
    inv = {v: k for k, v in _COLUNAS_CLIMA.items()}
    inv["Data"] = "Data"
    return dff[[c for c in mapa]].rename(columns=mapa)


def _to_csv(dff):
    return dff.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")


def _to_excel(dff, sheet_name="Dados"):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        dff.to_excel(writer, index=False, sheet_name=sheet_name)
    return buf.getvalue()


def _get_sihsim(sistema, causa, rms, tipo):
    """Carrega e concatena dados SIH/SIM para as RMs selecionadas."""
    if not _SIH_SIM_OK or not rms:
        return pd.DataFrame()
    fn = getattr(ds, tipo, None)
    if fn is None:
        return pd.DataFrame()
    frames = []
    for rm in rms:
        try:
            if tipo in ("serie_mensal", "taxa_anual", "sexo_por_ano"):
                frames.append(fn(sistema, causa, rm))
            elif tipo in ("faixa_etaria", "raca_cor"):
                frames.append(fn(sistema, causa, rm))
            elif tipo == "serie_mensal_taxa":
                frames.append(fn(sistema, causa, rm))
        except Exception:
            pass
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def _stats_badge(n_total, n_preview, extra=""):
    cor = "#1761a0"
    return html.Div([
        html.Span(
            f"{n_total:,} registros".replace(",", "."),
            className="badge me-2",
            style={"background": cor, "fontSize": "0.8rem", "fontWeight": "600"},
        ),
        html.Span(
            f"Pré-visualização: {min(n_preview, n_total):,} de {n_total:,}".replace(",", "."),
            className="text-muted small",
        ),
        html.Span(f"  {extra}", className="text-muted small ms-2") if extra else None,
    ], className="d-flex align-items-center flex-wrap gap-1 mb-2")


# ── Layout ───────────────────────────────────────────────────────────────────

def layout_dados(app, df, anos):
    ano_min = int(min(anos)) if anos else 1981
    ano_max = int(max(anos)) if anos else 2024
    todas_cidades = sorted([c for cs in _REGIOES.values() for c in cs])

    # ── Tab Climático ────────────────────────────────────────────────────────
    tab_clima = dbc.Tab(
        label="Dados Climáticos",
        tab_id="tab-clima",
        children=[
            chart_card(
                "Filtros e seleção",
                [
                    dbc.Row([
                        # Regiões
                        dbc.Col([
                            html.P("Regiões", className="fw-semibold small mb-2"),
                            html.Div([
                                html.Div([
                                    dbc.Checkbox(
                                        id=f"dados-reg-{reg}",
                                        value=True,
                                        className="me-1",
                                    ),
                                    html.Span(
                                        reg,
                                        style={"color": _COR_REGIAO[reg],
                                               "fontWeight": "600",
                                               "fontSize": "0.85rem"},
                                    ),
                                ], className="d-flex align-items-center mb-2")
                                for reg in _REGIOES
                            ]),
                        ], xs=12, md=3, className="mb-3"),

                        # Cidades
                        dbc.Col([
                            html.P("Cidades", className="fw-semibold small mb-2"),
                            dcc.Dropdown(
                                id="dados-cidades",
                                options=[{"label": c, "value": c} for c in todas_cidades],
                                value=todas_cidades,
                                multi=True,
                                placeholder="Selecione as cidades...",
                                clearable=True,
                                className="small",
                            ),
                        ], xs=12, md=4, className="mb-3"),

                        # Período
                        dbc.Col([
                            html.P(
                                ["Período: ",
                                 html.Span(id="dados-periodo-label",
                                           children=f"{ano_min} – {ano_max}",
                                           className="text-primary fw-semibold")],
                                className="fw-semibold small mb-2",
                            ),
                            dcc.RangeSlider(
                                id="dados-ano-range",
                                min=ano_min, max=ano_max,
                                value=[ano_min, ano_max],
                                marks={
                                    y: str(y)
                                    for y in range(ano_min, ano_max + 1, 5)
                                },
                                step=1,
                                tooltip={"placement": "bottom", "always_visible": False},
                                allowCross=False,
                                className="mt-2",
                            ),
                        ], xs=12, md=5, className="mb-3"),
                    ], className="mb-2"),

                    html.Hr(className="my-2"),

                    dbc.Row([
                        # Variáveis
                        dbc.Col([
                            html.P("Variáveis a exportar", className="fw-semibold small mb-2"),
                            dcc.Checklist(
                                id="dados-colunas",
                                options=[{"label": k, "value": k}
                                         for k in _COLUNAS_CLIMA],
                                value=list(_COLUNAS_CLIMA.keys()),
                                inputStyle={"marginRight": "5px"},
                                labelStyle={
                                    "display": "inline-flex",
                                    "alignItems": "center",
                                    "width": "32%",
                                    "marginBottom": "5px",
                                    "fontSize": "0.82rem",
                                },
                            ),
                        ], xs=12, md=8, className="mb-3"),

                        # Formato + Download
                        dbc.Col([
                            html.P("Formato", className="fw-semibold small mb-2"),
                            dbc.RadioItems(
                                id="dados-formato",
                                options=[
                                    {"label": html.Span(
                                        [html.I(className="fas fa-file-csv me-1"), "CSV"],
                                        className="small"), "value": "csv"},
                                    {"label": html.Span(
                                        [html.I(className="fas fa-file-excel me-1"), "Excel (.xlsx)"],
                                        className="small"), "value": "excel"},
                                ],
                                value="csv",
                                className="mb-3",
                            ),
                            dbc.Button(
                                [html.I(className="fas fa-download me-2"), "Baixar dados"],
                                id="dados-download-btn",
                                color="primary",
                                size="sm",
                                className="w-100",
                            ),
                            html.Div(id="dados-download-info",
                                     className="text-muted small mt-2"),
                        ], xs=12, md=4, className="mb-3"),
                    ]),
                ],
                fa_icon="fas fa-filter",
            ),

            # Stats + Preview
            html.Div(id="dados-stats-clima", className="mb-2"),
            chart_card(
                f"Pré-visualização (primeiros {_PREVIEW_ROWS} registros)",
                [
                    dash_table.DataTable(
                        id="dados-preview-clima",
                        columns=[],
                        data=[],
                        page_size=20,
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        style_table={"overflowX": "auto"},
                        style_header={
                            "backgroundColor": "#eaf1f8",
                            "fontWeight": "700",
                            "fontSize": "0.78rem",
                            "border": "1px solid #ccd6e0",
                            "whiteSpace": "normal",
                        },
                        style_cell={
                            "fontSize": "0.78rem",
                            "padding": "6px 10px",
                            "border": "1px solid #e8eef4",
                            "minWidth": "80px",
                            "maxWidth": "200px",
                            "whiteSpace": "nowrap",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                        },
                        style_data_conditional=[
                            {"if": {"row_index": "odd"},
                             "backgroundColor": "#f7fafd"},
                        ],
                        filter_options={"placeholder_text": "Filtrar..."},
                    ),
                ],
                fa_icon="fas fa-table",
            ),
        ],
    )

    # ── Tab SIH/SIM ──────────────────────────────────────────────────────────
    if _SIH_SIM_OK:
        rms_init = ds.rms_disponiveis("SIH", "CARDIOVASCULAR")
    else:
        rms_init = []

    tab_sihsim = dbc.Tab(
        label="Internações e Óbitos (SIH/SIM)",
        tab_id="tab-sihsim",
        children=[
            chart_card(
                "Filtros e seleção",
                [
                    dbc.Row([
                        # Sistema
                        dbc.Col([
                            html.P("Sistema", className="fw-semibold small mb-2"),
                            dbc.RadioItems(
                                id="dados-sihsim-sistema",
                                options=[
                                    {"label": html.Span(
                                        [html.I(className="fas fa-hospital me-1"),
                                         "SIH — Internações"],
                                        className="small"), "value": "SIH"},
                                    {"label": html.Span(
                                        [html.I(className="fas fa-heartbeat me-1"),
                                         "SIM — Óbitos"],
                                        className="small"), "value": "SIM"},
                                ],
                                value="SIH",
                                className="mb-2",
                            ),
                        ], xs=12, md=3, className="mb-3"),

                        # Causa
                        dbc.Col([
                            html.P("Grupo de causas", className="fw-semibold small mb-2"),
                            dcc.Dropdown(
                                id="dados-sihsim-causa",
                                options=_CAUSAS,
                                value="CARDIOVASCULAR",
                                clearable=False,
                                className="small",
                            ),
                        ], xs=12, md=3, className="mb-3"),

                        # RM
                        dbc.Col([
                            html.P("Região Metropolitana", className="fw-semibold small mb-2"),
                            dcc.Dropdown(
                                id="dados-sihsim-rm",
                                options=[{"label": r, "value": r} for r in rms_init],
                                value=rms_init[:1] if rms_init else [],
                                multi=True,
                                placeholder="Selecione a RM...",
                                className="small",
                            ),
                        ], xs=12, md=4, className="mb-3"),

                        # Tipo
                        dbc.Col([
                            html.P("Tipo de dado", className="fw-semibold small mb-2"),
                            dcc.Dropdown(
                                id="dados-sihsim-tipo",
                                options=_TIPOS_DADO,
                                value="taxa_anual",
                                clearable=False,
                                className="small",
                            ),
                        ], xs=12, md=2, className="mb-3"),
                    ]),

                    html.Hr(className="my-2"),

                    dbc.Row([
                        dbc.Col([
                            html.P("Formato", className="fw-semibold small mb-2"),
                            dbc.RadioItems(
                                id="dados-sihsim-formato",
                                options=[
                                    {"label": html.Span(
                                        [html.I(className="fas fa-file-csv me-1"), "CSV"],
                                        className="small"), "value": "csv"},
                                    {"label": html.Span(
                                        [html.I(className="fas fa-file-excel me-1"), "Excel (.xlsx)"],
                                        className="small"), "value": "excel"},
                                ],
                                value="csv",
                                inline=True,
                                className="mb-3",
                            ),
                        ], xs=12, md=8),
                        dbc.Col([
                            dbc.Button(
                                [html.I(className="fas fa-download me-2"), "Baixar dados"],
                                id="dados-sihsim-download-btn",
                                color="primary",
                                size="sm",
                                className="w-100 mt-4",
                            ),
                        ], xs=12, md=4),
                    ]),

                    html.Div(
                        [
                            html.I(className="fas fa-info-circle me-1 text-muted"),
                            html.Span(
                                "Os dados SIH/SIM são disponibilizados em formato agregado "
                                "(contagens e taxas), não em nível individual de paciente.",
                                className="text-muted small",
                            ),
                        ],
                        className="mt-2",
                    ),
                ],
                fa_icon="fas fa-filter",
            ),

            html.Div(id="dados-stats-sihsim", className="mb-2"),
            chart_card(
                f"Pré-visualização (primeiros {_PREVIEW_ROWS} registros)",
                [
                    dash_table.DataTable(
                        id="dados-preview-sihsim",
                        columns=[],
                        data=[],
                        page_size=20,
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        style_table={"overflowX": "auto"},
                        style_header={
                            "backgroundColor": "#eaf1f8",
                            "fontWeight": "700",
                            "fontSize": "0.78rem",
                            "border": "1px solid #ccd6e0",
                        },
                        style_cell={
                            "fontSize": "0.78rem",
                            "padding": "6px 10px",
                            "border": "1px solid #e8eef4",
                            "minWidth": "80px",
                            "maxWidth": "220px",
                            "whiteSpace": "nowrap",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                        },
                        style_data_conditional=[
                            {"if": {"row_index": "odd"},
                             "backgroundColor": "#f7fafd"},
                        ],
                    ),
                ],
                fa_icon="fas fa-table",
            ),
        ] if _SIH_SIM_OK else [
            info_card(
                "Dados não disponíveis",
                html.P(
                    "Execute prepare_sih_sim_data.py para gerar os dados SIH/SIM "
                    "antes de usar esta seção.",
                    className="mb-0 text-muted",
                ),
                fa_icon="fas fa-exclamation-triangle",
            )
        ],
    )

    return dbc.Container([
        dbc.Row(dbc.Col([
            html.Img(src=app.get_asset_url("geocalor.png"), className="logo-img"),
            html.H2("Dados", className="text-center my-4"),
        ], width=12), className="text-center mb-2"),

        info_card(
            "Sobre os dados",
            html.Div([
                html.P(
                    "Faça o download dos dados utilizados no dashboard GeoCalor. "
                    "Escolha o conjunto de dados, filtre por região, cidade e período, "
                    "selecione as variáveis desejadas e exporte em CSV ou Excel.",
                    className="mb-1 text-muted",
                ),
                html.P(
                    "Dados climáticos: 1981–2024 | 15 cidades em 5 regiões do Brasil. "
                    "Dados SIH/SIM: internações e óbitos por causas cardiovasculares e respiratórias, "
                    "por Região Metropolitana.",
                    className="mb-0 text-muted small",
                ),
            ]),
            fa_icon="fas fa-database",
        ),

        html.Hr(className="my-3"),

        dbc.Tabs(
            [tab_clima, tab_sihsim],
            id="dados-tabs",
            active_tab="tab-clima",
            className="mb-4",
        ),

        dcc.Download(id="dados-download-clima"),
        dcc.Download(id="dados-download-sihsim"),

    ], fluid=True, className="py-4")


# ── Callbacks ────────────────────────────────────────────────────────────────

def register_callbacks_dados(app, df):

    # 1. Atualiza as opções e valor do dropdown de cidades conforme regiões selecionadas
    @app.callback(
        Output("dados-cidades", "options"),
        Output("dados-cidades", "value"),
        [Input(f"dados-reg-{reg}", "value") for reg in _REGIOES],
    )
    def _update_cidades(*vals):
        regioes_sel = [reg for reg, v in zip(_REGIOES.keys(), vals) if v]
        cidades = _cidades_from_regioes(regioes_sel)
        opts = [{"label": c, "value": c} for c in cidades]
        return opts, cidades

    # 2. Atualiza label do período
    app.clientside_callback(
        "function(v) { return v[0] + ' – ' + v[1]; }",
        Output("dados-periodo-label", "children"),
        Input("dados-ano-range", "value"),
    )

    # 3. Preview dos dados climáticos
    @app.callback(
        Output("dados-preview-clima", "columns"),
        Output("dados-preview-clima", "data"),
        Output("dados-stats-clima", "children"),
        Input("dados-cidades", "value"),
        Input("dados-ano-range", "value"),
        Input("dados-colunas", "value"),
    )
    def _update_preview_clima(cidades, ano_range, col_labels):
        if df is None or df.empty:
            return [], [], html.Div()
        ano_min, ano_max = (ano_range or [1981, 2024])
        dff = _prep_clima(df, cidades, int(ano_min), int(ano_max))
        dff_sel = _select_cols(dff, col_labels)
        n_total = len(dff_sel)
        preview = dff_sel.head(_PREVIEW_ROWS)
        cols = [{"name": c, "id": c} for c in preview.columns]
        data = preview.to_dict("records")
        n_cidades = dff["Cidade"].nunique() if "Cidade" in dff.columns else 0
        extra = f"| {n_cidades} cidade(s)"
        stats = _stats_badge(n_total, _PREVIEW_ROWS, extra)
        return cols, data, stats

    # 4. Download dos dados climáticos
    @app.callback(
        Output("dados-download-clima", "data"),
        Output("dados-download-info", "children"),
        Input("dados-download-btn", "n_clicks"),
        State("dados-cidades", "value"),
        State("dados-ano-range", "value"),
        State("dados-colunas", "value"),
        State("dados-formato", "value"),
        prevent_initial_call=True,
    )
    def _download_clima(n, cidades, ano_range, col_labels, fmt):
        if not n or df is None or df.empty:
            return None, ""
        ano_min, ano_max = (ano_range or [1981, 2024])
        dff = _prep_clima(df, cidades, int(ano_min), int(ano_max))
        dff_sel = _select_cols(dff, col_labels)
        nome = f"geocalor_climatico_{ano_min}_{ano_max}"
        info = f"{len(dff_sel):,} registros exportados.".replace(",", ".")
        if fmt == "excel":
            return dcc.send_bytes(_to_excel(dff_sel, "Dados Climáticos"), f"{nome}.xlsx"), info
        return dcc.send_bytes(_to_csv(dff_sel), f"{nome}.csv"), info

    if not _SIH_SIM_OK:
        return

    # 5. Atualiza opções de RM quando sistema/causa mudam
    @app.callback(
        Output("dados-sihsim-rm", "options"),
        Output("dados-sihsim-rm", "value"),
        Input("dados-sihsim-sistema", "value"),
        Input("dados-sihsim-causa",   "value"),
    )
    def _update_rms(sistema, causa):
        rms = ds.rms_disponiveis(sistema or "SIH", causa or "CARDIOVASCULAR")
        opts = [{"label": r, "value": r} for r in rms]
        return opts, rms[:1]

    # 6. Preview dos dados SIH/SIM
    @app.callback(
        Output("dados-preview-sihsim", "columns"),
        Output("dados-preview-sihsim", "data"),
        Output("dados-stats-sihsim", "children"),
        Input("dados-sihsim-sistema", "value"),
        Input("dados-sihsim-causa",   "value"),
        Input("dados-sihsim-rm",      "value"),
        Input("dados-sihsim-tipo",    "value"),
    )
    def _update_preview_sihsim(sistema, causa, rms, tipo):
        dff = _get_sihsim(sistema or "SIH", causa or "CARDIOVASCULAR",
                          rms or [], tipo or "taxa_anual")
        if dff.empty:
            return [], [], html.Div(
                "Nenhum dado disponível para a seleção.",
                className="text-muted small",
            )
        # Arredonda floats para exibição
        dff = dff.copy()
        for col in dff.select_dtypes("float").columns:
            dff[col] = dff[col].round(3)
        n_total = len(dff)
        preview = dff.head(_PREVIEW_ROWS)
        cols = [{"name": c, "id": c} for c in preview.columns]
        data = preview.to_dict("records")
        stats = _stats_badge(n_total, _PREVIEW_ROWS)
        return cols, data, stats

    # 7. Download dos dados SIH/SIM
    @app.callback(
        Output("dados-sihsim-download", "data"),
        Input("dados-sihsim-download-btn", "n_clicks"),
        State("dados-sihsim-sistema", "value"),
        State("dados-sihsim-causa",   "value"),
        State("dados-sihsim-rm",      "value"),
        State("dados-sihsim-tipo",    "value"),
        State("dados-sihsim-formato", "value"),
        prevent_initial_call=True,
    )
    def _download_sihsim(n, sistema, causa, rms, tipo, fmt):
        if not n:
            return None
        dff = _get_sihsim(sistema or "SIH", causa or "CARDIOVASCULAR",
                          rms or [], tipo or "taxa_anual")
        if dff.empty:
            return None
        sistema_lb = sistema or "SIH"
        causa_lb   = (causa or "CARDIOVASCULAR").lower()
        tipo_lb    = tipo or "taxa_anual"
        nome = f"geocalor_{sistema_lb.lower()}_{causa_lb}_{tipo_lb}"
        if fmt == "excel":
            return dcc.send_bytes(_to_excel(dff, sistema_lb), f"{nome}.xlsx")
        return dcc.send_bytes(_to_csv(dff), f"{nome}.csv")
