"""
Equipe e contato — ex-dashboard-contato.
"""
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_leaflet as dl

_CITACAO = (
    "HENDESSON ALVES; PORTO, B. L.; GURGEL, H. C.; BEZERRA, A. B.; "
    "SILVA, E. L. E.; OLIVEIRA, L. F.; LEAL, C. M.; CIPRIANO, R. O.; "
    "SÁ, I. A. A. Dashboard de Ondas de Calor e Saúde. "
    "Laboratório de Geografia, Ambiente e Saúde (LAGAS), "
    "Universidade de Brasília, Brasília, DF."
)


TEAM_MEMBERS = [
    {
        "name": "Helen C. Gurgel",
        "role": "COORDENAÇÃO",
        "institution": "UnB / GEA",
        "areas": "Geotecnologia, Saúde e Meio Ambiente, Geocartografia",
        "image": "helen.jpg",
        "lattes": "http://lattes.cnpq.br/0975018553829295"
    },
    {
        "name": "Eliane Lima e Silva",
        "role": "PESQUISADORES PARCEIROS",
        "institution": "Consultora em Saúde Pública",
        "areas": "Saúde Coletiva, Saúde Pública, Saúde Ambiental, Ciências Ambientais",
        "image": "eliane.png",
        "lattes": "http://lattes.cnpq.br/2241554336609585"
    },
    {
        "name": "Eucilene Alves Santanna Porto",
        "role": "PESQUISADORES PARCEIROS",
        "institution": "Consultora em Saúde Pública",
        "areas": "Ambiente e Saúde",
        "image": "eucilene.jpg",
        "lattes": "http://lattes.cnpq.br/5603383846224202"
    },
    {
        "name": "Amarílis Bahia Bezerra",
        "role": "PESQUISADORES COLABORADORES",
        "institution": "Pesquisadora Colaboradora UnB/LAGAS",
        "areas": "Geoprocessamento, Geografia da Saúde, Ondas de Calor",
        "image": "amarilis.png",
        "lattes": "http://lattes.cnpq.br/5691395606608035"
    },
    {
        "name": "Bruno Lofrano-Porto",
        "role": "PESQUISADORES COLABORADORES",
        "institution": "Pesquisador Colaborador UnB/LAGAS",
        "areas": "Geoprocessamento, Climatologia, Ondas de Calor, Atividade Física",
        "image": "bruno.jpeg",
        "lattes": "http://lattes.cnpq.br/9681269314498480"
    },
    {
        "name": "Peter Zeilhofer",
        "role": "PÓS-DOUTORANDOS",
        "institution": "UnB / LAGAS",
        "areas": "Geoprocessamento, SIG, Modelação Hidrológica",
        "image": "peter.png",
        "lattes": "http://lattes.cnpq.br/1101747116364613"
    },
    {
        "name": "Adriana Dennise Rodriguez Blanco",
        "role": "PESQUISADORES COLABORADORES",
        "institution": "UnB / GEA",
        "areas": "Geografia da Saúde, Turismo e Saúde",
        "image": "Adriana-Rodriguez-Blanco.png",
        "lattes": "http://lattes.cnpq.br/7459490421107821"
    },
    {
        "name": "Caio Martins Leal",
        "role": "GRADUANDOS",
        "institution": "UnB / GEA",
        "areas": "Geoprocessamento, Geografia da Saúde",
        "image": "caio.jpeg",
        "lattes": "http://lattes.cnpq.br/5570352800075153"
    },
    {
        "name": "Rafaela Oliveira Cipriano",
        "role": "GRADUANDOS",
        "institution": "UnB / GEA",
        "areas": "Geoprocessamento, Geografia da Saúde",
        "image": "rafaela.jpeg",
        "lattes": "http://lattes.cnpq.br/2024566715066310"
    },
    {
        "name": "Hendesson Alves Pereira",
        "role": "MESTRANDOS",
        "institution": "UnB / GEA",
        "areas": "Geoprocessamento, Geografia da Saúde",
        "image": "hend.jpeg",
        "lattes": "http://lattes.cnpq.br/7900166623696256"
    },
    {
        "name": "Isabella Anderson de Jesus Gomes de Sá",
        "role": "GRADUANDOS",
        "institution": "UnB / GEA",
        "areas": "Geoprocessamento, Geografia da Saúde",
        "image": "isabella.png",
        "lattes": "http://lattes.cnpq.br/0686385905856513"
    },
    {
        "name": "Lívia Feitosa de Oliveira",
        "role": "MESTRANDOS",
        "institution": "UnB / GEA",
        "areas": "Geoprocessamento, Geografia da Saúde",
        "image": "livia.jpeg",
        "lattes": "http://lattes.cnpq.br/4395234813514048"
    }
]


