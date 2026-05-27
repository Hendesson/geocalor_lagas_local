"""
Página informativa: O que são as ondas de calor?
"""
import gzip
import json
import urllib.request

from dash import html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_extensions.javascript import Namespace, arrow_function

from components import chart_card, info_card

_ns = Namespace("dashExtensions", "default")
_BRASIL_STYLE = _ns("function3")
_BRASIL_ON_EACH = _ns("function4")
_BRASIL_HOVER = arrow_function({"weight": 2.5, "color": "#333333", "fillOpacity": 0.9})

# ── Dados regionais ───────────────────────────────────────────────────────────
_REGIOES = {
    "1": {
        "nome": "Norte",
        "cor": "#6ec1a6",
        "hover": (
            "<b>Norte</b><br><br>"
            "É difícil tratar a região norte como uma unidade, por conta do tamanho. Mas, no geral," 
            "as ondas de calor na região norte tendem a ser mais duradouras que no resto do Brasil," 
            "é bem comum encontrar ondas de calor que durem mais de 10 dias! As ondas de calor no" 
            "Norte acontecem mais na primavera, que é o período de menor umidade. Além disso, as ondas" 
            "de calor estão ficando mais frequentes na região Norte e em muitas partes estão ficando mais"
            "intensas e duradouras também. Em Manaus e Belém, por exemplo, a situação é bastante crítica!"
        ),
    },
    "2": {
        "nome": "Nordeste",
        "cor": "#e63946",
        "hover": (
            "<b>Nordeste</b><br><br>"
            "A região nordeste, como as temperaturas são naturalmente mais altas,"
             "as ondas de calor tendem a ser menos frequentes e mais curtas.No nordeste"
             "as ondas de calor são mais comuns no verão e são acompanhadas de umidade, ou" 
             "seja, a tendência é de que fique quente durante a noite também."
        ),
    },
    "3": {
        "nome": "Sudeste",
        "cor": "#9b59b6",
        "hover": (
            "<b>Sudeste</b><br><br>"
            "A região sudeste no geral tem no verão e úmidas, mas nas partes mais longe do litoral," 
            "como Belo Horizonte, elas podem ocorrer também no fim do período de seca. As cidades da" 
            "região sudeste não costumavam ter mais de 50 dias de ondas de calor por ano. Mas, isso está"
             "se tornando mais comum nos anos recentes. Em São Paulo e Belo Horizonte, principalmente." 
             "Em BH, nós também identificamos que esses eventos estão ficando mais extremos."
        ),
    },
    "4": {
        "nome": "Sul",
        "cor": "#2b9eb3",
        "hover": (
            "<b>Sul</b><br><br>"
            "A Região Sul também enfrenta os efeitos das mudanças climáticas, mas não é região brasileira"
            "menos afetada pelas ondas de calor. No geral, quando esses eventos acontecem, eles costumam ser"
            "nos meses de verão e não são muito duradouros, mas é até comum que as ondas de calor aconteçam"
             "próximas uma da outra, o que aumenta o desgaste acumulado na saúde."
        ),
    },
    "5": {
        "nome": "Centro-Oeste",
        "cor": "#ff9f1c",
        "hover": (
            "<b>Centro-Oeste</b><br><br>"
            "Na Região Centro-Oeste os meses de primavera costumam concentrar muito as"
            "ondas de calor e elas costumam acontecer nesse fim do período seco, quando a "
            "umidade começa a aumentar. Essa é uma região muito preocupante, pois as ondas" 
            "de calor na região Centro-Oeste estão ficando cada vez mais frequentes, duradouras"
            "e intensas em todos os locais que nós analisamos. "
        ),
    },
}

_IBGE_BASE = (
    "https://servicodados.ibge.gov.br/api/v3/malhas/regioes/{cod}"
    "?formato=application%2Fvnd.geo%2Bjson&resolucao=1"
)

_geojson_cache = None


