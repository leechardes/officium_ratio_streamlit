import pandas as pd
from babel.numbers import format_currency

def format_real(value):
    return format_currency(value, 'BRL', locale='pt_BR')

def apply_filters(df, trimestre_selecionado, mes_ano_selecionado, grupo_selecionado, subgrupo_selecionado, categoria_selecionada):
    """
    Aplica os filtros selecionados ao DataFrame.
    
    :param df: DataFrame original
    :param trimestre_selecionado: Lista de trimestres selecionados
    :param mes_ano_selecionado: Lista de meses/anos selecionados
    :param grupo_selecionado: Lista de grupos selecionados
    :param subgrupo_selecionado: Lista de subgrupos selecionados
    :param categoria_selecionada: Lista de categorias selecionadas
    :return: DataFrame filtrado
    """
    df_filtered = df[
        (df['Trimestre'].isin(trimestre_selecionado)) &
        (df['Mês/Ano'].isin(mes_ano_selecionado)) &
        (df['Descrição Grupo'].isin(grupo_selecionado)) &
        (df['Descrição SubGrupo'].isin(subgrupo_selecionado)) &
        (df['Descrição Categoria'].isin(categoria_selecionada))
    ]
    
    return df_filtered