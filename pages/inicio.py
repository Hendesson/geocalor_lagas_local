"""
Página inicial — boas-vindas e apoiadores (ex-dashboard-inicio).
"""
from dash import html
import dash_bootstrap_components as dbc

from components import chart_card, info_card


def logo_apoiador(app, img, href, height="90px"):
    return html.A(
        html.Img(
            src=app.get_asset_url(img),
            style={"height": height, "width": "auto", "maxWidth": "200px"},
            className="img-fluid apoiador-logo",
        ),
        href=href,
        target="_blank",
        className="apoiador-link"
    )


APOIADORES = [
    ("unb.png",               "https://www.unb.br",                           "UnB"),
    ("fiocruz.png",            "https://portal.fiocruz.br",                    "Fiocruz"),
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
    "Revista Brasileira de Geografia, 2026: Lofrano-Porto, B., Gurgel, H., Monteiro dos Santos Junior, D. A, "
    "Alves, H., Zeilhofer, P., Bezerra, A. B., Lima, E., Santana, E. A., Miranda, M., Libonati, R. "
    "Fequência, duração e intensidade de ondas de calor em áreas urbanas do Brasil no período de 1981 a 2023.",
    
    "Revista Estrabão, 2026: Bezerra, AB, Gurgel, H, Santana, EA, Silva, EL, Lofrano-Porto, B. "
    "Ondas de calor e internações por doenças respiratórias na Região Integrada de Desenvolvimento "
    "do Distrito Federal e Entorno.",

    "Revista Estrabão, 2026: Lofrano-Porto, B. Gurgel, H., Oliveira, LF., Pereira, HA., Bezerra, AB. "
    "Ondas de calor e mortalidade por doenças respiratórias na RIDE/DF: evidências de associação e "
    "implicações para a vigilância em saúde.",
]


