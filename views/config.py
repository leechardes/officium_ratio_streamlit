import json
import streamlit as st

# Carregar e salvar categorias
# Carregar categorias e garantir que as propriedades existam
def load_categories():
    with open('config/categories.json', 'r') as f:
        categories = json.load(f)
    
    # Verifica se as propriedades 'categories' e 'excluded_categories' existem
    if "categories" not in categories:
        categories["categories"] = []
    if "excluded_categories" not in categories:
        categories["excluded_categories"] = []

    return categories

def save_categories(categories):
    with open('config/categories.json', 'w') as f:
        json.dump(categories, f, indent=4)

# Função para adicionar nova categoria
def add_category(categories):
    st.subheader("Adicionar nova categoria")
    new_category_title = st.text_input("Título da categoria", key="new_category_title")
    new_category_description = st.text_input("Descrição da categoria", key="new_category_description")
    
    def add_category_action():
        new_category = {
            "title": st.session_state["new_category_title"],
            "description_category": [st.session_state["new_category_description"]]
        }
        if new_category["title"] not in [cat["title"] for cat in categories["categories"]]:
            categories["categories"].append(new_category)
            save_categories(categories)
            st.success("Categoria adicionada com sucesso!")
        else:
            st.warning("Essa categoria já existe.")
        # Limpar campos
        st.session_state["new_category_title"] = ""
        st.session_state["new_category_description"] = ""

    st.button("Adicionar", on_click=add_category_action)

# Função para editar categorias
def edit_category(categories):
    st.subheader("Editar categorias existentes")
    category_titles = [category["title"] for category in categories["categories"]]
    selected_category = st.selectbox("Selecione a categoria para editar", category_titles)

    # Função para adicionar a nova descrição e limpar os campos
    def add_description():
        if st.session_state["new_description"].strip():
            for category in categories["categories"]:
                if category["title"] == selected_category:
                    category["description_category"].append(st.session_state["new_description"].strip())
                    save_categories(categories)
                    st.success("Descrição adicionada com sucesso!")
                    # Limpar o campo após adicionar
                    st.session_state["new_description"] = ""

    # Função para editar a descrição
    def edit_description(index, new_value):
        for category in categories["categories"]:
            if category["title"] == selected_category:
                category["description_category"][index] = new_value.strip()
                save_categories(categories)
                st.success("Descrição editada com sucesso!")
                st.rerun()

    # Função para deletar uma descrição
    def delete_description(index):
        for category in categories["categories"]:
            if category["title"] == selected_category:
                category["description_category"].pop(index)
                save_categories(categories)
                st.success("Descrição deletada com sucesso!")
                st.rerun()

    # Inicializar o session_state para new_description
    if "new_description" not in st.session_state:
        st.session_state["new_description"] = ""

    if selected_category:
        for category in categories["categories"]:
            if category["title"] == selected_category:
                category_title = st.text_input("Título da categoria", value=category["title"])
                descriptions = category["description_category"]
                num_descriptions = len(descriptions)

                col1, col2, col3 = st.columns([3, 1, 4])  # Adiciona uma terceira coluna para o botão de deletar
                with col1:
                    st.write("Descrição")
                with col2:
                    st.write("Editar")
                with col3:
                    st.write("Deletar")

                # Loop para editar e deletar as descrições existentes
                for i in range(num_descriptions):
                    col1, col2, col3 = st.columns([3, 1, 4])  # Configura as três colunas
                    with col1:
                        description = st.text_input(f"Descrição {i+1}", value=descriptions[i], key=f"description_{i}", label_visibility="collapsed")
                    with col2:
                        if st.button("Salvar", key=f"save_{i}", on_click=edit_description, args=(i, description)):
                            pass
                    with col3:
                        if st.button("Deletar", key=f"delete_{i}", on_click=delete_description, args=(i,)):
                            pass

                # Adicionar nova descrição
                st.text_input("Nova descrição", key="new_description")
                st.button("Adicionar", key="add_description_button", on_click=add_description)

# Função para excluir categorias
def delete_category(categories):
    st.subheader("Excluir categorias existentes")
    category_titles = [category["title"] for category in categories["categories"]]
    selected_category_to_delete = st.selectbox("Selecione a categoria para excluir", category_titles, key="selected_category_to_delete")
    
    if selected_category_to_delete:
        def delete_action():
            for category in categories["categories"]:
                if category["title"] == selected_category_to_delete:
                    categories["categories"].remove(category)
                    save_categories(categories)
                    st.success("Categoria excluída com sucesso!")
                    # Remover a categoria e reiniciar a página
                    # st.rerun()
        
        st.button("Excluir", on_click=delete_action)

def edit_excluded_categories(categories):
    st.subheader("Editar categorias excluídas")
    excluded_descriptions = categories["excluded_categories"]

    # Função para remover uma descrição
    def remove_excluded_description(index):
        excluded_descriptions.pop(index)
        save_categories(categories)
        st.success("Descrição excluída com sucesso!")

    # Função para adicionar uma nova descrição
    def add_new_excluded_description():
        if st.session_state["new_excluded_description"].strip():
            excluded_descriptions.append(st.session_state["new_excluded_description"].strip())
            save_categories(categories)
            st.success("Descrição adicionada com sucesso!")
            st.session_state["new_excluded_description"] = ""

    # Listar as descrições excluídas existentes
    for i, desc in enumerate(excluded_descriptions):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input(f"Descrição Excluída {i+1}", value=desc, key=f"excluded_{i}", disabled=True, label_visibility="collapsed")
        with col2:
            st.button("Remover", key=f"remove_excluded_{i}", on_click=remove_excluded_description, args=(i,))

    # Adicionar uma nova descrição excluída
    st.text_input("Nova descrição excluída", key="new_excluded_description")
    st.button("Adicionar nova descrição", key="add_new_excluded", on_click=add_new_excluded_description)


# Função principal de configuração
def show_config():
    st.title("Configuração")
    categories = load_categories()

    # Inicializar o session_state
    if "new_category_title" not in st.session_state:
        st.session_state["new_category_title"] = ""
    if "new_category_description" not in st.session_state:
        st.session_state["new_category_description"] = ""

    # Chamar as funções
    add_category(categories)
    edit_category(categories)
    delete_category(categories)
    edit_excluded_categories(categories)