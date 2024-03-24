
# Importação das bibliotecas
import streamlit as st

# def main():
cor_estilizada = 'color: #0145AC;'
fonte_negrito = 'font-weight: bold;'

st.markdown(f"<h2 style='{cor_estilizada}; text-align: center'><span style='{fonte_negrito}'>COMO DOAR?</span></h2>", unsafe_allow_html=True)

st.markdown(f"<h5 style='{cor_estilizada}; text-align: center'>Ajude a fazer a diferença! Sua doação é fundamental para o sucesso da nossa missão.</h5>", unsafe_allow_html=True)


# Valores de doação em botões e opção de inserir outros valores
st.header("Selecione ou insira o valor da sua doação:")
valores_doacao = [10, 20, 50, 100, 200, "Outro"]
valor_doacao = st.radio("Escolha o valor:", valores_doacao)
if valor_doacao == "Outro":
    valor_doacao = st.number_input("Digite o valor da doação:", step=10.0)

# Opção de recorrência de doação
recorrencia = st.radio("Deseja fazer uma doação única ou recorrente?", ["Única", "Recorrente"])

# Formas de pagamento
st.header("Selecione a forma de pagamento:")
forma_pagamento = st.selectbox("Forma de pagamento:", ["Cartão de crédito", "Boleto bancário", "PIX"])

# Formulário para preencher dados pessoais e de pagamento
st.header("Preencha seus dados:")
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

