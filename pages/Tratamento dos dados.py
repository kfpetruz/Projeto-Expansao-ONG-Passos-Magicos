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

dados_tratados_2020 = tratamento_base_passos(dados, todas_colunas, '2020')
dados_tratados_2021 = tratamento_base_passos(dados, todas_colunas, '2021')
dados_tratados_2022 = tratamento_base_passos(dados, todas_colunas, '2022')

df_concatenado = pd.concat([dados_tratados_2020, dados_tratados_2021, dados_tratados_2022], ignore_index=True)

# df_concatenado['ANO'] = pd.to_numeric(df_concatenado['ANO'], errors='coerce')
# df_concatenado['ANOS_PM'] = pd.to_numeric(df_concatenado['ANOS_PM'], errors='coerce')
# df_concatenado['ANO_INGRESSO'] = pd.to_numeric(df_concatenado['ANO_INGRESSO'], errors='coerce')
# df_concatenado['CF'] = pd.to_numeric(df_concatenado['CF'], errors='coerce')
# df_concatenado['CG'] = pd.to_numeric(df_concatenado['CG'], errors='coerce')
# df_concatenado['CT'] = pd.to_numeric(df_concatenado['CT'], errors='coerce')
# df_concatenado['DEFASAGEM'] = pd.to_numeric(df_concatenado['DEFASAGEM'], errors='coerce')
# df_concatenado['IAA'] = pd.to_numeric(df_concatenado['IAA'], errors='coerce')
# df_concatenado['IEG'] = pd.to_numeric(df_concatenado['IEG'], errors='coerce')
# df_concatenado['IPS'] = pd.to_numeric(df_concatenado['IPS'], errors='coerce')
# df_concatenado['IPP'] = pd.to_numeric(df_concatenado['IPP'], errors='coerce')
# df_concatenado['IPS'] = pd.to_numeric(df_concatenado['IPS'], errors='coerce')
# df_concatenado['IPV'] = pd.to_numeric(df_concatenado['IPV'], errors='coerce')
# df_concatenado['IAN'] = pd.to_numeric(df_concatenado['IAN'], errors='coerce')
# df_concatenado['IDA'] = pd.to_numeric(df_concatenado['IDA'], errors='coerce')


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
    
# insert_bq(df_concatenado,'tb_pesquisa_desenvolvimento_educacional_passos')

def tratamento_base_idade():
    dados_idade_total = select_bq ('tb_populacao_total_idade')
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

    dados_idade_total['Pessoas em idade elegível'] = dados_idade_total.iloc[:, 7:27].astype(int).sum(axis=1) # 5 a 24
    dados_idade_total['Pessoas de 6 a 19 anos'] = dados_idade_total.iloc[:, 8:22].astype(int).sum(axis=1)
    return dados_idade_total
dados_idade_total = tratamento_base_idade()

# dados_economicos = select_bq ('tb_populacao_economia')

# DADOS ECONÔMICOS
dados_economicos = pd.read_csv('Base de dados\\populacao_economia_2022.csv')
dados_economicos.rename(columns={'Municípios': 'Município','Densidade demográfica':'Densidade demográfica habitante/km²'}, inplace=True)
dados_economicos['Densidade demográfica habitante/km²'] = dados_economicos['Densidade demográfica habitante/km²'].str.replace('habitante por quilômetro quadrado', '')
dados_economicos['Densidade demográfica habitante/km²'] = dados_economicos['Densidade demográfica habitante/km²'].str.strip()
dados_economicos['Salário médio mensal dos trabalhadores formais'] = dados_economicos['Salário médio mensal dos trabalhadores formais'].str.replace('salários mínimos', '')
dados_economicos['Salário médio mensal dos trabalhadores formais'] = dados_economicos['Salário médio mensal dos trabalhadores formais'].str.strip()
dados_economicos['PIB per capita'] = dados_economicos['PIB per capita'].str.replace('R', '')
dados_economicos['PIB per capita'] = dados_economicos['PIB per capita'].str.replace('$', '')
dados_economicos['PIB per capita'] = dados_economicos['PIB per capita'].str.strip()
dados_economicos['Área da unidade territorial'] = dados_economicos['Área da unidade territorial'].str.replace('km²', '')
dados_economicos['Área da unidade territorial'] = dados_economicos['Área da unidade territorial'].str.strip()
dados_economicos['População no último censo'] = dados_economicos['População no último censo'].str.replace('pessoas', '')
dados_economicos['População no último censo'] = dados_economicos['População no último censo'].str.strip()
dados_economicos.drop(dados_economicos.columns[1], axis=1, inplace = True)
# dados_economicos = dados_economicos.astype(str)
# dados_economicos.rename(columns={'Município' :'Municipios', 
#                                  'Gentílico':'Gentilico',
#                                  'Salário médio mensal dos trabalhadores formais':'Salario_medio_trabalhadores_formais',
#                                  'Índice de Desenvolvimento Humano Municipal (IDHM)':'IDHM',
#                                  'PIB per capita':'PIB_per_capita',
#                                  'Área da unidade territorial':'Area_da_unidade_territorial',
#                                  'População no último censo':'Populacao_no_ultimo_censo',
#                                  'Densidade demográfica habitante/km²':'Densidade_demografica'}, inplace=True)
                           

# insert_bq(dados_economicos,'tb_economia_sp')

