import streamlit as st

def show_version():
    st.title("Versão Atual")
    st.write("Número da versão: 1.0.3")
    st.write("Data de lançamento: 30/10/2024")
    st.write("Alterações:")
    st.write("* Correção de bugs")
    st.write("* Adição de recursos novos")

    st.title("Histórico de Versões")
    st.write("Versão 1.0.1: 08/10/2024")
    st.write("* Login de acesso")
    st.write("* Gerenciamento de usuário")

    st.title("Histórico de Versões")
    st.write("Versão 1.0.2: 08/10/2024")
    st.write("* Upload e processamento de arquivos CSV")

    st.title("Histórico de Versões")
    st.write("Versão 1.0.3: 30/10/2024")
    st.write("* Ajuste nos calculos e utilização do banco de dados mongodb")

    st.title("Notas de Lançamento")
    st.write("Versão 1.0.3: 08/10/2024")
    st.write("* Melhorias..")