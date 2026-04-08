"""
Componentes de card reutilizáveis — padrão GeoCalor.
Uso: from components import chart_card, kpi_box, info_card
"""
from dash import html


def kpi_box(valor, label: str, icon: str = "", classe: str = "kpi-teal") -> html.Div:
    """Card numérico tipo KPI.

    Args:
        valor: Valor a exibir (int, float ou string formatada).
        label: Rótulo descritivo abaixo do valor.
        icon: Classe Font Awesome ou emoji. Ex: "fas fa-thermometer-half".
        classe: Modificador CSS. Opções: kpi-teal, kpi-orange, kpi-red, kpi-green.
    """
    children = []
    if icon:
        children.append(html.Span(className=f"kpi-icon {icon}" if icon.startswith("fa") else "kpi-icon",
                                  children=icon if not icon.startswith("fa") else None))
    children.append(html.Span(str(valor), className="kpi-value"))
    children.append(html.Span(label, className="kpi-label"))
    return html.Div(className=f"kpi-card {classe}", children=children)


def chart_card(titulo: str, children, fa_icon: str = "fas fa-chart-line") -> html.Div:
    """Card com header gradiente e corpo branco — contêiner padrão para gráficos.

    Args:
        titulo: Texto do header.
        children: Conteúdo (dcc.Graph, html.Div, etc.).
        fa_icon: Ícone Font Awesome para o header.
    """
    return html.Div(
        className="chart-card shadow-sm border-0 mb-4",
        children=[
            html.Div(
                [html.I(className=f"{fa_icon} me-2"), titulo],
                className="geo-map-section-header",
            ),
            html.Div(children, className="chart-card-body p-3"),
        ],
    )


def info_card(titulo: str, children, fa_icon: str = "fas fa-info-circle") -> html.Div:
    """Card informativo leve — texto explicativo, estatísticas, notas."""
    return html.Div(
        className="info-card border rounded p-3 mb-3",
        style={"background": "rgba(234,246,251,0.6)", "borderColor": "#b3d6e6"},
        children=[
            html.Div(
                [html.I(className=f"{fa_icon} me-2"), titulo],
                className="section-heading mb-2",
            ),
            children,
        ],
    )
