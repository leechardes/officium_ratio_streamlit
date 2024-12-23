from io import BytesIO
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import format_real
import uuid
from data.categories import CategoryManager

# Inicializa o CategoryManager
category_manager = CategoryManager()

# Função para carregar as categorias e categorias excluídas do MongoDB
def load_categories():
    categories = {
        "categories": category_manager.list_categories(st.session_state.company),
        "excluded_categories": category_manager.list_excluded_categories(st.session_state.company)
    }
    return categories

def show_overview():

    st.title("Dashboard Financeiro - Visão Geral")

    if st.session_state.df.empty:
        return

    # Carrega as categorias a partir do MongoDB
    categories = load_categories()

    # Aplicar o filtro para remover as categorias excluídas
    excluded_categories = categories["excluded_categories"]

    # Ordenar por ordem alfabetica as categorias
    included_categories = categories["categories"]

    ordered_categories = sorted(included_categories, key=lambda x: x["title"])

    # Remover as linhas que contenham as categorias excluídas
    df_filtered = st.session_state.df[~st.session_state.df['Descrição Categoria'].isin(excluded_categories)]
    df_excluded = st.session_state.df[st.session_state.df['Descrição Categoria'].isin(excluded_categories)]

    
    # st.write(st.session_state.df)
    # st.write(df_excluded)
    # st.write(df_filtered)
    # st.write("Categorias Excluídas:")

    # for category in excluded_categories:
    #     st.write(category)

    # st.write("Categorias Incluídas:")

    # for category in included_categories:
    #     st.write(category)

    # st.write(df_filtered)

    categorias_301 = [categoria for categoria in categories["categories"] if categoria["title"].startswith("3.01")]

    description_category = categorias_301[0]["description_category"]

    df_filtered_301 = df_filtered[df_filtered['Descrição Categoria'].isin(description_category)]

    total_receitas = df_filtered_301.sum()['Valor']

    st.session_state.total_301 = total_receitas 


    # st.write(categorias_301)
    # st.write(df_filtered_301)
    # st.write(total_receitas)

    # Agrupa por Ano-Mês-Dia e Trimestre
    st.session_state.total_grupo_1_ymd = df_filtered_301[df_filtered_301['Código Grupo'] == '1'].groupby('Mês/Ano')['Valor'].sum()
    st.session_state.total_grupo_1_trimestre = df_filtered_301[df_filtered_301['Código Grupo'] == '1'].groupby('Trimestre')['Valor'].sum()

    # st.write(st.session_state.total_grupo_1_ymd)
    # st.write(st.session_state.total_grupo_1_trimestre)


    # Filtros
    st.session_state.is_quarterly = st.session_state.exibe_trimestre == "Trimestre"
    st.session_state.is_percent = st.session_state.calcula_percentual == "Sim"
    st.session_state.is_graph = st.session_state.exibe_grafico == "Sim" and st.session_state.is_percent

    show_main_metrics(df_filtered)
    show_bar_chart(df_filtered, 'Descrição Grupo')

    # Chamada da função para exibir o resumo total
    show_total_summary(df_filtered, ordered_categories)

    # Chamada da função para exibir o resumo total
    show_total_summary(df_filtered, ordered_categories, is_quarterly = not st.session_state.is_quarterly)

    # Lista para armazenar todas as descrições de categoria do MongoDB
    all_defined_categories = []

    for category in ordered_categories:
        title = category['title']
        description_category = category['description_category']
        all_defined_categories.extend(description_category)

        # Filtra o DataFrame com base nas descrições de categoria
        df_filtered_category = df_filtered[df_filtered['Descrição Categoria'].isin(description_category)]
        show_summary(df_filtered_category, title=title, x_field='Descrição Categoria')

    # Gera o df_outros filtrando todas as categorias que não estão no MongoDB
    df_outros = df_filtered[~df_filtered['Descrição Categoria'].isin(all_defined_categories)]

    if not df_outros.empty:
        show_summary(df_outros, title='Outros', x_field='Descrição Categoria')

    show_summary(df_excluded, title='Repasses Laboratoriais', x_field='Descrição Categoria')


def show_dataframe(df):
    st.write(df)

def show_main_metrics(df):
    col1, col2, col3 = st.columns(3)
    total_geral = df['Valor'].sum()
    total_receitas = df[df['Valor'] > 0]['Valor'].sum()
    total_despesas = df[df['Valor'] < 0]['Valor'].sum()

    col1.metric("Total Geral", format_real(total_geral))
    col2.metric("Total de Receitas", format_real(total_receitas))
    col3.metric("Total de Despesas", format_real(total_despesas))

