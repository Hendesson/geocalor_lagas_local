"""
Página inicial — boas-vindas e apoiadores (ex-dashboard-inicio).
"""
from dash import html
import dash_bootstrap_components as dbc


def logo_apoiador(app, img, href, height="60px"):
    return html.A(
        html.Img(
            src=app.get_asset_url(img),
            style={"height": height, "width": "auto", "maxWidth": "140px"},
            className="img-fluid apoiador-logo"
        ),
        href=href,
        target="_blank",
        className="apoiador-link"
    )


APOIADORES = [
    ("unb.png",               "https://www.unb.br",                           "UnB"),
    ("fiocruz.jpg",            "https://portal.fiocruz.br",                    "Fiocruz"),
    ("ufrj_logo.png",          "https://ufrj.br",                              "UFRJ"),
    ("ird.png",                "https://en.ird.fr/",                           "IRD"),
    ("cnpq.png",               "https://www.gov.br/cnpq",                      "CNPq"),
    ("lmi_logo.png",           "#",                                            "LMI"),
    ("observatorio.png.png",   "https://climaesaude.icict.fiocruz.br/",        "Observatório"),
]


_PUBLICACOES = [
    {
        "img": "Bezerra_artigo.png",
        "href": "http://cienciaesaudecoletiva.com.br/artigos/ondas-de-calor-e-saude-humana-revisao-de-escopo-dos-codigos-cid10-para-mortalidade-e-morbidade/19937?id=19937",
        "ref": (
            "Bezerra, AB, Gurgel, H, Santana, EA, Silva, EL, Oliveira, LF, Lofrano-Porto, B, Miranda, MJ. "
            "ONDAS DE CALOR E SAÚDE HUMANA: REVISÃO DE ESCOPO DOS CÓDIGOS CID-10 PARA MORTALIDADE E MORBIDADE. "
            "Cien Saude Colet, 2026."
        ),
    },
    {
        "img": "bruno_artigo.png",
        "href": "https://rbafs.org.br/RBAFS/article/view/15567",
        "ref": (
            "Porto, LGG; Porto, BL; Gurgel, H; Matsudo, VKR; Costa, L. As recomendações de atividade física "
            "para a saúde no contexto das emergências climáticas: estamos suficientemente atentos? "
            "Revista Brasileira de Atividade Física e Saúde, v. 31, p. 1-6, 2026."
        ),
    },
    {
        "img": "eliane_artigo_1.png",
        "href": "https://www.sciencedirect.com/science/article/pii/S2667193X25002868?via%3Dihub",
        "ref": (
            "Hartinger, SM; Palmeiro-Silva, Y; Llerena-Cayo, C; Araujo Palharini, RS; et al. "
            "The 2025 Lancet Countdown Latin America report: moving from promises to equitable climate "
            "action for a prosperous future. Lancet Regional Health-Americas, v. 52, p. 101276, 2025."
        ),
    },
    {
        "img": "eliane_artigo_2.png",
        "href": "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0295766",
        "ref": (
            "Monteiro dos Santos, D; Libonati, R; Garcia, BN; Geirinhas, JL; Salvi, BB; Lima e Silva, E; "
            "et al. Twenty-first-century demographic and social inequalities of heat-related deaths in "
            "Brazilian urban areas. PLoS One, v. 19, p. e0295766, 2024."
        ),
    },
]

_ACEITOS = [
    "Revista Estrabão, 2026: Bezerra, AB, Gurgel, H, Santana, EA, Silva, EL, Lofrano-Porto, B. "
    "Ondas de calor e internações por doenças respiratórias na Região Integrada de Desenvolvimento "
    "do Distrito Federal e Entorno.",
]


def _pub_card(app, pub):
    ref_text = html.P(pub["ref"], className="small text-muted mb-2")
    btn = html.A(
        "Acessar",
        href=pub["href"],
        target="_blank",
        className="btn btn-outline-primary btn-sm",
    )
    if pub["img"]:
        img_el = html.A(
            html.Img(
                src=app.get_asset_url(pub["img"]),
                style={"maxHeight": "160px", "maxWidth": "100%", "objectFit": "contain"},
                className="img-fluid rounded shadow-sm mb-3",
            ),
            href=pub["href"],
            target="_blank",
        )
        body = html.Div([img_el, ref_text, btn])
    else:
        body = html.Div([ref_text, btn])
    return dbc.Col(
        dbc.Card(dbc.CardBody(body), className="h-100 shadow-sm"),
        xs=12, sm=6, lg=3, className="mb-4"
    )


