"""
Gerenciador de conexão DuckDB — dados locais (parquets).

Uso:
    from db import get_conn

    conn = get_conn()
    df = conn.execute("SELECT * FROM clima WHERE cidade = ?", ["Belém"]).df()

Modo de operação: DuckDB in-memory com VIEWs apontando para os parquets em processed/.
Não é necessário nenhuma variável de ambiente ou conta em nuvem.
"""
import logging
import threading
from pathlib import Path

import duckdb

from config_paths import PROCESSED_DIR

logger = logging.getLogger(__name__)

# ── Caminhos dos parquets locais ─────────────────────────────────────────────
_BASE    = Path(PROCESSED_DIR)
_SIH_DIR = _BASE / "sih_sim"

_CORE_TABLES = {
    "clima":     _BASE / "banco_dados_climaticos_consolidado (2).parquet",
    "medias_hw": _BASE / "medias_HW_Severe_Extreme.parquet",
}

# ── Thread-local storage (DuckDB: uma conexão por thread) ────────────────────
_local = threading.local()

# Lista de parquets SIH/SIM — calculada uma vez no import, não a cada nova thread
_SIH_PARQUETS: list = sorted(_SIH_DIR.glob("*.parquet")) if _SIH_DIR.exists() else []


def _make_conn() -> duckdb.DuckDBPyConnection:
    """Cria conexão DuckDB in-memory e registra as VIEWs sobre os parquets."""
    logger.info("DuckDB local (in-memory) — registrando VIEWs…")
    conn = duckdb.connect(":memory:")
    _register_local_views(conn)
    return conn


def get_conn() -> duckdb.DuckDBPyConnection:
    """Retorna a conexão DuckDB da thread atual (cria se ainda não existir)."""
    if not hasattr(_local, "conn") or _local.conn is None:
        _local.conn = _make_conn()
    return _local.conn


def execute(sql: str, params: list | None = None):
    """Executa SQL e retorna DuckDBPyRelation (chame .df() para pandas)."""
    conn = get_conn()
    return conn.execute(sql, params) if params else conn.execute(sql)


def query(sql: str, params: list | None = None):
    """Alias de execute — mantém compatibilidade."""
    return execute(sql, params)


def table_ref(name: str) -> str:
    """Retorna o nome da tabela entre aspas duplas para uso em f-strings SQL."""
    return f'"{name}"'


# ── Registro de VIEWs ────────────────────────────────────────────────────────

def _register_local_views(conn: duckdb.DuckDBPyConnection) -> None:
    """Cria VIEWs DuckDB apontando para os parquets locais."""
    for table, path in _CORE_TABLES.items():
        _create_view(conn, table, path)

    if _SIH_PARQUETS:
        for p in _SIH_PARQUETS:
            _create_view(conn, p.stem, p)
    elif not _SIH_DIR.exists():
        logger.warning(
            "Pasta sih_sim não encontrada: %s — execute prepare_sih_sim_data.py", _SIH_DIR
        )


def _create_view(conn: duckdb.DuckDBPyConnection, name: str, path: Path) -> None:
    if not path.exists():
        logger.warning("Parquet ausente, view '%s' não criada: %s", name, path)
        return
    safe = str(path).replace("\\", "/")
    conn.execute(f"CREATE OR REPLACE VIEW \"{name}\" AS SELECT * FROM read_parquet('{safe}')")
    logger.debug("View: %s → %s", name, safe)
