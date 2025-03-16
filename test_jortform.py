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
server = os.getenv("200.98.80.97")
database = os.getenv("E_XLS_JOTFORM")
username = os.getenv("sa")
password = os.getenv("SantoAndre2021")

# Função para buscar dados do JotForm via link direto para o cadastro de esgoto
def get_jotform_data_esgoto():
    jotform_excel_url = "https://www.jotform.com/excel/250513248478056"  # Link para a planilha de cadastro de esgoto
    try:
        # Baixar o arquivo Excel do JotForm
        response = requests.get(jotform_excel_url)
        
        # Verificar se o download foi bem-sucedido
        if response.status_code == 200:
            # Ler o arquivo Excel diretamente na memória
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
    jotform_excel_url = "https://www.jotform.com/excel/250653960017051"  # Link para a planilha de iniciativas
    try:
        # Baixar o arquivo Excel do JotForm
        response = requests.get(jotform_excel_url)
        
        # Verificar se o download foi bem-sucedido
        if response.status_code == 200:
            # Ler o arquivo Excel diretamente na memória
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
def get_sql_data():
    """Consulta os dados do SQL Server e retorna um DataFrame."""
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        )

        # Query para obter os totais
        query = """
        WITH Ocorrencias AS (
            SELECT [OCO_CAMPO], COUNT(*) AS TOTAL_OCORRENCIA
            FROM [E_XLS_JOTFORM].[dbo].[TAB_GUARULHOS_III]
            GROUP BY [OCO_CAMPO]
        )
        SELECT 
            (SELECT COUNT(*) FROM [E_XLS_JOTFORM].[dbo].[TAB_GUARULHOS_III]) AS TOTAL_CADASTRO,
            (SELECT COUNT(*) FROM [E_XLS_JOTFORM].[dbo].[TAB_GUARULHOS_III_CAIXA]) AS TOTAL_CAIXA,
            (SELECT COUNT(*) FROM [E_XLS_JOTFORM].[dbo].[TAB_GUARULHOS_III_LIGAGUA]) AS TOTAL_LIGACAO,
            O.OCO_CAMPO,
            O.TOTAL_OCORRENCIA,
            -- Nova consulta para o total de registros do dia de execução
            (SELECT COUNT(*) 
             FROM [E_XLS_JOTFORM].[dbo].[TAB_GUARULHOS_III]
             WHERE CAST([XDATE] AS DATE) = CAST(GETDATE() AS DATE)) AS TOTAL_REGISTROS_DIA
        FROM Ocorrencias O
        ORDER BY TOTAL_OCORRENCIA DESC
        """
        
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Configuração da página
st.set_page_config(page_title="DASHBOARD GUARULHOS  - VU III", layout="wide")

# Título
st.title("📊 DASHBOARD GUARULHOS  - VU III")

# Obter dados do JotForm para cadastro de esgoto
jotform_data_esgoto = get_jotform_data_esgoto()

# Obter dados do JotForm para iniciativas
jotform_data_ligacao = get_jotform_data_ligacao()

# Obter dados do banco SQL Server
sql_data = get_sql_data()

if jotform_data_esgoto is not None and sql_data is not None:
    # Exibir gráficos usando dados do SQL
    col1, col2, col3 = st.columns(3)
    col1.metric("📋 Total de Cadastros", f"{sql_data['TOTAL_CADASTRO'][0]:,}".replace(",", "."))
    col2.metric("📦 Total Caixa UMA", f"{sql_data['TOTAL_CAIXA'][0]:,}".replace(",", "."))
    col3.metric("🔗 Total Ligações", f"{sql_data['TOTAL_LIGACAO'][0]:,}".replace(",", "."))

    # Exibir o total de registros do dia
    st.subheader(f"📅 Total de Registros de Execução de Hoje: {sql_data['TOTAL_REGISTROS_DIA'][0]:,}".replace(",", "."))

    # Gráfico de Total de Ocorrências
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
    
    # Exibir tabela de dados
    st.subheader("📋 Tabela de Ocorrências")
    st.dataframe(sql_data[['OCO_CAMPO', 'TOTAL_OCORRENCIA']])

    # Exibir o total de cadastros do JotForm diretamente
    total_jotform_cadastros_esgoto = len(jotform_data_esgoto)
    st.subheader(f"📊 Total de Cadastros de Esgoto: {total_jotform_cadastros_esgoto:,}".replace(",", "."))

# Verificação de valores antes de calcular o total
if jotform_data_ligacao is not None:
    # Garantir que não haja valores infinitos ou inválidos na contagem
    try:
        total_jotform_cadastros_iniciativas = len(jotform_data_ligacao)
        st.subheader(f"📊 Total de Iniciativas: {total_jotform_cadastros_iniciativas:,}".replace(",", "."))
    except Exception as e:
        st.error(f"Erro ao calcular o total de iniciativas: {e}")
else:
    st.warning("⚠️ Não foi possível carregar os dados de JotForm ou SQL.")
