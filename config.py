"""
Constantes globais do projeto GeoCalor Dashboard.
Paleta de cores, layout Plotly base e limites de dados.
Caminhos importados de config_paths (mantém compatibilidade).
"""
from config_paths import BASE_DIR, DATA_DIR, PROCESSED_DIR, CACHE_DIR, ASSETS_DIR  # noqa: F401

# ── Paleta de cores (GeoCalor / dashboard_unico) ───────────────────────────
PRIMARY      = "#1761a0"   # azul escuro — navbar, títulos, eixos
TEAL         = "#2b9eb3"   # teal médio — destaques, gradiente
GREEN        = "#6ec1a6"   # verde claro — bordas, highlights
BG_START     = "#eaf6fb"   # início do gradiente de fundo
BG_END       = "#e3f7ee"   # fim do gradiente de fundo
CARD_BORDER  = "#b3d6e6"   # borda de cards

# Cores de intensidade de ondas de calor
ORANGE       = "#ff9f1c"
RED          = "#e63946"
DARK_RED     = "#dc2f3d"
GRAY         = "#888888"
WHITE        = "#ffffff"

COLORS_INTENSITY = {
    "Low Intensity": ORANGE,
    "Severe":        RED,
    "Extreme":       DARK_RED,
}

# ── Layout base Plotly (usado por todos os gráficos) ───────────────────────
LAYOUT_BASE: dict = dict(
    font=dict(family="Segoe UI, Arial, sans-serif", size=12, color="#333333"),
    paper_bgcolor=WHITE,
    plot_bgcolor=WHITE,
    margin=dict(l=56, r=16, t=40, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5),
    colorway=[PRIMARY, TEAL, GREEN, ORANGE, RED],
    hoverlabel=dict(bgcolor=WHITE, font_size=12, font_family="Segoe UI, Arial"),
)

GRID_COLOR = "rgba(23, 97, 160, 0.10)"

# ── Limites de dados ───────────────────────────────────────────────────────
YEAR_MIN = 1981
YEAR_MAX = 2023
