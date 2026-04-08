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
from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc

from components import chart_card, dd
from config import PRIMARY, TEAL, GREEN, ORANGE, RED, DARK_RED, WHITE, LAYOUT_BASE
import data_sih_sim as ds

logger = logging.getLogger(__name__)


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

    return dbc.Container(
        [
            # ── Título ────────────────────────────────────────────────────
            dbc.Row(dbc.Col(
                html.H2("Sistema de Informações SIH/SIM", className="text-center my-4"),
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
                        _tab_mapa(_anos_init, _ano_init),
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
                                              "conforme classificação IBGE/DATASUS.")],
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
                           "Valores são contagens brutas, não taxas populacionais.")],
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
                                              "populacional.")],
                                       fa_icon="fas fa-chart-bar"),
                            xs=12, md=6, className="mb-3"),
                    dbc.Col(chart_card("Internações/óbitos por sexo",
                                       [dcc.Loading(dcc.Graph(id="sihsim-g6"), type="circle"),
                                        _nota("Contagem absoluta por sexo ao longo dos anos. "
                                              "Evidencia diferenças no padrão de adoecimento e "
                                              "mortalidade entre homens e mulheres.")],
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
                                  "cardiovasculares e respiratórias na população da RM.")],
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


def _tab_mapa(anos_init: list, ano_init) -> dbc.Container:
    return dbc.Container(
        [
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
                                    dbc.Col(
                                        dd("sihsim-mapa-ano",
                                           [{"label": str(a), "value": a} for a in anos_init],
                                           ano_init, label="Ano"),
                                        xs=12, md=4,
                                    ),
                                    dbc.Col(
                                        html.Div(id="sihsim-mapa-aviso",
                                                 className="text-muted small mt-4"),
                                        xs=12, md=8,
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
                            dcc.Graph(id="sihsim-mapa-graph", style={"height": "580px"}),
                            type="circle",
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
            df3 = df3.copy()
            df3["lbl"] = df3["pct"].round(1).astype(str) + "%"
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
            df7 = df7.copy()
            df7["lbl"] = df7["pct"].round(1).astype(str) + "%"
            g7 = px.bar(df7, x="pct", y="FAIXA_ETARIA", orientation="h",
                        labels={"pct": "Percentual (%)", "FAIXA_ETARIA": "Faixa etária"}, text="lbl")
            g7.update_traces(textposition="outside", marker_color=ORANGE)
            _base(g7, height=320)
            g7.update_layout(margin=dict(l=80, r=60, t=40, b=40))

        return title1, title2, note1, note2, g1, g2, g3, g4, g5, g6, g7

    @app.callback(
        Output("sihsim-mapa-graph",  "figure"),
        Output("sihsim-mapa-titulo", "children"),
        Output("sihsim-mapa-aviso",  "children"),
        Input("sihsim-sistema",  "value"),
        Input("sihsim-causa",    "value"),
        Input("sihsim-rm",       "value"),
        Input("sihsim-mapa-ano", "value"),
    )
    def _update_mapa(sistema, causa, rm, ano):
        titulo, aviso = "", ""
        if not rm or ano is None:
            return _empty("Selecione uma RM e um ano.", 580), titulo, aviso

        label_evento = "internações" if sistema == "SIH" else "óbitos"
        label_causa  = "cardiovasculares" if causa == "CARDIOVASCULAR" else "respiratórias"
        titulo = f"Taxa de {label_evento} por doenças {label_causa} por 1.000 hab. — {rm} ({ano})"

        data = ds.mapa_data(sistema, causa, rm, int(ano))
        if data is None:
            aviso = (
                "Sem dados geográficos para esta seleção. "
                "Verifique se geojson_rm.json foi gerado pelo prepare_sih_sim_data.py."
            )
            return _empty("Mapa indisponível", 580), titulo, aviso

        taxa_df = data["taxa_df"]
        geojson = data["geojson"]

        if taxa_df.empty or "taxa" not in taxa_df.columns:
            return _empty("Sem dados de taxa para esta RM/ano.", 580), titulo, aviso

        # Usa COD_MUN6 como chave — já definido como id em cada feature pelo mapa_data()
        taxa_df = taxa_df.copy()
        taxa_df["COD_MUN6"] = taxa_df["COD_MUN6"].astype(str).str.strip()

        # Centroide da RM a partir das features filtradas
        try:
            lats, lons = [], []
            for feat in geojson["features"]:
                geom = feat.get("geometry", {})
                coords = geom.get("coordinates", [])
                if geom.get("type") == "Polygon" and coords:
                    ring = coords[0]
                    lons += [p[0] for p in ring]
                    lats += [p[1] for p in ring]
                elif geom.get("type") == "MultiPolygon" and coords:
                    for poly in coords:
                        ring = poly[0]
                        lons += [p[0] for p in ring]
                        lats += [p[1] for p in ring]
            lat_c = float(np.mean(lats)) if lats else -15.0
            lon_c = float(np.mean(lons)) if lons else -50.0
        except Exception:
            lat_c, lon_c = -15.0, -50.0

        # Zoom automático: maior RM → menor zoom
        n_feat = len(geojson["features"])
        zoom = 7 if n_feat <= 15 else (6 if n_feat <= 40 else 5)

        nome_col = next(
            (c for c in ["NM_MUN", "NOME_MUN", "NM_MUNICIP"] if c in taxa_df.columns),
            None,
        )
        hover = {c: True for c in ([nome_col] if nome_col else []) + ["taxa"]}

        fig = px.choropleth_map(
            taxa_df,
            geojson=geojson,
            locations="COD_MUN6",
            featureidkey="id",
            color="taxa",
            color_continuous_scale=[[0, "#eaf6fb"], [0.5, TEAL], [1, PRIMARY]],
            map_style="carto-positron",
            zoom=zoom,
            center={"lat": lat_c, "lon": lon_c},
            opacity=0.75,
            hover_data=hover,
            labels={"taxa": "Taxa/1.000 hab.", "COD_MUN6": "Código"},
        )
        fig.update_layout(
            **{**LAYOUT_BASE,
               "height": 580,
               "margin": dict(l=0, r=0, t=10, b=0),
               "coloraxis_colorbar": dict(
                   title="Taxa por<br>1.000 hab.", thickness=15, len=0.55,
               )},
        )
        return fig, titulo, aviso

