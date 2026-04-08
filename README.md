# GeoCalor Dashboard — Versão Local

Dashboard interativo de ondas de calor e saúde para as Regiões Metropolitanas brasileiras.  
Esta versão roda **100% localmente**, sem MotherDuck nem nenhuma conta em nuvem.  
Os dados ficam em arquivos Parquet dentro de `processed/` — solicite-os ao responsável pelo projeto.

---

## Estrutura de pastas

```
geocalor_lagas_local/
│
├── app.py                    ← Ponto de entrada do Dash (roteamento + navbar + callbacks globais)
├── config.py                 ← Paleta de cores e layout base Plotly
├── config_paths.py           ← Caminhos do projeto (BASE_DIR, DATA_DIR, PROCESSED_DIR, …)
├── db.py                     ← Conexão DuckDB in-memory + registro automático de VIEWs nos parquets
├── data_processing.py        ← DataProcessor: carga e agregações do dado climático
├── data_sih_sim.py           ← Leitura dos parquets SIH/SIM pré-agregados
├── visualization.py          ← Visualizer: fábrica de figuras Plotly
├── cache_manager.py          ← Cache joblib + decorator @cached_dataframe
├── nota_tecnica_html.py      ← HTML estático das notas técnicas (rotas Flask)
├── prepare_sih_sim_data.py   ← Script de pré-processamento (roda UMA vez, não é importado)
├── requirements.txt
│
├── pages/                    ← Uma página Dash por arquivo
│   ├── inicio.py             → /
│   ├── temperaturas.py       → /temperaturas
│   ├── ondas.py              → /ondas
│   ├── sistemas_alerta.py    → /sistemas-alerta
│   ├── sih_sim.py            → /sih-sim
│   └── contato.py            → /contato
│
├── components/               ← Componentes reutilizáveis (cards, dropdowns, filter_bar)
│
├── assets/                   ← CSS, imagens, JS — servidos automaticamente pelo Dash
│
├── processed/                ← Parquets prontos (NÃO versionados — solicite ao responsável)
│   ├── banco_dados_climaticos_consolidado (2).parquet
│   ├── medias_HW_Severe_Extreme.parquet
│   └── sih_sim/
│       ├── geojson_rm.json
│       ├── populacao_RM.parquet
│       ├── sih_cardiovascular_*.parquet
│       ├── sih_respiratorias_*.parquet
│       ├── sim_cardiovascular_*.parquet
│       └── sim_respiratorias_*.parquet
│
├── data/                     ← Excel legado (fallback quando parquet não existe)
├── cache/                    ← Cache gerado em runtime (não versionar)
└── mapa_eventos/             ← HTMLs dos mapas de eventos (solicite ao responsável)
    ├── mapa_interativo.html  → rota /mapa-eventos-extremos
    └── mapa_geral.html       → rota /mapa-eventos-geral
```

---

## Arquivos de dados necessários

Os arquivos abaixo **não estão no repositório** (tamanho). Peça ao responsável e coloque nos caminhos indicados:

| Arquivo | Onde colocar |
|---------|-------------|
| `banco_dados_climaticos_consolidado (2).parquet` | `processed/` |
| `medias_HW_Severe_Extreme.parquet` | `processed/` |
| `geojson_rm.json` | `processed/sih_sim/` |
| `populacao_RM.parquet` | `processed/sih_sim/` |
| `sih_cardiovascular_*.parquet` (8 arquivos) | `processed/sih_sim/` |
| `sih_respiratorias_*.parquet` (8 arquivos) | `processed/sih_sim/` |
| `sim_cardiovascular_*.parquet` (8 arquivos) | `processed/sih_sim/` |
| `sim_respiratorias_*.parquet` (8 arquivos) | `processed/sih_sim/` |
| `mapa_interativo.html` | `mapa_eventos/` |
| `mapa_geral.html` | `mapa_eventos/` |

---

## Instalação e execução

```bash
# 1. Clone
git clone https://github.com/Hendesson/geocalor_lagas_local.git
cd geocalor_lagas_local

# 2. Ambiente virtual
python -m venv .venv
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 3. Dependências
pip install -r requirements.txt

# 4. Coloque os parquets em processed/ (veja tabela acima)

# 5. Execute
python app.py
```

Acesse `http://127.0.0.1:8050`.

---

## Como funciona (sem MotherDuck)

`db.py` cria uma conexão **DuckDB in-memory** e registra automaticamente uma VIEW SQL
para cada `.parquet` encontrado em `processed/` e `processed/sih_sim/`.  
Todos os módulos (`data_processing.py`, `data_sih_sim.py`) fazem `SELECT` nessas VIEWs
como se fossem tabelas normais — sem nenhuma diferença de código em relação à versão em nuvem.

```
processed/*.parquet          ┐
processed/sih_sim/*.parquet  ┘  ← lidos por db.py no startup

         ↓ VIEWs DuckDB in-memory

data_processing.py  →  DataProcessor  →  páginas /temperaturas e /ondas
data_sih_sim.py     →  funções livres  →  página /sih-sim
```

---

## Diferença em relação à versão com MotherDuck

| | Versão local (este repo) | Versão nuvem |
|---|---|---|
| `db.py` | DuckDB in-memory + parquets locais | MotherDuck (token obrigatório) |
| `MOTHERDUCK_TOKEN` | não necessário | obrigatório |
| Mapas de eventos | arquivo em `mapa_eventos/` | blob em tabela `mapa_html` |
| GeoJSON SIH/SIM | `processed/sih_sim/geojson_rm.json` | blob em tabela `mapa_html` |
