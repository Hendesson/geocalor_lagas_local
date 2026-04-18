"""
Página: Sistema de Informações SIH/SIM
Internações hospitalares (SIH) e óbitos (SIM) por doenças cardiovasculares e respiratórias
nas Regiões Metropolitanas brasileiras.
"""
import logging

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html
import dash_bootstrap_components as dbc

from components import chart_card, dd, dl_btn
from config import PRIMARY, TEAL, GREEN, ORANGE, RED, DARK_RED, WHITE, LAYOUT_BASE
import data_sih_sim as ds

logger = logging.getLogger(__name__)

# Cache de nomes de município por objeto GeoJSON (evita re-parse por callback)
_geojson_name_cache: dict = {}


def _nota(texto: str) -> html.P:
    """Descrição informativa abaixo de um gráfico."""
    return html.P(texto, className="text-muted small mt-2 mb-0",
                  style={"fontStyle": "italic"})


SISTEMA_OPTS = [
    {"label": "SIH — Internações hospitalares", "value": "SIH"},
    {"label": "SIM — Óbitos",                   "value": "SIM"},
]
CAUSA_OPTS = [
    {"label": "Doenças cardiovasculares", "value": "CARDIOVASCULAR"},
    {"label": "Doenças respiratórias",    "value": "RESPIRATORIAS"},
]

_SISTEMA_DEFAULT = "SIH"
_CAUSA_DEFAULT   = "CARDIOVASCULAR"


# ── figuras auxiliares ──────────────────────────────────────────────────────

def _empty(msg: str = "Sem dados disponíveis", height: int = 300) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        **{**LAYOUT_BASE, "height": height},
        annotations=[dict(
            text=msg, x=0.5, y=0.5, xref="paper", yref="paper",
            showarrow=False, font=dict(size=13, color="#888"),
        )],
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig


def _base(fig: go.Figure, height: int = 320) -> go.Figure:
    fig.update_layout(**{**LAYOUT_BASE, "height": height})
    return fig


# ── layout ──────────────────────────────────────────────────────────────────