def show_bar_chart(df, x_field):
    fig_bar = px.bar(
        df.groupby(x_field)['Valor'].sum().reset_index(),
        x=x_field,
        y='Valor',
        title='Valores por ' + x_field.capitalize(),
        labels={'Valor': 'Valor Total', x_field: x_field.capitalize()},
        color='Valor',
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

def show_line_chart(df, x_field, group_field):
    df_time = df.groupby([x_field, group_field])['Valor'].sum().reset_index()
    fig_line = px.line(
        df_time,
        x=x_field,
        y='Valor',
        color=group_field,
        title='Evolução Temporal por ' + group_field.capitalize(),
        labels={'Valor': 'Valor Total', x_field: x_field.capitalize()}
    )
    st.plotly_chart(fig_line, use_container_width=True)

def show_summary(df, x_field, title, is_quarterly=None, group_1=None, group_2=None, description_1=None, description_2=None):
    
    if is_quarterly is None:
        is_quarterly = st.session_state.get('is_quarterly', False)

    if is_quarterly:
        df = df.groupby(['Trimestre', x_field])['Valor'].sum().reset_index()
    else:
        df = df.groupby(['Ano-Mês-Dia', x_field, 'Mês/Ano'])['Valor'].sum().reset_index()

    pivot = create_pivot_table(df, x_field, is_quarterly)
    pivot_combined = create_combined_pivot(pivot, is_quarterly, group_1, group_2, description_1, description_2)

    pivot_combined.index.name = title
    display_pivot_table(pivot_combined)

    if st.session_state.is_graph:
        display_percentage_chart(pivot_combined, is_quarterly)

    df_excel = pivot_combined.copy()

    unique_id = str(uuid.uuid4())
    st.download_button(
        label="Download em Excel",
        data=to_excel(df_excel),
        file_name="dados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"download_button_{unique_id}"
    )

def create_pivot_table(df, x_field, is_quarterly):
    if is_quarterly:
        x_field_pivot = 'Trimestre'
    else:
        x_field_pivot = 'Ano-Mês-Dia'

    pivot = pd.pivot_table(
        df,
        values='Valor',
        index=[x_field],
        columns=[x_field_pivot],
        aggfunc='sum',
        fill_value=0
    )
    if not is_quarterly:
        ordered_columns = sorted(df['Ano-Mês-Dia'].unique())
        pivot = pivot[ordered_columns]
        pivot.columns = df['Mês/Ano'].unique()
    return pivot

def create_combined_pivot(pivot, is_quarterly, group_1, group_2, description_1, description_2):
    if st.session_state.is_percent:
        pivot_percent = calculate_percentages(pivot, is_quarterly)
        pivot_combined = combine_pivot_and_percent(pivot, pivot_percent)
    else:
        pivot_combined = pivot.copy()

    pivot_combined = add_totals(pivot_combined, group_1, group_2, description_1, description_2)
    return pivot_combined

def calculate_percentages(pivot, is_quarterly):
    pivot_percent = pivot.copy()
    for col in pivot.columns:
        if is_quarterly:
            first_row_value = st.session_state.total_grupo_1_trimestre[col]
        else:
            first_row_value = st.session_state.total_grupo_1_ymd[col]
        pivot_percent[col] = pivot[col] / first_row_value * 100 if first_row_value != 0 else 0
    return pivot_percent

def combine_pivot_and_percent(pivot, pivot_percent):
    pivot_combined = pd.DataFrame()
    for col in pivot.columns:
        pivot_combined[f'{col}'] = pivot[col]
        pivot_combined[f'{col} %'] = pivot_percent[col]
    new_order = [item for pair in zip(pivot.columns, [f'{col} %' for col in pivot.columns]) for item in pair]
    return pivot_combined[new_order]

def add_totals(pivot_combined, group_1=None, group_2=None, description_1=None, description_2=None):
    if group_1 is not None and description_1 is not None:
        grupo_1_total = pivot_combined.loc[group_1].sum()
        grupo_1_total.name = description_1

    if group_2 is not None and description_2 is not None:
        grupo_2_total = pivot_combined.loc[group_2].sum()
        grupo_2_total.name = description_2

    if group_1 is not None and group_2 is not None:
        pivot_combined = pd.concat([
            pivot_combined.loc[group_1],
            pd.DataFrame([grupo_1_total]),
            pivot_combined.loc[group_2],
            pd.DataFrame([grupo_2_total]),
            pivot_combined.drop(group_1 + group_2)
        ])
    elif group_1 is not None:
        pivot_combined = pd.concat([
            pivot_combined.loc[group_1],
            pd.DataFrame([grupo_1_total]),
            pivot_combined.drop(group_1)
        ])
    elif group_2 is not None:
        pivot_combined = pd.concat([
            pivot_combined.loc[group_2],
            pd.DataFrame([grupo_2_total]),
            pivot_combined.drop(group_2)
        ])

    total_receitas = st.session_state.total_301

    total_geral = pivot_combined.sum()
    total_geral.name = 'Total Geral'
    pivot_combined = pd.concat([pivot_combined, pd.DataFrame([total_geral])])
    
    pivot_combined['Total por Linha'] = pivot_combined[[col for col in pivot_combined.columns if "%" not in col]].sum(axis=1)

    # Adiciona a coluna de Percentual
    pivot_combined['Total por Linha %'] = (pivot_combined['Total por Linha'] / total_receitas) * 100
    
    return pivot_combined

def display_pivot_table(pivot_combined):
    column_configs = {
        col: st.column_config.NumberColumn(
            label=col,
            format="%.2f%%"
        )
        for col in pivot_combined.columns if "%" in col
    }
    st.dataframe(
        pivot_combined,
        column_config=column_configs,
        use_container_width=True
    )

def display_percentage_chart(pivot_combined, is_quarterly):
    percent_columns = [col for col in pivot_combined.columns if '%' in col]
    df_percentual = pivot_combined[percent_columns].transpose()

    title = 'Evolução Percentual / ' + ('Trimestre' if is_quarterly else 'Mês')
    labels = {'value': 'Percentual (%)', 'index': 'Trimestres' if is_quarterly else 'Meses'}

    fig = px.line(
        df_percentual,
        title=title,
        labels=labels
    )
    st.plotly_chart(fig, use_container_width=True)

def show_total_summary(df, categories, is_quarterly=None):
    if is_quarterly is None:
        is_quarterly = st.session_state.get('is_quarterly', False)

    # DataFrame temporário para armazenar totais de cada categoria
    df_totals = pd.DataFrame(columns=['Descrição Categoria', 'Valor', 'Trimestre', 'Ano-Mês-Dia', 'Mês/Ano'])

    df = st.session_state.df
    # Itera sobre as categorias para calcular o total de cada uma, agrupado por tempo
    for category in categories:
        title = category['title']
        description_category = category['description_category']
        
        # Filtra o DataFrame para apenas as linhas que correspondem à categoria atual
        df_filtered_category = df[df['Descrição Categoria'].isin(description_category)]
        
        # Aplica o agrupamento de tempo baseado em `is_quarterly` e nas colunas disponíveis
        if is_quarterly and 'Trimestre' in df_filtered_category.columns:
            df_category_grouped = df_filtered_category.groupby(['Trimestre'])['Valor'].sum().reset_index()
            df_category_grouped['Descrição Categoria'] = title
            df_category_grouped['Ano-Mês-Dia'] = None
            df_category_grouped['Mês/Ano'] = None
        else:
            # Agrupamento sem considerar o tempo se as colunas esperadas não estão disponíveis
            df_category_grouped = df_filtered_category.groupby(['Ano-Mês-Dia', 'Mês/Ano'])['Valor'].sum().reset_index()
            df_category_grouped['Descrição Categoria'] = title
            df_category_grouped['Trimestre'] = None

        # Concatena o total da categoria no DataFrame de totais
        df_totals = pd.concat([df_totals, df_category_grouped], ignore_index=True)

    # Total geral para todas as categorias
    total_geral = df_totals['Valor'].sum()
    df_totals = pd.concat(
        [df_totals, pd.DataFrame({
            'Descrição Categoria': ['Total Geral'],
            'Valor': [total_geral],
            'Trimestre': [None],
            'Ano-Mês-Dia': [None],
            'Mês/Ano': [None]
        })],
        ignore_index=True
    )

    # Exibe o resumo com os totais adaptado ao tempo
    show_summary(df_totals, title='Resumo Total por Categoria', x_field='Descrição Categoria',is_quarterly=is_quarterly)

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    df = df.reset_index()
    
    # Escreve o DataFrame no Excel
    df.to_excel(writer, sheet_name='Dados', index=False)
    
    # Obtém o workbook e worksheet do XlsxWriter para formatação
    workbook = writer.book
    worksheet = writer.sheets['Dados']

    # Formatação das células (opcional, mas recomendada para visualização)
    format1 = workbook.add_format({'bg_color': '#CCCCCC'})
    format2 = workbook.add_format({'bg_color': '#FFFFFF'})

    # Alterna as cores das linhas (se necessário)
    for i, row in enumerate(df.index):
        if i % 2 == 0:
            worksheet.set_row(i + 1, None, format1)
        else:
            worksheet.set_row(i + 1, None, format2)

    # Formata a primeira linha como negrito
    worksheet.set_row(0, None, workbook.add_format({'bold': True}))
 
    writer.close()
    processed_data = output.getvalue()
    return processed_data