def _fetch_geojson():
    features = []
    for cod in ["1", "2", "3", "4", "5"]:
        try:
            url = _IBGE_BASE.format(cod=cod)
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "GeoCalor/1.0", "Accept-Encoding": "gzip, identity"},
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                raw = resp.read()
                # descomprime se necessário
                if raw[:2] == b"\x1f\x8b":
                    raw = gzip.decompress(raw)
                data = json.loads(raw.decode("utf-8"))
                features.extend(data.get("features", []))
        except Exception:
            pass
    if not features:
        return None
    return {"type": "FeatureCollection", "features": features}


def _get_geojson():
    global _geojson_cache
    if _geojson_cache is None:
        _geojson_cache = _fetch_geojson()
    return _geojson_cache


def _legenda_regioes():
    ordem = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    por_nome = {v["nome"]: v for v in _REGIOES.values()}
    items = []
    for nome in ordem:
        info = por_nome[nome]
        items.append(
            html.Div([
                html.Span(style={
                    "width": "12px", "height": "12px",
                    "backgroundColor": info["cor"],
                    "borderRadius": "2px",
                    "display": "inline-block",
                    "flexShrink": "0",
                }, className="me-2"),
                html.Span(nome, className="small text-muted"),
            ], className="d-flex align-items-center me-4")
        )
    return html.Div(items, className="d-flex flex-wrap mt-2")