def _pub_card(app, pub):
    ref_text = html.P(pub["ref"], className="small text-muted mb-2")
    btn = html.A(
        [html.I(className="fas fa-external-link-alt me-1"), "Acessar"],
        href=pub["href"],
        target="_blank",
        className="btn btn-outline-primary btn-sm",
    )
    if pub["img"]:
        img_col = dbc.Col(
            html.A(
                html.Img(
                    src=app.get_asset_url(pub["img"]),
                    style={"width": "100%", "height": "110px", "objectFit": "cover", "borderRadius": "8px"},
                    className="img-fluid",
                ),
                href=pub["href"],
                target="_blank",
            ),
            xs=12, sm=4,
        )
        text_col = dbc.Col([ref_text, btn], xs=12, sm=8)
        body = dbc.Row([img_col, text_col], className="g-2 align-items-start")
    else:
        body = html.Div([ref_text, btn])
    return dbc.Col(
        dbc.Card(dbc.CardBody(body), className="h-100 shadow-sm"),
        xs=12, md=6, className="mb-4"
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


_SECOES = [
    {
        "id": "temperaturas",
        "icon": "fas fa-thermometer-half",
        "href": "/temperaturas",
        "titulo": "Caracterização climática",
        "desc": "Temperaturas médias, anomalias e sazonalidade nas 15 RMB de 1981 a 2023.",
        "cor": "#1761a0",
        "pos": "center center",
    },
    {
        "id": "ondas",
        "icon": "fas fa-fire",
        "href": "/ondas",
        "titulo": "Ondas de calor",
        "desc": "Frequência, duração e intensidade dos eventos com mapas, gráficos e calendário interativo por cidade e ano.",
        "cor": "#e63946",
        "pos": "center center",
    },
    {
        "id": "sih_sim",
        "icon": "fas fa-hospital",
        "href": "/sih-sim",
        "titulo": "Perfil epidemiológico",
        "desc": "Internações e óbitos por doenças cardiovasculares e respiratórias por região e ano, analise através de gráficos e mapas interativos.",
        "cor": "#2b9eb3",
        "pos": "center center",
    },
    {
        "id": "mortalidade",
        "icon": "fas fa-heartbeat",
        "href": "/mortalidade",
        "titulo": "Mortalidade × OC",
        "desc": "Relação entre ondas de calor e mortalidade por doenças cardiovasculares e respiratórias.",
        "cor": "#dc2f3d",
        "pos": "center center",
    },
    {
        "id": "correlacao",
        "icon": "fas fa-chart-bar",
        "href": "/correlacao",
        "titulo": "Internação × OC",
        "desc": "Associação estatística entre ondas de calor e internações hospitalares.",
        "cor": "#6ec1a6",
        "pos": "center center",
    },
    {
        "id": "sistemas_alerta",
        "icon": "fas fa-bell",
        "href": "/sistemas-alerta",
        "titulo": "Sistemas de alerta",
        "desc": "Revisão e comparação de sistemas internacionais de alerta para ondas de calor.",
        "cor": "#ff9f1c",
        "pos": "center center",
    },
    {
        "id": "contato",
        "icon": "fas fa-users",
        "href": "/contato",
        "titulo": "Equipe e contato",
        "desc": "Conheça a equipe do Projeto GeoCalor e entre em contato.",
        "cor": "#1761a0",
        "pos": "center center",
        "size": "contain",
    },
]


def _secoes_row():
    cards = []
    for s in _SECOES:
        img_url = f"/assets/preview_{s['id']}.png"
        cards.append(
            dbc.Col(
                html.A(
                    html.Div([
                        html.Div(
                            className="secao-card-img",
                            style={
                                "backgroundImage": f"url('{img_url}')",
                                "backgroundColor": "#deedf7",
                                "backgroundPosition": s.get("pos", "center center"),
                                "backgroundSize": s.get("size", "cover"),
                                "backgroundRepeat": "no-repeat",
                            },
                        ),
                        html.Div([
                            html.P(s["titulo"],
                                   className="fw-bold mb-1",
                                   style={"color": "#1761a0", "fontSize": "0.9rem"}),
                            html.P(s["desc"], className="text-muted small mb-0", style={"lineHeight": "1.4"}),
                        ], className="secao-card-body"),
                    ]),
                    href=s["href"],
                    className="nav-card-link",
                ),
                xs=12, sm=6, lg=3, className="mb-3"
            )
        )
    return dbc.Row(cards, className="justify-content-center")


def layout_inicio(app):
    return dbc.Container([

        # ── Banner compacto ───────────────────────────────────────────────────
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Img(
                        src=app.get_asset_url("geocalor.png"),
                        style={"height": "52px", "width": "auto", "flexShrink": "0"},
                        className="me-3",
                    ),
                    html.Div([
                        html.Span(
                            "GeoCalor",
                            style={"fontWeight": "700", "fontSize": "1.4rem", "color": "#1761a0",
                                   "display": "block", "lineHeight": "1.2"},
                        ),
                        html.Span(
                            "Ondas de calor e saúde nas Regiões Metropolitanas do Brasil",
                            style={"fontSize": "0.88rem", "color": "#555"},
                        ),
                        html.Span(
                            [html.I(className="fas fa-flask me-1", style={"color": "#6ec1a6"}),
                             "Chamada CNPq/DECIT/SECTICS/MS Nº 18/2023"],
                            className="d-block text-muted mt-1",
                            style={"fontSize": "0.78rem"},
                        ),
                    ]),
                ], className="d-flex align-items-center"),
                xs=12, md=7, className="mb-3 mb-md-0",
            ),
            dbc.Col(
                html.Div([
                    html.A(
                        html.Img(src=app.get_asset_url("logo.png"),
                                 style={"height": "46px", "width": "auto"},
                                 className="img-fluid"),
                        href="http://www.lagas.unb.br", target="_blank",
                    ),
                    html.A(
                        html.Img(src=app.get_asset_url("geocalor_nome.png"),
                                 style={"height": "34px", "width": "auto"},
                                 className="img-fluid"),
                        href="http://www.lagas.unb.br/index.php/produtos/geocalor",
                        target="_blank",
                    ),
                ], className="d-flex justify-content-md-end justify-content-start align-items-center gap-3"),
                xs=12, md=5,
            ),
        ], className="align-items-center mb-3 pt-2"),

        html.Hr(style={"borderColor": "#b3d6e6", "marginTop": "0", "marginBottom": "1.25rem"}),

        # ── Explore o Dashboard ───────────────────────────────────────────────
        html.H3("Explore o Dashboard", className="text-center mb-1"),
        html.P(
            "Navegue pelas seções para acessar os dados climáticos e epidemiológicos.",
            className="text-muted text-center small mb-3",
        ),
        _secoes_row(),

        # ── Sobre o projeto (abaixo das cards) ────────────────────────────────
        html.Hr(className="my-4"),
        dbc.Row(dbc.Col(
            info_card(
                "Sobre o GeoCalor",
                html.Div([
                    html.P(
                        "O projeto GeoCalor investiga os impactos das ondas de calor a partir da "
                        "integração de dados climáticos e de saúde, com foco nas três regiões "
                        "metropolitanas mais populosas de cada região do Brasil.",
                        className="mb-2 text-muted",
                    ),
                    html.P(
                        "Este dashboard reúne dados de caracterização climática, ondas de calor, "
                        "perfil epidemiológico e sistemas de alerta, permitindo visualizar padrões, "
                        "identificar anomalias e apoiar o monitoramento, a comunicação de risco e "
                        "o planejamento de ações em saúde, com o objetivo de gerar evidências "
                        "científicas e subsidiar a atuação do Sistema Único de Saúde — SUS.",
                        className="mb-0 text-muted",
                    ),
                ]),
                fa_icon="fas fa-info-circle",
            ),
            width=12,
        ), className="mb-3"),

        # ── O que são ondas de calor? (CTA) ──────────────────────────────────
        dbc.Row(dbc.Col(
            chart_card(
                "O que são as ondas de calor?",
                dbc.Row([
                    dbc.Col(
                        html.P(
                            "Entenda o conceito científico, a metodologia do Fator de Excesso "
                            "de Calor (EHF), a classificação por intensidade e os impactos na "
                            "saúde humana.",
                            className="text-muted small mb-0",
                        ),
                        xs=12, md=9, className="mb-2 mb-md-0",
                    ),
                    dbc.Col(
                        html.A(
                            [html.I(className="fas fa-book-open me-1"), "Saiba mais"],
                            href="/o-que-sao-ondas-de-calor",
                            className="btn btn-outline-primary btn-sm",
                        ),
                        xs=12, md=3,
                        className="d-flex align-items-center justify-content-start justify-content-md-end",
                    ),
                ], className="align-items-center"),
                fa_icon="fas fa-fire",
                header_class="geo-header-orange",
            ),
            width=12,
        ), className="mb-3"),

        # ── Feedback ─────────────────────────────────────────────────────────
        dbc.Row(dbc.Col(
            chart_card(
                "Avaliação do dashboard",
                dbc.Row([
                    dbc.Col(
                        html.P(
                            "Sua opinião é importante para melhorarmos o dashboard. "
                            "Responda a um breve formulário e nos ajude a aprimorar "
                            "a experiência de uso.",
                            className="text-muted small mb-0",
                        ),
                        xs=12, md=9, className="mb-2 mb-md-0",
                    ),
                    dbc.Col(
                        html.A(
                            [html.I(className="fas fa-external-link-alt me-1"), "Responder"],
                            href="https://docs.google.com/forms/d/e/1FAIpQLSfCpeKb-VNoTos8n5Pr0mr6wtNt2re8-ZTn94caXqRq-xTwkg/viewform",
                            target="_blank",
                            className="btn btn-outline-primary btn-sm",
                        ),
                        xs=12, md=3,
                        className="d-flex align-items-center justify-content-start justify-content-md-end",
                    ),
                ], className="align-items-center"),
                fa_icon="fas fa-poll-h",
                header_class="geo-header-teal",
            ),
            width=12,
        ), className="mb-3"),

        # ── Publicações ───────────────────────────────────────────────────────
        html.Hr(className="my-4"),
        html.P("Publicações", className="section-heading text-center mb-4"),
        publicacoes_section(app),
        html.Hr(className="my-4"),
        html.P("Apoiadores e Financiadores", className="section-heading text-center mb-4"),
        apoiadores_row(app),
        html.Br(), html.Br(),

    ], fluid=True, className="py-3")
