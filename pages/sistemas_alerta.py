"""
Sistemas de alerta — página Dash (mesmo padrão de temperaturas/ondas).
Mapa: dash-leaflet + GeoJSON em assets; carrossel e figuras via callbacks/layout Python.
"""
import inspect
import json
import os

import folium
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_extensions.javascript import Namespace
import plotly.graph_objs as go

from config import LAYOUT_BASE, PRIMARY, TEAL, GREEN, ORANGE, GRID_COLOR
from components import chart_card, dl_btn

_NUM_INFOGRAFICOS = 20

_GEOJSON_PROTOCOLOS = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets", "sistemas_alerta", "json", "paises_com_protocolos.geojson",
)

_COR_PROTOCOLOS = {
    (1,  4):  "#c6dbef",
    (5,  8):  "#6baed6",
    (9,  13): "#2171b5",
    (14, 18): "#084594",
    (19, 99): "#08306b",
}

def _cor_protocolo(n: int) -> str:
    for (lo, hi), cor in _COR_PROTOCOLOS.items():
        if lo <= n <= hi:
            return cor
    return "#c6dbef"


_mapa_protocolos_html: str | None = None


def build_mapa_protocolos() -> str:
    global _mapa_protocolos_html
    if _mapa_protocolos_html is not None:
        return _mapa_protocolos_html

    m = folium.Map(location=[20, 10], zoom_start=2,
                   tiles="CartoDB positron")

    if os.path.exists(_GEOJSON_PROTOCOLOS):
        with open(_GEOJSON_PROTOCOLOS, encoding="utf-8") as f:
            geojson_data = json.load(f)

        def _style(feature):
            n = feature["properties"].get("NUM_PROTOC") or 0
            return {
                "fillColor":   _cor_protocolo(int(n)),
                "color":       "#333",
                "weight":      0.8,
                "fillOpacity": 0.75,
            }

        folium.GeoJson(
            geojson_data,
            name="Protocolos",
            style_function=_style,
            highlight_function=lambda _: {"weight": 2, "color": "#1761a0", "fillOpacity": 0.92},
            tooltip=folium.GeoJsonTooltip(
                fields=["NOME_PT", "NUM_PROTOC"],
                aliases=["País:", "Nº de protocolos:"],
                sticky=True,
                style="font-family:Arial,sans-serif;font-size:13px;padding:6px 10px;",
            ),
            popup=folium.GeoJsonPopup(
                fields=["NOME_PT", "NUM_PROTOC"],
                aliases=["País", "Protocolos"],
                max_width=250,
            ),
        ).add_to(m)

    # Legenda
    legend_html = """
    <div style="position:fixed;bottom:28px;left:28px;z-index:1000;background:white;
                padding:12px 16px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,.25);
                font-family:Arial,sans-serif;font-size:12px;line-height:1.8;">
      <strong style="display:block;margin-bottom:6px;color:#1761a0;">Nº de protocolos</strong>
      <span style="display:inline-block;width:14px;height:14px;background:#c6dbef;
                   border:1px solid #555;margin-right:6px;vertical-align:middle;"></span>1–4<br>
      <span style="display:inline-block;width:14px;height:14px;background:#6baed6;
                   border:1px solid #555;margin-right:6px;vertical-align:middle;"></span>5–8<br>
      <span style="display:inline-block;width:14px;height:14px;background:#2171b5;
                   border:1px solid #555;margin-right:6px;vertical-align:middle;"></span>9–13<br>
      <span style="display:inline-block;width:14px;height:14px;background:#084594;
                   border:1px solid #555;margin-right:6px;vertical-align:middle;"></span>14–18<br>
      <span style="display:inline-block;width:14px;height:14px;background:#08306b;
                   border:1px solid #555;margin-right:6px;vertical-align:middle;"></span>19+
    </div>"""
    m.get_root().html.add_child(folium.Element(legend_html))

    _mapa_protocolos_html = m._repr_html_()
    return _mapa_protocolos_html


