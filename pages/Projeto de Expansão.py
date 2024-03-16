# Importação das bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title= 'ONG Passos Mágicos', layout='wide', page_icon= '🤝')

# Título da página
st.title('Projeto de expansão 🤝')

## VISUALIZAÇÃO NO STREAMLIT
aba1, aba2= st.tabs(['Modelo', 'Propostas'])
with aba1:
    st.title('Modelo matemático')

    st.title('Modelo K-means')

with aba2:
    st.title('Propostas para Expansão')

