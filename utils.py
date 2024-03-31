# Importação das bibliotecas
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from google.oauth2 import service_account
from google.cloud import bigquery
from pandas_gbq import to_gbq
from geopy.distance import geodesic
import plotly.express as px


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

@st.cache_data 
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

@st.cache_data 
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
    dados_idade_total.iloc[:, 1:] = dados_idade_total.iloc[:, 1:].astype(str).replace(',', '')
    dados_idade_total.iloc[:, 1:] = dados_idade_total.iloc[:, 1:].astype(str).replace('.', '')
    # dados_idade_total['Pessoas em idade elegível'] = dados_idade_total.iloc[:, 7:27].astype(int).sum(axis=1) 
    dados_idade_total['Pessoas de 6 a 19 anos'] = dados_idade_total.iloc[:, 8:22].astype(int).sum(axis=1)
    return dados_idade_total

@st.cache_data 
def tratamento_base_economia(dados_economicos):
    dados_economicos.rename(columns={dados_economicos.columns[0]: 'Município',
                                    dados_economicos.columns[1]:'Gentílico',
                                    dados_economicos.columns[2]:'Salário médio mensal dos trabalhadores formais',
                                    dados_economicos.columns[3]:'Índice de Desenvolvimento Humano Municipal (IDHM)',
                                    dados_economicos.columns[4]:'PIB per capita',
                                    dados_economicos.columns[5]:'Área da unidade territorial',
                                    dados_economicos.columns[6]:'População no último censo',
                                    dados_economicos.columns[7]:'Densidade demográfica habitante/km²'}, inplace=True)

    dados_economicos['Densidade demográfica habitante/km²'] = dados_economicos['Densidade demográfica habitante/km²'].str.replace('habitante por quilômetro quadrado', '')
    dados_economicos['Densidade demográfica habitante/km²'] = dados_economicos['Densidade demográfica habitante/km²'].str.strip()
    dados_economicos['Salário médio mensal dos trabalhadores formais'] = dados_economicos['Salário médio mensal dos trabalhadores formais'].str.replace('salários mínimos', '')
    dados_economicos['Salário médio mensal dos trabalhadores formais'] = dados_economicos['Salário médio mensal dos trabalhadores formais'].str.strip()
    dados_economicos['PIB per capita'] = dados_economicos['PIB per capita'].replace(',', '')
    dados_economicos['Área da unidade territorial'] = dados_economicos['Área da unidade territorial'].str.replace('km²', '')
    dados_economicos['Área da unidade territorial'] = dados_economicos['Área da unidade territorial'].str.strip()
    dados_economicos['População no último censo'] = dados_economicos['População no último censo'].str.replace('pessoas', '')
    dados_economicos['População no último censo'] = dados_economicos['População no último censo'].str.strip()
    dados_economicos.drop(dados_economicos.columns[1], axis=1, inplace = True)
    return dados_economicos

@st.cache_data 
def tratamento_base_coordenadas(coordenadas):
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
    # Cálculo da distância
    for i in range(len(dados_coordenadas['Distância'])):
        dados_coordenadas['Distância'][i] = geodesic(embu_guacu_coord, eval(dados_coordenadas['Coordenadas'].values[i])).kilometers
    return dados_coordenadas

