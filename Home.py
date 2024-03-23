# Importação das bibliotecas
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from utils import select_bq


# Configuração da página
st.set_page_config(page_title= 'ONG Passos Mágicos', layout='wide', page_icon= '🤝')

# Título da página
st.title('Projeto ONG Passos Mágicos 🤝')

cor_estilizada = 'color: #0145AC;'
fonte_negrito = 'font-weight: bold;'

dados = [(2016, 70), (2017, 300), (2018, 550), (2019, 812), (2020, 841), (2021, 824), (2022, 970)]

# Criar um DataFrame a partir da lista de tuplas
linha_do_tempo_ong = pd.DataFrame(dados, columns=['Ano', 'Quantidade de alunos'])


dados_estimados = pd.read_csv('Base de dados\\populacao_estimativa_2001_2021.csv',sep = ';', encoding='utf-8-sig')
novos_nomes = dados_estimados.iloc[2]
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

dados_2022 = pd.read_excel('tb_populacao_economia_idade_distancia.xlsx')
dados_2022 =  dados_2022[dados_2022['Município']=='Embu-Guaçu']
dados_estimados['2022'] = dados_2022['População no último censo'].values

dados_estimados_ultimos_anos = dados_estimados[dados_estimados.columns[-7:]].T.reset_index()
dados_estimados_ultimos_anos = dados_estimados_ultimos_anos.rename(columns= {'index': 'Ano', 168: 'População do município'})
dados_estimados_ultimos_anos['Ano'] = dados_estimados_ultimos_anos['Ano'].astype('int64')

df_alunos_populacao = pd.merge(linha_do_tempo_ong, dados_estimados_ultimos_anos, on='Ano', how='left')
df_alunos_populacao['Quantidade de alunos'] = df_alunos_populacao['Quantidade de alunos'].astype('int64')
df_alunos_populacao['População do município'] = df_alunos_populacao['População do município'].astype('int64')

df_alunos_populacao['Alunos/População'] = df_alunos_populacao['Quantidade de alunos'] /df_alunos_populacao['População do município']*100
df_alunos_populacao['Alunos/População'] = df_alunos_populacao['Alunos/População'].apply(lambda x: '{:.2f}'.format(x))


def grafico_duas_linhas_ponto(x,y,y2,percentual):
    # Criar o gráfico
    fig = go.Figure()

    # Adicionar a linha ao gráfico para y
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Quantidade de alunos', line=dict(color='#0145AC')))

    # Adicionar os pontos ao gráfico com os percentuais
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Quantidade de Alunos / População (%)',
                            text=percentual.astype(str)+'%', hoverinfo='text+x+y', marker=dict(color='#0145AC', size=10)))

    # Adicionar a linha ao gráfico para y2
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='População de Embu-Guaçu', yaxis='y2', line=dict(color='#82C7A5')))

    # Atualizar o layout
    fig.update_layout(
        title='Quantidade de alunos da ONG x População de Embu-Guaçu',
        yaxis=dict(title='Quantidade de alunos da ONG', side='left'),
        yaxis2=dict(
            title='População de Embu-Guaçu', 
            overlaying='y', 
            side='right'
        ),
        legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center', yanchor='top')
    )
    return fig

