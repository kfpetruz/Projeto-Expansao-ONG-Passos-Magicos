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
# Leitura do dados no site e armazenamento no banco de dados no BigQuery
def webscraping(url,coluna): # a aplicação faz leitura de dois sites, fazendo necessário a identificação da URL e como será chamada a coluna de valores
    dados = pd.read_html(url, encoding='utf-8', decimal=',')
    dados = dados[2]
    dados.columns = dados.iloc[0]
    dados = dados[1:]
    dados = dados.rename(columns={dados.columns[1]: coluna})
    dados['Data'] = pd.to_datetime(dados['Data'], format = '%d/%m/%Y')
    dados[dados.columns[1]] = dados[dados.columns[1]].astype(float)
    dados[dados.columns[1]]= dados[dados.columns[1]]/100
    dados.set_index('Data', inplace = True)
    dados.sort_index(ascending=True, inplace=True)
    insert_dados = dados.reset_index()
    insert_dados['Data'] =  pd.to_datetime(insert_dados['Data']).dt.strftime('%d/%m/%Y')
    projeto = 'sixth-aloe-402921'
    dataset = 'dados_preco_petroleo'
    parametro =  'replace'
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    if coluna == 'Preco':
        tabela = 'tb_preco_petroleo'
        insert_dados.to_gbq(destination_table= f'{projeto}.{dataset}.{tabela}',
                    project_id = projeto,
                    if_exists = parametro,
                    credentials = credentials)
    else:
        tabela = 'tb_taxa_cambio'
        insert_dados.to_gbq(destination_table= f'{projeto}.{dataset}.{tabela}',
                    project_id = projeto,
                    if_exists = parametro,
                    credentials = credentials)
    return dados

# Armazenamento dos dados em cache
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

# Gráfico de decomposição sazonal, que pode ser selecionados para diferentes períodos pelo usuário
def decomposicao(dados,resultado):
    st.subheader('Série Temporal Original')
    st.line_chart(dados)
    st.subheader('Tendência')
    st.markdown('<p style="text-align: justify;">Quando falamos sobre tendência na decomposição de uma série temporal, estamos interessados em identificar padrões de crescimento ou declínio que ocorrem ao longo de um período de tempo significativo, ignorando as variações sazonais e flutuações aleatórias que podem ocorrer em escalas de tempo menores.</p>', unsafe_allow_html = True)
    st.line_chart(resultado.trend)
    st.subheader('Sazonalidade')
    st.markdown('<p style="text-align: justify;">A sazonalidade indica variações sistemáticas que ocorrem em determinados momentos ou períodos do ano e são independentes da tendência de longo prazo e das flutuações aleatórias na série temporal. Ela reflete regularidades que podem ser observadas ao longo de múltiplos ciclos sazonais.</p>', unsafe_allow_html = True)
    st.line_chart(resultado.seasonal)
    st.subheader('Residual')
    st.markdown('<p style="text-align: justify;">Na decomposição de uma série temporal, o resíduo (também conhecido como erro ou componente aleatório) é a parte da série que não pode ser explicada pela tendência de longo prazo e pela sazonalidade. Em outras palavras, o resíduo representa as flutuações irregulares e imprevisíveis que não seguem nenhum padrão discernível na série temporal.</p>', unsafe_allow_html = True)
    st.line_chart(resultado.resid)

