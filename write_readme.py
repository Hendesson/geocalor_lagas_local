readme = """\
# GeoCalor Dashboard — Versão Local

Dashboard interativo de ondas de calor e saúde para as Regiões Metropolitanas brasileiras.
Esta versão roda **100% localmente**, sem MotherDuck nem conta em nuvem.
Os dados pesados (parquets e mapas HTML) **não estão no repositório** — solicite ao Hendesson.

---

## Índice

1. [Estrutura do projeto](#1-estrutura-do-projeto)
2. [O que está no repo vs. o que solicitar](#2-o-que-está-no-repo-vs-o-que-solicitar)
3. [Instalação passo a passo](#3-instalação-passo-a-passo)
4. [Como executar](#4-como-executar)
5. [Descrição de cada arquivo](#5-descrição-de-cada-arquivo)
6. [Páginas do dashboard](#6-páginas-do-dashboard)
7. [Como o modo local funciona](#7-como-o-modo-local-funciona)

---

## 1. Estrutura do projeto

```
geocalor_local-/
│
│  ── Raiz ───────────────────────────────────────────────────────────────────
├── app.py                    ← Ponto de entrada: Dash, navbar, roteamento, callbacks
├── config.py                 ← Paleta de cores, layout Plotly base, YEAR_MIN/MAX
├── config_paths.py           ← Caminhos absolutos (BASE_DIR, DATA_DIR, PROCESSED_DIR…)
├── db.py                     ← DuckDB in-memory + registro automático de VIEWs nos parquets
├── data_processing.py        ← DataProcessor: carga, normalização e agregações do clima
├── data_sih_sim.py           ← Leitura dos parquets SIH/SIM pré-agregados
├── visualization.py          ← Visualizer: fábrica de figuras Plotly
├── cache_manager.py          ← CacheManager (joblib) + decorator @cached_dataframe
├── nota_tecnica_html.py      ← HTML das notas técnicas (rotas Flask /nota-tecnica-*)
├── prepare_sih_sim_data.py   ← Script standalone de pré-processamento (roda 1 vez)
├── requirements.txt
│
│  ── pages/ ─────────────────────────────────────────────────────────────────
├── pages/
│   ├── inicio.py             → rota /
│   ├── temperaturas.py       → rota /temperaturas
│   ├── ondas.py              → rota /ondas
│   ├── sistemas_alerta.py    → rota /sistemas-alerta
│   ├── sih_sim.py            → rota /sih-sim
│   └── contato.py            → rota /contato
│
│  ── components/ ────────────────────────────────────────────────────────────
├── components/
│   ├── cards.py              ← chart_card, info_card, kpi_box
│   └── controls.py           ← dd (Dropdown padronizado), filter_bar
│
│  ── assets/ ────────────────────────────────────────────────────────────────
├── assets/
│   ├── custom.css            ← Estilos globais
│   ├── geocalor.png          ← Logo da navbar
│   ├── *.png / *.jpg         ← Fotos da equipe e logos dos apoiadores
│   └── sistemas_alerta/
│       ├── images/           ← Infográficos de sistemas de alerta
│       └── json/             ← GeoJSONs de países e RMs
│
│  ── data/ (incluído no repo — fallback Excel) ──────────────────────────────
├── data/
│   ├── temp.xlsx             ← Dado climático Excel (usado quando parquet ausente)
│   └── temp1.xlsx
│
│  ── processed/ (NÃO versionado — solicite ao Hendesson) ───────────────────
├── processed/
│   ├── banco_dados_climaticos_consolidado (2).parquet  ← dado principal (+300 MB)
│   ├── medias_HW_Severe_Extreme.parquet
│   └── sih_sim/
│       ├── geojson_rm.json                   ← GeoJSON das RMs (~50 MB)
│       ├── populacao_RM.parquet
│       ├── sih_cardiovascular_car_int.parquet
│       ├── sih_cardiovascular_espec.parquet
│       ├── sih_cardiovascular_faixa_etaria.parquet
│       ├── sih_cardiovascular_mapa_mun.parquet
│       ├── sih_cardiovascular_raca.parquet
│       ├── sih_cardiovascular_serie_mensal.parquet
│       ├── sih_cardiovascular_sexo_ano.parquet
│       ├── sih_cardiovascular_taxa_anual.parquet
│       ├── sih_respiratorias_*.parquet         (8 arquivos, mesma estrutura)
│       ├── sim_cardiovascular_estciv.parquet
│       ├── sim_cardiovascular_faixa_etaria.parquet
│       ├── sim_cardiovascular_lococor.parquet
│       ├── sim_cardiovascular_mapa_mun.parquet
│       ├── sim_cardiovascular_raca.parquet
│       ├── sim_cardiovascular_serie_mensal.parquet
│       ├── sim_cardiovascular_sexo_ano.parquet
│       ├── sim_cardiovascular_taxa_anual.parquet
│       └── sim_respiratorias_*.parquet         (8 arquivos, mesma estrutura)
│
│  ── mapa_eventos/ (NÃO versionado — solicite ao Hendesson) ─────────────────
├── mapa_eventos/
│   ├── mapa_interativo.html  → rota /mapa-eventos-extremos
│   └── mapa_geral.html       → rota /mapa-eventos-geral
│
│  ── cache/ (gerado em runtime) ─────────────────────────────────────────────
└── cache/
    └── *.pkl                 ← Gerado automaticamente na 1ª execução
```

---

## 2. O que está no repo vs. o que solicitar

### Incluído no repositório

| O que é | Onde fica |
|---------|-----------|
| Todo o código Python | `*.py`, `pages/`, `components/` |
| CSS e imagens da interface | `assets/` |
| Dado climático em Excel (fallback) | `data/temp.xlsx`, `data/temp1.xlsx` |
| Dependências | `requirements.txt` |

### Solicitar ao Hendesson (arquivos grandes, fora do repo)

| Arquivo | Onde colocar após receber |
|---------|--------------------------|
| `banco_dados_climaticos_consolidado (2).parquet` | `processed/` |
| `medias_HW_Severe_Extreme.parquet` | `processed/` |
| `geojson_rm.json` | `processed/sih_sim/` |
| `populacao_RM.parquet` | `processed/sih_sim/` |
| `sih_cardiovascular_car_int.parquet` | `processed/sih_sim/` |
| `sih_cardiovascular_espec.parquet` | `processed/sih_sim/` |
| `sih_cardiovascular_faixa_etaria.parquet` | `processed/sih_sim/` |
| `sih_cardiovascular_mapa_mun.parquet` | `processed/sih_sim/` |
| `sih_cardiovascular_raca.parquet` | `processed/sih_sim/` |
| `sih_cardiovascular_serie_mensal.parquet` | `processed/sih_sim/` |
| `sih_cardiovascular_sexo_ano.parquet` | `processed/sih_sim/` |
| `sih_cardiovascular_taxa_anual.parquet` | `processed/sih_sim/` |
| `sih_respiratorias_car_int.parquet` | `processed/sih_sim/` |
| `sih_respiratorias_espec.parquet` | `processed/sih_sim/` |
| `sih_respiratorias_faixa_etaria.parquet` | `processed/sih_sim/` |
| `sih_respiratorias_mapa_mun.parquet` | `processed/sih_sim/` |
| `sih_respiratorias_raca.parquet` | `processed/sih_sim/` |
| `sih_respiratorias_serie_mensal.parquet` | `processed/sih_sim/` |
| `sih_respiratorias_sexo_ano.parquet` | `processed/sih_sim/` |
| `sih_respiratorias_taxa_anual.parquet` | `processed/sih_sim/` |
| `sim_cardiovascular_estciv.parquet` | `processed/sih_sim/` |
| `sim_cardiovascular_faixa_etaria.parquet` | `processed/sih_sim/` |
| `sim_cardiovascular_lococor.parquet` | `processed/sih_sim/` |
| `sim_cardiovascular_mapa_mun.parquet` | `processed/sih_sim/` |
| `sim_cardiovascular_raca.parquet` | `processed/sih_sim/` |
| `sim_cardiovascular_serie_mensal.parquet` | `processed/sih_sim/` |
| `sim_cardiovascular_sexo_ano.parquet` | `processed/sih_sim/` |
| `sim_cardiovascular_taxa_anual.parquet` | `processed/sih_sim/` |
| `sim_respiratorias_estciv.parquet` | `processed/sih_sim/` |
| `sim_respiratorias_faixa_etaria.parquet` | `processed/sih_sim/` |
| `sim_respiratorias_lococor.parquet` | `processed/sih_sim/` |
| `sim_respiratorias_mapa_mun.parquet` | `processed/sih_sim/` |
| `sim_respiratorias_raca.parquet` | `processed/sih_sim/` |
| `sim_respiratorias_serie_mensal.parquet` | `processed/sih_sim/` |
| `sim_respiratorias_sexo_ano.parquet` | `processed/sih_sim/` |
| `sim_respiratorias_taxa_anual.parquet` | `processed/sih_sim/` |
| `mapa_interativo.html` | `mapa_eventos/` |
| `mapa_geral.html` | `mapa_eventos/` |

> As páginas /temperaturas e /ondas só precisam de
> `banco_dados_climaticos_consolidado (2).parquet`.
> A página /sih-sim fica em branco sem os arquivos de `sih_sim/`.

---

## 3. Instalação passo a passo

```powershell
# 1. Clone
git clone https://github.com/Hendesson/geocalor_local-.git
cd geocalor_local-

# 2. Ambiente virtual
python -m venv .venv
.venv\\Scripts\\activate          # Windows
# source .venv/bin/activate       # Linux/Mac

# 3. Dependências
pip install -r requirements.txt

# 4. Crie as pastas de dados (se não existirem)
mkdir processed
mkdir processed\\sih_sim
mkdir mapa_eventos
mkdir cache

# 5. Copie os arquivos recebidos para os caminhos da tabela acima
```

---

## 4. Como executar

Execute **sempre de dentro da pasta do projeto**:

```powershell
cd geocalor_local-
python app.py
```

Acesse `http://127.0.0.1:8050` no navegador.

Mudar porta:
```powershell
set PORT=8080 && python app.py    # Windows
PORT=8080 python app.py           # Linux/Mac
```

Servidor de produção:
```bash
gunicorn app:server -b 0.0.0.0:8050 --workers 2
```

---

## 5. Descrição de cada arquivo

### `db.py`

Cria uma conexão DuckDB **in-memory** e registra automaticamente uma VIEW SQL para cada
`.parquet` encontrado em `processed/` e `processed/sih_sim/`. O restante do código faz
`SELECT` nessas VIEWs como tabelas normais — sem servidor, sem token.

| Função | O que faz |
|--------|-----------|
| `get_conn()` | Retorna a conexão DuckDB da thread atual |
| `execute(sql, params)` | Executa SQL; chame `.df()` para pandas DataFrame |
| `table_ref(name)` | Retorna `"name"` entre aspas para f-strings SQL |

VIEWs criadas automaticamente:

| VIEW | Parquet |
|------|---------|
| `clima` | `processed/banco_dados_climaticos_consolidado (2).parquet` |
| `medias_hw` | `processed/medias_HW_Severe_Extreme.parquet` |
| `sih_cardiovascular_taxa_anual` | `processed/sih_sim/sih_cardiovascular_taxa_anual.parquet` |
| *(todos os demais .parquet em sih_sim/)* | *(registrados automaticamente)* |

---

### `data_processing.py`

Classe `DataProcessor`. Fonte de dados por prioridade:
1. `processed/banco_dados_climaticos_consolidado (2).parquet`
2. `data/temp.xlsx` (fallback)

Colunas do dado climático:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `index` | datetime | Data |
| `cidade` | string | Nome da capital |
| `year` / `month` | int | Ano / Mês |
| `tmax` / `tmin` / `tmed` | float | Temperaturas diárias (°C) |
| `isHW` | string | `"TRUE"` se dia de onda de calor |
| `intensidade` | string | `"Low Intensity"`, `"Severe"` ou `"Extreme"` |

Métodos principais (todos cacheados em `cache/`):

| Método | Retorna | Página |
|--------|---------|--------|
| `load_data()` | DataFrame completo | startup |
| `calculate_hw_monthly(cidade, ano)` | Dias OC por mês | /ondas |
| `calculate_hw_events(cidade, ano)` | Eventos (>=3 dias) por mês | /ondas |
| `prepare_heatmap_data()` | cidade x ano com dias OC | /ondas |
| `prepare_heatmap_events_data()` | cidade x ano com eventos | /ondas |

---

### `data_sih_sim.py`

Funções que leem parquets de `processed/sih_sim/`.
Nome dos arquivos: `<sih|sim>_<cardiovascular|respiratorias>_<agregacao>.parquet`

| Função | Retorna |
|--------|---------|
| `rms_disponiveis(sistema, causa)` | Lista de RMs disponíveis |
| `anos_disponiveis(sistema, causa, rm)` | Anos com dados |
| `serie_mensal(sistema, causa, rm)` | Série mensal (ANO, MES, N) |
| `taxa_anual(sistema, causa, rm)` | Taxa por 1.000 hab. por ano |
| `sexo_por_ano(sistema, causa, rm)` | Contagem por sexo e ano |
| `raca_cor(sistema, causa, rm)` | Distribuição por raça/cor |
| `faixa_etaria(sistema, causa, rm)` | Distribuição etária |
| `car_int(causa, rm)` | Caráter de internação — SIH |
| `espec(causa, rm)` | Especialidade do leito top 12 — SIH |
| `lococor(causa, rm)` | Local do óbito — SIM |
| `estciv(causa, rm)` | Estado civil — SIM |
| `mapa_data(sistema, causa, rm, ano)` | GeoJSON + taxa municipal |

---

### `cache_manager.py`

Salva DataFrames em `cache/*.pkl` com joblib (compressão nível 3).
Na segunda execução o dashboard inicia mais rápido por usar o cache.

Limpar após trocar os parquets:
```powershell
del cache\\*.pkl
```

---

### `visualization.py`

Classe `Visualizer`: recebe DataFrames e devolve figuras `go.Figure` do Plotly.
Usada por /temperaturas e /ondas. Todos os gráficos usam `LAYOUT_BASE` de `config.py`.

---

### `config.py`

| Constante | Valor | Uso |
|-----------|-------|-----|
| `PRIMARY` | `#1761a0` | Azul — navbar, títulos |
| `ORANGE` | `#ff9f1c` | OC Low Intensity |
| `RED` | `#e63946` | OC Severe |
| `DARK_RED` | `#dc2f3d` | OC Extreme |
| `LAYOUT_BASE` | dict | Base de todos os gráficos Plotly |
| `YEAR_MIN / YEAR_MAX` | 1981 / 2023 | Limites temporais dos dados |

---

### `prepare_sih_sim_data.py`

Script standalone — não é importado pelo dashboard.
Gera os parquets de `sih_sim/` a partir dos CSVs brutos do DataSUS.
Execute uma única vez se quiser regenerar os dados:
```powershell
python prepare_sih_sim_data.py
```

---

## 6. Páginas do dashboard

| URL | Arquivo | Conteúdo |
|-----|---------|----------|
| `/` | `pages/inicio.py` | Apresentação, logos dos apoiadores |
| `/temperaturas` | `pages/temperaturas.py` | Séries de temperatura, anomalias, heatmap |
| `/ondas` | `pages/ondas.py` | Frequência de OC, eventos, calendário, heatmap |
| `/sistemas-alerta` | `pages/sistemas_alerta.py` | Sistemas de alerta com mapas e infográficos |
| `/sih-sim` | `pages/sih_sim.py` | Internações e óbitos por doença, RM e ano |
| `/contato` | `pages/contato.py` | Equipe e contato |

Cada página exporta:
- `layout_<nome>(app, ...)` — layout Dash da página
- `register_callbacks_<nome>(app, ...)` — callbacks interativos

---

## 7. Como o modo local funciona

O `db.py` substitui o MotherDuck por DuckDB in-memory + parquets locais.
O restante do código é **idêntico** à versão em nuvem.

```
processed/*.parquet          lidos no startup
processed/sih_sim/*.parquet  ---> VIEWs DuckDB in-memory
                                        |
                    data_processing.py  SELECT * FROM "clima"
                    data_sih_sim.py     SELECT * FROM "sih_cardiovascular_*"
                                        |
                               páginas Dash (código sem diferença)
```

Se `banco_dados_climaticos_consolidado (2).parquet` não existir,
o `DataProcessor` usa `data/temp.xlsx` automaticamente como fallback.
"""

with open(r"C:\tmp\geocalor_local-\README.md", "w", encoding="utf-8") as f:
    f.write(readme)
print("README escrito com sucesso")
