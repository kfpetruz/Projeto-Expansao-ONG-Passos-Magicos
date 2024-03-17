# Importação das bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title= 'ONG Passos Mágicos', layout='wide', page_icon= '🤝')

# Título da página
st.title('Projeto ONG Passos Mágicos 🤝')

cor_estilizada = 'color: #0145AC;'
fonte_negrito = 'font-weight: bold;'

dados = [(2016, 70), (2017, 300), (2018, 550), (2019, 812), (2020, 841), (2021, 824), (2022, 940)]

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

dados_estimados_ultimos_anos = dados_estimados[dados_estimados.columns[-6:-1]].T.reset_index()
dados_estimados_ultimos_anos = dados_estimados_ultimos_anos.rename(columns= {'index': 'Ano', 168: 'População do município'})
dados_estimados_ultimos_anos['Ano'] = dados_estimados_ultimos_anos['Ano'].astype('int64')
df_alunos_populacao = pd.merge(linha_do_tempo_ong, dados_estimados_ultimos_anos, on='Ano', how='left')

#GRÁFICO ALUNOS VS POPULAÇÃO
# Criando uma figura e eixos com tamanho personalizado
fig, ax1 = plt.subplots(figsize=(10, 6))
# Plotando a primeira série de dados (Quantidade de alunos)
ax1.plot(df_alunos_populacao['Ano'], df_alunos_populacao['Quantidade de alunos'], color='#0145AC', label='Quantidade de alunos', marker='o')
ax1.set_xlabel('Ano')
ax1.set_ylabel('Quantidade de alunos', color='#0145AC')
# Adicionando rótulos de dados (annotações) para os pontos específicos
for x, y in zip(df_alunos_populacao['Ano'], df_alunos_populacao['Quantidade de alunos']):
    ax1.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0,10), ha='center', color='#0145AC')
# Criando o segundo eixo y (População do município)
ax2 = ax1.twinx()
ax2.plot(df_alunos_populacao['Ano'], df_alunos_populacao['População do município'], color='#82C7A5', label='População do município', marker='o')
ax2.set_ylabel('População do município', color='#82C7A5')
# Adicionando rótulos de dados (annotações) para os pontos específicos
for x, y in zip(df_alunos_populacao['Ano'], df_alunos_populacao['População do município']):
    ax2.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0,10), ha='center', color='#82C7A5')
# Adicionando legenda fora do gráfico
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='center left', bbox_to_anchor=(0.1, 0.1))
# Exibindo o gráfico
plt.title('Quantidade de Alunos vs. População do Município')

dados_2022 = pd.read_excel('tb_populacao_economia_idade_distancia.xlsx')
dados_2022 =  dados_2022[dados_2022['Município']=='Embu-Guaçu']
dados_estimados['2022'] = dados_2022['População no último censo'].values



## VISUALIZAÇÃO NO STREAMLIT
aba1, aba2, aba3 = st.tabs(['Sobre a ONG', 'Fatores de sucesso', 'Impacto Social'])
with aba1:
    st.title('Sobre a ONG')
    st.markdown('<p style="text-align: justify;"> A Passos Mágicos é uma associação sem fins lucrativos de educação complementar, não formal e assistência social que possui o objetivo de transformar a vida de crianças e adolescentes em situação de vulnerabilidade social no município de Embu-Guaçu. A Associação teve início em 1992, auxiliando crianças em orfanato com origem da idealização de seus fundadores: Michelle Flues Ivanoff, Dimitri Ivanoff, Carol Ivanoff e Alexandre Ivanoff.</p>', unsafe_allow_html = True)
    
    st.subheader('O que fazemos?')
    st.markdown('<p style="text-align: justify;">A Associação Passos Mágicos atua dentro do Município de Embu-Guaçu, zona sul de São Paulo, com um programa educacional para crianças e jovens, oferecendo um processo que visa três pontos de impacto: oferecer uma educação de qualidade, suporte psicológico e ampliar a visão de mundo de cada aluno impactado.</p>', unsafe_allow_html = True)
    col1, col2, col3 = st.columns(3)
    with col1: #utilizando a cláusula with, mas poderíamos escrever apenas "col1." antes da métrica
        st.markdown(f"<h2 style='{cor_estilizada}'>3 a cada 20</h2> <span style='{fonte_negrito}'>pessoas de Embu-Guaçu são atendidas</span>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h2 style='{cor_estilizada}'>4 núcleos</h2> <span style='{fonte_negrito}'>distribuídos pelo município </span>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<h2 style='{cor_estilizada}'>Mais de 10.500</h2> <span style='{fonte_negrito}'>horas de aula no Programa de Aceleração do Conhecimento (PAC) </span>", unsafe_allow_html=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True) #Linha 
    st.pyplot(fig)


with aba2:


    col1, col2 = st.columns(2)
    with col1: 
        st.title('Fatores chave de sucesso')
    with col2:
        st.title('Coluna 2')

with aba3:
    col1, col2 = st.columns(2)
    with col1: 
        st.title('Impacto social')
    with col2:
        st.title('Coluna 2')

# 1ª aba - Análise Dados Históricos
# 2ª aba - Resultado das ações na cidade - Fatores-Chave de Sucesso
# 3ª aba - Desempenho dos alUnos - Análise do Impacto Emocional e Social
# 4ª aba - Aprimoramento de estratégias e operações Futuras (PIX, Potencias cidades para expansão(Modelo) e Previsão de aumento de alunos (Quantidade de alunos para os próximos anos))
# 5ª aba - Sobre

# Anotações :
# História da Passos(Overview) - qualificações dos professores
# Linha do tempo de quantidade de alunos, percentual de genero, raça e em relação a Embu-Guaçu de acordo com o ano
# Amostra do desempenho dos alunos: Notas com o passar dos anos , qual idade tem maior desempenho, notas por matéria, avaliação qualitativa (quantidade de comentários sobre os alunos),  tem desistência?
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
        
    