import os
import shutil

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def create_file(path, content):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

def generate_project_structure():
    # Define the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Create directories
    directories = [
        'assets',
        'components',
        'config',
        'data',
        'utils',
        'views',
    ]
    for directory in directories:
        create_directory(os.path.join(project_root, directory))

    # Create files with content
    files_content = {
        'main.py': '''
import streamlit as st
from components.sidebar import create_sidebar
from views.overview import show_overview
from data.data_loader import load_data
from config.settings import set_page_config

def main():
    set_page_config()
    df = load_data()
    
    page = create_sidebar(df)
    
    if page == "Visão Geral":
        show_overview(df)
    else:
        st.write("Página em desenvolvimento")

if __name__ == "__main__":
    main()
''',
        'components/sidebar.py': '''
import streamlit as st

def create_sidebar(df):
    st.sidebar.title("Menu")
    page = st.sidebar.selectbox("Escolha uma página", ["Visão Geral"])

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

    return page, trimestre_selecionado, mes_ano_selecionado, grupo_selecionado, subgrupo_selecionado, categoria_selecionada
''',
        'data/data_loader.py': '''
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('/Users/leechardes/Python/dashboard/heraclito/dre_process.csv',
                         sep=';',
                         encoding='utf-8',
                         quotechar='"',
                         escapechar='\\',
                         on_bad_lines='warn')
        
        # Converter a coluna 'Valor' para numérico, tratando erros
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {str(e)}")
        return pd.DataFrame()
''',
        'config/settings.py': '''
import streamlit as st
import locale

def set_page_config():
    st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
    locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
''',
        'utils/helpers.py': '''
import locale

def format_real(value):
    return locale.currency(value, grouping=True, symbol=None)
''',
        'views/overview.py': '''
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import format_real

def show_overview(df):
    st.title("Dashboard Financeiro - Visão Geral")

    # Métricas principais
    col1, col2, col3 = st.columns(3)
    total_geral = df['Valor'].sum()
    total_receitas = df[df['Valor'] > 0]['Valor'].sum()
    total_despesas = df[df['Valor'] < 0]['Valor'].sum()

    col1.metric("Total Geral", format_real(total_geral))
    col2.metric("Total de Receitas", format_real(total_receitas))
    col3.metric("Total de Despesas", format_real(total_despesas))

    # Gráfico de barras por grupo
    fig_bar = px.bar(
        df.groupby('Descrição Grupo')['Valor'].sum().reset_index(),
        x='Descrição Grupo',
        y='Valor',
        title='Valores por Grupo',
        labels={'Valor': 'Valor Total', 'Descrição Grupo': 'Grupo'},
        color='Valor',
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Gráfico de linha temporal
    df_time = df.groupby(['Ano-Mês-Dia', 'Descrição Grupo'])['Valor'].sum().reset_index()
    fig_line = px.line(
        df_time,
        x='Ano-Mês-Dia',
        y='Valor',
        color='Descrição Grupo',
        title='Evolução Temporal por Grupo (Mês/Ano)',
        labels={'Valor': 'Valor Total', 'Ano-Mês-Dia': 'Período'}
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # ... (resto do código para a visão geral)
''',
        'assets/styles.css': '''
/* Adicione seus estilos personalizados aqui */
body {
    font-family: Arial, sans-serif;
}
''',
    }

    for file_path, content in files_content.items():
        create_file(os.path.join(project_root, file_path), content.strip())

    # Create an empty logo.png file
    open(os.path.join(project_root, 'assets', 'logo.png'), 'w').close()

    print("Estrutura do projeto gerada com sucesso!")

if __name__ == "__main__":
    generate_project_structure()