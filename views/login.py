import json
import streamlit as st


def show_login():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user"] = None


    # Verifica se o usuário já está logado
    if st.session_state["logged_in"]:
        return True  # Se já está logado, retorna True


    # Caso não esteja logado, exibe a tela de login
    st.title("Login")

    st.markdown("""
    <style>
        input[type="text"] {
            width: 200px;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        st.form_submit_button("Login")


    if st.form("Login"):
        with open("config/users.json", "r") as f:
            users = json.load(f)


        for user in users:
            if user["username"] == username and user["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user
                st.success("Login efetuado com sucesso!")
                st.rerun()
                return True  # Login bem-sucedido, retorna True


        # st.error("Usuário ou senha incorretos")
    return False  # Caso o login não tenha sido feito, retorna False