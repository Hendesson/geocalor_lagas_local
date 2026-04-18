"""
Dashboard GeoCalor unificado — navegação por menu (URL) e páginas escaláveis.
Integra: início, temperaturas, ondas de calor, sistemas de alerta (página Dash + assets), contato.
"""
import logging
import os

import dash
from dash import Input, Output, State, dcc, html, callback
import dash_bootstrap_components as dbc
import flask
import pandas as pd

from data_processing import DataProcessor
from visualization import Visualizer
from db import execute as db_execute
from nota_tecnica_html import NOTA_ONDAS, NOTA_TEMPERATURAS, NOTA_SIH_SIM
from pages import contato, inicio, ondas, sistemas_alerta, temperaturas, sih_sim

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAPA_EVENTOS_DIR = os.path.join(BASE_DIR, "mapa_eventos")

# ── Páginas: ordem do menu (fácil acrescentar entradas) ─────────────────────
PAGE_ENTRIES = [
    {"path": "/", "label": "Sobre o GeoCalor"},
    {"path": "/temperaturas", "label": "Caracterização Climática das RMB"},
    {"path": "/ondas", "label": "Ondas de calor"},
    {"path": "/sistemas-alerta", "label": "Sistemas de alerta"},
    {"path": "/sih-sim",         "label": "Perfil"},
    {"path": "/contato",         "label": "Equipe e contato"},
]

# ── Dados (uma única carga) ───────────────────────────────────────────────────
try:
    data_processor = DataProcessor()
    visualizer = Visualizer()
    df = data_processor.df if data_processor.df is not None else pd.DataFrame()
    cidades = data_processor.cidades if data_processor.cidades else []
    anos = data_processor.anos if data_processor.anos else []
    if not isinstance(cidades, list):
        cidades = []
    if not isinstance(anos, list):
        anos = []
    logger.info("Dados: %s linhas, %s cidades", len(df), len(cidades))
    # Pré-aquece os dois heatmaps pesados para que o primeiro clique seja rápido
    if not df.empty:
        try:
            data_processor.prepare_heatmap_data()
            data_processor.prepare_heatmap_events_data()
            logger.info("Caches de heatmap pré-computados.")
        except Exception as _e:
            logger.warning("Erro ao pré-computar caches de heatmap: %s", _e)
except Exception as e:
    logger.error("Erro ao inicializar dados: %s", e)
    df = pd.DataFrame()
    cidades, anos = [], []
    data_processor = None
    visualizer = Visualizer()

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
    ],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.title = "Dashboard de Ondas de Calor — GeoCalor"

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        <link rel="icon" type="image/png" href="/assets/geocalor.png">
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""