def make_member_card(app, member: dict, card_class: str) -> html.Div:
    is_center = (card_class == "card-center")
    img_size = "200px" if is_center else "120px"

    links = [
        html.A(
            html.Img(src=app.get_asset_url('logo_lattes.png'),
                     style={"height": "32px", "width": "32px"},
                     title="Lattes"),
            href=member.get("lattes", "#"),
            target="_blank"
        )
    ]

    return html.Div([
        html.Span(member["role"],
                  className="role-badge mb-2 d-block text-center"),
        html.Img(
            src=app.get_asset_url(member["image"]),
            style={"width": img_size, "height": img_size,
                   "objectFit": "cover", "borderRadius": "50%",
                   "margin": "0 auto", "display": "block"},
            className="mb-2"
        ),
        html.H5(member["name"], className="text-center mb-1",
                style={"fontSize": "1rem" if is_center else "0.85rem"}),
        html.P(member.get("institution", ""),
               className="text-center mb-1 text-muted",
               style={"fontSize": "0.82em"}),
        html.P(f"Áreas: {member['areas']}",
               className="text-center mb-2 text-muted",
               style={"fontSize": "0.78em"}),
        html.Div(links, className="d-flex justify-content-center")
    ], className=f"team-card {card_class}")


def layout_contato(app):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Img(src=app.get_asset_url('geocalor.png'), className="logo-img"),
                html.H2("Equipe e contato", className="text-center my-4")
            ], width=12)
        ], className="text-center"),

        html.Br(),

        dbc.Card([
            dbc.CardBody([
                html.H3("Equipe Principal", className="text-center mb-4"),
                dbc.Row([
                    dbc.Col([
                        dbc.Button(
                            html.I(className="fas fa-chevron-left"),
                            id="prev-button", color="primary", className="me-2",
                            title="Membro anterior"
                        )
                    ], width=2, className="d-flex align-items-center justify-content-end"),
                    dbc.Col([
                        html.Div(id="team-cards-row", className="team-cards-container")
                    ], width=8),
                    dbc.Col([
                        dbc.Button(
                            html.I(className="fas fa-chevron-right"),
                            id="next-button", color="primary", className="ms-2",
                            title="Próximo membro"
                        )
                    ], width=2, className="d-flex align-items-center justify-content-start")
                ], className="align-items-center"),
                html.Div(id="carousel-indicator", className="text-center text-muted mt-3",
                         style={"fontSize": "0.85rem"}),
                dcc.Store(id="current-member-index", data=0),
                dcc.Store(id="team-members", data=TEAM_MEMBERS),
            ])
        ], className="mb-4 shadow-sm"),

        html.Br(),

        dbc.Card([
            dbc.CardBody([
                html.H3("Contato", className="text-center mb-4"),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-building me-2 text-primary"),
                                html.Strong("Laboratório de Geografia, Ambiente e Saúde (LAGAS)")
                            ], className="mb-2"),
                            html.Div([
                                html.I(className="fas fa-university me-2 text-muted"),
                                "Universidade de Brasília — Campus Darcy Ribeiro"
                            ], className="mb-1 text-muted"),
                            html.Div([
                                html.I(className="fas fa-map-marker-alt me-2 text-muted"),
                                "Instituto de Ciências Humanas — Depto. de Geografia"
                            ], className="mb-1 text-muted"),
                            html.Div([
                                html.I(className="fas fa-door-open me-2 text-muted"),
                                "ICC Norte, Subsolo, Módulo 23"
                            ], className="mb-1 text-muted"),
                            html.Div([
                                html.I(className="fas fa-mail-bulk me-2 text-muted"),
                                "Brasília-DF — CEP 70.904-970"
                            ], className="mb-3 text-muted"),
                            html.Div([
                                html.I(className="fas fa-envelope me-2 text-primary"),
                                html.A("lagas@unb.br", href="mailto:lagas@unb.br",
                                       className="text-primary fw-semibold")
                            ], className="mb-4"),
                            html.H6("Acompanhe o LAGAS nas redes sociais",
                                    className="mb-3 fw-semibold"),
                            html.Div([
                                html.A(
                                    [html.I(className="fab fa-instagram me-2"), "Instagram"],
                                    href="https://www.instagram.com/lagas_unb",
                                    target="_blank",
                                    className="btn btn-redes me-2 mb-2"
                                ),
                                html.A(
                                    [html.I(className="fab fa-youtube me-2"), "YouTube"],
                                    href="https://www.youtube.com/channel/UC2_1JOADwnkAK7d3I3llRwg",
                                    target="_blank",
                                    className="btn btn-redes me-2 mb-2"
                                ),
                                html.A(
                                    [html.I(className="fab fa-facebook me-2"), "Facebook"],
                                    href="https://facebook.com/UnBLagas",
                                    target="_blank",
                                    className="btn btn-redes mb-2"
                                )
                            ], className="d-flex flex-wrap"),
                            html.Hr(className="my-4"),
                            html.A(
                                [html.Img(src=app.get_asset_url('logo.png'),
                                          style={"height": "56px", "width": "auto"},
                                          className="me-3"),
                                 html.Img(src=app.get_asset_url('geocalor_nome.png'),
                                          style={"height": "44px", "width": "auto"})],
                                href="http://www.lagas.unb.br",
                                target="_blank",
                                className="d-flex align-items-center text-decoration-none"
                            )
                        ], className="contact-info-block")
                    ], width=12, lg=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6([html.I(className="fas fa-map-marker-alt me-2"),
                                         "Localização — LAGAS/UnB"],
                                        className="mb-3 text-primary"),
                                dl.Map([
                                    dl.TileLayer(),
                                    dl.Marker(
                                        position=[-15.761342, -47.870362],
                                        children=dl.Tooltip(
                                            html.Div([
                                                html.Strong("LAGAS — UnB"),
                                                html.Br(),
                                                "ICC Norte, Subsolo, Módulo 23"
                                            ])
                                        )
                                    )
                                ],
                                style={"width": "100%", "height": "clamp(200px, 46vw, 340px)"},
                                center=[-15.761342, -47.870362],
                                zoom=16,
                                className="mapa-contato")
                            ])
                        ], className="mapa-card h-100")
                    ], width=12, lg=6, className="mt-4 mt-lg-0")
                ], className="align-items-start")
            ])
        ], className="mb-5 shadow-sm"),

        html.Br(),

        dbc.Card([
            dbc.CardBody([
                html.H3(
                    [html.I(className="fas fa-quote-left me-2"), "Como Referenciar"],
                    className="text-center mb-4",
                ),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.P(
                                [
                                    "Pereira, HA, Lofrano-Porto, B, Gurgel, H, "
                                    "Bezerra, AB, Silva, EL, Oliveira, LF, Leal, C. M., "
                                    "Cipriano, R. O. Sá, IAA. ",
                                    html.Strong("Dashboard de Ondas de Calor e Saúde."),
                                    " Laboratório de Geografia, Ambiente e Saúde (LAGAS), "
                                    "Universidade de Brasília, Brasília, DF.",
                                ],
                                className="mb-3",
                                style={"fontSize": "0.95rem", "lineHeight": "1.7"},
                            ),
                            html.Div([
                                dcc.Clipboard(
                                    content=_CITACAO,
                                    title="Copiar citação",
                                    style={
                                        "display": "inline-flex",
                                        "alignItems": "center",
                                        "gap": "6px",
                                        "background": "linear-gradient(90deg,#1761a0,#2b9eb3)",
                                        "color": "#fff",
                                        "border": "none",
                                        "borderRadius": "8px",
                                        "padding": "6px 14px",
                                        "fontSize": "0.85rem",
                                        "fontWeight": "600",
                                        "cursor": "pointer",
                                    },
                                ),
                                html.Span(
                                    id="msg-copiado",
                                    className="text-success small ms-2",
                                    style={"display": "none"},
                                ),
                            ], className="d-flex align-items-center"),
                        ], className="p-3",
                           style={
                               "background": "linear-gradient(120deg, #eaf6fb 0%, #e3f7ee 100%)",
                               "borderRadius": "12px",
                               "border": "1.5px solid #b3d6e6",
                           }),
                    ], width=12),
                ]),
            ])
        ], className="mb-5 shadow-sm"),

        html.Br(),
    ], fluid=True, className="py-4")


