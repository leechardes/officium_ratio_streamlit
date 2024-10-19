import streamlit as st

from data.data import DataManager
from data.companys import CompanyManager
from data.categories import CategoryManager

# Inicializa as classes
data = DataManager()
companies = CompanyManager()
categories = CategoryManager()

def create_sidebar():

    # Configurando as páginas disponíveis com `st.navigation`
    navigation_items = {
        "Home": [
            st.Page(overview_page, title="Visão Geral", icon=":material/home:"),
            st.Page(filters_page, title="Filtros", icon=":material/filter_list:"),
            ],
        "Configurações": [
            st.Page(user_page, title="Gerenciar Usuários", icon=":material/person:"),
            st.Page(categories_page, title="Gerenciar Categorias", icon=":material/category:"),
            st.Page(companies_page, title="Gerenciar Empresas", icon=":material/business:"),
            st.Page(import_page, title="Importar Arquivos CSV", icon=":material/file_upload:"),
            st.Page(version_page, title="Sobre", icon=":material/info:"),
        ]
    }

    # Seleção de outras configurações
    st.sidebar.selectbox("Exibe gráfico?", ["Sim", "Não"], key="exibe_grafico")
    st.sidebar.selectbox("Exibe por trimestre ou mês?", ["Trimestre", "Mês"], key="exibe_trimestre")
    st.sidebar.selectbox("Calcular percentual?", ["Sim", "Não"], key="calcula_percentual")

    # Seleção da empresa
    company_selected = st.session_state.company

    # Migração de categorias associadas à empresa
    categories.migrate_categories_from_file(company_selected)

    # Carregar o dataframe no session_state
    st.session_state.df = data.get_company_dataframe(company_selected)

    # Configuração da navegação com o componente padrão
    pg = st.navigation(navigation_items)

    pg.run()  # Executa a página selecionada no menu

# Definição das páginas de exemplo
def overview_page():
    st.session_state.page = "Visão Geral"

def config_page():
    st.session_state.page = "Configuração"

def version_page():
    st.session_state.page = "Versão"

def user_page():
    st.session_state.page = "Gerenciar Usuários"

def categories_page():        
    st.session_state.page = "Gerenciar Categorias"

def companies_page():
    st.session_state.page = "Gerenciar Empresas"

def import_page():        
    st.session_state.page = "Importar Arquivos CSV"

# Página de Filtros
def filters_page():
    st.title("Filtros")
    st.session_state.page = "Filtros"

    # Se o DataFrame não estiver vazio, exibir os filtros
    if not st.session_state.df.empty:
        # Filtros
        trimestre = sorted(st.session_state.df['Trimestre'].unique())
        meses_anos = sorted(st.session_state.df['Mês/Ano'].unique())
        grupos = sorted(st.session_state.df['Descrição Grupo'].unique())
        subgrupos = sorted(st.session_state.df['Descrição SubGrupo'].unique())
        categorias = sorted(st.session_state.df['Descrição Categoria'].unique())

        # Armazenando os filtros no session_state
        st.session_state['trimestre_selecionado'] = st.multiselect('Selecione o(s) Trimestre(s)', trimestre, default=trimestre)
        st.session_state['mes_ano_selecionado'] = st.multiselect('Selecione o(s) Mês(es)/Ano(s)', meses_anos, default=meses_anos)
        st.session_state['grupo_selecionado'] = st.multiselect('Selecione o(s) Grupo(s)', grupos, default=grupos)
        st.session_state['subgrupo_selecionado'] = st.multiselect('Selecione o(s) Subgrupo(s)', subgrupos, default=subgrupos)
        st.session_state['categoria_selecionada'] = st.multiselect('Selecione a(s) Categoria(s)', categorias, default=categorias)
    else:
        st.warning("O DataFrame está vazio. Verifique os dados carregados.")