def grafico_tres_linhas_ponto(x,y1,y2,y3,percentual1,percentual2):

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='Quantidade de alunos', line=dict(color='#0145AC')))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='Bolsistas em escola parceira', line=dict(color='#82C7A5')))
    fig.add_trace(go.Scatter(x=x, y=y3, mode='lines', name='Universitários', line=dict(color='#CD5C5C')))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='markers', name='Bolsistas / Quantidade de alunos (%)',
                            text=percentual1.astype(str)+'%', hoverinfo='text+x+y', marker=dict(color='#82C7A5', size=10)))
    fig.add_trace(go.Scatter(x=x, y=y3, mode='markers', name='Universitários / Quantidade de alunos (%)',
                            text=percentual2.astype(str)+'%', hoverinfo='text+x+y', marker=dict(color='#CD5C5C', size=10)))

    
    fig.update_layout(title='Quantidade de Alunos x Bolsistas x Universitários da ONG',
                    xaxis_title='Ano',
                    yaxis_title='Quantidade',
                    legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center', yanchor='top'))
    return fig

# Função para plotar o gráfico com base nas categorias selecionadas
def plotar_grafico(categorias_selecionadas):
    fig = go.Figure()
    
    # Adicionar barras para cada categoria selecionada
    for categoria in categorias_selecionadas:
        if categoria == 'Professor':
            fig.add_trace(go.Bar(
                x=linha_do_tempo_completo['Ano'],
                y=linha_do_tempo_completo['Professores'],
                name='Professores',
                marker_color='#0145AC'
            ))

        elif categoria == 'Psicóloga':
            fig.add_trace(go.Bar(
                x=linha_do_tempo_completo['Ano'],
                y=linha_do_tempo_completo['Psicólogas'],
                name='Psicólogas',
                marker_color='#82C7A5'
            ))

        elif categoria == 'Psicopedagoga':
            fig.add_trace(go.Bar(
                x=linha_do_tempo_completo['Ano'],
                y=linha_do_tempo_completo['Psicopedagoga'],
                name='Psicopedagogas',
                marker_color='#CD5C5C'
            ))
        
        elif categoria == 'Psiquiatra':
            fig.add_trace(go.Bar(
                x=linha_do_tempo_completo['Ano'],
                y=linha_do_tempo_completo['Psiquiatra'],
                name='Psiquiatras',
                marker_color='#F4A460'
            ))

        elif categoria == 'Assistente Social':
            fig.add_trace(go.Bar(
                x=linha_do_tempo_completo['Ano'],
                y=linha_do_tempo_completo['Assistente Social'],
                name='Assistente Social',
                marker_color='#D8BFD8'
            ))

    # Atualizar layout do gráfico
    fig.update_layout(
        #legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center', yanchor='top'),
        title='Formação da equipe ao longo dos anos',
        xaxis=dict(title='Ano'),
        yaxis=dict(title='Quantidade'),
        barmode='stack'
    )

    st.plotly_chart(fig, use_container_width=True)

## VISUALIZAÇÃO NO STREAMLIT
aba1, aba2, aba3 = st.tabs(['Sobre a ONG', 'Fatores de sucesso', 'Impacto Social'])
with aba1:

    st.markdown('<p style="text-align: justify;"> A Passos Mágicos é uma organização social, cujo objetivo é transformar a vida de crianças e adolescentes do Município de Embu-Guaçu, zona sul de São Paulo, em situação de vulnerabilidade social, através da educação.</p>', unsafe_allow_html = True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: #utilizando a cláusula with, mas poderíamos escrever apenas "col1." antes da métrica
        st.markdown(f"<h2 style='{cor_estilizada}'>+ 30 anos</h2> <span style='{fonte_negrito}'>transformando a vida de crianças e jovens de baixa renda</span>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h2 style='{cor_estilizada}'>4 núcleos</h2> <span style='{fonte_negrito}'>distribuídos pelo município </span>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<h2 style='{cor_estilizada}'>+ 1000</h2> <span style='{fonte_negrito}'>alunos anual no programa de Aceleração do Conhecimento</span>", unsafe_allow_html=True) 
    with col4:
        st.markdown(f"<h2 style='{cor_estilizada}'>6 anos</h2> <span style='{fonte_negrito}'>idade mínima de entrada dos beneficiários</span>", unsafe_allow_html=True)

    st.markdown('<p style="text-align: justify;"></p>', unsafe_allow_html = True)
    st.markdown('<p style="text-align: justify;"></p>', unsafe_allow_html = True)
    
    st.markdown('<p style="text-align: justify;"> A Associação teve início em 1992, auxiliando crianças em orfanato com origem da idealização de seus fundadores: Michelle Flues Ivanoff, Dimitri Ivanoff, Carol Ivanoff e Alexandre Ivanoff.</p><p style="text-align: justify;">Em 2016, decidem ampliar o programa para que mais jovens tivessem acesso a essa fórmula mágica para transformação que inclui: educação de qualidade, auxílio psicológico/psicopedagógico, ampliação de sua visão de mundo e protagonismo. Passaram então a atuar como um projeto social e educacional, criando assim a Associação Passos Mágicos.</p>', unsafe_allow_html = True)
    
    st.markdown(f"<h3 style='{cor_estilizada}'>O que fazemos?</h3>", unsafe_allow_html=True)

    
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Aceleração do Conhecimento:</span> Oferecer uma educação de qualidade, suporte psicológico e ampliar a visão de mundo de cada aluno impactado. Possui aulas de alfabetização, língua portuguesa e matemática para crianças e adolescentes. Os alunos são divididos por nível de conhecimento, determinado por meio de uma prova de sondagem que é realizada ao ingressarem na Passos Mágicos, e são inseridos em turmas que variam da alfabetização até o nível 8, sendo:</p>', unsafe_allow_html = True)
    aceleracao = {
    'Fase de alfabetização': ['Alunos que estejam em fase de alfabetização ou que apresentem dificuldade na leitura e na escrita'],
    'Fases 1 e 2': ['Focadas em conteúdo do ensino fundamental 1, sendo explorados com mais detalhes de um nível para o outro'],
    'Fases 3 e 4': ['Focadas em conteúdo do ensino fundamental 2, sendo explorado com mais detalhes de um nível para o outro'],
    'Fases 5 e 6':['Focadas em conteúdos para jovens e adolescentes do ensino médio para um maior nível de conhecimento'],
    'Fases 7 e 8':['Destinadas aos jovens alunos terceiranistas e vestibulandos com foco na aceleração do conhecimento']
    }
    df_aceleracao = pd.DataFrame(aceleracao)
    html = df_aceleracao.to_html(index=False)
    # Adicionar estilos CSS para centralizar os nomes das colunas e justificar o texto das células

    # Adicionando estilos CSS para a cor da borda de todas as células
    # html_estilizado = html.replace('<th>', '<th style=\'border: 2px solid #0145AC; color: #0145AC; text-align: center;\'>').replace('<td>', '<td style=\'border: 2px solid #0145AC; text-align: center;\'>')
    html_estilizado = html.replace('<th>', '<th style=\'border: 2px solid #0145AC; text-align: center;\'>').replace('<td>', '<td style=\'border: 2px solid #0145AC; text-align: center;\'>')

    # Exibir a tabela estilizada no Streamlit
    st.write("<style>table {{ width: 100%; border-collapse: collapse; }} th, td {{ padding: 10px; }}</style>{}".format(html_estilizado), unsafe_allow_html=True)

    st.markdown('<p style="text-align: justify;"></p>', unsafe_allow_html = True)

    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Programas Especiais:</span> Projeto de apadrinhamento e de intercâmbio, visando uma maior integração dos alunos com diferentes ambientes e culturas.</p>', unsafe_allow_html = True)
    programas = {
    'Apadrinhamento': ['Os alunos que se destacam dentro da Associação Passos Mágicos, a partir da evolução apresentada dentro da aplicação do conhecimento absorvido e dos princípios vividos, são expostos a diversas oportunidades e, dentre elas, a de ser apadrinhado e viver a experiência de estudar em uma escola de ensino particular.'],
    'Intercâmbio': ['Visando uma maior integração dos alunos com diferentes ambientes e culturas, a Associação Passos Mágicos promove diversas atividades que possibilitam esse contato.'],
    'Graduação': ['O suporte da Passos Mágicos no desenvolvimento acadêmico de nossos alunos, se estende além da fase escolar.']
    }
    df_programas = pd.DataFrame(programas)
    html = df_programas.to_html(index=False)

    # Adicionando estilos CSS para a cor da borda de todas as células
    html_estilizado = html.replace('<th>', '<th style=\'border: 2px solid #0145AC; text-align: center;\'>').replace('<td>', '<td style=\'border: 2px solid #0145AC; text-align: center;\'>')

    # Exibir a tabela estilizada no Streamlit
    st.write("<style>table {{ width: 100%; border-collapse: collapse; }} th, td {{ padding: 10px; }}</style>{}".format(html_estilizado), unsafe_allow_html=True)

    st.markdown('<p style="text-align: justify;"></p>', unsafe_allow_html = True)

    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Eventos e ações sociais:</span> Anualmente, em prol dos alunos, são promovidas campanhas de arrecadação para presentear as centenas de crianças e adolescentes Passos Mágicos.</p>', unsafe_allow_html = True)
    eventos = {
    'Materiais escolares': ['Campanha de arrecadação de doações de materiais para os alunos bolsistas  e alunos no geral.'],
    'Páscoa Mágica': ['Arrecadação de ovos de páscoa, barras e caixas de chocolate para distribuir aos alunos.'],
    'Dia das Crianças': ['Arrecadação de brinquedos para os alunos.'],
    'Campanha do Agasalho': ['Arrecadação de roupas de inverno  para os alunos e suas famílias.'],
    'Natal mágico': ['Na ação são entregues presentes pensados especialmente nos alunos e, as sacolas feitas a partir das doações e distribuídas aos familiares das crianças.'],
    'Confraternização de encerramento': ['Anualmente um evento de confraternização é promovido para celebrar as conquistas e realizações do ano que se passou.']
    }
    df_eventos = pd.DataFrame(eventos)
    html = df_eventos.to_html(index=False)

    # Adicionando estilos CSS para a cor da borda de todas as células
    html_estilizado = html.replace('<th>', '<th style=\'border: 2px solid #0145AC; text-align: center;\'>').replace('<td>', '<td style=\'border: 2px solid #0145AC; text-align: center;\'>')

    # Exibir a tabela estilizada no Streamlit
    st.write("<style>table {{ width: 100%; border-collapse: collapse; }} th, td {{ padding: 10px; }}</style>{}".format(html_estilizado), unsafe_allow_html=True)

with aba2:

    st.markdown(f"<p style='text-align: justify;'> Indicadores de impacto da Passos Mágicos em <span style='{fonte_negrito}'>2023</span>:</p>", unsafe_allow_html = True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<h2 style='{cor_estilizada}'>4400</h2> <span style='{fonte_negrito}'>pessoas impactadas (Considerando a média de 4 familiares por aluno)</span>", unsafe_allow_html=True) 
    with col2:
        st.markdown(f"<h2 style='{cor_estilizada}'>98</h2> <span style='{fonte_negrito}'>bolsistas em instituições de ensino particular</span>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<h2 style='{cor_estilizada}'>103</h2> <span style='{fonte_negrito}'>universitários em instituições de ensino superior</span>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<h2 style='{cor_estilizada}'>41</h2> <span style='{fonte_negrito}'>universitários formados</span>", unsafe_allow_html=True) 
       
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True) #Linha 
    st.markdown(f"<p style='text-align: justify;'> Variação do número de alunos beneficiados, bem como à relação entre bolsistas e universitários nas escolas parceiras ao longo do tempo:</p>", unsafe_allow_html = True)
    
    
    dados = [(2016, 70, 26, 0, 5, 1, 0, 0, 0), (2017, 300, 35, 0, 6, 1, 1, 0, 0), (2018, 550, 80, 1, 7, 1, 1, 0, 0), (2019, 812, 106, 2, 9, 2, 1, 0, 0), (2020, 841, 112, 26, 9, 2, 1, 0, 0), (2021, 824, 133, 51, 12, 2, 2, 0, 0), (2022, 970, 112, 71, 13, 3, 3, 1, 1), (2023, 1100, 100, 94, 14, 3, 3, 1, 1)]
    linha_do_tempo_completo = pd.DataFrame(dados, columns=['Ano', 'Quantidade de alunos', 'Bolsistas em escola parceira', 'Universitários', 'Professores', 'Psicólogas', 'Psicopedagoga', 'Psiquiatra', 'Assistente Social'])
    linha_do_tempo_completo['Bolsistas/Alunos'] = linha_do_tempo_completo['Bolsistas em escola parceira'] /linha_do_tempo_completo['Quantidade de alunos']*100
    linha_do_tempo_completo['Bolsistas/Alunos'] = linha_do_tempo_completo['Bolsistas/Alunos'].apply(lambda x: '{:.2f}'.format(x))
    linha_do_tempo_completo['Universitários/Alunos'] = linha_do_tempo_completo['Universitários'] /linha_do_tempo_completo['Quantidade de alunos']*100
    linha_do_tempo_completo['Universitários/Alunos'] = linha_do_tempo_completo['Universitários/Alunos'].apply(lambda x: '{:.2f}'.format(x))

    st.plotly_chart(grafico_tres_linhas_ponto(linha_do_tempo_completo['Ano'],linha_do_tempo_completo['Quantidade de alunos'],linha_do_tempo_completo['Bolsistas em escola parceira'],linha_do_tempo_completo['Universitários'],linha_do_tempo_completo['Bolsistas/Alunos'],linha_do_tempo_completo['Universitários/Alunos']), use_container_width=True)
    
    st.markdown(f"<p style='text-align: justify;'> Evolução da quantidade de alunos atendidos em relação a população do município de Embu-Guaçu:</p>", unsafe_allow_html = True)
    st.plotly_chart(grafico_duas_linhas_ponto(df_alunos_populacao['Ano'],df_alunos_populacao['Quantidade de alunos'],df_alunos_populacao['População do município'],df_alunos_populacao['Alunos/População'] ), use_container_width=True)
    
   


    st.markdown(f"<p style='text-align: justify;'> A equipe Passos Mágicos é formada por profissionais que têm em mente o objetivo de atuarem como agentes transformadores da vida de cada um dos alunos.</p>", unsafe_allow_html = True)
    # Interface do usuário com multiselect (com alunos e professores pré-selecionados)
    categorias_selecionadas = st.multiselect(
        'Selecione as categorias:',
        ['Professor','Psicóloga', 'Psicopedagoga', 'Psiquiatra', 'Assistente Social'],
        default=['Professor','Psicóloga','Psicopedagoga', 'Psiquiatra', 'Assistente Social']  # Predefinindo Professor e Aluno como selecionados
    )

    # Plotar gráfico com base nas categorias selecionadas
    plotar_grafico(categorias_selecionadas)

with aba3:
    
    st.markdown(f"<p style='text-align: justify;'> Análise da <span style='{fonte_negrito}'>PEDE (Pesquisa de Desenvolvimento Educacional)</span> dos alunos da Passos Mágicos entre os anos de <span style='{fonte_negrito}'>2020 a 2022</span>:</p>", unsafe_allow_html = True)
    tabela = 'tb_pede_passos'
    dados_passos_tratado = select_bq (tabela)
    # st.write(dados_passos_tratado)
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        alunos_distintos = len(dados_passos_tratado['NOME'].unique())
        st.markdown(f"<h2 style='{cor_estilizada}'>{alunos_distintos}</h2> <span style='{fonte_negrito}'>alunos distintos analisados na pesquisa</span>", unsafe_allow_html=True) 
    with col2:
        # idade = pd.to_numeric(dados_passos_tratado['IDADE_ALUNO'], errors='coerce').dropna()
        # idade_min = int(idade.min())
        # idade_max = int(idade.max())
        # st.markdown(f"<h2 style='{cor_estilizada}'>Entre {idade_min} a {idade_max}</h2> <span style='{fonte_negrito}'>idade dos alunos em 2020</span>", unsafe_allow_html=True) 
        dados_passos_sem_nome = dados_passos_tratado.drop('NOME', axis=1)
        dados_passos_2020 = dados_passos_sem_nome[dados_passos_sem_nome['ANO']=='2020']
        dados_passos_2020_drop = dados_passos_2020.drop('ANO', axis=1)
        # Substituir valores vazios por None
        dados_passos_2020_drop.replace('', np.nan, inplace=True)
        # Substituir valores None por NaN
        dados_passos_2020_drop.fillna(np.nan, inplace=True)
        alunos_distintos_2020 = len(dados_passos_2020_drop.dropna(how='all'))
        percentual_alunos_distintos_2020 = alunos_distintos_2020/linha_do_tempo_completo[linha_do_tempo_completo['Ano']==2020]['Quantidade de alunos'].iloc[0]*100
        percentual_alunos_distintos_2020 = int(round(percentual_alunos_distintos_2020,0))
        st.markdown(f"<h2 style='{cor_estilizada}'>{alunos_distintos_2020}</h2> <span style='{fonte_negrito}'>respostas em 2020 <br>({percentual_alunos_distintos_2020}% do total de alunos no ano)</span>", unsafe_allow_html=True) 
        
    with col3:
        # dados_pv = dados_passos_tratado[dados_passos_tratado['PONTO_VIRADA']=='Sim']
        # alunos_distintos_pv = len(dados_pv['NOME'].unique())
        # st.markdown(f"<h2 style='{cor_estilizada}'>{alunos_distintos_pv}</h2> <span style='{fonte_negrito}'>alunos que atigiram o ponto de virada nesse período</span>", unsafe_allow_html=True) 
        dados_passos_2021 = dados_passos_sem_nome[dados_passos_sem_nome['ANO']=='2021']
        dados_passos_2021_drop = dados_passos_2021.drop('ANO', axis=1)
        # Substituir valores vazios por None
        dados_passos_2021_drop.replace('', np.nan, inplace=True)
        # Substituir valores None por NaN
        dados_passos_2021_drop.fillna(np.nan, inplace=True)
        alunos_distintos_2021 = len(dados_passos_2021_drop.dropna(how='all'))
        percentual_alunos_distintos_2021 = alunos_distintos_2021/linha_do_tempo_completo[linha_do_tempo_completo['Ano']==2021]['Quantidade de alunos'].iloc[0]*100
        percentual_alunos_distintos_2021 = int(round(percentual_alunos_distintos_2021,0))
        st.markdown(f"<h2 style='{cor_estilizada}'>{alunos_distintos_2021}</h2> <span style='{fonte_negrito}'>respostas em 2021 <br>({percentual_alunos_distintos_2021}% do total de alunos no ano)</span>", unsafe_allow_html=True) 
    with col4:
        # dados_bolsa = dados_passos_tratado[dados_passos_tratado['BOLSISTA']=='Sim']
        # alunos_distintos_bolsa = len(dados_bolsa['NOME'].unique())
        # st.markdown(f"<h2 style='{cor_estilizada}'>{alunos_distintos_bolsa}</h2> <span style='{fonte_negrito}'>alunos bolsistas em 2022</span>", unsafe_allow_html=True) 
        dados_passos_2022 = dados_passos_sem_nome[dados_passos_sem_nome['ANO']=='2022']
        dados_passos_2022_drop = dados_passos_2022.drop('ANO', axis=1)
        # Substituir valores vazios por None
        dados_passos_2022_drop.replace('', np.nan, inplace=True)
        # Substituir valores None por NaN
        dados_passos_2022_drop.fillna(np.nan, inplace=True)
        alunos_distintos_2022 = len(dados_passos_2022_drop.dropna(how='all'))
        percentual_alunos_distintos_2022 = alunos_distintos_2022/linha_do_tempo_completo[linha_do_tempo_completo['Ano']==2022]['Quantidade de alunos'].iloc[0]*100
        percentual_alunos_distintos_2022 = int(round(percentual_alunos_distintos_2022,0))
        st.markdown(f"<h2 style='{cor_estilizada}'>{alunos_distintos_2022}</h2> <span style='{fonte_negrito}'>respostas em 2022 <br>({percentual_alunos_distintos_2022}% do total de alunos no ano)</span>", unsafe_allow_html=True) 
# Big numbers com percentual
# Usuário escolher entre pedra e INDE
# Pedra -> Gráfico de barras (Ponto de virada por pedra)
# INDE -> Métricas que compõe o INDE + INDE - Colocar o descritivo do racional - Multiseleção
# Fazer um gráfico por matéria quebrado por fase
# Total de alunos por fase x Fase ideal - Filtro por ano (Total de alunos por fase x Fase ideal para o aluno) 
    st.markdown('<p style="text-align: justify;"></p>', unsafe_allow_html = True)
    st.markdown('<p style="text-align: justify;"></p>', unsafe_allow_html = True)
    
    st.markdown(f"<p style='text-align: justify;''> Do total de alunos <span style='{fonte_negrito}'>distintos</span>, <span style='{fonte_negrito}'>500</span> estiveram presentes nos três anos consecutivos.</p>", unsafe_allow_html = True)

# Média do tempo de casa dos alunos em cada ano, quantidade de alunos em cada ano
        
# --------------------------------------------------------------
        
# 1ª aba - História da Passos(Overview), Análise Dados Históricos e Resultado das ações na cidade - 
# 2ª aba - Fatores-Chave de Sucesso - Colocar os big numbers, linha do tempo (Ver o que mais da para aproveitar dos documentos do site e acrescentar percentual por genero, raça, idade, quantidade de professores(possível bignumber), alunos formados no ensino superior(Relatório universitários completo), cursando ensino superior - colocar que é referente a 2022 os bignumbers - Colocar descrições com cores destaques 
# 3ª aba - Análise do Impacto Emocional e Social - Desempenho dos alUnos - (Análise do dataset - Notas com o passar dos anos , qual idade tem maior desempenho, notas por matéria, avaliação qualitativa (quantidade de comentários sobre os alunos),  tem desistência? ponto de virada PV) - colocar cursos que os alunos estão fazendo
# 4ª aba - Aprimoramento de estratégias e operações Futuras (PIX, Potencias cidades para expansão(Modelo) e Previsão de aumento de alunos (Quantidade de alunos para os próximos anos))
# 5ª aba - Sobre

# Anotações :
# História da Passos(Overview) - qualificações dos professores


# Quantidade de população de Embu Guaçu, percentual de matriculados no ensino básico, PIB

# Qual o impacto e potencial para a região?
# Onde direcionar mais esforços e recursos?
# O quanto a psicologia impacta a vida das crianças?
# Como medir o desempenho das crianças? Antes e depois
# Como ter uma comunicação mais efetiva com todos os alunos?
# Como administrar/monitorar o aluno? Sem perder o contato humanizado
# Quantas pessoas conhecem a Passos? Como mudar o comportamento das pessoas? 
# Qual a Previsão de receita e pessoas impactadas?
# Em que momento o aluno começa a acreditar no futuro?
# Como reproduzir em outras regiões as ações da Passos?
        
    