# Importação da biblioteca streamlit
import streamlit as st

# Configuração da página
st.set_page_config(page_title= 'Sobre o Projeto', layout='wide', page_icon= '🤝')

# Título da página
st.title('Desenvolvimento do Projeto 🤝')

# Descrição do projeto
st.markdown('<p style="text-align: justify;">Para além de um Tech Challenge, este projeto foi uma nobre proposta como trabalho de conclusão de Pós-graduação em Data Analytics da faculdade Fiap - Datathon. Nós alunos fomos instigados a analisar dados da ONG Passos Mágicos, uma ONG que tem mudado vidas de centenas de crianças e adolescentes na cidade de Embu-Guaçu.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;">Durante aproximadamente um mês nos debruçamos sobre os dados da ONG a fim de:</p>', unsafe_allow_html = True)
st.markdown('- Extrair insights dos dados históricos de alunos;')
st.markdown('- Apresentar fatores de sucesso;')
st.markdown('- Apresentar o impacto social da ONG na cidade onde atua;')
st.markdown('- Criar visualizações impactantes para os dados;')
st.markdown('- Promover transparência e conscientização;')
st.markdown('- Propôr plano de ampliação da atuação da ONG;')

# Visualização da fluxo de trabalho do projeto
st.markdown('## Fluxo de Trabalho')
miro_url = 'https://miro.com/app/live-embed/uXjVKdWsCz4=/?moveToViewport=-1438,-982,3725,1759&embedId=826178763300'
st.markdown(f'<iframe width="80%" height="600" src="{miro_url}" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>', unsafe_allow_html=True)

# Links
st.markdown('## Links Úteis')
st.markdown('##### Repositório do projeto')
st.markdown('[Repositório do projeto no Github](https://github.com/kfpetruz/Projeto-Expansao-ONG-Passos-Magicos)')
st.markdown('##### Fontes de dados')
st.markdown('[Idade da população](https://sidra.ibge.gov.br/tabela/9514)')
st.markdown('[Dados econômicos e populacionais](https://cidades.ibge.gov.br/brasil/sintese/sp?indicadores=47001,97907,97911,29167,29765,30255)')
st.markdown('[População estimada nos anos que não tem Censo](https://sidra.ibge.gov.br/tabela/6579)') 
st.markdown('[Coordenadas geográficas - cidades de São Paulo](https://github.com/alanwillms/geoinfo/blob/master/latitude-longitude-cidades.csv)')
st.markdown('[Dados da educação básica](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/sinopses-estatisticas/educacao-basica)')


# Equipe do projeto
st.markdown('## Equipe')
st.markdown('#####  Keila Ferreira Petruz - Analista de BI <a href="https://www.linkedin.com/in/keila-ferreira-petruz/" target="_blank"  style="margin: 0px 5px 0px 10px;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="30" height="30"></a> <a href="https://github.com/kfpetruz" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub" width="30" height="30"></a>', unsafe_allow_html = True)
st.markdown('##### Tainá Maria Dias de Paula - Analista de BI <a href="https://www.linkedin.com/in/tainamdpaula/" target="_blank"  style="margin: 0px 5px 0px 10px;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="30" height="30"></a> <a href="https://github.com/tainamaria" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub" width="30" height="30"></a>', unsafe_allow_html = True)

#BACKUP DO TEMA
# [theme]
# base="light"
# primaryColor="#0145AC"
# backgroundColor="#F2F2F2"
# secondaryBackgroundColor="#e2e4e9"
# textColor="#292F39"
# font="sans serif"