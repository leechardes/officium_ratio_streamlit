import pandas as pd
from babel.numbers import format_currency
import streamlit as st

def format_real(value):
    return format_currency(value, 'BRL', locale='pt_BR')

def apply_filters():
    """
    Aplica os filtros selecionados ao DataFrame no session_state.
    
    :return: DataFrame filtrado
    """
    st.session_state.df = st.session_state.df[
        (st.session_state.df['Trimestre'].isin(st.session_state.trimestre_selecionado)) &
        (st.session_state.df['Mês/Ano'].isin(st.session_state.mes_ano_selecionado)) &
        (st.session_state.df['Descrição Grupo'].isin(st.session_state.grupo_selecionado)) &
        (st.session_state.df['Descrição SubGrupo'].isin(st.session_state.subgrupo_selecionado)) &
        (st.session_state.df['Descrição Categoria'].isin(st.session_state.categoria_selecionada))
    ]

