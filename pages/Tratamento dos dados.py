# Importação das bibliotecas
import streamlit as st
import pandas as pd
import numpy as np
from utils import select_bq

# Configuração da página
st.set_page_config(page_title= 'Indicadores', layout='wide', page_icon= ':fuelpump:')

st.title('Indicadores 🕵️‍♀️')
st.markdown('<p style="text-align: justify;">Uma análise mais abrangente dos dados.</p>', unsafe_allow_html = True)

tabela = 'tb_pede_passos_dataset_fiap'
dados = select_bq (tabela)

# Dividir a coluna com base no delimitador ';' e expandir em várias colunas
dados = dados[dados.columns[0]].str.split(';', expand=True)
# Definir a primeira linha como o cabeçalho das colunas
dados.columns = dados.iloc[0]
# Excluir a primeira linha do DataFrame
dados = dados[1:]
# Reinicializar os índices do DataFrame
dados.reset_index(drop=True, inplace=True)

# Tratamento dos dados do dataset da Passos Mágicos
colunas = dados.columns.str.replace('_2020', '')
colunas = colunas.str.replace('_2021', '')
colunas = colunas.str.replace('_2022', '')
todas_colunas = colunas.drop_duplicates()

# Palavras a serem excluídas
palavras_a_excluir = ['REC_EQUIPE_1', 'REC_EQUIPE_2', 'REC_EQUIPE_3', 'REC_EQUIPE_4','FASE_TURMA']

# Criar uma nova lista excluindo as palavras especificadas
todas_colunas = [word for word in todas_colunas if word not in palavras_a_excluir]

# 2020

def tratamento_base(dados, todas_colunas, ano):
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

dados_tratados_2020 = tratamento_base(dados, todas_colunas, '2020')
dados_tratados_2021 = tratamento_base(dados, todas_colunas, '2021')
dados_tratados_2022 = tratamento_base(dados, todas_colunas, '2022')

df_concatenado = pd.concat([dados_tratados_2020, dados_tratados_2021, dados_tratados_2022], ignore_index=True)

df_concatenado['ANO'] = pd.to_numeric(df_concatenado['ANO'], errors='coerce')
df_concatenado['ANOS_PM'] = pd.to_numeric(df_concatenado['ANOS_PM'], errors='coerce')
df_concatenado['ANO_INGRESSO'] = pd.to_numeric(df_concatenado['ANO_INGRESSO'], errors='coerce')
df_concatenado['CF'] = pd.to_numeric(df_concatenado['CF'], errors='coerce')
df_concatenado['CG'] = pd.to_numeric(df_concatenado['CG'], errors='coerce')
df_concatenado['CT'] = pd.to_numeric(df_concatenado['CT'], errors='coerce')
df_concatenado['DEFASAGEM'] = pd.to_numeric(df_concatenado['DEFASAGEM'], errors='coerce')
df_concatenado['IAA'] = pd.to_numeric(df_concatenado['IAA'], errors='coerce')
df_concatenado['IEG'] = pd.to_numeric(df_concatenado['IEG'], errors='coerce')
df_concatenado['IPS'] = pd.to_numeric(df_concatenado['IPS'], errors='coerce')
df_concatenado['IPP'] = pd.to_numeric(df_concatenado['IPP'], errors='coerce')
df_concatenado['IPS'] = pd.to_numeric(df_concatenado['IPS'], errors='coerce')
df_concatenado['IPV'] = pd.to_numeric(df_concatenado['IPV'], errors='coerce')
df_concatenado['IAN'] = pd.to_numeric(df_concatenado['IAN'], errors='coerce')
df_concatenado['IDA'] = pd.to_numeric(df_concatenado['IDA'], errors='coerce')



st.write(len(df_concatenado))