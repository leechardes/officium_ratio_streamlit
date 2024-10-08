from io import BytesIO
import json
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import format_real
import uuid 
import xlsxwriter

# Função para carregar o arquivo JSON
def load_categories():
    with open('config/categories.json', 'r') as f:
        return json.load(f)
    
def show_overview(df,exibe_grafico, exibe_por):
    st.title("Dashboard Financeiro - Visão Geral")

    # # Primeiro, crie a condição corretamente
    # condition_repasse = (df['Código Grupo'].isin([6])) & \
    #                     (df['Código SubGrupo'].isin([1,2])) & \
    #                     (df['Descrição Categoria'].isin(['Repasse laboratório Dore','Distrib. Lucro Laboratório']))
    
    # df_semrepasse = df[~condition_repasse]
    # df_repasse = df[condition_repasse]

    # Carrega as categorias a partir do arquivo JSON
    categories = load_categories()

    # Aplicar o filtro para remover as categorias excluídas
    excluded_categories = categories["excluded_categories"]

    # Remover as linhas que contenham as categorias excluídas
    df_filtered = df[~df['Descrição Categoria'].isin(excluded_categories)]

    # Filtros
    is_quarterly = exibe_por == "Trimestre"
    is_percent = exibe_grafico == "Sim"

    show_main_metrics(df_filtered)
    show_bar_chart(df_filtered,'Descrição Grupo')

    show_summary(df_filtered, title='Resumo por Grupo', x_field='Descrição Grupo', is_quarterly=is_quarterly, is_percent=is_percent)

    show_summary(df_filtered, title='Resumo por Grupo', x_field='Descrição Grupo', is_quarterly= not is_quarterly, is_percent=is_percent)

    # Lista para armazenar todas as descrições de categoria do JSON
    all_defined_categories = []

    # Itera pelas categorias e exibe a análise de cada uma
    for category in categories['categories']:
        title = category['title']
        description_category = category['description_category']

        # Adiciona as categorias definidas à lista
        all_defined_categories.extend(description_category)

        # Filtra o DataFrame com base nas descrições de categoria
        df_filtered = df[df['Descrição Categoria'].isin(description_category)]
        
        # Chama a função show_summary para exibir a análise
        show_summary(df_filtered, title=title, x_field='Descrição Categoria', is_quarterly=is_quarterly, is_percent=is_percent)

    # Gera o df_outros filtrando todas as categorias que não estão no JSON
    df_outros = df[~df['Descrição Categoria'].isin(all_defined_categories)]

    # Exibe o df_outros
    show_summary(df_outros, title='Outros', x_field='Descrição Categoria', is_quarterly=is_quarterly, is_percent=is_percent)

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

def show_summary(df, x_field, title, is_quarterly=False, is_percent=False, group_1=None, group_2=None, description_1=None, description_2=None):
    
    if is_quarterly:
        df = df.groupby(['Trimestre', x_field])['Valor'].sum().reset_index()
    else:
        df = df.groupby(['Ano-Mês-Dia', x_field, 'Mês/Ano'])['Valor'].sum().reset_index()

    pivot = create_pivot_table(df, x_field, is_quarterly)
    pivot_combined = create_combined_pivot(pivot, is_percent, group_1, group_2, description_1, description_2)
    
    pivot_combined.index.name = title   
    
    display_pivot_table(pivot_combined)
    
    if is_percent:
        display_percentage_chart(pivot_combined)

    df_excel = pivot_combined.copy()

    # Gera um identificador único usando uuid
    unique_id = str(uuid.uuid4())  # Gera um ID único aleatório
    
    st.download_button(
        label="Download em Excel",
        data=to_excel(df_excel),
        file_name="dados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"download_button_{unique_id}"  # Usa o ID único como a key
    )

def create_pivot_table(df,x_field,is_quarterly):
    
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

def create_combined_pivot(pivot,is_percent=False,group_1=None,group_2=None,description_1=None,description_2=None):
    
    if is_percent:
        pivot_percent = calculate_percentages(pivot)
        pivot_combined = combine_pivot_and_percent(pivot, pivot_percent)
    else:
        pivot_combined = pivot.copy()
    
    pivot_combined = add_totals(pivot_combined,group_1,group_2,description_1,description_2)
    return pivot_combined

def calculate_percentages(pivot):
    pivot_percent = pivot.copy()
    for col in pivot.columns:
        first_row_value = pivot.iloc[0][col]
        pivot_percent[col] = pivot[col] / first_row_value * 100 if first_row_value != 0 else 0
    return pivot_percent

def combine_pivot_and_percent(pivot, pivot_percent):
    pivot_combined = pd.DataFrame()
    for col in pivot.columns:
        pivot_combined[f'{col}'] = pivot[col]
        pivot_combined[f'{col} %'] = pivot_percent[col]
    new_order = [item for pair in zip(pivot.columns, [f'{col} %' for col in pivot.columns]) for item in pair]
    return pivot_combined[new_order]

def add_totals(pivot_combined,group_1=None,group_2=None,description_1=None,description_2=None):

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

    total_geral = pivot_combined.sum()
    total_geral.name = 'Total Geral'
    pivot_combined = pd.concat([pivot_combined, pd.DataFrame([total_geral])])
    
    pivot_combined['Total por Linha'] = pivot_combined[[col for col in pivot_combined.columns if "%" not in col]].sum(axis=1)
    
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

def display_percentage_chart(pivot_combined):
    percent_columns = [col for col in pivot_combined.columns if '%' in col]
    df_percentual = pivot_combined[percent_columns].transpose()
    fig = px.line(
        df_percentual, 
        title='Evolução Percentual por Grupo / Trimestre',
        labels={'value': 'Percentual (%)', 'index': 'Trimestres'}
    )
    st.plotly_chart(fig, use_container_width=True)

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



