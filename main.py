import streamlit as st
from components.sidebar import create_sidebar
from views.overview import show_overview
from views.config import show_config
from views.login import show_login
from views.version import show_version
from data.data_loader import load_data
from config.settings import set_page_config
from utils.helpers import apply_filters

def main():
    set_page_config()
    df = load_data()

    # Verifica se o login foi bem-sucedido antes de exibir o restante da aplicação
    if show_login():  # O login só retorna True quando o login for bem-sucedido
        page, trimestre_selecionado, mes_ano_selecionado, grupo_selecionado, subgrupo_selecionado, categoria_selecionada, exibe_grafico, exibe_por = create_sidebar(df)

        # Aplicar os filtros
        df_filtered = apply_filters(df, trimestre_selecionado, mes_ano_selecionado, grupo_selecionado, subgrupo_selecionado, categoria_selecionada)
        
        if page == "Visão Geral":
            show_overview(df_filtered, exibe_grafico, exibe_por)
        elif page == "Configuração":
            if st.session_state.user["grupo"] == "admin":
                show_config()
            else:
                st.write("Você não tem permissão para acessar essa página")
        elif page == "Versão":
            show_version()
        else:
            st.write("Página em desenvolvimento")

if __name__ == "__main__":
    main()
