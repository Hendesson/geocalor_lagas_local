import plotly.express as px
import plotly.graph_objs as go
from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np
import logging

from config import PRIMARY, TEAL, GREEN, ORANGE, RED, GRID_COLOR, LAYOUT_BASE, WHITE

logger = logging.getLogger(__name__)


class Visualizer:
    """Paleta alinhada ao tema GeoCalor / custom.css do dashboard."""

    def _layout_temp_padrao(self, title: str, height: int = 400) -> dict:
        """Layout base para gráficos de temperaturas/séries temporais."""
        base = {**LAYOUT_BASE}
        base.update(
            title=dict(text=title, x=0.5, xanchor="center", font=dict(size=16, color=PRIMARY)),
            hovermode="x unified",
            height=height,
            margin=dict(l=56, r=28, t=72, b=56),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(255,255,255,0.85)",
            ),
        )
        return base

    def _axes_temp_grid(self, fig: go.Figure) -> None:
        """Grade padronizada para gráficos de temperatura."""
        fig.update_xaxes(
            showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
            linecolor="rgba(0,0,0,0.15)",
        )
        fig.update_yaxes(
            showgrid=True, gridcolor=GRID_COLOR, zeroline=True,
            zerolinecolor="rgba(0,0,0,0.2)", linecolor="rgba(0,0,0,0.15)",
        )

    def create_temperature_plot(
        self,
        df: pd.DataFrame,
        cidade: str,
        ano_inicio: int,
        ano_fim: int,
    ) -> go.Figure:
        if df.empty:
            return go.Figure()

        logger.info("create_temperature_plot: cidade='%s', anos=%s-%s", cidade, ano_inicio, ano_fim)

        dff = df[
            (df["cidade"] == cidade)
            & (df["year"] >= ano_inicio)
            & (df["year"] <= ano_fim)
        ]

        if dff.empty:
            logger.warning("Nenhum dado após filtro — cidade=%s, anos=%s-%s", cidade, ano_inicio, ano_fim)
            return go.Figure()

        # Scattergl (WebGL) para datasets grandes — muito mais rápido no browser
        Trace = go.Scattergl if len(dff) > 1500 else go.Scatter
        fig = go.Figure()
        fig.add_trace(Trace(x=dff["index"], y=dff["tempMax"], name="Máxima",
                            mode="lines", line=dict(color=RED)))
        fig.add_trace(Trace(x=dff["index"], y=dff["tempMed"], name="Média",
                            mode="lines", line=dict(color=ORANGE)))
        fig.add_trace(Trace(x=dff["index"], y=dff["tempMin"], name="Mínima",
                            mode="lines", line=dict(color=TEAL)))

        fig.update_layout(
            **self._layout_temp_padrao(
                f"Temperaturas diárias — {cidade} ({ano_inicio}–{ano_fim})"
            ),
            xaxis_title="Data",
            yaxis_title="Temperatura (°C)",
        )
        self._axes_temp_grid(fig)
        return fig

    def create_heatmap(self, df_heatmap: pd.DataFrame) -> go.Figure:
        if df_heatmap.empty:
            return go.Figure()

        fig = px.density_heatmap(
            df_heatmap,
            x="year", y="cidade", z="dias_hw",
            color_continuous_scale="OrRd",
            labels={"dias_hw": "Dias de Onda de Calor"},
            title=(
                f"Total de Dias de Onda de Calor por Cidade e Ano "
                f"({df_heatmap['year'].min()}-{df_heatmap['year'].max()})"
            ),
        )
        fig.update_layout(
            xaxis=dict(title="Ano", tickangle=45, tickfont=dict(size=10),
                       tickmode="linear", dtick=1, gridcolor="rgba(0,0,0,0.1)"),
            yaxis=dict(title="Cidade", tickfont=dict(size=10), automargin=True),
            coloraxis_colorbar=dict(
                title=dict(text="Dias de Onda de Calor", font=dict(size=14)),
                tickfont=dict(size=12),
            ),
            height=600,
            margin=dict(l=150, r=50, t=100, b=100),
            plot_bgcolor=WHITE,
            paper_bgcolor=WHITE,
        )
        return fig

    def create_polar_plot(
        self,
        df_polar: pd.DataFrame,
        cidade: str,
        ano: Optional[int],
    ) -> go.Figure:
        if df_polar.empty or df_polar["frequencia"].sum() == 0:
            fig = go.Figure()
            fig.add_annotation(
                text="Nenhuma onda de calor registrada para esta cidade/ano",
                xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            )
            return fig

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=df_polar["frequencia"],
            theta=df_polar["mes"],
            fill="toself",
            fillcolor="rgba(255, 159, 28, 0.18)",
            mode="lines+markers",
            line=dict(color=ORANGE, width=2.5),
            marker=dict(color=ORANGE, size=8),
            name="Frequência",
        ))

        title = f"Frequência de Ondas de Calor em {cidade}"
        if ano is not None:
            title += f" — {ano}"
        else:
            title += " (1981 - 2023)"

        fig.update_layout(
            title=title,
            polar=dict(
                radialaxis=dict(visible=True, tickfont=dict(size=10), gridcolor=GRID_COLOR),
                angularaxis=dict(direction="clockwise", tickfont=dict(size=10)),
            ),
            showlegend=False,
            height=400,
            margin=dict(l=50, r=50, t=100, b=50),
            plot_bgcolor=WHITE,
            paper_bgcolor=WHITE,
        )
        return fig

    def create_umidity_plot(
        self,
        df: pd.DataFrame,
        cidade: str,
        ano_inicio: int,
        ano_fim: int,
    ) -> go.Figure:
        if df.empty:
            return go.Figure()

        dff = df[
            (df["cidade"] == cidade)
            & (df["year"] >= ano_inicio)
            & (df["year"] <= ano_fim)
        ]
        if dff.empty:
            return go.Figure()

        um_col = next(
            (c for c in ("HumidadeMed", "humidade", "UmidadeMed", "Umidade") if c in dff.columns),
            None,
        )
        if not um_col:
            return go.Figure()

        meses_nome = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
        }
        tmp = dff.assign(mes_num=dff["index"].dt.month)
        monthly = tmp.groupby("mes_num", as_index=False)[um_col].mean()
        monthly["mes"] = monthly["mes_num"].map(meses_nome)

        order = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
        ]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly["mes"], y=monthly[um_col], name="Umidade Média",
            line=dict(color=TEAL),
        ))
        fig.update_layout(
            **self._layout_temp_padrao(
                f"Umidade média mensal — {cidade} ({ano_inicio}–{ano_fim})", height=380
            ),
        )
        fig.update_xaxes(
            categoryorder="array", categoryarray=order, title=dict(text="Mês"),
            showgrid=True, gridcolor=GRID_COLOR, zeroline=False, linecolor="rgba(0,0,0,0.15)",
        )
        fig.update_yaxes(
            title=dict(text="Umidade relativa (%)"),
            showgrid=True, gridcolor=GRID_COLOR, zeroline=True,
            zerolinecolor="rgba(0,0,0,0.2)", linecolor="rgba(0,0,0,0.15)",
        )
        return fig

    def create_amplitude_plot(
        self,
        df: pd.DataFrame,
        cidade: str,
        ano_inicio: int,
        ano_fim: int,
    ) -> go.Figure:
        """Amplitude térmica diária (tempMax − tempMin) com média móvel de 30 dias."""
        if df.empty:
            return go.Figure()

        dff = df[
            (df["cidade"] == cidade)
            & (df["year"] >= ano_inicio)
            & (df["year"] <= ano_fim)
        ]

        if dff.empty or "tempMax" not in dff.columns or "tempMin" not in dff.columns:
            return go.Figure()

        dff = dff.sort_values("index")
        amplitude = dff["tempMax"] - dff["tempMin"]
        amp_mm30  = amplitude.rolling(window=30, min_periods=1).mean()

        Trace = go.Scattergl if len(dff) > 1500 else go.Scatter
        fig = go.Figure()
        fig.add_trace(Trace(
            x=dff["index"], y=amplitude, name="Amplitude diária",
            mode="lines", line=dict(color=GREEN, width=1.2),
            fill="tozeroy", fillcolor="rgba(110, 193, 166, 0.18)",
            hovertemplate="<b>%{x|%d/%m/%Y}</b><br>Amplitude: %{y:.1f} °C<extra></extra>",
        ))
        fig.add_trace(Trace(
            x=dff["index"], y=amp_mm30, name="Média móvel 30 dias",
            mode="lines", line=dict(color=PRIMARY, width=2.4, dash="dash"),
            hovertemplate="<b>%{x|%d/%m/%Y}</b><br>MM30: %{y:.1f} °C<extra></extra>",
        ))
        fig.update_layout(
            **self._layout_temp_padrao(
                f"Amplitude térmica diária — {cidade} ({ano_inicio}–{ano_fim})", height=400
            ),
            xaxis_title="Data",
            yaxis_title="Amplitude (°C)",
        )
        self._axes_temp_grid(fig)
        return fig

    def create_anomaly_plot(
        self,
        df: pd.DataFrame,
        cidade: str,
        ano_inicio: int,
        ano_fim: int,
    ) -> go.Figure:
        """Anomalia de temperatura mensal vs. climatologia da série filtrada."""
        if df.empty:
            return go.Figure()

        dff = df[
            (df["cidade"] == cidade)
            & (df["year"] >= ano_inicio)
            & (df["year"] <= ano_fim)
        ]

        if dff.empty or "tempMed" not in dff.columns:
            return go.Figure()

        month_s      = dff["index"].dt.month
        year_month_s = dff["index"].dt.to_period("M")
        climatologia = dff.groupby(month_s)["tempMed"].mean()

        mensal = (
            dff.assign(_m=month_s, _ym=year_month_s)
            .groupby(["_ym", "_m"])["tempMed"].mean()
            .reset_index()
            .rename(columns={"_m": "month", "_ym": "year_month"})
        )
        mensal["anomalia"] = mensal["tempMed"] - mensal["month"].map(climatologia)
        mensal["date"]     = mensal["year_month"].dt.to_timestamp()
        mensal = mensal.dropna(subset=["anomalia"])

        if mensal.empty:
            return go.Figure()

        colors = [RED if a >= 0 else TEAL for a in mensal["anomalia"]]

        # dtick dinâmico: evita rótulos sobrepostos quando muitos anos selecionados
        n_months = len(mensal)
        if n_months > 240:      # > 20 anos → rótulo a cada 2 anos
            dtick_val, tick_fmt, tick_angle = "M24", "%Y", -45
        elif n_months > 96:     # > 8 anos → rótulo anual
            dtick_val, tick_fmt, tick_angle = "M12", "%Y", -45
        elif n_months > 36:     # > 3 anos → semestral
            dtick_val, tick_fmt, tick_angle = "M6", "%b %Y", -35
        else:
            dtick_val, tick_fmt, tick_angle = "M3", "%b %Y", -35

        # Altura proporcional: mais espaço para muitas barras
        chart_h = 420 if n_months <= 60 else 460

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=mensal["date"], y=mensal["anomalia"], name="Anomalia",
            marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.35)", width=0.5)),
            hovertemplate="<b>%{x|%b %Y}</b><br>Anomalia: %{y:+.2f} °C<extra></extra>",
        ))
        fig.add_hline(y=0, line_dash="solid", line_color=PRIMARY, line_width=1.2, opacity=0.45)
        fig.update_layout(
            **self._layout_temp_padrao(
                f"Anomalia de temperatura média mensal — {cidade} ({ano_inicio}–{ano_fim})",
                height=chart_h,
            ),
            showlegend=False,
            bargap=0.15,
        )
        fig.update_xaxes(
            title=dict(text="Período"),
            tickformat=tick_fmt,
            tickangle=tick_angle,
            dtick=dtick_val,
            showgrid=True, gridcolor=GRID_COLOR, zeroline=False, linecolor="rgba(0,0,0,0.15)",
        )
        fig.update_yaxes(
            title=dict(text="Anomalia em relação à média mensal (°C)"),
            showgrid=True, gridcolor=GRID_COLOR, zeroline=True,
            zerolinecolor="rgba(0,0,0,0.2)", linecolor="rgba(0,0,0,0.15)",
        )
        return fig

    def create_temperature_hw_plot(
        self,
        df: pd.DataFrame,
        cidade: str,
        ano: int,
    ) -> go.Figure:
        if df.empty:
            return go.Figure()

        dff = df[(df["cidade"] == cidade) & (df["year"] == ano)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dff["index"], y=dff["tempMax"], mode="lines+markers",
                                 name="Máxima", line=dict(color=RED), marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=dff["index"], y=dff["tempMed"], mode="lines+markers",
                                 name="Média", line=dict(color=ORANGE), marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=dff["index"], y=dff["tempMin"], mode="lines+markers",
                                 name="Mínima", line=dict(color=TEAL), marker=dict(size=4)))

        _intensity_opacity = {"low-intensity": 0.4, "severe": 0.6, "extreme": 0.8}
        threshold_95 = dff["tempMax"].quantile(0.95) if not dff["tempMax"].empty else None
        half_day = pd.Timedelta(days=0.5)

        _isHW_mask = (dff["isHW"] == "TRUE") | (dff["isHW"] == True)
        hw_df    = dff[_isHW_mask]
        opacities = hw_df["HW_Intensity"].fillna("").astype(str).str.strip().str.lower().map(_intensity_opacity).fillna(0.3)
        shapes = [
            {
                "type": "rect", "xref": "x", "yref": "paper",
                "x0": idx - half_day, "x1": idx + half_day,
                "y0": 0, "y1": 1,
                "fillcolor": ORANGE, "opacity": float(op),
                "line": {"width": 0}, "layer": "below",
            }
            for idx, op in zip(hw_df["index"], opacities)
        ]
        ann_df = hw_df[hw_df["HWDay_Intensity"].notna()]
        hw_annotations = [
            {
                "x": idx, "y": 1.02, "xref": "x", "yref": "paper",
                "text": str(txt), "showarrow": False,
                "bgcolor": "rgba(255,159,28,0.6)", "bordercolor": ORANGE,
                "borderwidth": 1, "borderpad": 2,
                "font": {"color": "white", "size": 9},
                "xanchor": "center", "yanchor": "bottom",
            }
            for idx, txt in zip(ann_df["index"], ann_df["HWDay_Intensity"])
        ]
        if threshold_95 is not None:
            pk_df = dff[dff["tempMax"] >= threshold_95]
            peak_annotations = [
                {
                    "x": idx, "y": tmax, "xref": "x", "yref": "y",
                    "text": "Pico", "showarrow": True, "arrowhead": 2,
                    "ax": 0, "ay": -40,
                    "bgcolor": "rgba(230,57,70,0.8)", "bordercolor": RED,
                    "borderwidth": 1, "borderpad": 4, "opacity": 0.9,
                    "font": {"color": "white", "size": 10},
                }
                for idx, tmax in zip(pk_df["index"], pk_df["tempMax"])
            ]
        else:
            peak_annotations = []

        fig.update_layout(
            title=f"Temperaturas Diárias e Ondas de Calor — {cidade}, {ano}",
            xaxis_title="Data", yaxis_title="Temperatura (°C)",
            plot_bgcolor=WHITE, paper_bgcolor=WHITE,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            shapes=shapes,
            annotations=peak_annotations + hw_annotations,
        )
        return fig

    def create_umidity_hw_plot(
        self,
        df: pd.DataFrame,
        cidade: str,
        ano: int,
    ) -> go.Figure:
        if df.empty:
            return go.Figure()

        dff = df[(df["cidade"] == cidade) & (df["year"] == ano)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dff["index"], y=dff["HumidadeMed"], mode="lines+markers",
            name="Umidade Média", line=dict(color=TEAL), marker=dict(size=4),
        ))

        _intensity_opacity = {"low-intensity": 0.4, "severe": 0.6, "extreme": 0.8}
        half_day = pd.Timedelta(days=0.5)

        _isHW_mask2 = (dff["isHW"] == "TRUE") | (dff["isHW"] == True)
        hw_df     = dff[_isHW_mask2]
        opacities = hw_df["HW_Intensity"].fillna("").astype(str).str.strip().str.lower().map(_intensity_opacity).fillna(0.3)
        shapes = [
            {
                "type": "rect", "xref": "x", "yref": "paper",
                "x0": idx - half_day, "x1": idx + half_day,
                "y0": 0, "y1": 1,
                "fillcolor": ORANGE, "opacity": float(op),
                "line": {"width": 0}, "layer": "below",
            }
            for idx, op in zip(hw_df["index"], opacities)
        ]
        ann_df = hw_df[hw_df["HWDay_Intensity"].notna()]
        hw_annotations = [
            {
                "x": idx, "y": 1.02, "xref": "x", "yref": "paper",
                "text": str(txt), "showarrow": False,
                "bgcolor": "rgba(255,159,28,0.6)", "bordercolor": ORANGE,
                "borderwidth": 1, "borderpad": 2,
                "font": {"color": "white", "size": 9},
                "xanchor": "center", "yanchor": "bottom",
            }
            for idx, txt in zip(ann_df["index"], ann_df["HWDay_Intensity"])
        ]

        fig.update_layout(
            title=f"Umidade Diária e Ondas de Calor — {cidade}, {ano}",
            xaxis_title="Data", yaxis_title="Umidade Relativa (%)",
            plot_bgcolor=WHITE, paper_bgcolor=WHITE,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            shapes=shapes, annotations=hw_annotations,
        )
        return fig