def register_callbacks_contato(app):
    @app.callback(
        [Output("team-cards-row",    "children"),
         Output("carousel-indicator", "children")],
        [Input("current-member-index", "data"),
         Input("team-members",         "data")]
    )
    def update_team_cards(index, members):
        if not members:
            return [], ""
        n = len(members)
        i = 0 if index is None else int(index) % n
        positions = [
            ((i - 2) % n, "card-far-left"),
            ((i - 1) % n, "card-left"),
            (i       % n, "card-center"),
            ((i + 1) % n, "card-right"),
            ((i + 2) % n, "card-far-right"),
        ]
        cards = [make_member_card(app, members[j], cls) for j, cls in positions]
        indicator = f"{i + 1} / {n} — {members[i]['name']}"
        return cards, indicator

    @app.callback(
        Output("current-member-index", "data"),
        [Input("prev-button", "n_clicks"),
         Input("next-button", "n_clicks")],
        [State("current-member-index", "data"),
         State("team-members",         "data")]
    )
    def update_member_index(prev_clicks, next_clicks, current_index, members):
        if not members:
            return 0
        n = len(members)
        cur = 0 if current_index is None else int(current_index) % n
        ctx = dash.callback_context
        if not ctx.triggered:
            return cur
        trig = ctx.triggered[0]
        if trig.get("value") is None:
            return cur
        btn = trig["prop_id"].split(".")[0]
        if btn == "prev-button":
            return (cur - 1) % n
        if btn == "next-button":
            return (cur + 1) % n
        return cur

