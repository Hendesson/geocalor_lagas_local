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
                        html.P([
                            "O projeto Geocalor tem como principal objetivo pesquisar os impactos das "
                            "ondas de calor na saúde para ter subsídios científicos para criação de um "
                            "sistema de alerta e apoiar a gestão do SUS na definição de melhores "
                            "estratégias para direcionar a população nesses períodos de elevadas "
                            "temperaturas em decorrência dos extremos de calor.",
                            html.Br(), html.Br(),
                            "Atualmente, as mudanças ambientais globais que presenciamos no mundo todo "
                            "têm feito com que as ondas de calor sejam cada vez mais intensas e "
                            "frequentes, trazendo mais riscos à saúde humana.",
                            html.Br(), html.Br(),
                            "Este dashboard foi desenvolvido para analisar e visualizar dados "
                            "climáticos, com foco em ondas de calor e anomalias de temperatura. "
                            "Utilizamos dados de estações meteorológicas para identificar padrões "
                            "climáticos e eventos extremos, contribuindo para a conscientização e "
                            "planejamento frente às mudanças climáticas."
                        ], className="text-center mb-4 text-muted"),
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
