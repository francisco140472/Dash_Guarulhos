import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import plotly.express as px
import pyodbc
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do SQL Server (usando variáveis de ambiente)
server = os.getenv("SERVER")
database = os.getenv("DATABASE")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Função para buscar dados do JotForm via link direto para o cadastro de esgoto
def get_jotform_data_esgoto():
    jotform_excel_url = "https://www.jotform.com/excel/250513248478056"
    try:
        response = requests.get(jotform_excel_url)
        if response.status_code == 200:
            excel_file = BytesIO(response.content)
            df = pd.read_excel(excel_file)
            return df
        else:
            st.error(f"Erro ao baixar o arquivo: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar dados do JotForm: {e}")
        return None

# Função para buscar dados do JotForm via link direto para as iniciativas
def get_jotform_data_ligacao():
    jotform_excel_url = "https://www.jotform.com/excel/250653960017051"
    try:
        response = requests.get(jotform_excel_url)
        if response.status_code == 200:
            excel_file = BytesIO(response.content)
            df = pd.read_excel(excel_file)
            return df
        else:
            st.error(f"Erro ao baixar o arquivo: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar dados do JotForm: {e}")
        return None

# Função para buscar dados do SQL Server
@st.cache_data
def get_sql_data(date_filter=None):
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        )
        where_clause = ""
        if date_filter:
            where_clause = f"WHERE CAST([XDATE] AS DATE) = '{date_filter}'"
        
        query = f"""
        WITH Ocorrencias AS (
            SELECT [OCO_CAMPO], COUNT(*) AS TOTAL_OCORRENCIA
            FROM [E_XLS_JOTFORM].[dbo].[TAB_GUARULHOS_III]
            {where_clause}
            GROUP BY [OCO_CAMPO]
        )
        SELECT 
            (SELECT COUNT(*) FROM [E_XLS_JOTFORM].[dbo].[TAB_GUARULHOS_III] {where_clause}) AS TOTAL_CADASTRO,
            (SELECT COUNT(*) FROM [E_XLS_JOTFORM].[dbo].[TAB_GUARULHOS_III_CAIXA] {where_clause}) AS TOTAL_CAIXA,
            (SELECT COUNT(*) FROM [E_XLS_JOTFORM].[dbo].[TAB_GUARULHOS_III_LIGAGUA] {where_clause}) AS TOTAL_LIGACAO,
            O.OCO_CAMPO,
            O.TOTAL_OCORRENCIA,
            (SELECT COUNT(*) FROM [E_XLS_JOTFORM].[dbo].[TAB_GUARULHOS_III] WHERE CAST([XDATE] AS DATE) = CAST(GETDATE() AS DATE)) AS TOTAL_REGISTROS_DIA
        FROM Ocorrencias O
        ORDER BY TOTAL_OCORRENCIA DESC
        """
        
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

st.set_page_config(page_title="DASHBOARD GUARULHOS - VU III", layout="wide")
st.title("📊 DASHBOARD GUARULHOS - VU III")

# Painel lateral para filtros
with st.sidebar:
    st.header("Filtros")
    date_filter = st.date_input("Filtrar por Data")
    clear_filter = st.button("Limpar Filtro")

# Resetar filtro ao clicar no botão "Limpar Filtro"
if clear_filter:
    date_filter = None
    st.rerun()

# Obter dados
jotform_data_esgoto = get_jotform_data_esgoto()
jotform_data_ligacao = get_jotform_data_ligacao()
sql_data = get_sql_data(date_filter)

if jotform_data_esgoto is not None and sql_data is not None:
    col1, col2, col3 = st.columns(3)
    col1.metric("📋 Total de Cadastros", f"{sql_data['TOTAL_CADASTRO'][0]:,}".replace(",", "."))
    col2.metric("📦 Total Caixa UMA", f"{sql_data['TOTAL_CAIXA'][0]:,}".replace(",", "."))
    col3.metric("🔗 Total Ligações", f"{sql_data['TOTAL_LIGACAO'][0]:,}".replace(",", "."))
    
    total_jotform_cadastros_esgoto = len(jotform_data_esgoto)
    st.subheader(f"📊 Total de Cadastros de Esgoto: {total_jotform_cadastros_esgoto:,}".replace(",", "."))

    if jotform_data_ligacao is not None:
        total_jotform_cadastros_iniciativas = len(jotform_data_ligacao)
        st.subheader(f"📊 Total de Iniciativas: {total_jotform_cadastros_iniciativas:,}".replace(",", "."))
    
    st.subheader(f"📅 Total de Registros de Execução de Hoje: {sql_data['TOTAL_REGISTROS_DIA'][0]:,}".replace(",", "."))
    
    fig2 = px.bar(
        data_frame=sql_data,
        x="OCO_CAMPO",
        y="TOTAL_OCORRENCIA",
        title="🔴 Total de Ocorrências por Tipo",
        text_auto=True,
        color="TOTAL_OCORRENCIA",
        color_continuous_scale="viridis",
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader("📋 Tabela de Ocorrências")
    st.dataframe(sql_data[['OCO_CAMPO', 'TOTAL_OCORRENCIA']])