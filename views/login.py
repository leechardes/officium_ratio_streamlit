import streamlit as st
from data.users import UserManager 
from data.companys import CompanyManager

def show_login():
    # Inicializa a classe de gerenciamento de usuários
    user_manager = UserManager()
    
    # Verifica se o usuário já está logado
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user"] = None

    if st.session_state["logged_in"]:
        return True  # Se já está logado, retorna True

    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
        # Exibe a tela de login
        st.title("Login")

        st.markdown("""
        <style>
            input[type="text"] {
                width: 200px;
            }
        </style>
        """, unsafe_allow_html=True)

        # Formulário de login
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            companies = st.session_state.companies

            companies_list = list(map(lambda x: x['company'], companies))
            company_selected = st.selectbox("Selecione um grupo de empresas", companies_list, index=0, key="company_selected")

            submit_button = st.form_submit_button("Login")

        # Autenticar o usuário quando o formulário for submetido
        if submit_button:
            # Usa o método authenticate_user da classe UserManager
            result = user_manager.authenticate_user(username, password)

            if result["status"] == "success":
                st.session_state["logged_in"] = True
                st.session_state["user"] = user_manager.get_user(username)["user"] 
                st.session_state["company"] = company_selected
                st.success("Login efetuado com sucesso!")
                st.rerun()  # Atualiza a página
                return True
            else:
                st.error("Usuário ou senha incorretos")

    return False  # Caso o login não tenha sido feito, retorna False
