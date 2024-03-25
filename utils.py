# Importação das bibliotecas
import pandas as pd
import streamlit as st
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
from datetime import timedelta
import plotly.graph_objects as go
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from google.oauth2 import service_account
from google.cloud import bigquery
from pandas_gbq import to_gbq

# Armazenamento dos dados em cache, melhorando a performance do site
@st.cache_data 
# Consulta full de cada tabela criada no BigQuery
def select_bq (tabela):
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)

    query = f'select * from `sixth-aloe-402921.dados_expansao_passos_magicos.{tabela}`'

    resultado = client.query(query)
    df_resultado = resultado.to_dataframe()
    
    return df_resultado

# Os dados do site de petróleo não são atualizados todos os dias, mas como a aplicação está armazenando os dados em cache, quando estiverem desatualizados, se faz necessário clicar 
def atualiza_dados():
    if st.sidebar.button("###### Clique para atualizar os dados da aplicação"):
        # Limpa o cache de dados
        st.cache_data.clear()
        st.cache_resource.clear()

def tratamento_base_passos(dados, todas_colunas, ano):
    dados_tratados = pd.DataFrame()
    colunas_filtradas = [coluna for coluna in dados.columns if ano in coluna]
    dados_tratados['NOME'] = dados['NOME']
    dados_tratados['ANO'] = ano
    dados_tratados[colunas_filtradas] = dados[colunas_filtradas]
    dados_tratados.columns = dados_tratados.columns.str.replace('_'+ano, '')
    dados_tratados.rename(columns={'REC_EQUIPE_1': 'REC_AVA_1','REC_EQUIPE_2': 'REC_AVA_2','REC_EQUIPE_3': 'REC_AVA_3','REC_EQUIPE_4': 'REC_AVA_4'}, inplace=True)
    colunas_anual = dados_tratados.columns

    if ano == '2020':
        dados_tratados[['FASE', 'TURMA']] = dados_tratados['FASE_TURMA'].str.extract('(\d+)(\D+)')
        dados_tratados = dados_tratados.drop(columns=['FASE_TURMA'])

    # Converter as listas em conjuntos
    set_originais = set(todas_colunas)
    set_subtrair = set(colunas_anual)

    # Encontrar as palavras que sobram
    palavras_sobrando = set_originais - set_subtrair

    # Converter o resultado de volta para uma lista, se necessário
    palavras_sobrando = list(palavras_sobrando)

    dados_tratados[palavras_sobrando]= np.nan

    colunas_ordenadas = sorted(dados_tratados.columns)

    # Reorganizar o DataFrame com as colunas ordenadas
    dados_tratados = dados_tratados[colunas_ordenadas]
    return dados_tratados

def insert_bq(dados,tabela):
    from google.oauth2 import service_account
    projeto = 'sixth-aloe-402921'
    dataset = 'dados_expansao_passos_magicos'
    parametro =  'replace'
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    dados.to_gbq(destination_table= f'{projeto}.{dataset}.{tabela}',
                project_id = projeto,
                if_exists = parametro,
                credentials = credentials)
    
def tratamento_base_idade(dados_idade_total):
    dados_idade_total.drop(index=range(5), inplace=True)

    # Dividir a coluna com base no delimitador ';' e expandir em várias colunas
    dados_idade_total = dados_idade_total[dados_idade_total.columns[0]].str.split(';', expand=True)
    dados_idade_total.drop(columns=dados_idade_total.columns[1], inplace=True)

    novos_nomes = dados_idade_total.iloc[0]
    novos_nomes[0] = 'Município'
    dados_idade_total = dados_idade_total.rename(columns=novos_nomes)
    dados_idade_total['Município'].fillna('', inplace=True)
    dados_idade_total.reset_index(inplace = True, drop=True)
    dados_idade_total.drop(index=range(1), inplace=True)
    dados_idade_total.reset_index(inplace = True, drop=True)
    dados_idade_total = dados_idade_total.iloc[:, :103]

    dados_idade_total = dados_idade_total[dados_idade_total['Município'].str.contains('(SP)')]
    dados_idade_total.reset_index(inplace = True, drop=True)

    dados_idade_total['Município'] = dados_idade_total['Município'].str.replace('(', '')
    dados_idade_total['Município'] = dados_idade_total['Município'].str.replace(')', '')
    dados_idade_total['Município'] = dados_idade_total['Município'].str.replace('SP', '')
    dados_idade_total['Município'] = dados_idade_total['Município'].str.strip()

    dados_idade_total.iloc[:, 1:] = dados_idade_total.iloc[:, 1:].astype(str).replace('-', '0')
    # 5 a 24
    dados_idade_total['Pessoas em idade elegível'] = dados_idade_total.iloc[:, 7:27].astype(int).sum(axis=1) 
    dados_idade_total['Pessoas de 6 a 19 anos'] = dados_idade_total.iloc[:, 8:22].astype(int).sum(axis=1)
    return dados_idade_total