_ns = Namespace("dashExtensions", "default")
_ALERTA_STYLE           = _ns("function0")
_ALERTA_ON_EACH_FEATURE = _ns("function1")

# Parâmetros da assinatura de dl.GeoJSON inspecionados uma única vez no import
_DL_GEOJSON_PARAMS = inspect.signature(dl.GeoJSON).parameters


def chart_note(texto: str) -> html.P:
    return html.P(texto, className="chart-note text-muted small mt-2")


def _p(text: str, className: str = "text-muted", **kwargs) -> html.P:
    return html.P(text, className=className, **kwargs)


def _geojson_paises(geo_url: str) -> dl.GeoJSON:
    par = _DL_GEOJSON_PARAMS
    kw = {"id": "alerta-paises-geojson", "style": _ALERTA_STYLE}
    if "url" in par:
        kw["url"] = geo_url
    else:
        kw["data"] = geo_url
    if "zoom_to_bounds" in par:
        kw["zoom_to_bounds"] = True
    elif "zoomToBounds" in par:
        kw["zoomToBounds"] = True
    if "on_each_feature" in par:
        kw["on_each_feature"] = _ALERTA_ON_EACH_FEATURE
    elif "onEachFeature" in par:
        kw["onEachFeature"] = _ALERTA_ON_EACH_FEATURE
    hov = dict(weight=2, color="#111", fillOpacity=0.82)
    if "hover_style" in par:
        kw["hover_style"] = hov
    elif "hoverStyle" in par:
        kw["hoverStyle"] = hov
    if "format" in par:
        kw["format"] = "geojson"
    return dl.GeoJSON(**kw)


def _legenda_protocolos() -> html.Div:
    grades = [1, 5, 9, 14, 19]
    colors = ["#e5f5e0", "#41ab5d", "#238b45", "#006d2c", "#00441b"]
    rows = []
    for i, g in enumerate(grades):
        to = grades[i + 1] - 1 if i + 1 < len(grades) else None
        label = f"{g}–{to}" if to is not None else f"{g}+"
        rows.append(
            html.Div(
                [
                    html.Span(
                        style={
                            "display": "inline-block",
                            "width": "18px",
                            "height": "18px",
                            "backgroundColor": colors[i],
                            "marginRight": "8px",
                            "verticalAlign": "middle",
                            "border": "1px solid #333",
                        }
                    ),
                    html.Small(label),
                ],
                className="mb-1",
            )
        )
    return html.Div(
        [html.Strong("Nº de protocolos", className="d-block mb-2 small"), *rows],
        className="sistemas-alerta-legend border rounded p-2 bg-white small shadow-sm",
    )


def _texto(children) -> html.Div:
    content = children if isinstance(children, list) else [children]
    return html.Div(
        html.P(content, className="mb-0"),
        className="text-center fw-semibold my-4 px-3 px-md-5",
        style={"color": "#1761a0", "fontSize": "1rem", "lineHeight": "1.7"},
    )


# ── Funções de figura Plotly ─────────────────────────────────────────────────

def _base_layout(title: str = "", **kw) -> dict:
    lo = {**LAYOUT_BASE}
    lo.update(dict(
        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(size=14, color=PRIMARY, family="Segoe UI, Arial, sans-serif"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=56, r=24, t=55, b=44),
        showlegend=False,
    ))
    lo.update(kw)
    return lo


def _fig_continentes() -> go.Figure:
    """Gráfico de barras verticais — distribuição por continente."""
    cats   = ["Ásia", "América", "Europa", "Oceania"]
    vals   = [26, 17, 14, 5]
    colors = [PRIMARY, TEAL, GREEN, ORANGE]
    fig = go.Figure(go.Bar(
        x=cats, y=vals,
        marker_color=colors,
        text=vals,
        textposition="outside",
        textfont=dict(size=13, color="#333"),
        hovertemplate="%{x}: <b>%{y}</b> documentos<extra></extra>",
    ))
    fig.update_layout(_base_layout(
        "Distribuição por continente",
        xaxis=dict(showgrid=False, tickfont=dict(size=13)),
        yaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR,
            title="Nº de documentos",
            range=[0, 31],
        ),
        height=310,
    ))
    return fig