# Realização do teste de Dickey-Fuller Aumentado e dos gráfico de autocorreção de acordo com a seleção do usuário
def teste_estatistico(dados,string_teste):
    st.subheader('Testes Estatísticos')
    st.markdown('<p style="text-align: justify;">O teste de Dickey-Fuller Aumentado (ADF), frequentemente implementado na função adfuller do pacote statsmodels em Python, é um teste estatístico utilizado para determinar se uma série temporal é estacionária ou não. Uma série temporal é considerada estacionária quando suas propriedades estatísticas, como média e variância, permanecem constantes ao longo do tempo. Em outras palavras, não há padrões sistemáticos ou tendências discerníveis na série que afetem sua média ou variância.</p>', unsafe_allow_html = True)

    st.markdown(f'<p style="text-align: justify;"><span style="font-weight: bold">{string_teste}</span></p>', unsafe_allow_html = True)
    
    resultado_adf = adfuller(dados)
    st.markdown(f'<p style="text-align: justify;">Estatística do teste ADF: {resultado_adf[0]}.</p>', unsafe_allow_html = True)
    st.markdown(f'<p style="text-align: justify;">Valor-p: {resultado_adf[1]}.</p>', unsafe_allow_html = True)
    st.markdown(f'<p style="text-align: justify;">Valores críticos:</p>', unsafe_allow_html = True)
    for chave, valor in resultado_adf[4].items():
        st.markdown(f'<p style="text-align: justify;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{chave}: {valor}.</p>', unsafe_allow_html = True)
    st.markdown('<p style="text-align: justify;">Se o valor-p for menor que o nível de significância escolhido (geralmente 0.05), rejeitamos a hipótese nula e concluímos que a série é estacionária. Caso contrário, não rejeitamos a hipótese nula e inferimos que a série não é estacionária. Isso significa que a série possui tendência.</p>', unsafe_allow_html = True)
    
    # Interpretação do resultado do teste
    if resultado_adf[1] < 0.05:
        st.markdown(f'<p style="text-align: justify;">Dessa forma, a série temporal é estacionária (rejeitamos a hipótese nula).</p>', unsafe_allow_html = True)
    else:
        st.markdown(f'<p style="text-align: justify;">Dessa forma, a série temporal não é estacionária (falhamos em rejeitar a hipótese nula).</p>', unsafe_allow_html = True)

    st.subheader('Gráficos de Autocorrelação')
    st.markdown(f'<p style="text-align: justify;">Para identificar a presença de sazonalidade nos gráficos de autocorrelação simples (ACF) e autocorrelação parcial (PACF), é possível procurar padrões de picos significativos em intervalos regulares.</p>', unsafe_allow_html = True)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Autocorrelação Simples (ACF):</span> os picos indicam a correlação entre a série temporal atual e suas observações passadas em vários lags. Se houver picos significativos em intervalos regulares, isso sugere a presença de sazonalidade na série temporal.</p>', unsafe_allow_html = True)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Autocorrelação Parcial (PACF):</span> os picos representam a correlação entre a série temporal atual e suas observações passadas, removendo o efeito das observações intermediárias. Picos significativos em intervalos regulares no PACF também indicam a presença de sazonalidade.</p>', unsafe_allow_html = True)
    
    # Costrução dos gráficos de autocorrelação
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        plot_acf(dados, ax=ax)
        plt.xlabel('Lag')
        plt.ylabel('ACF')
        plt.title('Função de Autocorrelação (ACF)')
        fig.patch.set_alpha(0)
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        plot_pacf(dados, ax=ax)
        plt.xlabel('Lag')
        plt.ylabel('PACF')
        plt.title('Função de Autocorrelação (PACF)')
        fig.patch.set_alpha(0)
        st.pyplot(fig)

# Função para WMAPE (Weighted Mean Absolute Percentage Error), uma métrica de avaliação de desempenho usada em previsões e modelos de séries temporais. 
def wmape(y_true, y_pred):
  return np.abs(y_true-y_pred).sum() / np.abs(y_true).sum()

# Armazenamento do modelo em cache
@st.cache_resource 
# Função criada para encontrar a melhor perfomance do modelo ETS, com base nos dados de treino e teste
def modelo_ets_perfomance(dados, qt_dias):
    dados = dados.tail(qt_dias)
    # Definindo os parâmetros a serem testados
    parametros_grid = {
        'trend': ['additive', 'multiplicative'],
        'seasonal': ['additive', 'multiplicative'],
        'seasonal_periods': [30],  # Assumindo um padrão sazonal mensal
    }

    # Configurando a validação cruzada de séries temporais
    tscv = TimeSeriesSplit(n_splits=5)

    # Inicializando as variáveis para armazenar os melhores resultados
    melhor_mae = float('inf')
    melhor_wmape = float('inf')
    melhores_parametros = None
    df_completo = pd.DataFrame(columns=['Qtd dias treinados', 'Qtd dias testados', 'MAE', 'WMAPE', 'Tendência', 'Sazonalidade', 'Períodos Sazonais'])

    # Loop através dos parâmetros
    for trend in parametros_grid['trend']:
        for seasonal in parametros_grid['seasonal']:
            for seasonal_periods in parametros_grid['seasonal_periods']:
                # Criando o modelo ETS
                modelo_ets = ExponentialSmoothing(dados['Preco'], trend=trend, seasonal=seasonal, seasonal_periods=seasonal_periods)

                # Iterando sobre diferentes janelas de treinamento
                for train_index, test_index in tscv.split(dados):
                    dados_treino, dados_teste = dados.iloc[train_index], dados.iloc[test_index]

                    # Treinando o modelo
                    resultado = modelo_ets.fit()

                    # Fazendo previsões
                    previsao = resultado.forecast(steps=len(dados_teste))

                    # Calculando o MAE
                    mae = mean_absolute_error(dados_teste['Preco'].values, previsao)

                    # Calculando o WMAPE
                    wmape_teste = wmape(dados_teste['Preco'].reset_index(drop=True), previsao.reset_index(drop=True)) 

                    # Dados para adicionar como nova linha, para retornar todos os resultados
                    nova_linha = {'Qtd dias treinados': len(dados_treino), 'Qtd dias testados': len(dados_teste), 'MAE': mae, 'WMAPE': f'{wmape_teste:.2%}', 'Tendência': trend, 'Sazonalidade': seasonal, 'Períodos Sazonais': seasonal_periods}
                    
                    # Criando um novo DataFrame com a nova linha
                    nova_linha_df = pd.DataFrame([nova_linha])
                    
                    # Adicionando nova linha ao DataFrame original usando concatenação
                    df_completo = pd.concat([df_completo, nova_linha_df], ignore_index=True)

                # Atualizando os melhores parâmetros se este conjunto tiver um MAE menor
                if mae < melhor_mae:
                    melhor_mae = mae
                    melhores_parametros = {'trend': trend, 'seasonal': seasonal, 'seasonal_periods': seasonal_periods}
                    melhores_dados_treinamento = dados_treino
                    melhores_dados_teste = dados_teste
                    melhor_resultado_fit = resultado
                    melhor_wmape = wmape_teste

    return melhor_mae, melhores_parametros, melhores_dados_teste, melhores_dados_treinamento, melhor_resultado_fit, melhor_wmape,df_completo