def layout_sih_sim(app) -> dbc.Container:
    _rms_init  = ds.rms_disponiveis(_SISTEMA_DEFAULT, _CAUSA_DEFAULT)
    _rm_init   = _rms_init[0] if _rms_init else None
    _anos_init = ds.anos_disponiveis(_SISTEMA_DEFAULT, _CAUSA_DEFAULT, _rm_init) if _rm_init else []
    _ano_init  = _anos_init[-1] if _anos_init else None
    _anos_opts = [{"label": str(a), "value": a} for a in _anos_init]

    return dbc.Container(
        [
            # ── Título ────────────────────────────────────────────────────
            dbc.Row(dbc.Col(
                html.H2("Perfil epidemiológico das Regiões Metropolitanas", className="text-center my-4"),
                width=12,
            )),

            # ── Filtros ───────────────────────────────────────────────────
            dbc.Card(
                [
                    html.Div(
                        [html.I(className="fas fa-filter me-2"), "Filtros"],
                        className="geo-map-section-header",
                    ),
                    dbc.CardBody(
                        dbc.Row(
                            [
                                dbc.Col(dd("sihsim-sistema", SISTEMA_OPTS, _SISTEMA_DEFAULT,
                                           label="Sistema"),                xs=12, md=4),
                                dbc.Col(dd("sihsim-causa",   CAUSA_OPTS,   _CAUSA_DEFAULT,
                                           label="Grupo de causas"),        xs=12, md=4),
                                dbc.Col(dd("sihsim-rm",
                                           [{"label": r, "value": r} for r in _rms_init],
                                           _rm_init, label="Região Metropolitana"), xs=12, md=4),
                            ],
                            className="g-3",
                        )
                    ),
                ],
                className="shadow-sm border-0 mb-4",
            ),

            # ── Abas ─────────────────────────────────────────────────────
            html.Div(
                [
                    html.I(className="fas fa-chart-bar me-2"),
                    "Explorar dados — escolha uma visualização abaixo",
                ],
                className="sihsim-section-banner mb-0",
            ),
            dbc.Tabs(
                [
                    dbc.Tab(
                        _tab_infograficos(),
                        label="Infográficos",
                        label_style={"fontWeight": "700"},
                        tab_id="sihsim-tab-info",
                    ),
                    dbc.Tab(
                        _tab_mapa(_anos_opts, _ano_init),
                        label="Mapa Coroplético",
                        label_style={"fontWeight": "700"},
                        tab_id="sihsim-tab-mapa",
                    ),
                ],
                id="sihsim-tabs",
                active_tab="sihsim-tab-info",
                className="mb-4",
                style={"borderTop": "3px solid #1761a0"},
            ),

            # ── Nota Técnica ──────────────────────────────────────────────
            dbc.Card(
                dbc.CardBody([
                    html.H5([html.I(className="fas fa-file-alt me-2"), "Nota Técnica"],
                            className="card-title mb-3"),
                    html.P(
                        "Dados do Sistema de Informações Hospitalares (SIH) e do "
                        "Sistema de Informações sobre Mortalidade (SIM), "
                        "disponibilizados pelo DATASUS/MS. "
                        "Cobre o período de 2010 a 2022 (SIH) e 2010 a 2023 (SIM) "
                        "para 15 Regiões Metropolitanas brasileiras. "
                        "Causas classificadas pelo CID-10: doenças cardiovasculares "
                        "(Cap. IX, I00–I99) e respiratórias (Cap. X, J00–J99). "
                        "As taxas são calculadas por 1.000 habitantes com estimativas "
                        "populacionais do IBGE.",
                        className="card-text text-muted small mb-3",
                    ),
                    html.Div([
                        html.A(
                            [html.I(className="fas fa-external-link-alt me-1"), " Visualizar"],
                            href="/nota-tecnica-sih-sim",
                            target="_blank",
                            className="btn btn-info btn-sm me-2",
                        ),
                        html.A(
                            [html.I(className="fas fa-print me-1"), " Baixar PDF"],
                            href="/nota-tecnica-sih-sim",
                            target="_blank",
                            className="btn btn-outline-secondary btn-sm",
                            title="Abrirá em nova aba — use Ctrl+P para salvar como PDF",
                        ),
                    ], className="d-flex flex-wrap gap-2"),
                ]),
                className="mt-2 mb-4 shadow-sm border-0",
            ),

            html.Div(style={"height": "40px"}),
        ],
        fluid=True,
        className="py-3 pb-5",
    )


def _tab_infograficos() -> dbc.Container:
    return dbc.Container(
        [
            # Linha 1: específico 1 | específico 2 | raça/cor
            dbc.Row(
                [
                    dbc.Col(_dyn_card("sihsim-g1-title", "sihsim-g1", "fas fa-hospital",
                                     "sihsim-g1-note"),
                            xs=12, md=4, className="mb-3"),
                    dbc.Col(_dyn_card("sihsim-g2-title", "sihsim-g2", "fas fa-procedures",
                                     "sihsim-g2-note"),
                            xs=12, md=4, className="mb-3"),
                    dbc.Col(chart_card("Raça/cor",
                                       [dcc.Loading(dcc.Graph(id="sihsim-g3"), type="circle"),
                                        _nota("Distribuição por raça/cor autodeclarada, "
                                              "conforme classificação IBGE/DATASUS."),
                                        dl_btn("sihsim-g3", "raca_cor")],
                                       fa_icon="fas fa-users"),
                            xs=12, md=4, className="mb-3"),
                ],
                className="align-items-stretch",
            ),

            # Linha 2: mapa de calor temporal (ano × mês)
            dbc.Row(dbc.Col(
                chart_card(
                    "Sazonalidade mensal — mapa de calor (ano × mês)",
                    [dcc.Loading(
                        dcc.Graph(id="sihsim-g4", style={"height": "400px"}),
                        type="circle",
                    ),
                     _nota("Contagem absoluta de internações/óbitos por mês e ano. "
                           "Cores mais escuras = maior volume. Identifica sazonalidade "
                           "(ex.: picos respiratórios no inverno) e tendências de longo prazo. "
                           "Valores são contagens brutas, não taxas populacionais."),
                     dl_btn("sihsim-g4", "sazonalidade_mensal")],
                    fa_icon="fas fa-th",
                ),
                width=12, className="mb-3",
            )),

            # Linha 3: taxa anual | contagem por sexo
            dbc.Row(
                [
                    dbc.Col(chart_card("Taxa anual por 1.000 hab.",
                                       [dcc.Loading(dcc.Graph(id="sihsim-g5"), type="circle"),
                                        _nota("Taxa anual ajustada pela população da RM. "
                                              "Permite comparar RMs de tamanhos diferentes e "
                                              "identificar tendências independente do crescimento "
                                              "populacional."),
                                        dl_btn("sihsim-g5", "taxa_anual")],
                                       fa_icon="fas fa-chart-bar"),
                            xs=12, md=6, className="mb-3"),
                    dbc.Col(chart_card("Internações/óbitos por sexo",
                                       [dcc.Loading(dcc.Graph(id="sihsim-g6"), type="circle"),
                                        _nota("Contagem absoluta por sexo ao longo dos anos. "
                                              "Evidencia diferenças no padrão de adoecimento e "
                                              "mortalidade entre homens e mulheres."),
                                        dl_btn("sihsim-g6", "internacoes_por_sexo")],
                                       fa_icon="fas fa-venus-mars"),
                            xs=12, md=6, className="mb-3"),
                ],
                className="align-items-stretch",
            ),

            # Linha 4: faixa etária
            dbc.Row(dbc.Col(
                chart_card("Distribuição por faixa etária",
                           [dcc.Loading(dcc.Graph(id="sihsim-g7"), type="circle"),
                            _nota("Distribuição proporcional por faixa etária. "
                                  "Identifica os grupos mais afetados pelas doenças "
                                  "cardiovasculares e respiratórias na população da RM."),
                            dl_btn("sihsim-g7", "distribuicao_faixa_etaria")],
                           fa_icon="fas fa-baby"),
                width=12, className="mb-3",
            )),
        ],
        fluid=True,
        className="px-0 pt-3",
    )