def _hbar_colors(vals: list, hex_rgb: tuple) -> list:
    """Retorna lista de cores RGBA com opacidade proporcional ao valor."""
    r, g, b = hex_rgb
    max_v = max(vals) or 1
    return [
        f"rgba({r},{g},{b},{0.35 + 0.65 * v / max_v:.2f})"
        for v in vals
    ]


def _fig_abrangencia() -> go.Figure:
    """Barras horizontais — distribuição por abrangência."""
    data = [
        ("Metrópole",                           "Metrópole",                                              1),
        ("Nacional",                             "Nacional",                                               11),
        ("Local (distrito, canton, condado)",    "Local (distrito, canton, condado)",                      14),
        ("Cidade",                               "Cidade",                                                 15),
        ("Regional (estado, prov., c. autônoma)","Regional (estado, comunidade autônoma, província)",      21),
    ]
    # já ordenado ascendente → maior valor no topo do gráfico horizontal
    labels_short = [d[0] for d in data]
    labels_full  = [d[1] for d in data]
    vals         = [d[2] for d in data]
    colors       = _hbar_colors(vals, (43, 158, 179))   # TEAL

    fig = go.Figure(go.Bar(
        x=vals, y=labels_short,
        orientation="h",
        marker_color=colors,
        text=vals,
        textposition="outside",
        textfont=dict(size=12),
        customdata=labels_full,
        hovertemplate="%{customdata}: <b>%{x}</b> documentos<extra></extra>",
    ))
    fig.update_layout(_base_layout(
        "Distribuição por abrangência da implementação",
        xaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR,
            title="Nº de documentos",
            range=[0, 26],
        ),
        yaxis=dict(showgrid=False, automargin=True, tickfont=dict(size=12)),
        height=300,
        margin=dict(l=10, r=40, t=55, b=44),
    ))
    return fig


def _fig_orgao() -> go.Figure:
    """Barras horizontais — distribuição por órgão responsável."""
    data = [
        ("Desconhecido",
         "Desconhecido",                                                            1),
        ("Adaptação / resiliência climática",
         "Órgão dedicado à adaptação ou resiliência climática",                     2),
        ("Órgão de saúde",
         "Órgão de saúde",                                                          15),
        ("Órgão administrativo",
         "Órgão administrativo",                                                    16),
        ("Gestão de riscos / proteção civil",
         "Órgão de gestão de riscos, desastres ou proteção civil",                  18),
    ]
    labels_short = [d[0] for d in data]
    labels_full  = [d[1] for d in data]
    vals         = [d[2] for d in data]
    colors       = _hbar_colors(vals, (23, 97, 160))    # PRIMARY

    fig = go.Figure(go.Bar(
        x=vals, y=labels_short,
        orientation="h",
        marker_color=colors,
        text=vals,
        textposition="outside",
        textfont=dict(size=12),
        customdata=labels_full,
        hovertemplate="%{customdata}: <b>%{x}</b> documentos<extra></extra>",
    ))
    fig.update_layout(_base_layout(
        "Distribuição por instituição responsável",
        xaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR,
            title="Nº de documentos",
            range=[0, 23],
        ),
        yaxis=dict(showgrid=False, automargin=True, tickfont=dict(size=12)),
        height=300,
        margin=dict(l=10, r=40, t=55, b=44),
    ))
    return fig


