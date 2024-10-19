import streamlit as st
import os
import shutil
import logging
from utils.process_csv import process_csv  
from data.data import DataManager

manager = DataManager()

def process_uploaded_files(files):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    manager.delete_company_data(company=st.session_state.company)

    for file in files:
        file_path = os.path.join(upload_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
        logging.info(f"Arquivo carregado: {file_path}")

        company = st.session_state.company

        try:
            process_csv(file_path, company, manager)
            logging.info(f"Arquivo processado com sucesso: {file_path}")
        except Exception as e:
            logging.error(f"Erro ao processar o arquivo {file.name}: {e}")
            st.error(f"Erro ao processar o arquivo {file.name}: {e}")

    st.success("Processamento e backup concluídos com sucesso!")

def show_import_data():
    st.title("Importação de Arquivos CSV")

    if 'uploader_key' not in st.session_state:
        st.session_state['uploader_key'] = 0

    uploaded_files = st.file_uploader("Selecione um ou mais arquivos CSV", type=["csv"], accept_multiple_files=True, key=f"uploader_{st.session_state['uploader_key']}")

    if st.button("Processar"):
        if uploaded_files:
            process_uploaded_files(uploaded_files)
            st.cache_data.clear()
            st.session_state.df = manager.get_company_dataframe(st.session_state.company)
            st.session_state['uploader_key'] += 1
        else:
            st.warning("Por favor, selecione pelo menos um arquivo CSV para processar.")
