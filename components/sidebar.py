import streamlit as st
from data.data_loader import load_data

def create_sidebar():
    st.sidebar.title("Menu")
    st.session_state.df = load_data()  # Carrega o dataframe no session_state
    
    # Pergunta sobre exibição de gráfico e cálculo de percentual
    st.sidebar.selectbox("Exibe gráfico?", ["Sim", "Não"], key="exibe_grafico")
    st.sidebar.selectbox("Exibe por trimestre ou mês?", ["Trimestre", "Mês"], key="exibe_trimestre")
    st.sidebar.selectbox("Calcular percentual?", ["Sim", "Não"], key="calcula_percentual")
    st.sidebar.selectbox("Escolha uma página", ["Visão Geral", "Configuração", "Versão"], key="page")

    # Filtros
    trimestre = sorted(st.session_state.df['Trimestre'].unique())
    meses_anos = sorted(st.session_state.df['Mês/Ano'].unique())
    grupos = sorted(st.session_state.df['Descrição Grupo'].unique())
    subgrupos = sorted(st.session_state.df['Descrição SubGrupo'].unique())
    categorias = sorted(st.session_state.df['Descrição Categoria'].unique())

    # Armazenando os filtros no session_state
    st.sidebar.multiselect('Selecione o(s) Trimestre(es)', trimestre, default=trimestre, key="trimestre_selecionado")
    st.sidebar.multiselect('Selecione o(s) Mês(es)/Ano(s)', meses_anos, default=meses_anos, key="mes_ano_selecionado")
    st.sidebar.multiselect('Selecione o(s) Grupo(s)', grupos, default=grupos, key="grupo_selecionado")
    st.sidebar.multiselect('Selecione o(s) Subgrupo(s)', subgrupos, default=subgrupos, key="subgrupo_selecionado")
    st.sidebar.multiselect('Selecione a(s) Categoria(s)', categorias, default=categorias, key="categoria_selecionada")
