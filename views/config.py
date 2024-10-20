import streamlit as st
import csv
import os
import shutil
import logging
import pandas as pd
from datetime import datetime
from utils.process_csv import process_csv  
from data.categories import CategoryManager
from data.data import DataManager

# Inicializar o gerenciador de dados
manager = DataManager()

# Configurar logging
log_file = "processamento.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Inicializar a classe CategoryManager
category_manager = CategoryManager()

# Função para adicionar novo subgrupos
def add_category():
    st.subheader("Adicionar novo subgrupo")
    new_category_title = st.text_input("Título do subgrupo", key="new_category_title")
    new_category_description = st.text_input("Descrição do subgrupo", key="new_category_description")

    def add_category_action():
        if new_category_title and new_category_description:
            # Usa o valor de 'company' para associar a categoria à empresa
            result = category_manager.add_category(new_category_title, [new_category_description], st.session_state.company)
            st.success(result['message'])
            st.session_state["new_category_title"] = ""
            st.session_state["new_category_description"] = ""
        else:
            st.warning("Por favor, preencha os campos corretamente.")

    st.button("Adicionar", on_click=add_category_action)

# Função para editar subgrupos
def edit_category():
    st.subheader("Editar subgrupos existentes")
    # Lista as categorias associadas à empresa
    categories = category_manager.list_categories(st.session_state.company)
    category_titles = [category["title"] for category in categories]
    selected_category = st.selectbox("Selecione o subgrupo para editar", category_titles)

    if selected_category:
        # Recuperar a categoria selecionada
        category = next(cat for cat in categories if cat["title"] == selected_category)
        descriptions = category["description_category"]
        
        # Função para adicionar uma nova descrição e limpar os campos
        def add_description():
            if st.session_state["new_description"].strip():
                descriptions.append(st.session_state["new_description"].strip())
                category_manager.update_category(selected_category, descriptions, st.session_state.company)
                st.success("Descrição adicionada com sucesso!")
                st.session_state["new_description"] = ""

        # Função para editar uma descrição existente
        def edit_description(index, new_value):
            descriptions[index] = new_value.strip()
            category_manager.update_category(selected_category, descriptions, st.session_state.company)
            st.success("Descrição editada com sucesso!")
            st.rerun()

        # Função para deletar uma descrição
        def delete_description(index):
            descriptions.pop(index)
            category_manager.update_category(selected_category, descriptions, st.session_state.company)
            st.success("Descrição deletada com sucesso!")
            st.rerun()

        # Exibe as descrições existentes e as opções de editar e deletar
        for i, description in enumerate(descriptions):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                description_text = st.text_input(f"Descrição {i+1}", value=description, key=f"description_{i}", label_visibility="collapsed")
            with col2:
                st.button("Salvar", key=f"save_{i}", on_click=edit_description, args=(i, description_text))
            with col3:
                st.button("Deletar", key=f"delete_{i}", on_click=delete_description, args=(i,))

        # Adicionar nova descrição
        st.text_input("Nova descrição", key="new_description")
        st.button("Adicionar", key="add_description_button", on_click=add_description)

# Função para excluir subgrupos
def delete_category():
    st.subheader("Excluir subgrupos existentes")
    categories = category_manager.list_categories(st.session_state.company)
    category_titles = [category["title"] for category in categories]
    selected_category_to_delete = st.selectbox("Selecione o subgrupo para excluir", category_titles, key="selected_category_to_delete")
    
    if selected_category_to_delete:
        def delete_action():
            result = category_manager.delete_category(selected_category_to_delete, st.session_state.company)
            st.success(result["message"])
        
        st.button("Excluir", on_click=delete_action)

# Função para editar categorias excluídas
def edit_excluded_categories():
    st.subheader("Editar categorias excluídas")
    excluded_categories = category_manager.list_excluded_categories(st.session_state.company)

    # Função para remover uma descrição
    def remove_excluded_description(index):
        result = category_manager.remove_excluded_category(excluded_categories[index], st.session_state.company)
        st.success(result["message"])
        st.rerun()

    # Função para adicionar uma nova descrição excluída
    def add_new_excluded_description():
        if st.session_state["new_excluded_description"].strip():
            result = category_manager.add_excluded_category(st.session_state["new_excluded_description"].strip(), st.session_state.company)
            st.success(result["message"])
            st.session_state["new_excluded_description"] = ""

    # Exibe as categorias excluídas e opções para remover
    for i, desc in enumerate(excluded_categories):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input(f"Categoria Excluída {i+1}", value=desc, key=f"excluded_{i}", disabled=True, label_visibility="collapsed")
        with col2:
            st.button("Remover", key=f"remove_excluded_{i}", on_click=remove_excluded_description, args=(i,))

    # Adicionar uma nova descrição excluída
    st.text_input("Nova categoria excluída", key="new_excluded_description")
    st.button("Adicionar nova descrição", key="add_new_excluded", on_click=add_new_excluded_description)

# Função principal de configuração
def show_config():
    st.title("Configuração")

    company = st.session_state.company

    # Chamar as funções de gerenciamento de categorias
    add_category()
    edit_category()
    delete_category()
    edit_excluded_categories()

    # Interface com o usuário para upload e processamento de arquivos CSV
    st.write("### Upload e Processamento de Arquivos CSV")
    if 'uploader_key' not in st.session_state:
        st.session_state['uploader_key'] = 0

    uploaded_files = st.file_uploader("Selecione um ou mais arquivos CSV", type=["csv"], accept_multiple_files=True, key=f"uploader_{st.session_state['uploader_key']}")

    if st.button("Processar"):
        if uploaded_files:
            process_uploaded_files(uploaded_files)  # Processar os arquivos CSV
            reset_uploader()  # Reiniciar o file uploader
            st.cache_data.clear()  # Limpar o cache
            st.session_state.df = manager.get_company_dataframe(company)
            st.session_state['uploader_key'] += 1  # Incrementar a chave
        else:
            st.warning("Por favor, selecione pelo menos um arquivo CSV para processar.")

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

def reset_uploader():
    st.session_state['uploaded_files'] = []

def clear_upload_folder(upload_dir):
    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)
    os.makedirs(upload_dir)
