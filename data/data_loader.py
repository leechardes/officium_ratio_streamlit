import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/data.csv',
                         sep=';',
                         encoding='utf-8',
                         quotechar='"',
                         escapechar='\'',
                         on_bad_lines='warn')
        
        # Converter a coluna 'Valor' para numérico, tratando erros
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {str(e)}")
        return pd.DataFrame()