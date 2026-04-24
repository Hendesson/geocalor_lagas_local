"""
Controles de filtro reutilizáveis — padrão GeoCalor.
Uso: from components import dd, filter_bar
"""
from dash import html, dcc


def dd(
    id_: str,
    options: list,
    value,
    label: str = "",
    multi: bool = False,
    min_width: str = "160px",
) -> html.Div:
    """Dropdown com rótulo opcional.

    Args:
        id_: ID do componente Dash.
        options: Lista de dicts {label, value} ou lista de strings.
        value: Valor inicial selecionado.
        label: Texto do rótulo acima do dropdown.
        multi: Permite seleção múltipla.
        min_width: Largura mínima do contêiner.
    """
    items = []
    if label:
        items.append(html.Label(label, className="small fw-semibold text-muted mb-1 d-block"))
    items.append(
        dcc.Dropdown(
            id=id_,
            options=options,
            value=value,
            multi=multi,
            clearable=False,
            style={"minWidth": min_width},
        )
    )
    return html.Div(items, style={"flex": "1", "minWidth": min_width})


def filter_bar(*controls) -> html.Div:
    """Barra de filtros horizontal com alinhamento flexível.

    Uso:
        filter_bar(
            dd("cidade-sel", cidade_options, default_cidade, label="Cidade"),
            dd("ano-sel",    ano_options,    default_ano,    label="Ano"),
        )
    """
    return html.Div(
        list(controls),
        className="d-flex flex-wrap gap-3 align-items-end mb-4 p-3 rounded",
        style={
            "background": "rgba(234,246,251,0.7)",
            "border": "1px solid #b3d6e6",
            "borderRadius": "10px",
        },
    )