def build_navbar(app_dash: dash.Dash) -> dbc.Navbar:
    """Menu principal: colapsa em telas pequenas; suporta muitas páginas no futuro."""
    nav_links = [
        dbc.NavItem(
            dcc.Link(
                entry["label"],
                href=entry["path"],
                className="nav-link geocalor-nav-link",
            )
        )
        for entry in PAGE_ENTRIES
    ]
    return dbc.Navbar(
        dbc.Container(
            [
                dcc.Link(
                    [
                        html.Img(
                            src=app_dash.get_asset_url("geocalor.png"),
                            height="42",
                            className="me-2",
                            alt="GeoCalor",
                        ),
                        html.Div(
                            [
                                html.Span("GeoCalor", className="fw-bold d-block lh-sm"),
                                html.Small(
                                    "Ondas de calor e saúde",
                                    className="text-white-50 d-none d-md-inline",
                                ),
                            ],
                            className="d-flex flex-column",
                        ),
                    ],
                    href="/",
                    className="navbar-brand d-flex align-items-center text-white text-decoration-none py-0",
                ),
                dbc.NavbarToggler(id="navbar-toggler", className="border-light"),
                dbc.Collapse(
                    dbc.Nav(
                        nav_links,
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    navbar=True,
                    is_open=False,
                ),
            ],
            fluid=True,
        ),
        color="primary",
        dark=True,
        className="geocalor-topnav py-2 shadow-sm sticky-top mb-3",
        expand="lg",
    )


def render_page(pathname):
    path = pathname if pathname else "/"
    if path != "/" and path.rstrip("/") != path:
        path = path.rstrip("/") or "/"
    if path in ("/", "/inicio"):
        return inicio.layout_inicio(app)
    if path == "/temperaturas":
        return temperaturas.layout_temperaturas(app, df, cidades, anos)
    if path == "/ondas":
        return ondas.layout_ondas(app, df, cidades, anos)
    if path == "/sistemas-alerta":
        return sistemas_alerta.layout_sistemas_alerta(app)
    if path == "/sih-sim":
        return sih_sim.layout_sih_sim(app)
    if path == "/contato":
        return contato.layout_contato(app)
    return inicio.layout_inicio(app)


# ── Rotas Flask (notas técnicas, mapa eventos) ───────────────────────────────
@server.route("/nota-tecnica-temperaturas")
def nota_tecnica_temperaturas():
    return NOTA_TEMPERATURAS


@server.route("/nota-tecnica-ondas")
def nota_tecnica_ondas():
    return NOTA_ONDAS


@server.route("/nota-tecnica-sih-sim")
def nota_tecnica_sih_sim():
    return NOTA_SIH_SIM


_MAPA_INDISPONIVEL = """<!DOCTYPE html><html><body style="
    margin:0;display:flex;align-items:center;justify-content:center;
    height:100vh;font-family:sans-serif;background:#f8f9fa;color:#6c757d;">
    <p>Mapa não disponível.<br>
    Coloque o arquivo HTML em <strong>mapa_eventos/</strong>.</p>
</body></html>"""


def _serve_mapa(nome: str, filename: str):
    """Serve mapa HTML do diretório mapa_eventos/ ou página informativa."""
    local = os.path.join(MAPA_EVENTOS_DIR, filename)
    if os.path.exists(local):
        return flask.send_from_directory(MAPA_EVENTOS_DIR, filename)
    return flask.Response(_MAPA_INDISPONIVEL, mimetype="text/html; charset=utf-8")


@server.route("/mapa-eventos-extremos")
def serve_mapa_interativo():
    return _serve_mapa("mapa_interativo", "mapa_interativo.html")


@server.route("/mapa-eventos-geral")
def serve_mapa_geral():
    return _serve_mapa("mapa_geral", "mapa_geral.html")


SPA_INDEX_PATHS = sorted(
    {e["path"] for e in PAGE_ENTRIES if e["path"] != "/"} | {"/inicio"},
    key=len,
    reverse=True,
)

# Mesma entrada HTML que `/`, para F5 ou link direto em cada rota do menu.
for _pathname in SPA_INDEX_PATHS:
    _ep = "dash_spa_" + _pathname.strip("/").replace("-", "_").replace("/", "_") or "root"
    server.add_url_rule(_pathname, endpoint=_ep, view_func=app.index)


app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        build_navbar(app),
        html.Div(id="page-content", className="dashboard-main px-2 px-md-3 pb-4"),
    ],
    className="dashboard-shell min-vh-100",
)


@callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    return render_page(pathname)


app.clientside_callback(
    """
    function(n_clicks, pathname, is_open) {
        var ctx = window.dash_clientside.callback_context;
        if (!ctx || !ctx.triggered || ctx.triggered.length === 0) return false;
        var tid = ctx.triggered[0].prop_id.split('.')[0];
        if (tid === 'navbar-toggler' && n_clicks) return !is_open;
        if (tid === 'url') return false;
        return is_open;
    }
    """,
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    Input("url", "pathname"),
    State("navbar-collapse", "is_open"),
)


temperaturas.register_callbacks_temperaturas(app, df, visualizer)
ondas.register_callbacks_ondas(app, df, cidades, anos, data_processor, visualizer)
sistemas_alerta.register_callbacks_sistemas_alerta(app)
sih_sim.register_callbacks_sih_sim(app)
contato.register_callbacks_contato(app)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="127.0.0.1", port=port, debug=True)
