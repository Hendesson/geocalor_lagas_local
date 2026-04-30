import pandas as pd
import numpy as np
from datetime import datetime, date
import os
import logging
from typing import List, Dict, Optional, Tuple
from cache_manager import cache_manager, cached_dataframe
from config_paths import BASE_DIR, DATA_DIR, PROCESSED_DIR
from db import get_conn, execute as db_execute, table_ref

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, file_path: Optional[str] = None):
        """
        Inicializa o processador de dados.
        
        Args:
            file_path: Caminho opcional para o arquivo de dados. Se não fornecido, usa o caminho padrão.
        """
        # Usa Parquet local (prioritário) ou Excel legado como fallback
        parquet_path = os.path.join(PROCESSED_DIR, "banco_dados_climaticos_consolidado (2).parquet")
        excel_path   = file_path or os.path.join(DATA_DIR, "temp.xlsx")

        if os.path.exists(parquet_path):
            self.file_path   = parquet_path
            self.use_parquet = True
            logger.info(f"Usando arquivo Parquet: {self.file_path}")
        else:
            self.file_path   = excel_path
            self.use_parquet = False
            logger.info(f"Usando arquivo Excel: {self.file_path}")
        
        self.df = None
        self.cidades = []
        self.anos = []
        self.cidade_uf = {
            'Rio Branco': 'AC',
            'Maceió': 'AL',
            'Macapá': 'AP',
            'Manaus': 'AM',
            'Salvador': 'BA',
            'Fortaleza': 'CE',
            'Brasília': 'DF',
            'Vitória': 'ES',
            'Goiânia': 'GO',
            'São Luís': 'MA',
            'Cuiabá': 'MT',
            'Campo Grande': 'MS',
            'Belo Horizonte': 'MG',
            'Belém': 'PA',
            'João Pessoa': 'PB',
            'Curitiba': 'PR',
            'Recife': 'PE',
            'Teresina': 'PI',
            'Rio de Janeiro': 'RJ',
            'Natal': 'RN',
            'Porto Alegre': 'RS',
            'Porto Velho': 'RO',
            'Boa Vista': 'RR',
            'Florianópolis': 'SC',
            'São Paulo': 'SP',
            'Aracaju': 'SE',
            'Palmas': 'TO'
        }
        # Carrega dados na inicialização (como era antes)
        self.load_data()

    def load_data(self) -> pd.DataFrame:
        """
        Carrega os dados do arquivo Parquet (prioritário) ou Excel.
        
        Returns:
            DataFrame com os dados carregados.
        """
        try:
            # Tenta carregar do cache primeiro
            if self.file_path and not os.path.exists(self.file_path):
                logger.warning(f"Arquivo não encontrado: {self.file_path}")
                filename = os.path.basename(self.file_path)
                alt_path = os.path.join(DATA_DIR, filename)
                if os.path.exists(alt_path):
                    logger.info(f"Arquivo encontrado em DATA_DIR: {alt_path}")
                    self.file_path = alt_path
                else:
                    logger.error(f"Coloque o parquet em processed/ — arquivo ausente: {filename}")
                    return pd.DataFrame()
            cache_key = f"main_data_{os.path.getmtime(self.file_path) if self.file_path and os.path.exists(self.file_path) else 0}"

            logger.info(f"Tentando carregar dados (cache_key={cache_key})…")
            cached_df = cache_manager.get(cache_key)
            if cached_df is not None:
                logger.info("Dados carregados do cache - processando tipos...")
                df = cached_df.copy()
            else:
                df = None

            # Se não veio do cache, carrega via DuckDB
            if df is None:
                logger.info("Carregando dados via DuckDB…")
                df = db_execute(
                    f"SELECT * FROM {table_ref('clima')} WHERE year <= 2023"
                ).df()
                logger.info(f"Dados lidos via DuckDB. Shape: {df.shape}")
            
            # Processa dados (tanto Parquet quanto Excel precisam de processamento)
            logger.info("Processando dados...")
            
            # Garante que 'index' é datetime
            if "index" in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df["index"]):
                    df["index"] = pd.to_datetime(df["index"], errors="coerce")
                logger.info("Coluna 'index' convertida para datetime")
            
            # Garante que 'year' e 'month' existem
            if "index" in df.columns:
                if "year" not in df.columns or df["year"].isna().any():
                    df["year"] = df["index"].dt.year
                if "month" not in df.columns or df["month"].isna().any():
                    df["month"] = df["index"].dt.month
                logger.info("Colunas 'year' e 'month' criadas/atualizadas")
            
            # Garante que 'isHW' está no formato correto
            if "isHW" in df.columns:
                # Converte para string e uppercase, tratando todos os casos possíveis
                # Pode vir como boolean, int, float, category, object, etc.
                if df["isHW"].dtype == 'bool':
                    # Se for boolean, converte True -> "TRUE", False -> "FALSE"
                    df["isHW"] = df["isHW"].map({True: "TRUE", False: "FALSE"}).astype(str)
                elif df["isHW"].dtype in ['int64', 'int32', 'float64', 'float32']:
                    # Se for numérico, converte 1 -> "TRUE", 0 -> "FALSE"
                    df["isHW"] = df["isHW"].map({1: "TRUE", 1.0: "TRUE", 0: "FALSE", 0.0: "FALSE"}).fillna("FALSE").astype(str)
                else:
                    # Se for category ou object, converte para string e uppercase
                    df["isHW"] = df["isHW"].astype(str).str.upper().str.strip()
                    # Garante que valores vazios, nan e booleanos portugueses viram "TRUE"/"FALSE"
                    df["isHW"] = df["isHW"].replace({
                        "": "FALSE", "NAN": "FALSE", "NONE": "FALSE", "NULL": "FALSE",
                        "VERDADEIRO": "TRUE", "FALSO": "FALSE", "1": "TRUE", "0": "FALSE",
                    })
                
                logger.info("Coluna 'isHW' formatada")
                logger.info(f"  Valores únicos de isHW: {df['isHW'].unique()}")
                logger.info(f"  Contagem TRUE: {len(df[df['isHW'] == 'TRUE'])}")
                logger.info(f"  Contagem FALSE: {len(df[df['isHW'] == 'FALSE'])}")
            
            # IMPORTANTE: Converte colunas category de volta para tipos normais
            # Isso é necessário porque comparações diretas (==, >=, <=) não funcionam bem com category
            if "cidade" in df.columns:
                if df["cidade"].dtype == 'category':
                    df["cidade"] = df["cidade"].astype(str)
                    logger.info("Coluna 'cidade' convertida de category para string")
                # Remove espaços em branco e normaliza
                df["cidade"] = df["cidade"].astype(str).str.strip()
                # Remove valores NaN
                df = df[df["cidade"].notna() & (df["cidade"] != "nan")]
                logger.info("Coluna 'cidade' normalizada (sem espaços e NaN)")
            
            if "year" in df.columns:
                # Converte year de category para int se necessário
                if df["year"].dtype == 'category':
                    df["year"] = df["year"].astype(str).astype(int)
                elif not pd.api.types.is_integer_dtype(df["year"]):
                    df["year"] = pd.to_numeric(df["year"], errors='coerce').astype('Int64')
                # Remove valores NaN em year
                df = df[df["year"].notna()]
                logger.info("Coluna 'year' garantida como inteiro (sem NaN)")
            
            # Filtrar dados até 2023 (se year existir)
            if "year" in df.columns:
                antes = len(df)
                df = df[df["year"] <= 2023]
                depois = len(df)
                if antes != depois:
                    logger.info(f"Filtrados dados: {antes} -> {depois} linhas (apenas até 2023)")
            
            self.df = df
            
            # Extrai cidades (já convertida para string acima)
            if "cidade" in df.columns:
                self.cidades = sorted(df["cidade"].unique().tolist())
            else:
                self.cidades = []
                logger.warning("Coluna 'cidade' não encontrada no DataFrame")
            
            # Extrai anos (já convertida para int acima)
            if "year" in df.columns:
                self.anos = sorted([int(x) for x in df["year"].unique().tolist() if pd.notna(x)])
            else:
                self.anos = []
                logger.warning("Coluna 'year' não encontrada no DataFrame")
            
            # Salva no cache
            cache_manager.set(cache_key, df, use_joblib=True)
            
            logger.info(f"Dados processados com sucesso. Cidades encontradas: {len(self.cidades)}")
            logger.info(f"Anos encontrados: {len(self.anos)}")
            return df
                
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {str(e)}")
            logger.exception("Detalhes do erro:")
            return pd.DataFrame()

    @cached_dataframe(key_prefix="hw_monthly")
    def calculate_hw_monthly(self, cidade: str, ano: int) -> pd.DataFrame:  # noqa: C901
        """
        Calcula a frequência mensal de ondas de calor para um ano específico.
        
        Args:
            cidade: Nome da cidade
            ano: Ano para análise
            
        Returns:
            DataFrame com a frequência mensal
        """
        if self.df is None or self.df.empty:
            logger.warning("DataFrame vazio, não é possível calcular frequência mensal")
            return pd.DataFrame()

        dff = self.df[(self.df["cidade"] == cidade) & (self.df["year"] == ano)]

        all_months = pd.date_range(start=f"{ano}-01-01", end=f"{ano}-12-31", freq="ME")
        all_months_df = pd.DataFrame({
            "mes": all_months.strftime("%B"),
            "month": all_months.month,
        })

        hw_mask = dff["isHW"] == "TRUE" if "isHW" in dff.columns else pd.Series(False, index=dff.index)
        monthly_counts = dff[hw_mask].groupby(dff["index"].dt.month).size().reset_index(name="frequencia")
        monthly_counts.columns = ["month", "frequencia"]

        monthly_counts = all_months_df.merge(monthly_counts, on="month", how="left").fillna({"frequencia": 0})
        return monthly_counts.sort_values("month")[["mes", "frequencia"]]

    @cached_dataframe(key_prefix="hw_monthly_all")
    def calculate_hw_monthly_all_years(self, cidade: str) -> pd.DataFrame:
        """
        Calcula a frequência mensal de ondas de calor para todos os anos.
        
        Args:
            cidade: Nome da cidade
            
        Returns:
            DataFrame com a frequência mensal total
        """
        if self.df is None or self.df.empty:
            logger.warning("DataFrame vazio, não é possível calcular frequência mensal")
            return pd.DataFrame()

        dff = self.df[self.df["cidade"] == cidade]

        all_months = pd.DataFrame({
            "mes": ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"],
            "month": range(1, 13),
        })

        hw_mask = dff["isHW"] == "TRUE" if "isHW" in dff.columns else pd.Series(False, index=dff.index)
        monthly_counts = dff[hw_mask].groupby(dff["index"].dt.month).size().reset_index(name="frequencia")
        monthly_counts.columns = ["month", "frequencia"]

        monthly_counts = all_months.merge(monthly_counts, on="month", how="left").fillna({"frequencia": 0})
        return monthly_counts.sort_values("month")[["mes", "frequencia"]]

    @cached_dataframe(key_prefix="hw_events")
    def calculate_hw_events(self, cidade: str, ano: int) -> pd.DataFrame:
        """
        Calcula os eventos de ondas de calor por mês para um ano específico.
        Um evento é considerado quando há 3 ou mais dias consecutivos de onda de calor (isHW == TRUE).
        
        Args:
            cidade: Nome da cidade
            ano: Ano para análise
            
        Returns:
            DataFrame com os eventos de ondas de calor por mês
        """
        if self.df is None or self.df.empty:
            logger.warning("DataFrame vazio, não é possível calcular eventos de ondas de calor")
            return pd.DataFrame()

        # Seleciona só as colunas necessárias para reduzir uso de memória
        dff = self.df.loc[
            (self.df['cidade'] == cidade) & (self.df['year'] == ano),
            ["index", "month", "isHW"],
        ].copy()

        dff["isHW_bool"] = dff["isHW"] == "TRUE"
        dff = dff.reset_index(drop=True)
        dff["group"] = (dff["isHW_bool"] != dff["isHW_bool"].shift()).cumsum()

        hw_groups  = dff[dff["isHW_bool"]]
        hw_periods = hw_groups.groupby(["month", "group"]).size().reset_index(name="duration")
        hw_periods = hw_periods[hw_periods["duration"] >= 3]
        hw_events  = hw_periods.groupby("month")["group"].nunique().reset_index(name="frequencia")

        months = pd.DataFrame({
            'mes':   ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"],
            'month': range(1, 13),
        })

        hw_events = pd.merge(months, hw_events, on='month', how='left').fillna({'frequencia': 0})
        return hw_events.sort_values('month')[['mes', 'frequencia']]

    @cached_dataframe(key_prefix="hw_events_all")
    def calculate_hw_events_all_years(self, cidade: str) -> pd.DataFrame:
        """
        Calcula os eventos de ondas de calor por mês para todos os anos.
        Um evento é considerado quando há 3 ou mais dias consecutivos de onda de calor (isHW == TRUE).
        
        Args:
            cidade: Nome da cidade
            
        Returns:
            DataFrame com os eventos de ondas de calor por mês para todos os anos
        """
        if self.df is None or self.df.empty:
            logger.warning("DataFrame vazio, não é possível calcular eventos de ondas de calor")
            return pd.DataFrame()

        # Seleciona só as colunas necessárias para reduzir uso de memória
        dff = self.df.loc[self.df['cidade'] == cidade, ["year", "month", "isHW"]].copy()

        dff["isHW_bool"] = dff["isHW"] == "TRUE"
        dff["group"] = (dff["isHW_bool"] != dff["isHW_bool"].shift()).cumsum()

        hw_groups  = dff[dff["isHW_bool"]]
        hw_periods = hw_groups.groupby(["year", "month", "group"]).size().reset_index(name="duration")
        hw_periods = hw_periods[hw_periods["duration"] >= 3]
        hw_events  = hw_periods.groupby("month")["group"].nunique().reset_index(name="frequencia")

        months = pd.DataFrame({
            'mes':   ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"],
            'month': range(1, 13),
        })

        hw_events = pd.merge(months, hw_events, on='month', how='left').fillna({'frequencia': 0})
        return hw_events.sort_values('month')[['mes', 'frequencia']]

    @cached_dataframe(key_prefix="hw_days")
    def get_heat_wave_days(self, cidade: str) -> list:
        """Retorna os dias com ondas de calor (isHW == TRUE) para uma cidade."""
        if self.df is None or self.df.empty or "isHW" not in self.df.columns:
            return []
        mask = (self.df['cidade'] == cidade) & (self.df['isHW'] == "TRUE")
        return self.df.loc[mask, 'index'].dt.date.tolist()

    @cached_dataframe(key_prefix="heatmap_data")
    def prepare_heatmap_data(self) -> pd.DataFrame:
        """Prepara dados para o heatmap de dias de OC por ano e cidade (via DuckDB)."""
        try:
            df_hw = db_execute(f"""
                SELECT cidade, year, COUNT(*) AS count
                FROM {table_ref('clima')}
                WHERE UPPER(TRIM(CAST(isHW AS VARCHAR))) = 'TRUE'
                  AND year BETWEEN 1981 AND 2023
                GROUP BY cidade, year
            """).df()

            all_combinations = pd.MultiIndex.from_product(
                [self.cidades, list(range(1981, 2024))],
                names=["cidade", "year"],
            ).to_frame(index=False)

            return all_combinations.merge(df_hw, on=["cidade", "year"], how="left").fillna({"count": 0})
        except Exception as e:
            logger.error("prepare_heatmap_data DuckDB error: %s", e)
            return pd.DataFrame()

    def get_available_years(self):
        """Retorna a lista de anos disponíveis nos dados."""
        if self.df is not None and not self.df.empty:
            return sorted(self.df['year'].unique().tolist())
        return []

    def get_heat_wave_events(self, cidade: str) -> List[date]:
        """
        Retorna uma lista de datas que fazem parte de eventos de ondas de calor
        (3 ou mais dias consecutivos com isHW == TRUE).
        
        Args:
            cidade: Nome da cidade
            
        Returns:
            Lista de datas que fazem parte de eventos de ondas de calor
        """
        if self.df is None or self.df.empty:
            logger.warning("DataFrame vazio, não é possível obter dias de eventos de ondas de calor")
            return []

        needed = [c for c in ["index", "isHW"] if c in self.df.columns]
        dff = self.df.loc[self.df['cidade'] == cidade, needed].copy()

        dff["isHW_bool"] = dff["isHW"] == "TRUE"
        dff["group"] = (dff["isHW_bool"] != dff["isHW_bool"].shift()).cumsum()

        hw_groups   = dff[dff["isHW_bool"]]
        hw_periods  = hw_groups.groupby("group").size().reset_index(name="duration")
        valid_groups = hw_periods.loc[hw_periods["duration"] >= 3, "group"]

        return dff.loc[dff["group"].isin(valid_groups), "index"].dt.date.tolist()

    @cached_dataframe(key_prefix="heatmap_events")
    def prepare_heatmap_events_data(self) -> pd.DataFrame:
        """
        Prepara dados para o heatmap de eventos de ondas de calor (3+ dias) por ano e cidade.
        Um evento é definido como uma sequência de 3 ou mais dias consecutivos com isHW == TRUE.
        
        Returns:
            DataFrame formatado para o heatmap de eventos
        """
        if self.df is None or self.df.empty:
            logger.warning("DataFrame vazio, não é possível preparar dados do heatmap de eventos")
            return pd.DataFrame()

        # Copia apenas as colunas necessárias (~4 colunas × 234k linhas em vez de 26)
        needed = [c for c in ["cidade", "year", "index", "isHW"] if c in self.df.columns]
        df_copy = self.df[needed].copy()

        df_copy['isHW_bool'] = df_copy['isHW'] == "TRUE"

        # Ordena por cidade e data para garantir sequência correta
        df_copy = df_copy.sort_values(['cidade', 'index'])

        # Identifica períodos consecutivos de ondas de calor para cada cidade
        df_copy['_temp_group'] = df_copy.groupby('cidade')['isHW_bool'].transform(
            lambda x: (x != x.shift()).cumsum()
        )

        # Filtra apenas os dias que são ondas de calor
        hw_sequences = df_copy[df_copy['isHW_bool']].copy()

        # Calcula a duração de cada sequência por cidade e grupo
        sequence_durations = hw_sequences.groupby(['cidade', '_temp_group']).size().reset_index(name='duration')

        # Identifica os grupos que correspondem a eventos (duração >= 3)
        event_groups = sequence_durations[sequence_durations['duration'] >= 3][['cidade', '_temp_group']].copy()

        # Marca dias que pertencem a grupos de evento via MultiIndex isin (mais rápido que merge)
        event_idx = pd.MultiIndex.from_frame(event_groups[['cidade', '_temp_group']])
        df_keys   = pd.MultiIndex.from_arrays([df_copy['cidade'], df_copy['_temp_group']])
        df_copy['is_event'] = df_keys.isin(event_idx)
        df_copy = df_copy.drop(columns=['_temp_group'])

        # Identifica o início de cada evento (primeiro dia de cada sequência válida)
        df_copy['event_start'] = df_copy.groupby('cidade')['is_event'].transform(
            lambda x: (x & (~x.shift().fillna(False).infer_objects(copy=False))).astype(int)
        )

        # Conta o número de eventos por cidade e ano
        df_heatmap_events = df_copy.groupby(['cidade', 'year'])['event_start'].sum().reset_index(name='count')

        # Preenche combinações de cidade/ano sem eventos com 0
        all_combinations = pd.MultiIndex.from_product(
            [self.cidades, list(range(1981, 2024))],
            names=['cidade', 'year']
        ).to_frame(index=False)

        df_heatmap_events = all_combinations.merge(
            df_heatmap_events, on=['cidade', 'year'], how='left'
        ).fillna({'count': 0})

        return df_heatmap_events 