def _fig_populacoes() -> go.Figure:
    """Barras horizontais — frequência de menção de populações vulneráveis."""
    data = [
        ("Pop. privada da liberdade",           "População privada da liberdade",                                          1),
        ("Mulheres",                             "Mulheres",                                                                2),
        ("Pedestres",                            "Pedestres",                                                               2),
        ("Povos originários / indígenas",        "Povos originários / indígenas",                                           2),
        ("Migrantes / estrangeiros / refugiados","Migrantes / estrangeiros / turistas / deslocados / refugiados",           4),
        ("Pacientes com medicamentos termoreg.", "Pacientes que usam medicamentos que afetam a termorregulação",            7),
        ("PCD",                                  "Pessoas com deficiência (PCD)",                                           8),
        ("Usuários de drogas e/ou álcool",       "Usuários de drogas e/ou álcool",                                          9),
        ("Atletas / prática esportiva",          "Atletas / prática esportiva ao ar livre",                                 10),
        ("Portadores de doenças crônicas",       "Portadores de doenças crônicas / condições pré-existentes",               16),
        ("Grávidas",                             "Grávidas",                                                                17),
        ("Trabalhadores (informais, ao ar livre)","Trabalhadores (ao ar livre, informais, da indústria)",                   18),
        ("Pop. em isolamento social",            "População em isolamento social",                                          19),
        ("Baixa renda / moradia precária",       "Baixa renda / moradia precária / moradores de favela (slums) / abrigos", 20),
        ("Pop. em situação de rua",              "População em situação de rua",                                            20),
        ("Crianças",                             "Crianças",                                                                30),
        ("Idosos",                               "Idosos",                                                                  33),
    ]
    # já ordenado ascendente → maior valor (Idosos/Crianças) no topo
    labels_short = [d[0] for d in data]
    labels_full  = [d[1] for d in data]
    vals         = [d[2] for d in data]
    colors       = _hbar_colors(vals, (110, 193, 166))  # GREEN

    fig = go.Figure(go.Bar(
        x=vals, y=labels_short,
        orientation="h",
        marker_color=colors,
        text=vals,
        textposition="outside",
        textfont=dict(size=11),
        customdata=labels_full,
        hovertemplate="%{customdata}: <b>%{x}</b> menções<extra></extra>",
    ))
    fig.update_layout(_base_layout(
        "Frequência de menção como grupo vulnerável / de risco",
        xaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR,
            title="Nº de documentos",
            range=[0, 40],
        ),
        yaxis=dict(showgrid=False, automargin=True, tickfont=dict(size=11)),
        height=560,
        margin=dict(l=10, r=40, t=55, b=44),
    ))
    return fig


# ── Layout ───────────────────────────────────────────────────────────────────

