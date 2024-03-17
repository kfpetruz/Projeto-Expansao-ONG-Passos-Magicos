# Importação das bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title= 'ONG Passos Mágicos', layout='wide', page_icon= '🤝')

# Título da página
st.title('Projeto ONG Passos Mágicos 🤝')

cor_estilizada = 'color: #0145AC;'
fonte_negrito = 'font-weight: bold;'

## VISUALIZAÇÃO NO STREAMLIT
aba1, aba2, aba3 = st.tabs(['Sobre a ONG', 'Fatores de sucesso', 'Impacto Social'])
with aba1:
    st.title('Sobre a ONG')
    st.markdown('<p style="text-align: justify;"> A Passos Mágicos é uma associação sem fins lucrativos de educação complementar,não formal e assistência social que possui o objetivo de transformar a vida de crianças e adolescentes em situação de vulnerabilidade social no município de Embu-Guaçu. A Associação teve início em 1992, auxiliando crianças em orfanato com origem da idealização de seus fundadores: Michelle Flues Ivanoff, Dimitri Ivanoff, Carol Ivanoff e Alexandre Ivanoff.</p>', unsafe_allow_html = True)
    
    st.subheader('O que fazemos?')
    st.markdown('<p style="text-align: justify;">A Associação Passos Mágicos atua dentro do Município de Embu-Guaçu, zona sul de São Paulo, com um programa educacional para crianças e jovens, oferecendo um processo que visa três pontos de impacto: oferecer uma educação de qualidade, suporte psicológico e ampliar a visão de mundo de cada aluno impactado.</p>', unsafe_allow_html = True)
    col1, col2, col3 = st.columns(3)
    with col1: #utilizando a cláusula with, mas poderíamos escrever apenas "col1." antes da métrica
        st.markdown(f"<h2 style='{cor_estilizada}'>3 a cada 20</h2> <span style='{fonte_negrito}'>pessoas de Embu-Guaçu são atendidas</span>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h2 style='{cor_estilizada}'>4 núcleos</h2> <span style='{fonte_negrito}'>distribuídos pelo município </span>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<h2 style='{cor_estilizada}'>Mais de 10.500</h2> <span style='{fonte_negrito}'>horas de aula no Programa de Aceleração do Conhecimento (PAC) </span>", unsafe_allow_html=True)

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
# 3ª aba - Desempenho dos alnos - Análise do Impacto Emocional e Social
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
        
    