# DADOS COORDENADAS
coordenadas = pd.read_csv('Base de dados\\latitude-longitude-cidades.csv',sep = ';')
coordenadas = coordenadas[coordenadas['uf'] == 'SP']
coordenadas.reset_index(drop = True, inplace = True)
coordenadas['municipio'] = coordenadas['municipio'].str.replace('`',"'")
coordenadas['municipio'] = coordenadas['municipio'].str.replace('Biritiba-Mirim',"Biritiba Mirim")
coordenadas['municipio'] = coordenadas['municipio'].str.replace('Embu',"Embu das Artes")
coordenadas['municipio'] = coordenadas['municipio'].str.replace('Embu das Artes-Guaçu',"Embu-Guaçu")
coordenadas['municipio'] = coordenadas['municipio'].str.replace('Florínia',"Florínea")
coordenadas['municipio'] = coordenadas['municipio'].str.replace('Itaóca',"Itaoca")
coordenadas['coordenadas'] = '('+coordenadas['longitude'].astype(str)+', '+coordenadas['latitude'].astype(str)+')'
dados = {
    'Município': coordenadas['municipio'],
    'Coordenadas': coordenadas['coordenadas']
}
dados_coordenadas = pd.DataFrame(dados)
embu_guacu_coord = eval(dados_coordenadas[dados_coordenadas['Município'] == 'Embu-Guaçu']['Coordenadas'].values[0])
dados_coordenadas['Distância']=0

from geopy.distance import geodesic
for i in range(len(dados_coordenadas['Distância'])):
  dados_coordenadas['Distância'][i] = geodesic(embu_guacu_coord, eval(dados_coordenadas['Coordenadas'].values[i])).kilometers

# DADOS EDUCAÇÃO
dados_educacionais = pd.read_csv('Base de dados\\sinopses_estatisticas_censo_escolar_2022.csv',sep = ';', encoding='windows-1252')
dados_educacionais['Unnamed: 1'] = dados_educacionais['Unnamed: 1'].str.strip()
colunas = dados_educacionais.iloc[6]
dados_educacionais = dados_educacionais[dados_educacionais['Unnamed: 1'] == 'São Paulo']
dados_educacionais = dados_educacionais.iloc[1:]
dados_educacionais.reset_index(drop=True, inplace=True)
dados_educacionais.columns = colunas
colunas[0] = 0
colunas[1] = 1
colunas[2] = 'Município'
colunas[3] = 3
colunas[4] = 4
dados_educacionais = dados_educacionais.drop(dados_educacionais.columns[[0, 1, 3, 4]], axis=1)
dados_educacionais= dados_educacionais.iloc[:, :12]
for coluna in dados_educacionais.columns:
    # Aplicar strip() a cada valor na coluna
    dados_educacionais[coluna] = dados_educacionais[coluna].apply(lambda x: x.strip() if isinstance(x, str) else x)
dados_educacionais.iloc[:, 1:] = dados_educacionais.iloc[:, 1:].astype(str).replace('-', '0')
dados_educacionais.iloc[:, 1:] = dados_educacionais.iloc[:, 1:].astype(str).replace('.', '') 
dados_educacionais['6 a 10 anos'] = pd.to_numeric(dados_educacionais['6 a 10 anos'], errors='coerce')
dados_educacionais['11 a 14 anos'] = pd.to_numeric(dados_educacionais['11 a 14 anos'], errors='coerce')
dados_educacionais['15 a 17 anos'] = pd.to_numeric(dados_educacionais['15 a 17 anos'], errors='coerce')
dados_educacionais['18 a 19 anos'] = pd.to_numeric(dados_educacionais['18 a 19 anos'], errors='coerce')
dados_educacionais['Matriculados 6 a 19'] = dados_educacionais['6 a 10 anos']+dados_educacionais['11 a 14 anos']+dados_educacionais['15 a 17 anos']+dados_educacionais['18 a 19 anos'].astype(int)

# JUNÇÃO
df_junto = pd.merge(dados_economicos,dados_idade_total[['Município','Pessoas em idade elegível','Pessoas de 6 a 19 anos']], on='Município', how='left')
df_junto = pd.merge(df_junto, dados_coordenadas[['Município','Distância']], on='Município', how='left')
df_junto['Salário médio mensal dos trabalhadores formais'] = df_junto['Salário médio mensal dos trabalhadores formais'].str.replace(',', '.').astype(float)
df_junto['Índice de Desenvolvimento Humano Municipal (IDHM)'] = df_junto['Índice de Desenvolvimento Humano Municipal (IDHM)'].str.replace(',', '.').astype(float)
df_junto['PIB per capita'] = df_junto['PIB per capita'].str.replace(',', '.').astype(float)
df_junto['Área da unidade territorial'] = df_junto['Área da unidade territorial'].str.replace(',', '.').astype(float)
df_junto['Densidade demográfica habitante/km²'] = df_junto['Densidade demográfica habitante/km²'].str.replace(',', '.').astype(float)
df_junto['Distância'] = df_junto['Distância'].astype(float)
df_junto = pd.merge(df_junto, dados_educacionais[['Município','Matriculados 6 a 19']], on='Município', how='left')
df_junto['Elegíveis/População'] = df_junto['Pessoas em idade elegível'].astype(float)/df_junto['População no último censo'].astype(float)
df_junto['Matriculados/População 6 a 19'] = df_junto['Matriculados 6 a 19'].astype(float)/df_junto['Pessoas de 6 a 19 anos'].astype(float)
st.write(df_junto)