@st.cache_data 
def tratamento_base_educacional(dados_educacionais):
    dados_educacionais = dados_educacionais.drop(range(6))
    dados_educacionais = dados_educacionais[dados_educacionais.columns[0]].str.split(';', expand=True)
    dados_educacionais = dados_educacionais.iloc[:, :16]
    dados_educacionais = dados_educacionais.reset_index(drop = True)
    dados_educacionais.iloc[:, 1] = dados_educacionais.iloc[:, 1].str.strip()
    dados_educacionais = dados_educacionais[dados_educacionais.iloc[:, 1] == 'São Paulo']
    dados_educacionais = dados_educacionais.reset_index(drop = True)
    dados_educacionais = dados_educacionais.drop(dados_educacionais.columns[[0, 1, 3, 4]], axis=1)
    df_aux = pd.DataFrame(columns=['Município', 'Até 3 anos', '4 a 5 anos', '6 a 10 anos', '11 a 14 anos', '15 a 17 anos', '18 a 19 anos', '20 a 24 anos', '25 a 29 anos', '30 a 34 anos','35 a 39 anos', '40 anos ou mais'])
    df_aux [['Município', 'Até 3 anos', '4 a 5 anos', '6 a 10 anos', '11 a 14 anos', '15 a 17 anos', '18 a 19 anos', '20 a 24 anos', '25 a 29 anos', '30 a 34 anos','35 a 39 anos', '40 anos ou mais']]= dados_educacionais
    dados_educacionais = df_aux.copy()

    for coluna in dados_educacionais.columns:
        # Aplicar strip() a cada valor na coluna
        dados_educacionais[coluna] = dados_educacionais[coluna].apply(lambda x: x.strip() if isinstance(x, str) else x)

    dados_educacionais.iloc[:, 3] = dados_educacionais.iloc[:, 3].str.replace('-', '0')
    dados_educacionais.iloc[:, 3] = dados_educacionais.iloc[:, 3].str.replace('.', '')
    dados_educacionais.iloc[:, 3] = dados_educacionais.iloc[:, 3].str.replace(',', '')

    dados_educacionais.iloc[:, 4] = dados_educacionais.iloc[:, 4].str.replace('-', '0')
    dados_educacionais.iloc[:, 4] = dados_educacionais.iloc[:, 4].str.replace('.', '')
    dados_educacionais.iloc[:, 4] = dados_educacionais.iloc[:, 4].str.replace(',', '')

    dados_educacionais.iloc[:, 5] = dados_educacionais.iloc[:, 5].str.replace('-', '0')
    dados_educacionais.iloc[:, 5] = dados_educacionais.iloc[:, 5].str.replace('.', '')
    dados_educacionais.iloc[:, 5] = dados_educacionais.iloc[:, 5].str.replace(',', '')

    dados_educacionais.iloc[:, 6] = dados_educacionais.iloc[:, 6].str.replace('-', '0')
    dados_educacionais.iloc[:, 6] = dados_educacionais.iloc[:, 6].str.replace('.', '')
    dados_educacionais.iloc[:, 6] = dados_educacionais.iloc[:, 6].str.replace(',', '')

    dados_educacionais['6 a 10 anos'] = pd.to_numeric(dados_educacionais['6 a 10 anos'])
    dados_educacionais['11 a 14 anos'] = pd.to_numeric(dados_educacionais['11 a 14 anos'])
    dados_educacionais['15 a 17 anos'] = pd.to_numeric(dados_educacionais['15 a 17 anos'])
    dados_educacionais['18 a 19 anos'] = pd.to_numeric(dados_educacionais['18 a 19 anos'])
    dados_educacionais['Matriculados 6 a 19'] = dados_educacionais['6 a 10 anos'] +dados_educacionais['11 a 14 anos']+dados_educacionais['15 a 17 anos']+dados_educacionais['18 a 19 anos']
    dados_educacionais['Município'][560] = 'Redenção da Serra'
    dados_educacionais['Município'][581] = 'Santa Cruz da Conceição'
    dados_educacionais['Município'][471] = 'Lençóis Paulista'
    dados_educacionais['Município'][154] = 'Monções'
    return dados_educacionais

