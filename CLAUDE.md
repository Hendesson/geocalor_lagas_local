# GeoCalor Dashboard — Guia para Claude Code

## O que é este projeto

Dashboard interativo em **Python/Dash** para análise de ondas de calor e saúde nas Regiões Metropolitanas do Brasil. Desenvolvido pelo Projeto GeoCalor (LAGAS/UnB, Fiocruz/OCS, LASA-UFRJ & LMI-Sentinela).

Roda localmente com `python app.py` — **sem MotherDuck, sem banco remoto**.

---

## Estrutura de arquivos

```
app.py                  # Ponto de entrada, roteamento, layout global
config.py               # Cores, LAYOUT_BASE Plotly, YEAR_MIN/YEAR_MAX
config_paths.py         # Caminhos (BASE_DIR, PROCESSED_DIR, CACHE_DIR…)
data_processing.py      # DataProcessor — carga e cálculos dos dados
visualization.py        # Visualizer — todos os gráficos Plotly
nota_tecnica_html.py    # HTML das 3 notas técnicas (PDF-friendly)
cache_manager.py        # Decorator @cached_dataframe para performance
db.py                   # Abstração de leitura (Parquet local)

pages/
  inicio.py             # /  → Sobre o GeoCalor, apoiadores
  temperaturas.py       # /temperaturas → Caracterização Climática das RMB
  ondas.py              # /ondas → Análise de Ondas de Calor
  sistemas_alerta.py    # /sistemas-alerta
  sih_sim.py            # /sih-sim → Internações e óbitos (SIH/SIM)
  contato.py            # /contato → Equipe

components/
  cards.py              # chart_card(), info_card(), kpi_box()
  controls.py           # dd() (dropdown), filter_bar()

assets/
  custom.css            # CSS completo — paleta, cards, responsividade
  geocalor.png          # Logo principal (usado no header de cada página)
  lmi_logo.png          # LMI-Sentinela
  ufrj_logo.png         # LASA-UFRJ
  unb.png, fiocruz.png  # Logos institucionais
  sistemas_alerta/images/lagasLogo.png
  sistemas_alerta/images/geocalorLogo.png

processed/              # NÃO está no git — enviar manualmente
  banco_dados_climaticos_consolidado (2).parquet   # Dados climáticos principais
  medias_HW_Severe_Extreme.parquet
  sih_sim/              # Dados SIH/SIM

mapa_eventos/           # NÃO está no git — enviar manualmente
  mapa_geral.html       # Servido em /mapa-eventos-geral
  mapa_interativo.html  # Servido em /mapa-eventos-extremos
```

---

## Dataset principal

**Arquivo:** `processed/banco_dados_climaticos_consolidado (2).parquet`  
**Shape:** 234.865 linhas × 26 colunas  
**Período:** 1981–2024 (dashboard exibe até 2023)

### Colunas importantes

| Coluna | Descrição |
|--------|-----------|
| `index` | Data (datetime) |
| `cidade` | Nome da cidade |
| `year` | Ano |
| `tempMax`, `tempMed`, `tempMin` | Temperaturas diárias (°C) |
| `HumidadeMed` | Umidade relativa média (%) |
| `EHF` | Excess Heat Factor diário |
| `isHW` | Boolean — dia pertence a onda de calor |
| `HWDay_Intensity` | Intensidade **do dia** (`Low-Intensity`, `Severe`, `Extreme`, `Not HW`) |
| `HW_Intensity` | Intensidade **do evento** (`Low Intensity`, `Severe`, `Extreme`) ← usar para agrupar eventos |
| `HW_duration` | Duração do evento em dias |
| `group` | ID do grupo consecutivo de isHW |
| `thermalRange` | Amplitude térmica diária |
| `tempAnom` | Anomalia de temperatura |

> **Atenção crítica:** Para calcular estatísticas POR EVENTO (duração média, etc.) usar `HW_Intensity` + `HW_duration` + `drop_duplicates('group')`. Nunca usar `HWDay_Intensity` para isso — gera durações falsas menores que 3 dias.