def _dyn_card(title_id: str, graph_id: str, fa_icon: str, note_id: str = "") -> html.Div:
    """Card com título e nota informativa dinâmicos (atualizados via callback)."""
    body_children = [dcc.Loading(dcc.Graph(id=graph_id), type="circle")]
    if note_id:
        body_children.append(html.P(id=note_id, className="text-muted small mt-2 mb-0",
                                    style={"fontStyle": "italic"}))
    body_children.append(dl_btn(graph_id))
    return html.Div(
        className="chart-card shadow-sm border-0 mb-4",
        children=[
            html.Div(
                id=title_id,
                className="geo-map-section-header",
                children=[html.I(className=f"{fa_icon} me-2"), "Carregando..."],
            ),
            html.Div(body_children, className="chart-card-body p-3"),
        ],
    )


def _tab_mapa(anos_opts: list, ano_init) -> dbc.Container:
    # Exclui "all" do dropdown — modo "todos os anos" é ativado pelo botão dedicado
    anos_opts_clean = [o for o in anos_opts if o["value"] != "all"]
    return dbc.Container(
        [
            dcc.Store(id="sihsim-mapa-modo", data="single"),
            dbc.Row(dbc.Col(
                dbc.Card(
                    [
                        html.Div(
                            [html.I(className="fas fa-calendar-alt me-2"), "Filtro do Mapa"],
                            className="geo-map-section-header",
                        ),
                        dbc.CardBody(
                            dbc.Row(
                                [
                                    dbc.Col([
                                        html.Label("Ano", className="small fw-semibold text-muted mb-1 d-block"),
                                        dcc.Dropdown(
                                            id="sihsim-mapa-ano",
                                            options=anos_opts_clean,
                                            value=ano_init,
                                            clearable=False,
                                            disabled=False,
                                            style={"minWidth": "140px"},
                                        ),
                                    ], xs=12, md=4),
                                    dbc.Col([
                                        html.Label("Série histórica",
                                                   className="small fw-semibold text-muted mb-1 d-block"),
                                        html.Button(
                                            [html.I(className="fas fa-layer-group me-2"),
                                             "Ver todos os anos"],
                                            id="sihsim-mapa-all-btn",
                                            className="btn btn-outline-primary fw-bold w-100",
                                            n_clicks=0,
                                        ),
                                    ], xs=12, md=4),
                                    dbc.Col(
                                        html.Div(id="sihsim-mapa-aviso",
                                                 className="text-muted small mt-4"),
                                        xs=12, md=4,
                                    ),
                                ],
                                className="g-3",
                            )
                        ),
                    ],
                    className="shadow-sm border-0 mb-3",
                ),
                width=12,
            )),
            dbc.Row(dbc.Col(
                chart_card(
                    "Mapa de taxa por município",
                    [
                        html.Div(id="sihsim-mapa-titulo", className="text-muted small mb-2"),
                        dcc.Loading(
                            html.Div(id="sihsim-mapa-container", style={"minHeight": "200px"}),
                            type="circle",
                        ),
                        html.Button(
                            [html.I(className="fas fa-download me-1"), "Baixar PNG"],
                            className="btn-download-asset mt-2",
                            **{
                                "data-mapa-download": "sihsim-mapa-container",
                                "data-mapa-filename": "mapa_taxa_municipios",
                            },
                        ),
                    ],
                    fa_icon="fas fa-map",
                ),
                width=12,
            )),
        ],
        fluid=True,
        className="px-0 pt-3",
    )


