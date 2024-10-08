import streamlit as st


def create_sidebar(df):
    st.sidebar.title("Menu")

    # Perguntas iniciais
    exibe_grafico = st.sidebar.selectbox("Exibe gráfico?", ["Sim", "Não"])
    exibe_por = st.sidebar.selectbox("Exibe por trimestre ou mês?", ["Trimestre", "Mês"])

    page = st.sidebar.selectbox("Escolha uma página", ["Visão Geral", "Configuração"])

    # Filtros
    trimestre = sorted(df['Trimestre'].unique())
    meses_anos = sorted(df['Mês/Ano'].unique())
    grupos = sorted(df['Descrição Grupo'].unique())
    subgrupos = sorted(df['Descrição SubGrupo'].unique())
    categorias = sorted(df['Descrição Categoria'].unique())

    trimestre_selecionado = st.sidebar.multiselect('Selecione o(s) Trimestre(es)', trimestre, default=trimestre)
    mes_ano_selecionado = st.sidebar.multiselect('Selecione o(s) Mês(es)/Ano(s)', meses_anos, default=meses_anos)
    grupo_selecionado = st.sidebar.multiselect('Selecione o(s) Grupo(s)', grupos, default=grupos)
    subgrupo_selecionado = st.sidebar.multiselect('Selecione o(s) Subgrupo(s)', subgrupos, default=subgrupos)
    categoria_selecionada = st.sidebar.multiselect('Selecione a(s) Categoria(s)', categorias, default=categorias)

    return page, trimestre_selecionado, mes_ano_selecionado, grupo_selecionado, subgrupo_selecionado, categoria_selecionada, exibe_grafico, exibe_por