def layout_ondas_calor_info(app):
    return dbc.Container([

        # ── Cabeçalho ────────────────────────────────────────────────────────
        dbc.Row(dbc.Col([
            html.Img(src=app.get_asset_url("geocalor.png"), className="logo-img"),
            html.H2("O que são as ondas de calor?", className="text-center my-4"),
            info_card(
                "",
                html.P(
                    "O projeto GeoCalor tem como principal objetivo pesquisar os impactos das "
                    "ondas de calor na saúde para ter subsídios científicos para a criação de "
                    "um sistema de alerta e apoiar a gestão do SUS na definição de melhores "
                    "estratégias para direcionar a população nesses períodos de elevadas "
                    "temperaturas. Atualmente, as mudanças ambientais globais têm feito com que "
                    "as ondas de calor sejam cada vez mais intensas e frequentes, trazendo mais "
                    "riscos à saúde humana.",
                    className="mb-0 text-muted",
                ),
                fa_icon="fas fa-info-circle",
            ),
        ], width=12), className="text-center mb-4"),

        # ── Impactos na saúde ────────────────────────────────────────────────
        dbc.Row([
            dbc.Col(
                chart_card(
                    "Impactos diretos",
                    [
                        html.P(
                            "As altas temperaturas podem causar insolação, desidratação e "
                            "câimbras, especialmente nos momentos de sol mais intenso.",
                            className="text-muted small mb-3",
                        ),
                        html.P(
                            "Há doenças e condições que podem surgir ou piorar com o calor extremo:",
                            className="fw-semibold small mb-2",
                        ),
                        html.Ul([
                            html.Li("Doenças respiratórias crônicas",
                                    className="small text-muted"),
                            html.Li("Doenças cardiovasculares",
                                    className="small text-muted"),
                            html.Li("Doenças renais",
                                    className="small text-muted"),
                            html.Li("Questões relacionadas à saúde mental",
                                    className="small text-muted"),
                        ], className="mb-3"),
                        html.P(
                            "Idosos, crianças e mulheres grávidas são as populações mais "
                            "suscetíveis a terem complicações de saúde causadas por ondas de calor.",
                            className="small text-muted mb-0 fst-italic",
                        ),
                    ],
                    fa_icon="fas fa-heartbeat",
                ),
                xs=12, md=6, className="mb-3",
            ),
            dbc.Col(
                chart_card(
                    "Impactos indiretos",
                    [
                        html.P(
                            "As altas temperaturas aumentam os riscos de acidentes de trabalho. "
                            "Isso pode acontecer por conta do cansaço e do estresse causados pelo "
                            "calor, que deixam as pessoas mais desatentas.",
                            className="text-muted small mb-3",
                        ),
                        html.P(
                            "Com o aumento do número de doenças e de casos graves, mais pessoas "
                            "precisam de atendimento — e os sistemas de saúde, como o SUS, podem "
                            "ficar sobrecarregados.",
                            className="text-muted small mb-3",
                        ),
                        html.P(
                            "As ondas de calor afetam o ambiente como um todo: cidades, "
                            "plantações e estradas. Por isso, esses eventos podem comprometer o "
                            "fornecimento de serviços essenciais como água, energia e transporte.",
                            className="text-muted small mb-3",
                        ),
                        html.P(
                            [html.Span("Fonte: ", className="fw-semibold"),
                             "OMS — Organização Mundial da Saúde (2021)"],
                            className="small text-muted mb-0",
                        ),
                    ],
                    fa_icon="fas fa-link",
                ),
                xs=12, md=6, className="mb-3",
            ),
        ], className="mb-1"),

        # ── Definição ────────────────────────────────────────────────────────
        dbc.Row(dbc.Col(
            chart_card(
                "O que definimos como onda de calor?",
                [
                    html.P(
                        "Existem muitas metodologias para classificar o que é uma onda de calor.",
                        className="text-muted small mb-3",
                    ),
                    html.P(
                        "O Instituto Nacional de Meteorologia (INMET) segue as indicações da "
                        "Organização Meteorológica Mundial (OMM) e define ondas de calor como:",
                        className="fw-semibold small mb-2",
                    ),
                    html.P(
                        [html.Em(
                            '"Cinco ou mais dias consecutivos durante os quais a temperatura '
                            'máxima diária ultrapassa a temperatura máxima média mensal em '
                            '5°C ou mais."'
                        )],
                        className="text-muted small ps-3 mb-3",
                    ),
                    html.P(
                        "Essa definição tem algumas fragilidades: não consegue diferenciar ondas "
                        "de calor por intensidades diferentes e, por exigir um mínimo fixo de "
                        "5°C, não se adapta às especificidades climáticas locais.",
                        className="text-muted small mb-0",
                    ),
                ],
                fa_icon="fas fa-thermometer-half",
            ),
            width=12,
        ), className="mb-1"),

        # ── EHF + Classificação ───────────────────────────────────────────────
        dbc.Row([
            dbc.Col(
                chart_card(
                    "Excess Heat Factor (EHF)",
                    [
                        html.P(
                            "Neste projeto, utilizamos o Excess Heat Factor (EHF) para "
                            "definir e classificar as ondas de calor por intensidade. O EHF é um "
                            "cálculo desenvolvido por pesquisadores australianos em 2015, já "
                            "testado e aprovado para uso no mundo todo.",
                            className="text-muted small mb-3",
                        ),
                        html.P(
                            "Os cálculos do EHF levam em conta as características locais e fazem "
                            "uma média entre um período de vários anos anteriores e também dos "
                            "30 dias anteriores — pois esse é, aproximadamente, o tempo que o "
                            "corpo leva para se adaptar às temperaturas.",
                            className="text-muted small mb-3",
                        ),
                        html.P(
                            "Se a temperatura subir muito rapidamente, as pessoas não conseguirão "
                            "se adaptar às condições extremas e os impactos podem ser mais graves. "
                            "Por conta dessa característica, o EHF é recomendado para estudos "
                            "sobre ondas de calor e saúde.",
                            className="text-muted small mb-0",
                        ),
                    ],
                    fa_icon="fas fa-flask",
                ),
                xs=12, md=7, className="mb-3",
            ),
            dbc.Col(
                chart_card(
                    "Classificação por intensidade",
                    [
                        html.P(
                            "O EHF permite classificar cada evento conforme o EHF85 — "
                            "percentil 85 dos valores positivos históricos de cada cidade.",
                            className="text-muted small mb-3",
                        ),
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.I(className="fas fa-circle me-2",
                                           style={"color": "#ff9f1c", "fontSize": "0.6rem"}),
                                    html.Span("Baixa Intensidade",
                                              className="fw-semibold small"),
                                ], className="d-flex align-items-center"),
                                html.Span("0 < EHF ≤ EHF85",
                                          className="text-muted small font-monospace"),
                            ], className=(
                                "d-flex justify-content-between align-items-center "
                                "p-2 mb-2"
                            ), style={"background": "#fff8ec", "borderRadius": "4px",
                                      "border": "1px solid #ffd98a"}),

                            html.Div([
                                html.Div([
                                    html.I(className="fas fa-circle me-2",
                                           style={"color": "#e63946", "fontSize": "0.6rem"}),
                                    html.Span("Severa", className="fw-semibold small"),
                                ], className="d-flex align-items-center"),
                                html.Span("EHF85 < EHF ≤ 3 × EHF85",
                                          className="text-muted small font-monospace"),
                            ], className=(
                                "d-flex justify-content-between align-items-center "
                                "p-2 mb-2"
                            ), style={"background": "#fef0f1", "borderRadius": "4px",
                                      "border": "1px solid #f5a0a5"}),

                            html.Div([
                                html.Div([
                                    html.I(className="fas fa-circle me-2",
                                           style={"color": "#dc2f3d", "fontSize": "0.6rem"}),
                                    html.Span("Extrema", className="fw-semibold small"),
                                ], className="d-flex align-items-center"),
                                html.Span("EHF > 3 × EHF85",
                                          className="text-muted small font-monospace"),
                            ], className=(
                                "d-flex justify-content-between align-items-center p-2"
                            ), style={"background": "#fde0e2", "borderRadius": "4px",
                                      "border": "1px solid #f08589"}),
                        ]),
                    ],
                    fa_icon="fas fa-layer-group",
                ),
                xs=12, md=5, className="mb-3",
            ),
        ]),

        # ── Mapa do Brasil ───────────────────────────────────────────────────
        dbc.Row(dbc.Col(
            chart_card(
                "Ondas de calor no Brasil",
                html.Div([
                    html.P(
                        "Passe o cursor sobre cada região para ver as características "
                        "das ondas de calor.",
                        className="small text-muted mb-2",
                    ),
                    dl.Map(
                        [
                            dl.GeoJSON(
                                id="brasil-regioes-geojson",
                                data=_get_geojson(),
                                style=_BRASIL_STYLE,
                                onEachFeature=_BRASIL_ON_EACH,
                                hoverStyle=_BRASIL_HOVER,
                                zoomToBounds=True,
                            ) if _get_geojson() else html.P(
                                "Mapa indisponível — verifique a conexão.",
                                className="text-muted small",
                            ),
                        ],
                        id="mapa-brasil-regioes",
                        center=[-15, -53],
                        zoom=4,
                        maxBounds=[[-36, -75], [6, -28]],
                        maxBoundsViscosity=1.0,
                        dragging=False,
                        scrollWheelZoom=False,
                        doubleClickZoom=False,
                        zoomControl=False,
                        attributionControl=False,
                        style={
                            "width": "100%",
                            "height": "420px",
                            "borderRadius": "4px",
                            "background": "#eef2f7",
                        },
                    ),
                    _legenda_regioes(),
                ]),
                fa_icon="fas fa-map",
            ),
            width=12,
        ), className="mb-3"),

        # ── Referências ──────────────────────────────────────────────────────
        dbc.Row(dbc.Col(
            chart_card(
                "Referências",
                html.Ol([
                    html.Li(
                        "WORLD HEALTH ORGANIZATION. Mudança do clima para profissionais"
                        "da saúde: Guia de bolso. Washington, D.C.: Organização Pan-Americana da Saúde;"
                        "2021. Licença: CC BY-NC-SA 3.0 IGO. https://doi.org/10.37774/9789275721841.",
                         className="small text-muted mb-2",
                    ),
                    html.Li(
                        "LIBONATI, Renata et al. Assessing the role of compound drought and"
                        "heatwave events on unprecedented 2020 wildfires in the Pantanal."
                        "Environmental Research Letters, v. 17, n. 1, p. 015005, 2022.",
                        className="small text-muted mb-2",
                    ),
                    html.Li(
                        "GEIRINHAS, João L. et al. Climatic and synoptic characterization of heat waves in Brazil.",
                        "International Journal of Climatology, v. 38, n. 4, p. 1760-1776, 2018.",
                        className="small text-muted mb-2",
                    ),
                    html.Li(
                        "GEIRINHAS, João L. et al. Characterizing the atmospheric conditions during"
                        "the 2010 heatwave in Rio de Janeiro marked by excessive mortality rates."
                        "Science of The Total Environment, v. 650, p. 796-808, 2019.",
                        className="small text-muted mb-2",
                    ),
                    html.Li(
                        "GEIRINHAS, Joao L. et al. Recent increasing frequency of compound summer drought"
                        "and heatwaves in Southeast Brazil. Environmental Research Letters, v. 16, n. 3, p. 034036, 2021.",
                        className="small text-muted mb-2",
                    ),
                    html.Li(
                        "GEIRINHAS, João L. et al. Heat-related mortality at the beginning of the twenty-f the twenty-first century in Rio de Janeiro, Brazil. "
                        "International journal of biometeorology, v. 64, p. 1319-1332, 2020.",
                        className="small text-muted mb-2",
                    ),
                    html.Li(
                        "NARCIZO, Luiza Cavalcanti et al. Compound effects of drought and "
                        "heat waves on fire incidence over the Amazon. Biodiversidade "
                        "Brasileira, v. 9, n. 1, p. 167-167, 2019.",
                        className="small text-muted mb-2",
                    ),
                    html.Li(
                        "NAIRN, John R.; FAWCETT, Robert JB. The excess heat factor: a "
                        "metric for heatwave intensity and its use in classifying heatwave "
                        "severity. International journal of environmental research and public "
                        "health, v. 12, n. 1, p. 227-253, 2015.",
                        className="small text-muted mb-2",
                    ),
                    html.Li(
                        "MONTEIRO DOS SANTOS, Djacinto et al. Twenty-first-century "
                        "demographic and social inequalities of heat-related deaths in "
                        "Brazilian urban areas. PLoS one, v. 19, n. 1, p. e0295766, 2024.",
                        className="small text-muted mb-0",
                    ),
                ], className="mb-0 ps-3"),
                fa_icon="fas fa-book",
            ),
            width=12,
        ), className="mb-3"),

        # ── Navegação ────────────────────────────────────────────────────────
        html.Hr(className="my-2"),
        dbc.Row(dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dbc.Row([
                        dbc.Col([
                            html.P("Explore os dados no dashboard",
                                   className="fw-bold mb-1"),
                            html.P(
                                "Acesse gráficos, mapas e análises sobre ondas de calor "
                                "nas 15 regiões metropolitanas.",
                                className="text-muted small mb-0",
                            ),
                        ], xs=12, md=9, className="mb-2 mb-md-0"),
                        dbc.Col(
                            html.Div([
                                html.A(
                                    [html.I(className="fas fa-chart-line me-1"),
                                     "Ver análises"],
                                    href="/ondas",
                                    className="btn btn-primary btn-sm me-2",
                                ),
                                html.A(
                                    [html.I(className="fas fa-home me-1"), "Início"],
                                    href="/",
                                    className="btn btn-outline-secondary btn-sm",
                                ),
                            ]),
                            xs=12, md=3,
                            className="d-flex align-items-center justify-content-md-end",
                        ),
                    ], className="align-items-center"),
                ),
                style={"borderTop": "3px solid #1761a0"},
            ),
            width=12,
        ), className="mb-4"),

    ], fluid=True, className="py-4")