# ── callbacks ───────────────────────────────────────────────────────────────

def register_callbacks_sih_sim(app) -> None:

    @app.callback(
        Output("sihsim-rm", "options"),
        Output("sihsim-rm", "value"),
        Input("sihsim-sistema", "value"),
        Input("sihsim-causa",   "value"),
    )
    def _update_rms(sistema, causa):
        rms = ds.rms_disponiveis(sistema or "SIH", causa or "CARDIOVASCULAR")
        opts = [{"label": r, "value": r} for r in rms]
        return opts, (rms[0] if rms else None)

    @app.callback(
        Output("sihsim-mapa-ano", "options"),
        Output("sihsim-mapa-ano", "value"),
        Input("sihsim-sistema", "value"),
        Input("sihsim-causa",   "value"),
        Input("sihsim-rm",      "value"),
    )
    def _update_anos_mapa(sistema, causa, rm):
        if not rm:
            return [], None
        anos = ds.anos_disponiveis(sistema or "SIH", causa or "CARDIOVASCULAR", rm)
        opts = [{"label": str(a), "value": a} for a in anos]
        return opts, (anos[-1] if anos else None)

    app.clientside_callback(
        """
        function(n_clicks, rm, sistema, causa, modo_atual) {
            var ctx = window.dash_clientside.callback_context;
            if (!ctx || !ctx.triggered || ctx.triggered.length === 0)
                return window.dash_clientside.no_update;
            var tid = ctx.triggered[0].prop_id.split('.')[0];
            var novo = (tid === 'sihsim-mapa-all-btn')
                ? (modo_atual !== 'all' ? 'all' : 'single')
                : 'single';
            var btn_cls = (novo === 'all')
                ? 'btn btn-primary fw-bold w-100'
                : 'btn btn-outline-primary fw-bold w-100';
            return [novo, btn_cls, novo === 'all'];
        }
        """,
        Output("sihsim-mapa-modo",    "data"),
        Output("sihsim-mapa-all-btn", "className"),
        Output("sihsim-mapa-ano",     "disabled"),
        Input("sihsim-mapa-all-btn",  "n_clicks"),
        Input("sihsim-rm",            "value"),
        Input("sihsim-sistema",       "value"),
        Input("sihsim-causa",         "value"),
        State("sihsim-mapa-modo",     "data"),
        prevent_initial_call=True,
    )

    @app.callback(
        Output("sihsim-g1-title", "children"),
        Output("sihsim-g2-title", "children"),
        Output("sihsim-g1-note",  "children"),
        Output("sihsim-g2-note",  "children"),
        Output("sihsim-g1",       "figure"),
        Output("sihsim-g2",       "figure"),
        Output("sihsim-g3",       "figure"),
        Output("sihsim-g4",       "figure"),
        Output("sihsim-g5",       "figure"),
        Output("sihsim-g6",       "figure"),
        Output("sihsim-g7",       "figure"),
        Input("sihsim-sistema", "value"),
        Input("sihsim-causa",   "value"),
        Input("sihsim-rm",      "value"),
    )
    def _update_graficos(sistema, causa, rm):
        _vazio9 = ["—", "—", _empty(), _empty(), _empty(), _empty(), _empty(), _empty(), _empty()]
        _t_default = (
            [html.I(className="fas fa-hospital me-2"),   "—"],
            [html.I(className="fas fa-procedures me-2"), "—"],
        )
        if not rm or not sistema or not causa:
            return (*_t_default, *_vazio9)

        ano_col      = ds._ANO_COL[sistema]
        mes_col      = ds._MES_COL[sistema]
        label_evento = "Internações" if sistema == "SIH" else "Óbitos"

        # ── G1 / G2 — específico por sistema ─────────────────────────────
        if sistema == "SIH":
            t1, icon1, df_g1 = "Caráter de internação",  "fas fa-ambulance",  ds.car_int(causa, rm)
            t2, icon2, df_g2 = "Especialidade do leito", "fas fa-procedures", ds.espec(causa, rm)
            note1 = ("Tipo de admissão: Eletivo (internação programada) ou Urgência/Emergência "
                     "(admissão não planejada por condição aguda).")
            note2 = ("Top 12 especialidades de leito nas internações. Inclui leitos clínicos, "
                     "cirúrgicos, pediátricos, UTI adulto e UTI coronariana.")
        else:
            t1, icon1, df_g1 = "Local do óbito",   "fas fa-map-marker-alt", ds.lococor(causa, rm)
            t2, icon2, df_g2 = "Estado civil",      "fas fa-ring",           ds.estciv(causa, rm)
            note1 = ("Local de ocorrência do óbito: Hospital, Domicílio, Via pública ou "
                     "Outro estabelecimento de saúde.")
            note2 = ("Estado civil autodeclarado na Declaração de Óbito. Indicador de "
                     "determinantes sociais associados à mortalidade.")

        title1 = [html.I(className=f"{icon1} me-2"), t1]
        title2 = [html.I(className=f"{icon2} me-2"), t2]

        col1 = df_g1.columns[0] if not df_g1.empty else "x"
        col2 = df_g2.columns[0] if not df_g2.empty else "x"

        if df_g1.empty:
            g1 = _empty(f"Sem dados de {t1.lower()}")
        else:
            g1 = px.pie(df_g1, names=col1, values="pct", hole=0.4,
                        color_discrete_sequence=[PRIMARY, TEAL, GREEN, ORANGE, RED, DARK_RED, "#aaa"])
            g1.update_traces(
                textinfo="percent+label",
                insidetextorientation="radial",
                textfont_size=12,
                pull=[0.04 if (v < 5) else 0 for v in df_g1["pct"]],
            )
            _base(g1, height=370)
            g1.update_layout(
                uniformtext_minsize=10,
                uniformtext_mode="hide",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=11),
                ),
                margin=dict(t=20, b=60, l=20, r=20),
            )

        if df_g2.empty:
            g2 = _empty(f"Sem dados de {t2.lower()}")
        else:
            g2 = px.bar(df_g2, x="pct", y=col2, orientation="h",
                        labels={"pct": "Percentual (%)", col2: ""})
            g2.update_traces(marker_color=TEAL)
            _base(g2)
            g2.update_layout(margin=dict(l=160, r=20, t=40, b=40))

        # ── G3 — raça/cor ─────────────────────────────────────────────────
        df3 = ds.raca_cor(sistema, causa, rm)
        if df3.empty:
            g3 = _empty("Sem dados de raça/cor")
        else:
            df3 = df3.assign(lbl=(df3["pct"].round(1).astype(str) + "%"))
            g3 = px.bar(df3, x="pct", y="RACA_COR", orientation="h",
                        labels={"pct": "Percentual (%)", "RACA_COR": ""}, text="lbl")
            g3.update_traces(textposition="outside", marker_color=GREEN)
            _base(g3)
            g3.update_layout(margin=dict(l=100, r=50, t=40, b=40))

        # ── G4 — mapa de calor ano × mês ─────────────────────────────────
        df4 = ds.serie_mensal(sistema, causa, rm)
        if df4.empty:
            g4 = _empty("Sem série temporal disponível", height=400)
        else:
            df4 = df4.copy()
            df4["MES_NUM"] = pd.to_numeric(df4[mes_col], errors="coerce")
            df4["ANO_NUM"] = pd.to_numeric(df4[ano_col],  errors="coerce")
            df4 = df4.dropna(subset=["MES_NUM", "ANO_NUM"])
            pivot = (
                df4.groupby(["ANO_NUM", "MES_NUM"])["N"]
                .sum()
                .unstack(fill_value=0)
            )
            # Ordena meses e anos
            pivot = pivot.reindex(columns=sorted(pivot.columns))
            pivot = pivot.sort_index(ascending=False)          # anos mais recentes no topo
            meses_labels = [ds.MESES_PTBR.get(int(m), str(m)) for m in pivot.columns]
            anos_labels  = [str(int(a)) for a in pivot.index]

            g4 = px.imshow(
                pivot.values,
                x=meses_labels,
                y=anos_labels,
                color_continuous_scale=[[0, "#eaf6fb"], [0.5, TEAL], [1, PRIMARY]],
                aspect="auto",
                labels={"color": f"Nº de {label_evento.lower()}"},
            )
            g4.update_layout(
                **{**LAYOUT_BASE, "height": 400,
                   "coloraxis_colorbar": dict(title=f"Nº de<br>{label_evento.lower()}", thickness=14),
                   "xaxis_title": "Mês",
                   "yaxis_title": "Ano",
                },
            )

        # ── G5 — taxa anual ───────────────────────────────────────────────
        df5 = ds.taxa_anual(sistema, causa, rm)
        if df5.empty or df5["taxa"].isna().all():
            g5 = _empty("Taxa indisponível — verifique populacao_RM.parquet")
        else:
            df5p = df5.dropna(subset=["taxa"])
            g5 = px.bar(df5p, x=ano_col, y="taxa",
                        labels={ano_col: "Ano", "taxa": "Taxa / 1.000 hab."})
            g5.update_traces(marker_color=PRIMARY)
            _base(g5)
            g5.update_layout(showlegend=False, xaxis=dict(tickmode="linear", dtick=2))

        # ── G6 — contagem por sexo e ano ──────────────────────────────────
        df6 = ds.sexo_por_ano(sistema, causa, rm)
        if df6.empty:
            g6 = _empty("Sem dados por sexo")
        else:
            g6 = px.line(df6, x=ano_col, y="N", color="SEXO", markers=True,
                         labels={ano_col: "Ano", "N": f"Nº de {label_evento.lower()}", "SEXO": "Sexo"},
                         color_discrete_map={"Masculino": PRIMARY, "Feminino": RED})
            _base(g6)
            g6.update_layout(xaxis=dict(tickmode="linear", dtick=2))

        # ── G7 — faixa etária ─────────────────────────────────────────────
        df7 = ds.faixa_etaria(sistema, causa, rm)
        if df7.empty:
            g7 = _empty("Sem dados de faixa etária")
        else:
            df7 = df7.assign(lbl=(df7["pct"].round(1).astype(str) + "%"))
            g7 = px.bar(df7, x="pct", y="FAIXA_ETARIA", orientation="h",
                        labels={"pct": "Percentual (%)", "FAIXA_ETARIA": "Faixa etária"}, text="lbl")
            g7.update_traces(textposition="outside", marker_color=ORANGE)
            _base(g7, height=320)
            g7.update_layout(margin=dict(l=80, r=60, t=40, b=40))

        return title1, title2, note1, note2, g1, g2, g3, g4, g5, g6, g7

    def _build_choropleth_svg(taxa_df, geojson, all_codes,
                              range_min=None, range_max=None, height=580,
                              var_label="Taxa por 1.000 hab.") -> go.Figure:
        """
        Mapa coroplético SVG (go.Choropleth) com duas camadas:
          1) fundo cinza — todos os municípios da RM, incluindo sem dados
          2) dados coloridos — municípios com taxa disponível
        Usa fitbounds="locations" para zoom automático correto por RM.
        Escala de cores global (range_min/range_max) para comparação entre anos.
        """
        if taxa_df["COD_MUN6"].dtype != object:
            taxa_df = taxa_df.assign(COD_MUN6=taxa_df["COD_MUN6"].astype(str).str.strip())

        # Dicionário código → nome do município extraído do GeoJSON (cached por objeto)
        _nm_keys = ("NM_MUN", "NM_MUNICIP", "NOME_MUN", "NM_MUNICIPIO", "NOME_MUNICIPIO")
        _geo_key = id(geojson)
        if _geo_key not in _geojson_name_cache:
            _built: dict = {}
            for feat in geojson.get("features", []):
                props = feat.get("properties", {})
                fid   = feat.get("id", "")
                for k in _nm_keys:
                    if props.get(k):
                        _built[fid] = str(props[k]).title()
                        break
            _geojson_name_cache[_geo_key] = _built
        code_to_name = _geojson_name_cache[_geo_key]

        data_codes = set(taxa_df["COD_MUN6"].tolist())
        missing    = [c for c in all_codes if c not in data_codes]

        traces = []

        # Camada 1: fundo cinza com hover informativo para municípios sem dados
        if missing:
            missing_text = [
                f"<b>{code_to_name.get(c, c)}</b><br>Sem dados disponíveis"
                for c in missing
            ]
            traces.append(go.Choropleth(
                geojson=geojson,
                locations=missing,
                featureidkey="id",
                z=[0] * len(missing),
                colorscale=[[0, "#cccccc"], [1, "#cccccc"]],
                showscale=False,
                marker_line_color="white",
                marker_line_width=0.5,
                text=missing_text,
                hovertemplate="%{text}<extra></extra>",
                name="Sem dados",
            ))

        # Filtra apenas municípios com taxa válida para a camada colorida
        plot_df = taxa_df.dropna(subset=["taxa"])

        zmin = range_min if range_min is not None else (float(plot_df["taxa"].min()) if not plot_df.empty else 0.0)
        zmax = range_max if range_max is not None else (float(plot_df["taxa"].max()) if not plot_df.empty else 1.0)
        if zmin == zmax:
            zmax = zmin + 1.0

        has_n = "N" in plot_df.columns

        def _hover(r):
            nome = code_to_name.get(r["COD_MUN6"], r["COD_MUN6"])
            lines = [f"<b>{nome}</b>", f"{var_label}: <b>{r['taxa']:.2f}</b>"]
            if has_n:
                lines.append(f"Casos: {int(r['N']):,}".replace(",", "."))
            return "<br>".join(lines)

        hover_text = plot_df.apply(_hover, axis=1)

        # Camada 2: dados coloridos (apenas municípios com taxa válida)
        traces.append(go.Choropleth(
            geojson=geojson,
            locations=plot_df["COD_MUN6"],
            featureidkey="id",
            z=plot_df["taxa"],
            zmin=zmin,
            zmax=zmax,
            colorscale=[[0, "#eaf6fb"], [0.5, TEAL], [1, PRIMARY]],
            showscale=True,
            marker_line_color="white",
            marker_line_width=0.5,
            text=hover_text,
            hovertemplate="%{text}<extra></extra>",
            colorbar=dict(title=var_label.replace(" ", "<br>", 1), thickness=15, len=0.55),
            name=var_label,
        ))

        fig = go.Figure(data=traces)
        fig.update_layout(**{
            **LAYOUT_BASE,
            "height": height,
            "geo":    dict(
                fitbounds="locations",
                visible=False,
                projection_type="mercator",
            ),
            "margin": dict(l=0, r=0, t=20, b=0),
        })
        return fig

    @app.callback(
        Output("sihsim-mapa-container", "children"),
        Output("sihsim-mapa-titulo",    "children"),
        Output("sihsim-mapa-aviso",     "children"),
        Input("sihsim-sistema",    "value"),
        Input("sihsim-causa",      "value"),
        Input("sihsim-rm",         "value"),
        Input("sihsim-mapa-ano",   "value"),
        Input("sihsim-mapa-modo",  "data"),
    )
    def _update_mapa(sistema, causa, rm, ano, modo):
        titulo, aviso = "", ""
        if not rm or (ano is None and modo != "all"):
            return [dcc.Graph(figure=_empty("Selecione uma RM e um ano.", 580))], titulo, aviso

        label_evento = "internações" if sistema == "SIH" else "óbitos"
        label_causa  = "cardiovasculares" if causa == "CARDIOVASCULAR" else "respiratórias"

        _cfg = {"displayModeBar": True, "displaylogo": False}

        # ── Modo "Todos os anos" ──────────────────────────────────────────────
        if modo == "all":
            titulo        = f"Todos os anos — taxa de {label_evento} por doenças {label_causa} — {rm}"
            all_years_data = ds.mapa_data_all_years(sistema or "SIH", causa or "CARDIOVASCULAR", rm)
            if all_years_data is None:
                aviso = "Sem dados geográficos disponíveis para esta RM."
                return [dcc.Graph(figure=_empty("Sem dados disponíveis", 400))], titulo, aviso
            if all_years_data.get("no_overlap"):
                aviso = (
                    "⚠️ Mapa indisponível para SIM nesta RM: CODMUNRES (residência) não coincide "
                    "com os municípios da RM. Corrija o prepare_sih_sim_data.py para usar CODMUNOCOR."
                )
                return [dcc.Graph(figure=_empty(
                    "Dado geográfico incompatível para SIM nesta RM.\n"
                    "O município de residência (CODMUNRES) não pertence à RM selecionada.\n"
                    "Corrija o prepare_sih_sim_data.py para usar CODMUNOCOR.", 400
                ))], titulo, aviso

            geo_data   = all_years_data["geo_data"]
            geojson    = geo_data["geojson"]
            all_codes  = geo_data.get("all_codes", [])
            range_min  = all_years_data["global_min"]
            range_max  = all_years_data["global_max"]

            _vlabel = f"Taxa de {label_evento} {label_causa}/1.000 hab."
            cards = []
            for a, t_df in all_years_data["yearly"]:
                fig = _build_choropleth_svg(
                    t_df, geojson, all_codes,
                    range_min=range_min, range_max=range_max, height=420,
                    var_label=_vlabel,
                )
                cards.append(
                    dbc.Col([
                        html.H6(str(a), className="text-center text-primary fw-bold mb-1"),
                        dcc.Graph(
                            figure=fig,
                            style={"height": "420px"},
                            config={**_cfg, "toImageButtonOptions": {"filename": f"mapa_{rm}_{a}"}},
                        ),
                    ], xs=12, md=6, className="mb-4")
                )

            if not cards:
                aviso = "Sem dados geográficos disponíveis para esta RM."
                return [dcc.Graph(figure=_empty("Sem dados disponíveis", 400))], titulo, aviso
            return [dbc.Row(cards, className="g-3")], titulo, aviso

        # ── Modo ano único ────────────────────────────────────────────────────
        titulo = f"Taxa de {label_evento} por doenças {label_causa} por 1.000 hab. — {rm} ({ano})"
        data   = ds.mapa_data(sistema, causa, rm, int(ano))
        if data is None:
            aviso = (
                "Sem dados geográficos para esta seleção. "
                "Verifique se geojson_rm.json foi gerado pelo prepare_sih_sim_data.py."
            )
            return [dcc.Graph(figure=_empty("Mapa indisponível", 580))], titulo, aviso

        if data.get("no_overlap"):
            aviso = (
                "⚠️ Mapa indisponível para SIM nesta RM: o parquet foi gerado com CODMUNRES "
                "(município de residência do falecido), que não coincide com os municípios desta RM. "
                "Para corrigir, inclua CODMUNOCOR no prepare_sih_sim_data.py."
            )
            return [dcc.Graph(figure=_empty(
                "Dado geográfico incompatível para SIM nesta RM.\n"
                "O município de residência (CODMUNRES) não pertence à RM selecionada.\n"
                "Corrija o prepare_sih_sim_data.py para usar CODMUNOCOR.", 580
            ))], titulo, aviso

        taxa_df = data["taxa_df"]
        if taxa_df.empty or "taxa" not in taxa_df.columns:
            return [dcc.Graph(figure=_empty("Sem dados de taxa para esta RM/ano.", 580))], titulo, aviso

        all_codes = data.get("all_codes", [])
        _vlabel   = f"Taxa de {label_evento} {label_causa}/1.000 hab."
        fig = _build_choropleth_svg(taxa_df, data["geojson"], all_codes, height=580,
                                    var_label=_vlabel)
        return (
            [dcc.Graph(figure=fig,
                       config={**_cfg, "toImageButtonOptions": {"filename": f"mapa_{rm}_{ano}"}})],
            titulo,
            aviso,
        )

