import streamlit as st
from components.sidebar import create_sidebar
from views.overview import show_overview
from views.config import show_config
from views.login import show_login
from views.version import show_version
from views.users import show_user_management
from views.categories import show_category_management
from views.companies import show_company_management
from views.import_data import show_import_data
from data.companys import CompanyManager
from utils.helpers import apply_filters
from config.settings import set_page_config
import pandas as pd

companies = CompanyManager()

# Função para inicializar as variáveis de sessão
def initialize_session():

    companies_list = companies.list_companies()

    # Verifica se a variável 'company' já está na sessão, caso contrário, inicializa
    if 'company' not in st.session_state:
        st.session_state.company = list(map(lambda x: x['company'], companies_list))[0]

    # Inicializa a lista de empresas se ainda não existir
    if 'companies' not in st.session_state:
        st.session_state.companies = companies_list
    
    # Inicializa outros valores necessários, por exemplo:
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()  # Inicializa com um DataFrame vazio

    # Inicializa as seleções de filtros
    if 'page' not in st.session_state:
        st.session_state.page = "Visão Geral"

def main():

    # Inicializar todas as variáveis de sessão
    initialize_session()
    
    if show_login():  # O login só retorna True quando o login for bem-sucedido
       
        create_sidebar()  # Cria a sidebar e armazena as seleções no session_state
        
        if not st.session_state.df.empty:
            # Aplica os filtros
            apply_filters()  # Aplica os filtros ao df no session_state
        
        if st.session_state.page == "Visão Geral":
            show_overview()
        elif st.session_state.page == "Configuração":
            show_config()
        elif st.session_state.page == "Versão":
            show_version()
        elif st.session_state.page == "Gerenciar Usuários":
            show_user_management()
        elif st.session_state.page == "Gerenciar Categorias":
            show_category_management()
        elif st.session_state.page == "Gerenciar Empresas":
            show_company_management()
        elif st.session_state.page == "Importar Arquivos CSV":
            show_import_data()

if __name__ == "__main__":
    
    set_page_config()
    main()
