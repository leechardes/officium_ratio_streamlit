import streamlit as st
from components.sidebar import create_sidebar
from views.overview import show_overview
from views.config import show_config
from views.login import show_login
from views.version import show_version

from utils.helpers import apply_filters
from config.settings import set_page_config

def main():
    
    if show_login():  # O login só retorna True quando o login for bem-sucedido
        create_sidebar()  # Cria a sidebar e armazena as seleções no session_state
        
        apply_filters()  # Aplica os filtros ao df no session_state
        
        if st.session_state.page == "Visão Geral":
            show_overview()
        elif st.session_state.page == "Configuração":
            show_config()
        elif st.session_state.page == "Versão":
            show_version()
        else:
            st.write("Página em desenvolvimento")
    else:
        st.write("Você precisa fazer login para acessar o sistema")

if __name__ == "__main__":
    
    set_page_config()
    main()
