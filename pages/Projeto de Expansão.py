# Importação das bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from sklearn.preprocessing import StandardScaler, MinMaxScaler #Feature Engineer
from sklearn.cluster import KMeans # Algoritmo de Agrupamento
from sklearn.metrics import adjusted_rand_score, silhouette_score

# Configuração da página
st.set_page_config(page_title= 'ONG Passos Mágicos', layout='wide', page_icon= '🤝')
cor_estilizada = 'color: #1A4A6A;'
fonte_negrito = 'font-weight: bold;'
fonte_escura = 'color: #292F39;'

# Título da página
st.markdown(f"<h1 style='{fonte_escura} {fonte_negrito}'> Projeto de expansão 🤝 </h1>", unsafe_allow_html=True)


#PREPARAÇÃO DOS DADOS
dados_externos = pd.read_excel('tb_populacao_economia_idade_distancia.xlsx')

dados_externos['percent_elegiveis_6a19a'] = dados_externos['Pessoas de 6 a 19 anos'] / dados_externos['População no último censo'] * 100
dados_externos['Matriculados/População 6 a 19'] = dados_externos['Matriculados/População 6 a 19'] * 100

dados_externos = dados_externos[['Município', 'Salário médio mensal dos trabalhadores formais', 'PIB per capita', 'População no último censo', 'Densidade demográfica habitante/km²', 'Distância', 'Matriculados/População 6 a 19', 'percent_elegiveis_6a19a']]
dados_externos = dados_externos.rename(columns= {'Município': 'municipio', 'Salário médio mensal dos trabalhadores formais': 'salario_medio_trabalhadores', 'PIB per capita': 'pib_per_capita', 'Área da unidade territorial': 'area_territorial', 'População no último censo': 'populacao', 'Densidade demográfica habitante/km²': 'densidade_demografica_km2', 'Distância': 'distancia_de_embu_guacu', 'Matriculados/População 6 a 19': 'percent_matriculados_6a19a'})

# Modelo matemático
dados_model_math = dados_externos[['municipio', 'salario_medio_trabalhadores', 'pib_per_capita', 'densidade_demografica_km2', 'distancia_de_embu_guacu', 'percent_matriculados_6a19a', 'percent_elegiveis_6a19a']]

# Normalizandos os dados
variaveis_normalizar = ['densidade_demografica_km2', 'percent_elegiveis_6a19a']
variaveis_normalizar_inversamente = ['salario_medio_trabalhadores','pib_per_capita', 'distancia_de_embu_guacu', 'percent_matriculados_6a19a']

scaler = MinMaxScaler()
dados_model_math[variaveis_normalizar] = scaler.fit_transform(dados_model_math[variaveis_normalizar])

    # Normalização inversa
scaler = MinMaxScaler()
dados_model_math[variaveis_normalizar_inversamente] = 1 - scaler.fit_transform(dados_model_math[variaveis_normalizar_inversamente])