@st.cache_data 
def tratamento_base_estimativa_populacao(dados_estimados):
    dados_estimados = dados_estimados[dados_estimados.columns[0]].str.split(';', expand=True)
    novos_nomes = dados_estimados.iloc[3]
    dados_estimados = dados_estimados.rename(columns=novos_nomes)
    dados_estimados.columns = [str(col).replace('.0', '') for col in dados_estimados.columns]
    dados_estimados['Município'].fillna('', inplace=True)
    dados_estimados = dados_estimados[dados_estimados['Município'].str.contains('(SP)')]
    dados_estimados.reset_index(drop=True, inplace=True)
    dados_estimados['Município'] = dados_estimados['Município'].str.replace('(', '')
    dados_estimados['Município'] = dados_estimados['Município'].str.replace(')', '')
    dados_estimados['Município'] = dados_estimados['Município'].str.replace('SP', '')
    dados_estimados['Município'] = dados_estimados['Município'].str.strip()
    dados_estimados= dados_estimados[dados_estimados['Município']=='Embu-Guaçu']
    return dados_estimados

def juncao_dados_externos(dados_idade_total,dados_economicos,dados_coordenadas,dados_educacionais):
    df_junto = pd.merge(dados_economicos,dados_idade_total[['Município','Pessoas de 6 a 19 anos']], on='Município', how='left')
    df_junto = pd.merge(df_junto, dados_educacionais[['Município','Matriculados 6 a 19']], on='Município', how='left')
    df_junto = pd.merge(df_junto, dados_coordenadas[['Município','Distância']], on='Município', how='left')
    df_junto['Distância'] = df_junto['Distância'].astype(float)
    df_junto['Salário médio mensal dos trabalhadores formais'] = df_junto['Salário médio mensal dos trabalhadores formais'].str.replace(',', '.').astype(float)
    df_junto.drop(columns='Índice de Desenvolvimento Humano Municipal (IDHM)',inplace =True)
    df_junto['PIB per capita'] = df_junto['PIB per capita'].astype(float)
    df_junto['Área da unidade territorial'] = df_junto['Área da unidade territorial'].str.replace(',', '.').astype(float)
    df_junto['Densidade demográfica habitante/km²'] = df_junto['Densidade demográfica habitante/km²'].str.replace(',', '.').astype(float)
    df_junto['percent_elegiveis_6a19a'] = df_junto['Pessoas de 6 a 19 anos'].astype(float)/df_junto['População no último censo'].astype(float) * 100
    df_junto['Matriculados/População 6 a 19'] = df_junto['Matriculados 6 a 19'].astype(float)/df_junto['Pessoas de 6 a 19 anos'].astype(float) * 100
    df_junto = df_junto[['Município', 'Salário médio mensal dos trabalhadores formais', 'PIB per capita', 'Área da unidade territorial', 'População no último censo', 'Densidade demográfica habitante/km²', 'Distância', 'Matriculados/População 6 a 19', 'percent_elegiveis_6a19a']]
    df_junto = df_junto.rename(columns= {'Município': 'municipio', 'Salário médio mensal dos trabalhadores formais': 'salario_medio_trabalhadores', 'PIB per capita': 'pib_per_capita', 'Área da unidade territorial': 'area_territorial', 'População no último censo': 'populacao', 'Densidade demográfica habitante/km²': 'densidade_demografica_km2', 'Distância': 'distancia_de_embu_guacu', 'Matriculados/População 6 a 19': 'percent_matriculados_6a19a'})
    insert_bq(df_junto, 'tb_dados_externos')

def grafico_duas_linhas_ponto(x,y,y2,percentual):
    # Criar o gráfico
    fig = go.Figure()

    # Adicionar a linha ao gráfico para y
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Quantidade de alunos', line=dict(color='#1A4A6A')))

    # Adicionar os pontos ao gráfico com os percentuais
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Quantidade de Alunos / População (%)',
                            text=percentual.astype(str)+'%', hoverinfo='text+x+y', marker=dict(color='#1A4A6A', size=10)))

    # Adicionar a linha ao gráfico para y2
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='População de Embu-Guaçu', yaxis='y2', line=dict(color='#722f37')))

    fig.update_layout(
        title='Quantidade de alunos da ONG x População de Embu-Guaçu',
        yaxis=dict(title='Quantidade de alunos da ONG', side='left',gridcolor='#B5C7D5'),
        yaxis2=dict(
            title='População de Embu-Guaçu', 
            overlaying='y', 
            side='right',
            gridcolor='gray'
        ),
        legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center', yanchor='top'),
        title_font_color='#292F39',
        font_color='#292F39'              
    )
    return fig

