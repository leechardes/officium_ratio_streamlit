import streamlit as st
from components.sidebar import create_sidebar
from views.overview import show_overview
from data.data_loader import load_data
from config.settings import set_page_config
from views.config import show_config
from utils.helpers import apply_filters

def create_version_page():
    st.title("Versão Atual")
    st.write("Número da versão: 1.0.0")
    st.write("Data de lançamento: 08/10/2024")
    st.write("Alterações:")
    st.write("* Correção de bugs")
    st.write("* Adição de recursos novos")

    # st.title("Histórico de Versões")
    # st.write("Versão 0.9.0: 08/10/2024")
    # st.write("* Correção de bugs")
    # st.write("* Melhoria de desempenho")

    st.title("Notas de Lançamento")
    st.write("Versão 1.0.0: 08/10/2024")
    st.write("* Adição de recursos novos")
    st.write("* Correção de bugs")

def main():
    set_page_config()
    df = load_data()
    
    page, trimestre_selecionado, mes_ano_selecionado, grupo_selecionado, subgrupo_selecionado, categoria_selecionada, exibe_grafico, exibe_por = create_sidebar(df)
    
    # Aplicar os filtros
    df_filtered = apply_filters(df, trimestre_selecionado, mes_ano_selecionado, grupo_selecionado, subgrupo_selecionado, categoria_selecionada)
    
    if page == "Visão Geral":
        show_overview(df_filtered, exibe_grafico, exibe_por)
    elif page == "Configuração":
        show_config()
    elif page == "Versão":
        create_version_page()
    else:
        st.write("Página em desenvolvimento")


if __name__ == "__main__":
    main()