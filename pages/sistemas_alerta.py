"""
Sistemas de alerta — página Dash (mesmo padrão de temperaturas/ondas).
Mapa: dash-leaflet + GeoJSON em assets; carrossel e figuras via callbacks/layout Python.

As funções JS do mapa ficam em assets/dashExtensions_default.js (commitado no repo).
Usamos Namespace para referenciar sem depender de geração automática por assign().
"""
import inspect

from dash import Input, Output, State, dcc, html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_extensions.javascript import Namespace

_NUM_INFOGRAFICOS = 20

# Referências às funções JS em assets/dashExtensions_default.js
_ns = Namespace("dashExtensions", "default")
_ALERTA_STYLE         = _ns("function0")
_ALERTA_ON_EACH_FEATURE = _ns("function1")


def _p(text: str, className: str = "text-muted", **kwargs) -> html.P:
    return html.P(text, className=className, **kwargs)


def _fig(app, filename: str, alt: str) -> html.Img:
    return html.Img(
        src=app.get_asset_url(f"sistemas_alerta/images/{filename}"),
        alt=alt,
        className="img-fluid d-block mx-auto my-3 sistemas-alerta-fig",
    )


def _geojson_paises(geo_url: str) -> dl.GeoJSON:
    """Monta dl.GeoJSON conforme os nomes de parâmetros da versão instalada do dash-leaflet."""
    par = inspect.signature(dl.GeoJSON).parameters
    kw = {
        "id": "alerta-paises-geojson",
        "style": _ALERTA_STYLE,
    }
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
        [
            html.Strong("Nº de protocolos", className="d-block mb-2 small"),
            *rows,
        ],
        className="sistemas-alerta-legend border rounded p-2 bg-white small shadow-sm",
    )


def _texto(children) -> html.Div:
    """Bloco de texto centralizado — replica .text-section do original."""
    content = children if isinstance(children, list) else [children]
    return html.Div(
        html.P(content, className="mb-0"),
        className="text-center fw-semibold my-4 px-3 px-md-5",
        style={"color": "#1761a0", "fontSize": "1rem", "lineHeight": "1.7"},
    )


def _grafico(app, filename: str, alt: str) -> html.Img:
    """Imagem de gráfico centralizada e responsiva."""
    return html.Img(
        src=app.get_asset_url(f"sistemas_alerta/images/{filename}"),
        alt=alt,
        className="img-fluid d-block mx-auto my-3",
        style={"maxWidth": "860px", "width": "100%"},
    )


def layout_sistemas_alerta(app) -> dbc.Container:
    geo_url = app.get_asset_url("sistemas_alerta/json/paises_com_protocolos.geojson")
    map_layers = [dl.TileLayer(), _geojson_paises(geo_url)]

    return dbc.Container(
        [
            # ── 1. Cabeçalho: logo | título | logo ────────────────────────
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
                                className="text-center text-muted small mt-3 mb-0",
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
                        [html.I(className="fas fa-globe-americas me-2"),
                         "Distribuição espacial dos protocolos"],
                        className="geo-map-section-header",
                    ),
                    dbc.CardBody([
                        _p(
                            "Passe o mouse nos países e clique para ver o nome e o "
                            "número de protocolos identificados na revisão.",
                            className="small text-muted text-center mb-3",
                        ),
                        dbc.Row([
                            dbc.Col(
                                dl.Map(
                                    map_layers,
                                    id="mapa-sistemas-alerta",
                                    style={
                                        "width": "100%", "height": "65vh",
                                        "minHeight": "420px", "borderRadius": "12px",
                                    },
                                    center=[16.2, 19.8],
                                    zoom=3,
                                ),
                                xs=12, lg=9,
                            ),
                            dbc.Col(
                                _legenda_protocolos(),
                                xs=12, lg=3,
                                className="mt-3 mt-lg-0 d-flex align-items-start "
                                          "justify-content-center justify-content-lg-start",
                            ),
                        ], align="start"),
                    ]),
                ],
                className="shadow-sm border-0 mb-4",
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
                    "aqui!",
                    href="https://unbbr-my.sharepoint.com/:w:/g/personal/bruno_porto_unb_br/IQDqc4d9VCFcSYo5Dc6FvB0AAZCrzmLGjpv4lQ1p0rvuWSk?e=e4q6kf",
                    target="_blank",
                    rel="noopener noreferrer",
                    style={"color": "#1761a0"},
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

            # ── 8. Imagem continente → texto ──────────────────────────────
            _grafico(app, "continente.png", "Gráfico por continente"),
            _texto(
                "Identificamos que a maioria dos protocolos tem abrangência regional ou local, "
                "com um número menor de sistemas nacionais. Portanto, acreditamos que, para o "
                "sucesso dessa empreitada, é necessário que surjam sistemas loco-regionais, "
                "ainda que haja uma diretiva nacional e apoio do Ministério da Saúde."
            ),

            # ── 9. Imagem abrangência → texto ─────────────────────────────
            _grafico(app, "abrangencia.png", "Gráfico da área de abrangência dos protocolos"),
            _texto(
                "Além disso, faz sentido o Ministério da Saúde e as Secretarias Estaduais de "
                "Saúde serem responsáveis pela elaboração do sistema, visto que, em maioria, os "
                "protocolos são elaborados pelo órgão de saúde. Ainda assim, pela diversidade "
                "apresentada, acreditamos ser fulcral a colaboração entre diferentes órgãos."
            ),

            # ── 10. Imagem órgão responsável → texto ──────────────────────
            _grafico(app, "orgao_responsavel.png", "Gráfico por órgão responsável"),
            _texto(
                "Outros pontos importantes identificados nos protocolos revisados são as "
                "populações de risco. Como esperado, idosos e crianças aparecem de forma muito "
                "frequente. Além disso, foi interessante notar que uma quantidade considerável "
                "de protocolos indica atletas ou pessoas realizando prática desportiva ao ar "
                "livre, bem como usuários de drogas como populações sob maior risco."
            ),

            # ── 11. Imagem populações de risco (última) ────────────────────
            _grafico(app, "populacoes_risco.png", "Gráfico por populações de risco"),

            html.Div(style={"height": "40px"}),
        ],
        fluid=True,
        className="py-3 pb-5",
    )


def register_callbacks_sistemas_alerta(app) -> None:
    @app.callback(
        Output("alerta-carousel-img", "src"),
        Output("alerta-carousel-idx", "data"),
        Output("alerta-carousel-caption", "children"),
        Input("alerta-carousel-prev", "n_clicks"),
        Input("alerta-carousel-next", "n_clicks"),
        State("alerta-carousel-idx", "data"),
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
        src = app.get_asset_url(f"sistemas_alerta/images/infografico_{idx}.png")
        cap = f"Infográfico {idx} de {_NUM_INFOGRAFICOS}"
        return src, idx, cap