# Armazenamento do modelo em cache
@st.cache_resource
# Modelo ETS para previsão dos dias, utilizando qtd de dias recentes para treinamento, qtd de dias que deseja prever e, os parâmetros de tendência e sazonalidade
def modelo_ets_previsao(dados, qt_dias_historico, qt_dias_prever, trend, seasonal):
    dados = dados.tail(qt_dias_historico)

    # Criando o modelo ETS
    modelo_ets = ExponentialSmoothing(dados['Preco'], trend=trend, seasonal=seasonal, seasonal_periods=30)

    # Treinando o modelo
    resultado = modelo_ets.fit()

    # Fazendo previsões
    previsao = resultado.forecast(steps=qt_dias_prever)

    return previsao

# Futuros dias úteis da semana
def dias_uteis_futuros(data_inicial,qtd_dias):
  dias_uteis = []
  while len(dias_uteis) < qtd_dias:
      # Avança um dia de cada vez
      data_inicial += timedelta(days=1)  
      # Verifica se o dia da semana não é sábado (5) nem domingo (6)
      if data_inicial.weekday() not in [5, 6]:
          dias_uteis.append(data_inicial)
  return dias_uteis

# Gráfico de linha com marcação dos picos máximos e mínimos dos preços
def graf_marcado_max_min(dados):
    # Encontrar índice do maior e menor Preco
    indice_maior_preco = dados['Preco'].idxmax()
    indice_menor_preco = dados['Preco'].idxmin()

    # Plotar o gráfico
    fig = go.Figure()

    # Adicionar dados de linha
    fig.add_trace(go.Scatter(x=dados['Data'], y=dados['Preco'], mode='lines',showlegend=False))

    # Adicionar pico máximo
    fig.add_trace(go.Scatter(x=[dados['Data'].loc[indice_maior_preco]], y=[dados['Preco'].loc[indice_maior_preco]],
                            mode='markers', name='Máximo', marker=dict(color='red', size=10)))

    # Adicionar pico mínimo
    fig.add_trace(go.Scatter(x=[dados['Data'].loc[indice_menor_preco]], y=[dados['Preco'].loc[indice_menor_preco]],
                            mode='markers', name='Mínimo', marker=dict(color='green', size=10)))

    # Atualizar layout do gráfico
    fig.update_layout(title='Preço por barril de Petróleo ao longo do tempo',
                    xaxis_title='Data', yaxis_title='Preço (US$)',legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center', yanchor='top'))
    
    return fig

# Gráfico de dois eixos, com multiplas marcações de picos mínimos e máximos ao longo do tempo
def graf_marcado_multiplos(x, y, picos_indices_max, picos_indices_min,y2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Preço do barril de Petróleo (US$)'))

    # Adiciona a série de picos mais altos apenas uma vez
    if np.any(picos_indices_max):
        x_max = [x[i] for i in picos_indices_max]
        y_max = [y[i] for i in picos_indices_max]
        fig.add_trace(go.Scatter(x=x_max, y=y_max, mode='markers', name='Máximos', marker=dict(color='red', size=10)))

    # Adiciona a série de picos mais baixos apenas uma vez
    if np.any(picos_indices_min):
        x_min = [x[i] for i in picos_indices_min]
        y_min = [y[i] for i in picos_indices_min]
        fig.add_trace(go.Scatter(x=x_min, y=y_min, mode='markers', name='Mínimos', marker=dict(color='green', size=10)))

    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='Taxa de Câmbio (R$/US$)', yaxis='y2'))

    fig.update_layout( title='Preço do barril de Petróleo x Taxa de Câmbio',
        yaxis=dict(title='Preço do barril de Petróleo (US$)', side='left'),
        yaxis2=dict(title='Taxa de Câmbio (R$/US$)', overlaying='y', side='right'),
        legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center', yanchor='top')
    )
    return fig