### 15 Cidades (Regiões Metropolitanas)

Belém, Belo Horizonte, Brasília, Campo Grande, Curitiba, Florianópolis, Fortaleza, Goiânia, Manaus, Porto Alegre, Porto Velho, Recife, Rio de Janeiro, Salvador, São Paulo.

---

## Componentes de UI — padrão obrigatório

```python
from components import chart_card, info_card, kpi_box, dd

# Bloco de texto informativo/descritivo entre seções
info_card("", html.P("texto aqui", className="mb-0 text-muted"), fa_icon="fas fa-info-circle")

# Container de gráfico com header gradiente
chart_card("Título", [dcc.Graph(id="...")], fa_icon="fas fa-chart-line")

# Nota pequena abaixo de gráfico
chart_note("texto explicativo")  # definida localmente em cada page

# Dropdown padronizado
dd("id-do-dropdown", opcoes, valor_default, label="Rótulo")
```

**Não usar** `html.P` solto para textos descritivos entre seções — usar `info_card`.

---

## Paleta de cores (CSS vars + Python)

| Token | Hex | Uso |
|-------|-----|-----|
| `--color-primary` / `PRIMARY` | `#1761a0` | navbar, títulos, eixos |
| `--color-teal` / `TEAL` | `#2b9eb3` | destaques, gradiente |
| `--color-green` / `GREEN` | `#6ec1a6` | bordas, highlights |
| `ORANGE` | `#ff9f1c` | Baixa Intensidade OC |
| `RED` | `#e63946` | Severa OC |
| `DARK_RED` | `#dc2f3d` | Extrema OC |

---

## Identidade do projeto

**Nome completo:** `Projeto GeoCalor | LAGAS / UnB, Fiocruz/OCS, LASA-UFRJ & LMI-Sentinela`

Usar este nome em todas as notas técnicas e rodapés. As logos ficam em:
- `/assets/sistemas_alerta/images/lagasLogo.png`
- `/assets/sistemas_alerta/images/geocalorLogo.png`
- `/assets/unb.png`, `/assets/fiocruz.png`, `/assets/ufrj_logo.png`, `/assets/lmi_logo.png`

---

## Classificação de Ondas de Calor (EHF)

- **Definição OC:** ≥ 3 dias consecutivos com EHF > 0
- **Baixa Intensidade:** 0 < EHF ≤ EHF85
- **Severa:** EHF85 < EHF ≤ 3 × EHF85
- **Extrema:** EHF > 3 × EHF85
- **EHF85** = percentil 85 de todos os valores positivos do EHF histórico

---

## Notas técnicas (nota_tecnica_html.py)

Três constantes: `NOTA_TEMPERATURAS`, `NOTA_ONDAS`, `NOTA_SIH_SIM`.  
Servidas como HTML puro nas rotas `/nota-tecnica-temperaturas`, `/nota-tecnica-ondas`, `/nota-tecnica-sih-sim`.  
Sempre incluir as 4 logos institucionais e o nome completo do projeto.

---

## Git

- **Repositório:** https://github.com/Hendesson/geocalor_lagas_local
- **Branch:** `main`
- Commits **sempre** com perfil Hendesson — **nunca** adicionar `Co-Authored-By: Claude`
- `processed/`, `mapa_eventos/`, `data/`, `cache/` estão no `.gitignore`

---

## Mapas estáticos (mapa_eventos/)

São arquivos Folium pré-gerados, **não versionados**.  
Para regenerar `mapa_geral.html` usar `HW_Intensity` (não `HWDay_Intensity`) com `drop_duplicates('group')` para calcular duração por evento.

---

## Performance

- `cache_manager.py` tem decorator `@cached_dataframe` — usar em métodos pesados do `DataProcessor`
- `DataProcessor.load_data()` lê o parquet uma vez na inicialização do `app.py`
- Callbacks recebem o `df` já carregado — não reler dentro de callback
