import streamlit as st
from data.categories import CategoryManager

category_manager = CategoryManager()

# Função para adicionar novo subgrupos
def add_category():
    st.subheader("Adicionar novo subgrupo")
    new_category_title = st.text_input("Título do subgrupo", key="new_category_title")
    new_category_description = st.text_input("Descrição do subgrupo", key="new_category_description")

    def add_category_action():
        if new_category_title and new_category_description:
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
    categories = category_manager.list_categories(st.session_state.company)
    category_titles = [category["title"] for category in categories]
    selected_category = st.selectbox("Selecione o subgrupo para editar", category_titles)

    if selected_category:
        category = next(cat for cat in categories if cat["title"] == selected_category)
        descriptions = category["description_category"]
        
        def add_description():
            if st.session_state["new_description"].strip():
                descriptions.append(st.session_state["new_description"].strip())
                category_manager.update_category(selected_category, descriptions, st.session_state.company)
                st.success("Descrição adicionada com sucesso!")
                st.session_state["new_description"] = ""

        def edit_description(index, new_value):
            descriptions[index] = new_value.strip()
            category_manager.update_category(selected_category, descriptions, st.session_state.company)
            st.success("Descrição editada com sucesso!")
            # st.rerun()

        def delete_description(index):
            descriptions.pop(index)
            category_manager.update_category(selected_category, descriptions, st.session_state.company)
            st.success("Descrição deletada com sucesso!")
            # st.rerun()

        for i, description in enumerate(descriptions):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                description_text = st.text_input(f"Descrição {i+1}", value=description, key=f"description_{i}", label_visibility="collapsed")
            with col2:
                st.button("Salvar", key=f"save_{i}", on_click=edit_description, args=(i, description_text))
            with col3:
                st.button("Deletar", key=f"delete_{i}", on_click=delete_description, args=(i,))

        st.text_input("Nova descrição", key="new_description")
        st.button("Adicionar", key="add_description_button", on_click=add_description)

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

def edit_excluded_categories():
    st.subheader("Editar categorias excluídas")
    excluded_categories = category_manager.list_excluded_categories(st.session_state.company)

    def remove_excluded_description(index):
        result = category_manager.remove_excluded_category(excluded_categories[index], st.session_state.company)
        st.success(result["message"])
        # st.rerun()

    def add_new_excluded_description():
        if st.session_state["new_excluded_description"].strip():
            result = category_manager.add_excluded_category(st.session_state["new_excluded_description"].strip(), st.session_state.company)
            st.success(result["message"])
            st.session_state["new_excluded_description"] = ""

    for i, desc in enumerate(excluded_categories):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input(f"Categoria Excluída {i+1}", value=desc, key=f"excluded_{i}", disabled=True, label_visibility="collapsed")
        with col2:
            st.button("Remover", key=f"remove_excluded_{i}", on_click=remove_excluded_description, args=(i,))

    st.text_input("Nova categoria excluída", key="new_excluded_description")
    st.button("Adicionar nova descrição", key="add_new_excluded", on_click=add_new_excluded_description)

def show_category_management():
    st.title("Gerenciamento de Categorias")
    add_category()
    edit_category()
    delete_category()
    edit_excluded_categories()
