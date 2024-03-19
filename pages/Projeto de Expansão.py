# Importação das bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title= 'ONG Passos Mágicos', layout='wide', page_icon= '🤝')

# Título da página
st.title('Projeto de expansão 🤝')

dados_externos = pd.read_excel('tb_populacao_economia_idade_distancia.xlsx')

## VISUALIZAÇÃO NO STREAMLIT
aba1, aba2= st.tabs(['Modelo', 'Propostas'])
with aba1:
    st.markdown('<p style="text-align: justify;"> Para auxiliar a ONG em seu desejo de expandir as atividades, ampliando a capacidade para que ela possa atender e mudar a vida de centenas de crianças e adolescentes como vem fazendo há anos na cidade de Embu-Guaçu, foram criados dois modelos levando em consideração dados econômicos, de população, educacionais e de distância da cidade sede.</p>', unsafe_allow_html = True)

    st.markdown('<p style="text-align: justify;"> Em ambos os modelos foram consideradas as 645 cidades do estado de São Paulo e atribuídos pesos aos seus indicadores econômicos, populacionais e educacionais, com base no último censo geográfico, por ordem de prioridade:.</p>', unsafe_allow_html = True)

    st.markdown('<p style="text-align: justify;"> <strong> Quanto menor, maior o peso: </strong> </p>', unsafe_allow_html = True)
    st.markdown('- <p style="text-align: justify;"> Salário médio dos trabalhadores formais;</p>', unsafe_allow_html = True)
    st.markdown('- <p style="text-align: justify;"> Índice de desenvolvimento humano municipal (IDHM);</p>', unsafe_allow_html = True)
    st.markdown('- <p style="text-align: justify;"> PIB per capita;</p>', unsafe_allow_html = True)
    st.markdown('- <p style="text-align: justify;"> Percentual de alunos matriculados;</p>', unsafe_allow_html = True)

    st.markdown('<p style="text-align: justify;"> <strong> Quanto maior, maior o peso: </strong> </p>', unsafe_allow_html = True)
    st.markdown('- <p style="text-align: justify;"> Densidade demográfica - habitantes/km²;</p>', unsafe_allow_html = True)
    st.markdown('- <p style="text-align: justify;"> População no último censo; </p>', unsafe_allow_html = True)
    st.markdown('- <p style="text-align: justify;"> Percentual de crianças e jovens em idade elegível;</p>', unsafe_allow_html = True)


    st.subheader('Modelo matemático')
    st.markdown('##### Dataset')

    st.dataframe(dados_externos.head())



    st.subheader('Modelo K-means')

with aba2:
    st.title('Propostas para Expansão')