def grafico_tres_linhas_ponto(x,y1,y2,y3,percentual1,percentual2):

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='Quantidade de alunos', line=dict(color='#1A4A6A')))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='Bolsistas em escola parceira', line=dict(color='#722f37')))
    fig.add_trace(go.Scatter(x=x, y=y3, mode='lines', name='Universitários', line=dict(color='#006400')))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='markers', name='Bolsistas / Quantidade de alunos (%)',
                            text=percentual1.astype(str)+'%', hoverinfo='text+x+y', marker=dict(color='#722f37', size=10)))
    fig.add_trace(go.Scatter(x=x, y=y3, mode='markers', name='Universitários / Quantidade de alunos (%)',
                            text=percentual2.astype(str)+'%', hoverinfo='text+x+y', marker=dict(color='#006400', size=10)))

    
    fig.update_layout(title='Quantidade de Alunos x Bolsistas x Universitários da ONG',
                    xaxis_title='Ano',
                    yaxis_title='Quantidade',
                    legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center', yanchor='top'),
                    title_font_color='#292F39',  
                    font_color='#292F39',
                    xaxis=dict(
                        gridcolor='gray'
                    ),
                    yaxis=dict(
                        gridcolor='gray'
                    )
                    )

    return fig

# Função para plotar o gráfico com base nas categorias selecionadas
def plotar_grafico(categorias_selecionadas,dados):
    fig = go.Figure()
    # Adicionar barras para cada categoria selecionada
    for categoria in categorias_selecionadas:
        if categoria == 'Professor':
            fig.add_trace(go.Bar(
                x=dados['Ano'],
                y=dados['Professores'],
                name='Professores',
                marker_color='#1A4A6A'
            ))

        elif categoria == 'Psicóloga':
            fig.add_trace(go.Bar(
                x=dados['Ano'],
                y=dados['Psicólogas'],
                name='Psicólogas',
                marker_color='#722f37'
            ))

        elif categoria == 'Psicopedagoga':
            fig.add_trace(go.Bar(
                x=dados['Ano'],
                y=dados['Psicopedagoga'],
                name='Psicopedagogas',
                marker_color='#006400'
            ))
        
        elif categoria == 'Psiquiatra':
            fig.add_trace(go.Bar(
                x=dados['Ano'],
                y=dados['Psiquiatra'],
                name='Psiquiatras',
                marker_color='#F4A460'
            ))

        elif categoria == 'Assistente Social':
            fig.add_trace(go.Bar(
                x=dados['Ano'],
                y=dados['Assistente Social'],
                name='Assistente Social',
                marker_color='#9B59B6'
            ))

    # Atualizar layout do gráfico
    fig.update_layout(
        #legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center', yanchor='top'),
        title='Formação da equipe ao longo dos anos',
        xaxis=dict(title='Ano',gridcolor='gray'),
        yaxis=dict(title='Quantidade',gridcolor='gray'),
        barmode='stack',
        title_font_color='#292F39',  
        font_color='#292F39',

    )

    st.plotly_chart(fig, use_container_width=True)

def grafico_barra_um_valor(dados, x, y, xaxis, yaxis, titulo):

            fig = px.bar(dados, x=x, y=y,color =x,color_discrete_sequence=['#1A4A6A', '#722f37', '#006400', '#D35400','#D98880', '#F1C40F', '#9B59B6','#7DCEA0'])

            fig.update_layout(title=titulo,
                            xaxis_title=None,
                            yaxis_title=yaxis,
                            title_font_color='#292F39',  
                            font_color='#292F39',
                            xaxis_showticklabels=False,
                            xaxis=dict(
                                gridcolor='gray'
                            ),
                            yaxis=dict(
                                gridcolor='gray'
                            ),
                            legend=dict(title=None))
            return st.plotly_chart(fig,use_container_width=True)