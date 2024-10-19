import pandas as pd
from babel.numbers import format_currency
import streamlit as st

def format_real(value):
    return format_currency(value, 'BRL', locale='pt_BR')

def apply_filters():
    """
    Aplica os filtros selecionados ao DataFrame no session_state.
    
    :return: DataFrame filtrado ou mensagem de aviso se o DataFrame estiver vazio ou filtros não forem aplicados corretamente.
    """
    # Verifica se o DataFrame existe e não está vazio
    if 'df' not in st.session_state or st.session_state.df.empty:
        st.warning("O DataFrame está vazio ou não foi carregado.")
        return
    
    # Verifica se os filtros estão presentes no session_state
    required_filters = ['trimestre_selecionado', 'mes_ano_selecionado', 'grupo_selecionado', 'subgrupo_selecionado', 'categoria_selecionada']
    for filtro in required_filters:
        if filtro not in st.session_state:
            # st.warning(f"Filtro {filtro} não está definido.")
            return
    
    # Aplica os filtros ao DataFrame
    filtered_df = st.session_state.df[
        (st.session_state.df['Trimestre'].isin(st.session_state.trimestre_selecionado)) &
        (st.session_state.df['Mês/Ano'].isin(st.session_state.mes_ano_selecionado)) &
        (st.session_state.df['Descrição Grupo'].isin(st.session_state.grupo_selecionado)) &
        (st.session_state.df['Descrição SubGrupo'].isin(st.session_state.subgrupo_selecionado)) &
        (st.session_state.df['Descrição Categoria'].isin(st.session_state.categoria_selecionada))
    ]
    
    # Atualiza o DataFrame no session_state
    st.session_state.df = filtered_df
    
    # Retorna o DataFrame filtrado
    return filtered_df
