import streamlit as st
import locale

def set_page_config():
    st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
    # locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
    # locale.setlocale(locale.LC_MONETARY, 'pt_BR')