def layout_sistemas_alerta(app) -> dbc.Container:
    geo_url    = app.get_asset_url("sistemas_alerta/json/paises_com_protocolos.geojson")
    map_layers = [dl.TileLayer(), _geojson_paises(geo_url)]

    _cfg = {"responsive": True, "displaylogo": False}

    return dbc.Container(
        [
            # ── 1. Cabeçalho ───────────────────────────────────────────────
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src=app.get_asset_url("sistemas_alerta/images/lagasLogo.png"),
                            alt="Logo LAGAS",
                            className="d-none d-md-block",
                            style={"maxWidth": "130px", "maxHeight": "130px",
                                   "objectFit": "contain", "margin": "0 auto"},
                        ),
                        xs=0, md=2,
                        className="d-flex align-items-center justify-content-center",
                    ),
                    dbc.Col(
                        html.H2(
                            "Sistemas de alerta de ondas de calor e saúde pelo mundo",
                            className="text-center my-4",
                        ),
                        xs=12, md=8,
                    ),
                    dbc.Col(
                        html.Img(
                            src=app.get_asset_url("sistemas_alerta/images/geocalorLogo.png"),
                            alt="Logo GeoCalor",
                            className="d-none d-md-block",
                            style={"maxWidth": "130px", "maxHeight": "130px",
                                   "objectFit": "contain", "margin": "0 auto"},
                        ),
                        xs=0, md=2,
                        className="d-flex align-items-center justify-content-center",
                    ),
                ],
                align="center",
            ),

            # ── 2. Texto introdutório ──────────────────────────────────────
            _texto(
                "Com a ideia de apoiar o Ministério da Saúde no desenvolvimento de um sistema "
                "próprio, nós revisamos em grande detalhe alguns dos principais e mais "
                "consolidados sistemas de alerta para ondas de calor e saúde. A partir da "
                "leitura dos documentos diretamente ou de artigos que falam sobre esses "
                "documentos, construímos os infográficos abaixo resumindo nossos principais achados."
            ),

            # ── 3. Carrossel de infográficos ───────────────────────────────
            dbc.Card(
                [
                    html.Div(
                        [html.I(className="fas fa-images me-2"), "Infográficos da revisão"],
                        className="geo-map-section-header",
                    ),
                    dbc.CardBody(
                        [
                            dcc.Store(id="alerta-carousel-idx", data=1),
                            html.Div(
                                style={
                                    "position": "relative",
                                    "maxWidth": "900px",
                                    "margin": "0 auto",
                                    "padding": "0 36px",
                                },
                                children=[
                                    html.Img(
                                        id="alerta-carousel-img",
                                        src=app.get_asset_url(
                                            "sistemas_alerta/images/infografico_1.png"
                                        ),
                                        alt="Infográfico da revisão",
                                        style={
                                            "width": "100%", "height": "auto",
                                            "borderRadius": "6px",
                                            "border": "1px solid #dee2e6",
                                            "display": "block",
                                        },
                                    ),
                                    dbc.Button(
                                        html.I(className="fas fa-chevron-left"),
                                        id="alerta-carousel-prev",
                                        color="dark", size="sm",
                                        style={
                                            "position": "absolute", "top": "50%",
                                            "left": "0", "transform": "translateY(-50%)",
                                            "zIndex": 10,
                                        },
                                    ),
                                    dbc.Button(
                                        html.I(className="fas fa-chevron-right"),
                                        id="alerta-carousel-next",
                                        color="dark", size="sm",
                                        style={
                                            "position": "absolute", "top": "50%",
                                            "right": "0", "transform": "translateY(-50%)",
                                            "zIndex": 10,
                                        },
                                    ),
                                ],
                            ),
                            html.P(
                                id="alerta-carousel-caption",
                                children=f"Infográfico 1 de {_NUM_INFOGRAFICOS}",
                                className="text-center text-muted small mt-3 mb-1",
                            ),
                            html.Div(
                                html.A(
                                    [html.I(className="fas fa-download me-1"), "Baixar PNG"],
                                    id="alerta-carousel-dl",
                                    href=app.get_asset_url("sistemas_alerta/images/infografico_1.png"),
                                    download="infografico_1.png",
                                    className="btn-download-asset",
                                ),
                                className="text-center mt-1 mb-2",
                            ),
                        ]
                    ),
                ],
                className="shadow-sm border-0 mb-4",
            ),

            # ── 4. Texto pós-carrossel ─────────────────────────────────────
            _texto(
                "Após essa primeira revisão mais detalhada, com o decorrer do nosso projeto, "
                "atualizamos a revisão para englobar novos sistemas que foram elaborados em "
                "2025. Você pode ver uma síntese do que descobrimos no mapa e nas figuras abaixo!"
            ),

            # ── 5. Mapa mundial ────────────────────────────────────────────
            dbc.Card(
                [
                    html.Div(
                        [
                            html.Span([html.I(className="fas fa-globe-americas me-2"),
                                       "Distribuição espacial dos protocolos"]),
                            html.Div([
                                html.A(
                                    [html.I(className="fas fa-expand me-1"), "Tela cheia"],
                                    href="/mapa-protocolos",
                                    target="_blank",
                                    className="btn btn-sm btn-light border me-2",
                                    title="Abrir mapa em tela cheia (fácil de imprimir)",
                                ),
                                html.A(
                                    [html.I(className="fas fa-print me-1"), "Imprimir"],
                                    href="/mapa-protocolos",
                                    target="_blank",
                                    className="btn btn-sm btn-outline-light",
                                    title="Abra em tela cheia e use Ctrl+P para salvar como PDF",
                                ),
                            ], className="d-flex"),
                        ],
                        className="geo-map-section-header d-flex justify-content-between align-items-center",
                    ),
                    dbc.CardBody([
                        _p(
                            "Passe o mouse sobre os países para ver o número de protocolos. "
                            "Use os botões acima para abrir em tela cheia ou imprimir.",
                            className="small text-muted text-center mb-3",
                        ),
                        dbc.Row([
                            dbc.Col(
                                dl.Map(
                                    [
                                        dl.TileLayer(
                                            url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
                                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>',
                                            maxZoom=19,
                                        ),
                                        _geojson_paises(geo_url),
                                    ],
                                    id="mapa-sistemas-alerta",
                                    style={
                                        "width": "100%", "height": "70vh",
                                        "minHeight": "460px", "borderRadius": "10px",
                                        "boxShadow": "0 2px 8px rgba(0,0,0,.12)",
                                    },
                                    center=[20, 10],
                                    zoom=2,
                                ),
                                xs=12, lg=9,
                            ),
                            dbc.Col(
                                [
                                    _legenda_protocolos(),
                                    html.P(
                                        "Clique em um país para mais detalhes.",
                                        className="small text-muted mt-3 text-center text-lg-start",
                                    ),
                                ],
                                xs=12, lg=3,
                                className="mt-3 mt-lg-0 d-flex flex-column align-items-center "
                                          "align-items-lg-start",
                            ),
                        ], align="start"),
                    ]),
                ],
                className="shadow border-0 mb-4",
                style={"borderRadius": "12px", "overflow": "hidden"},
            ),

            # ── 6. Texto pós-mapa ──────────────────────────────────────────
            _texto([
                "Sem dúvidas a Índia é o país de maior destaque no que diz respeito a sistemas "
                "de alerta de ondas de calor e saúde, com 23 documentos identificados. Isso é "
                "fruto de um esforço do governo nacional em conjunto com os estaduais de "
                "desenvolver planos de ação específicos para cada localidade. No Brasil também "
                "identificamos dois planos locais, para os municípios do Rio de Janeiro e de "
                "São Paulo. Nos Estados Unidos identificam-se esforços locais promovidos por "
                "agências e governos estaduais e/ou municipais. Outros países como Austrália, "
                "Canadá, Espanha e Portugal possuem mais de um documento, mas a maioria possui "
                "apenas um plano nacional. Para acessar links e mais informações dos documentos "
                "que analisamos, você pode clicar ",
                html.A(
                    [html.I(className="fas fa-external-link-alt me-1"), "acessar os documentos"],
                    href="/nota-tecnica-sistemas-alerta",
                    target="_blank",
                    className="btn btn-info btn-sm ms-1",
                ),
            ]),

            # ── 7. Texto contagem geral ────────────────────────────────────
            _texto(
                "Ao total, foram identificados 63 documentos, oriundos de 18 países diferentes. "
                "A maior parte dos documentos veio da Ásia, Europa e América do Norte, com "
                "destaque para a Índia, que possui uma diretriz nacional e indicativo que os "
                "municípios devem fazer seu próprio sistema de alerta, gerando um alto número "
                "de protocolos."
            ),

            # ── 8. Gráfico continentes → texto ────────────────────────────
            chart_card(
                "Distribuição por continente",
                [
                    dcc.Graph(
                        id="sa-continentes",
                        figure=_fig_continentes(),
                        config=_cfg,
                    ),
                    chart_note(
                        "Número de documentos de sistemas de alerta identificados por continente. "
                        "A Ásia concentra a maior parte dos protocolos, principalmente pela Índia."
                    ),
                    dl_btn("sa-continentes", "distribuicao_continentes"),
                ],
                fa_icon="fas fa-globe",
            ),
            _texto(
                "Identificamos que a maioria dos protocolos tem abrangência regional ou local, "
                "com um número menor de sistemas nacionais. Portanto, acreditamos que, para o "
                "sucesso dessa empreitada, é necessário que surjam sistemas loco-regionais, "
                "ainda que haja uma diretiva nacional e apoio do Ministério da Saúde."
            ),

            # ── 9. Gráfico abrangência → texto ────────────────────────────
            chart_card(
                "Distribuição por abrangência da implementação",
                [
                    dcc.Graph(
                        id="sa-abrangencia",
                        figure=_fig_abrangencia(),
                        config=_cfg,
                    ),
                    chart_note(
                        "Escopo geográfico de implementação dos protocolos revisados. "
                        "Sistemas regionais (estaduais/provinciais) e municipais são maioria."
                    ),
                    dl_btn("sa-abrangencia", "distribuicao_abrangencia"),
                ],
                fa_icon="fas fa-map-marked-alt",
            ),
            _texto(
                "Além disso, faz sentido o Ministério da Saúde e as Secretarias Estaduais de "
                "Saúde serem responsáveis pela elaboração do sistema, visto que, em maioria, os "
                "protocolos são elaborados pelo órgão de saúde. Ainda assim, pela diversidade "
                "apresentada, acreditamos ser fulcral a colaboração entre diferentes órgãos."
            ),

            # ── 10. Gráfico órgão responsável → texto ─────────────────────
            chart_card(
                "Distribuição por instituição responsável",
                [
                    dcc.Graph(
                        id="sa-orgao",
                        figure=_fig_orgao(),
                        config=_cfg,
                    ),
                    chart_note(
                        "Tipo de instituição responsável pela elaboração ou publicação do protocolo. "
                        "Passe o mouse nas barras para ver o nome completo da categoria."
                    ),
                    dl_btn("sa-orgao", "distribuicao_orgao_responsavel"),
                ],
                fa_icon="fas fa-building",
            ),
            _texto(
                "Outros pontos importantes identificados nos protocolos revisados são as "
                "populações de risco. Como esperado, idosos e crianças aparecem de forma muito "
                "frequente. Além disso, foi interessante notar que uma quantidade considerável "
                "de protocolos indica atletas ou pessoas realizando prática desportiva ao ar "
                "livre, bem como usuários de drogas como populações sob maior risco."
            ),

            # ── 11. Gráfico populações de risco ───────────────────────────
            chart_card(
                "Populações vulneráveis / de risco",
                [
                    dcc.Graph(
                        id="sa-populacoes",
                        figure=_fig_populacoes(),
                        config=_cfg,
                    ),
                    chart_note(
                        "Frequência de menção de cada grupo como populações de risco nos documentos revisados. "
                        "Passe o mouse nas barras para ver o rótulo completo da categoria."
                    ),
                    dl_btn("sa-populacoes", "populacoes_de_risco"),
                ],
                fa_icon="fas fa-users",
            ),

            html.Div(style={"height": "40px"}),
        ],
        fluid=True,
        className="py-3 pb-5",
    )


def register_callbacks_sistemas_alerta(app) -> None:
    @app.callback(
        Output("alerta-carousel-img",     "src"),
        Output("alerta-carousel-idx",     "data"),
        Output("alerta-carousel-caption", "children"),
        Output("alerta-carousel-dl",      "href"),
        Output("alerta-carousel-dl",      "download"),
        Input("alerta-carousel-prev", "n_clicks"),
        Input("alerta-carousel-next", "n_clicks"),
        State("alerta-carousel-idx",  "data"),
        prevent_initial_call=False,
    )
    def carousel(_prev, _next, idx):
        from dash import callback_context

        idx = int(idx) if idx is not None else 1
        tid = callback_context.triggered_id
        if tid == "alerta-carousel-prev":
            idx = idx - 1 if idx > 1 else _NUM_INFOGRAFICOS
        elif tid == "alerta-carousel-next":
            idx = idx + 1 if idx < _NUM_INFOGRAFICOS else 1
        fname = f"infografico_{idx}.png"
        src   = app.get_asset_url(f"sistemas_alerta/images/{fname}")
        cap   = f"Infográfico {idx} de {_NUM_INFOGRAFICOS}"
        return src, idx, cap, src, fname