def publicacoes_section(app):
    cards = [_pub_card(app, p) for p in _PUBLICACOES]
    aceitos = [
        html.Li(txt, className="text-muted small") for txt in _ACEITOS
    ]
    return html.Div([
        dbc.Row(cards, className="justify-content-center"),
        html.Div([
            html.P("Aceito para publicação", className="fw-semibold mb-2 mt-2"),
            html.Ul(aceitos, className="mb-0"),
        ]) if aceitos else None,
    ])


def apoiadores_row(app):
    def col(img, href, label):
        return dbc.Col(
            html.Div([
                logo_apoiador(app, img, href),
                html.Small(label, className="d-block text-center text-muted mt-1",
                           style={"fontSize": "0.75rem"})
            ], className="text-center apoiador-item"),
            xs=6, md=3, className="mb-4"
        )

    linha1 = APOIADORES[:4]
    linha2 = APOIADORES[4:]

    return html.Div([
        dbc.Row(
            [col(img, href, lbl) for img, href, lbl in linha1],
            className="justify-content-center align-items-center"
        ),
        dbc.Row(
            [col(img, href, lbl) for img, href, lbl in linha2],
            className="justify-content-center align-items-center mt-2"
        )
    ])


def layout_inicio(app):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("Sobre o GeoCalor",
                                className="text-center mb-4"),
                        html.Div([
                            html.A(
                                html.Img(
                                    src=app.get_asset_url('logo.png'),
                                    style={'height': '80px', 'width': 'auto'},
                                    className="img-fluid"
                                ),
                                href="http://www.lagas.unb.br",
                                target="_blank"
                            ),
                            html.A(
                                html.Img(
                                    src=app.get_asset_url('geocalor_nome.png'),
                                    style={'height': '60px', 'width': 'auto'},
                                    className="img-fluid"
                                ),
                                href="http://www.lagas.unb.br/index.php/produtos/geocalor",
                                target="_blank"
                            )
                        ], className="d-flex justify-content-center align-items-center mb-4 gap-4"),
                        html.P(
                            "O aumento da frequência e intensidade das ondas de calor, impulsionado "
                            "pelas mudanças climáticas, tem ampliado os riscos à saúde da população, "
                            "especialmente entre grupos mais vulneráveis.",
                            className="text-center mb-3 text-muted"
                        ),
                        html.P(
                            "O projeto GeoCalor, intitulado Indicadores Espaciais e Sistema de Alerta "
                            "para Ondas de Calor para a Saúde Pública nas Regiões Metropolitanas "
                            "Brasileiras, investiga os impactos das ondas de calor a partir da "
                            "integração de dados climáticos e de saúde, com foco nas três regiões "
                            "metropolitanas mais populosas de cada região do Brasil.",
                            className="text-center mb-3 text-muted"
                        ),
                        html.P(
                            "Este dashboard reúne dados de caracterização climática, ondas de calor, "
                            "perfil epidemiológico e sistemas de alerta, permitindo visualizar padrões, "
                            "identificar anomalias e apoiar o monitoramento, a comunicação de risco e "
                            "o planejamento de ações em saúde, com o objetivo de gerar evidências "
                            "científicas e subsidiar a atuação do Sistema Único de Saúde - SUS.",
                            className="text-center mb-4 text-muted"
                        ),
                        html.Hr(className="my-4"),
                        html.P("Publicações", className="section-heading text-center mb-4"),
                        publicacoes_section(app),
                        html.Hr(className="my-4"),
                        html.P("Apoiadores e Financiadores", className="section-heading text-center mb-4"),
                        apoiadores_row(app),
                        html.Br(),
                    ])
                ], className="shadow-sm")
            ], width=12, lg=10, className="mx-auto")
        ]),

        html.Br(), html.Br(),
    ], fluid=True, className="py-4")