## VISUALIZAÇÃO NO STREAMLIT
aba1, aba2= st.tabs(['Modelo', 'Propostas'])
with aba1:
    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> Para auxiliar a ONG em seu desejo de expandir as atividades, ampliando a capacidade, para que ela possa atender e mudar a vida de centenas de crianças e adolescentes como vem fazendo há anos na cidade de Embu-Guaçu, foram criados dois modelos, levando em consideração dados <strong> econômicos </strong>, de <strong> população </strong>, <strong> educacionais </strong>, com base no último censo, e de <strong> distância da cidade sede</strong>  com base numa biblioteca geográfica do Python.</p>', unsafe_allow_html = True)

    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> Em ambos os modelos foram consideradas as 645 cidades do estado de São Paulo, a fim de propôr as <strong> potenciais cidades </strong> onde a ONG poderá investir seus esforços.</p>', unsafe_allow_html = True)

    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> Nesta análise, certos campos, como salário, têm um impacto maior no algoritmo quando são menores. Em termos de peso, isso significa que, quanto menor o salário, mais significativo é o efeito dele na análise.</p>', unsafe_allow_html = True)
    
    st.markdown(f"<h3 style='{cor_estilizada}'> Variáveis analisadas separadas por efeito </h3>", unsafe_allow_html=True)
    pesos = {
    'Quanto menor, maior o peso': ['Salário médio dos trabalhadores formais; Índice de desenvolvimento humano municipal (IDHM); PIB per capita; Percentual de alunos matriculados;'],
    'Quanto maior, maior o peso': ['Densidade demográfica - habitantes/km²; Percentual de crianças e jovens em idade elegível;']}
    
    df_pesos = pd.DataFrame(pesos)
    html = df_pesos.to_html(index=False)

    # Adicionando estilos CSS para a cor da borda de todas as células
    html_estilizado = html.replace('<th>', '<th style=\'border: 2px solid #0145AC; text-align: center; color: #292F39;\'>').replace('<td>', '<td style=\'border: 2px solid #0145AC; text-align: center; color: #292F39;\'>')

    # Exibir a tabela estilizada no Streamlit
    st.write("<style>table {{ width: 100%; border-collapse: collapse; }} th, td {{ padding: 10px; }}</style>{}".format(html_estilizado), unsafe_allow_html=True)
    st.markdown('<p style="text-align: justify; padding: 10px;"></p>', unsafe_allow_html = True) #linha para aumentar o espaço

    #ESCOLHA DAS PRIORIDADES
    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> Abaixo, os administradores da ONG têm a opção de selecionar a relevância atribuída a cada uma das variáveis nas análises. Podem testar diferentes graus de importância e realizar uma variedade de testes conforme desejarem.</p>', unsafe_allow_html = True) 
    
    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> Escolha a <strong> relevância das variáveis, de 1 a 6 </strong>. Quanto maior o número, maior o peso. Os pesos escolhidos nesta seção se aplicam tanto ao <strong> Modelo Matemático </strong> quanto ao <strong> Modelo K-means </strong></p>', unsafe_allow_html = True)
    col1, col2 = st.columns(2)
    with col1:
        # Pesos
        #st.markdown('<p>Escolha o peso que a <strong> distância </strong> que a cidade tem de Embu-Guaçu terá (de 1 a 6):</p>', unsafe_allow_html = True)
        prioridade_distancia_embu = st.number_input("Distância que a cidade tem de Embu-Guaçu:", min_value=1, value=6, max_value=6)
        prioridade_salario_medio = st.number_input("Salário médio mensal dos trabalhadores:", min_value=1, value=5, max_value=6)
        prioridade_pib_per_capita = st.number_input("PIB per capita:", min_value=1, value=4, max_value=6)
    with col2:
        prioridade_percent_idade_elegivel = st.number_input("Percentual de crianças e jovens em idade elegível :", min_value=1, value=3, max_value=6)
        prioridade_percent_matriculados = st.number_input("Percentual de matriculados em idade elegível:", min_value=1, value=2, max_value=6)
        prioridade_densidade_demografica = st.number_input("Densidade demográfica:", min_value=1, value=1, max_value=6)

        # Atribuição de pesos
    dados_model_math['distancia_de_embu_guacu'] = prioridade_distancia_embu * dados_model_math['distancia_de_embu_guacu']
    dados_model_math['salario_medio_trabalhadores'] = prioridade_salario_medio * dados_model_math['salario_medio_trabalhadores']
    dados_model_math['pib_per_capita'] = prioridade_pib_per_capita * dados_model_math['pib_per_capita']
    dados_model_math['percent_elegiveis_6a19a'] = prioridade_percent_idade_elegivel * dados_model_math['percent_elegiveis_6a19a']
    dados_model_math['percent_matriculados_6a19a'] = prioridade_percent_matriculados * dados_model_math['percent_matriculados_6a19a']
    dados_model_math['densidade_demografica_km2'] = prioridade_densidade_demografica * dados_model_math['densidade_demografica_km2']
    
    st.markdown('<p style="text-align: justify; padding: 10px;"></p>', unsafe_allow_html = True) #linha para aumentar o espaço

    #MODELO MATEMÁTICO
    st.markdown(f"<h3 style='{cor_estilizada}'> Modelo Matemático </h3>", unsafe_allow_html=True)
    st.markdown('<p style="text-align: justify;"> O modelo matemático calcula o valor das variáveis de acordo com os pesos escolhidos acima e dele extraímos o coeficiente chamado "resultado_modelo_expansao", que pode ser visto ao final da tabela. Quanto maior o resultado, maior o indicador de que a ONG deve expandir suas atividades para a respectiva cidade. </p>', unsafe_allow_html = True) 

        # Soma ponderada
    dados_model_math['resultado_modelo_expansao'] = dados_model_math[['distancia_de_embu_guacu', 'salario_medio_trabalhadores', 'pib_per_capita', 'percent_elegiveis_6a19a', 'percent_matriculados_6a19a', 'densidade_demografica_km2']].sum(axis=1)

        # Classificar o DataFrame com base na soma ponderada
    dados_externos_model_math = pd.merge(dados_externos, dados_model_math[['municipio', 'resultado_modelo_expansao']], on='municipio', how='left') #Merge dos dados originais, sem normalização, com o resultado do modelo matemático
    dados_externos_model_math = dados_externos_model_math.sort_values('resultado_modelo_expansao', ascending = False)

        #Mostra o dataframe gerado pelo modelo
    quantidade_cidades = st.number_input("Escolha a quantidade de cidades que deseja visualizar, entre as melhores classificadas, para potencial expansão das atividades da ONG:", min_value=1, value=15, max_value=645)
    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> De acordo com os pesos escolhidos acima, as <strong> cidades mais indicadas </strong> são:</p>', unsafe_allow_html = True) 
    st.dataframe(dados_externos_model_math.reset_index(drop=True).head(quantidade_cidades))

    st.markdown('<p style="text-align: justify; padding: 10px;"></p>', unsafe_allow_html = True) #linha para aumentar o espaço

    #MODELO UTILIZANDO ALGORITMO K-MEANS
    st.markdown(f"<h3 style='{cor_estilizada}'> Modelo K-means </h3>", unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> O modelo K-means também usa os pesos definidos acima pelos administradores da ONG, porém, neste modelo, é feito um cálculo de aproximação dos indicadores das cidades do estado de São Paulo com os indicadores da cidade de Embu-Guaçu. Assim, as cidades mais semelhantes (de acordo com os indicadores) ficarão no mesmo grupo que a cidade de Embu-Guaçu, e, portanto, recomenda-se a expansão a partir dessas cidades.</p>', unsafe_allow_html = True) 

    dados_model_kmeans = dados_model_math.drop('resultado_modelo_expansao', axis = 1)
    kmeans = KMeans(n_clusters=6,random_state=0) #definindo os hiperparametros do algoritmo (definir o número de grupo = cluster)

    #Implementando o K-Means nos dados:
    kmeans.fit(dados_model_kmeans[['distancia_de_embu_guacu', 'salario_medio_trabalhadores', 'pib_per_capita', 'percent_elegiveis_6a19a', 'percent_matriculados_6a19a', 'densidade_demografica_km2']])

    #Salvando os centroides de cada cluster
    centroides = kmeans.cluster_centers_

    #Salvando os labels dos clusters para cada exemplo
    kmeans_labels = kmeans.predict(dados_model_kmeans[['distancia_de_embu_guacu', 'salario_medio_trabalhadores', 'pib_per_capita', 'percent_elegiveis_6a19a', 'percent_matriculados_6a19a', 'densidade_demografica_km2']])

    dados_model_kmeans['grupos'] = kmeans_labels

    #pd.Series(kmeans_labels).value_counts() #Contagem de quantas cidades ficaram em cada grupo

    dados_externos_order_math = dados_externos_model_math.drop('resultado_modelo_expansao', axis = 1)
    dados_externos_model_kmeans = pd.merge(dados_externos_order_math, dados_model_kmeans[['municipio', 'grupos']], on='municipio', how='left')
    grupo_embu = dados_externos_model_kmeans[dados_externos_model_kmeans['municipio'] == 'Embu-Guaçu']['grupos'].values
    qtd_cidades_grupo_embu = dados_externos_model_kmeans[dados_externos_model_kmeans['grupos'] == grupo_embu[0]].shape[0]

    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> De acordo com os pesos escolhidos acima, as <strong> cidades mais indicadas </strong> são as <strong> {qtd_cidades_grupo_embu} </strong> listadas abaixo:</p>', unsafe_allow_html = True) 

    st.dataframe(dados_externos_model_kmeans[dados_externos_model_kmeans['grupos'] == grupo_embu[0]].reset_index(drop=True))


with aba2:
    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> Após analisar os dados históricos da ONG, dados da PEDE (Pesquisa de Desenvolvimento Educacional), os recursos digitais utilizados atualmente pela ONG, dados da economia, população e educacionais de Embu-Guaçu e demais cidades do estado de São Paulo, listamos as melhores propostas escolhidas para a ONG concretizar seu plano de expansão.</p>', unsafe_allow_html = True)

    st.markdown('<p style="text-align: justify; padding: 2px;"></p>', unsafe_allow_html = True) #linha para aumentar o espaço
    st.markdown(f'<h5 style="{cor_estilizada}"> Expandir a partir das cidades selecionadas no Modelo Matemático ou Modelo K-means </h5>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> Acreditamos que, num plano de expansão de suas atividades, a ONG terá maior impacto social e chance de sucesso ao escolher iniciar pelas cidades selecionadas nos modelos Matemático ou K-means, pois as cidades ali selecionadas, além de serem mais carentes de ações como as da ONG, têm um perfil semelhante ao que ela está habituada a atender.</p>', unsafe_allow_html = True)

    st.markdown('<p style="text-align: justify; padding: 2px;"></p>', unsafe_allow_html = True) #linha para aumentar o espaço
    st.markdown(f'<h5 style="{cor_estilizada}"> Disponibilizar meios de doação por boleto, cartão de crédito, pix, entre outros, diretamente pelo site </h5>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> Na era em que tudo é feito às pressas, acreditamos que haveria um ganho ao incluir a possibilidade de doação direto no site, através de meios de doação de autoatendimento, tirando a necessidade de a pessoa doadora ter que entrar em contato com a ONG, aguardar atendimento, tendo assim até mesmo a possibilidade de a pessoa desistir da doação nesse meio tempo. </p>', unsafe_allow_html = True)
    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> É sabido que é necessário contrato com adquirentes de cartão de crédito, bancos, entre outros intermediadores, para viabilizar algo do tipo, porém, vemos uma possibilidade de ganho nessa frente, especialmente quando se fala de pequenos doadores. </p>', unsafe_allow_html = True)

    
    st.markdown('<p style="text-align: justify; padding: 2px;"></p>', unsafe_allow_html = True) #linha para aumentar o espaço
    st.markdown(f'<h5 style="{cor_estilizada}"> Inclusão de opção de valores pré-cadastrados</h5>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> Inclusão de opção de valores pré-cadastrados, deixando a opção "outros" habilitada também para caso a pessoa doadora queira doar um valor diferente e até pessoas que queiram doar de forma recorrente.</p>', unsafe_allow_html = True)

    st.markdown(f'<p style="text-align: justify; {fonte_escura}"> Abaixo um exemplo gráfico de como poderia ser a página de doações no site da ONG.</p>', unsafe_allow_html = True)
    st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True) #Linha cinza sólida

    #FORMULÁRIO DE DOAÇÃO
    st.markdown(f"<h2 style='{cor_estilizada}; text-align: center'><span style='{fonte_negrito}'>COMO DOAR?</span></h2>", unsafe_allow_html=True)

    st.markdown(f"<h5 style='{cor_estilizada}; text-align: center'>Ajude a fazer a diferença! Sua doação é fundamental para o sucesso da nossa missão.</h5>", unsafe_allow_html=True)


    # Valores de doação em botões e opção de inserir outros valores
    st.markdown(f"<h4 style='{fonte_negrito} {fonte_escura}'> Selecione ou insira o valor da sua doação: </h4>", unsafe_allow_html=True)
    valores_doacao = [10, 20, 50, 100, 200, "Outro"]
    valor_doacao = st.radio("Escolha o valor:", valores_doacao)
    if valor_doacao == "Outro":
        valor_doacao = st.number_input("Digite o valor da doação:", step=10.0)

    # Opção de recorrência de doação
    recorrencia = st.radio("Deseja fazer uma doação única ou recorrente?", ["Única", "Recorrente"])

    # Formas de pagamento
    st.markdown(f"<h4 style='{fonte_negrito} {fonte_escura}'> Selecione a forma de pagamento: </h4>", unsafe_allow_html=True)
    forma_pagamento = st.selectbox("Forma de pagamento:", ["Cartão de crédito", "Boleto bancário", "PIX"])

    # Formulário para preencher dados pessoais e de pagamento
    st.markdown(f"<h4 style='{fonte_negrito} {fonte_escura}'> Preencha seus dados: </h4>", unsafe_allow_html=True)
    nome = st.text_input("Nome completo:")
    email = st.text_input("Email:")
    endereco = st.text_input("Endereço:")
    cidade = st.text_input("Cidade:")
    estado = st.text_input("Estado:")
    cep = st.text_input("CEP:")

    if forma_pagamento == "Cartão de crédito":
        numero_cartao = st.text_input("Número do cartão:")
        data_validade = st.text_input("Data de validade (MM/AAAA):")
        cvv = st.text_input("CVV:")

    # Botão para confirmar doação
    if st.button("Confirmar Doação"):
        if forma_pagamento == "Cartão de crédito":
            # Aqui você pode adicionar a lógica para processar o pagamento com cartão de crédito
            if recorrencia == "Única":
                st.success(f"Obrigado por sua doação única de R${valor_doacao}!")
            else:
                st.success(f"Obrigado por sua doação recorrente de R${valor_doacao}!")
        else:
            # Aqui você pode adicionar a lógica para gerar o boleto bancário
            if recorrencia == "Única":
                st.success(f"Obrigado por sua doação única de R${valor_doacao}! Seu boleto será enviado para o email {email}.")
            else:
                st.success(f"Obrigado por sua doação recorrente de R${valor_doacao}! Seu boleto será enviado para o email {email}.")
    st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True) #Linha cinza sólida

