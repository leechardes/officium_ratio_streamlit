import streamlit as st
from data.companys import CompanyManager

company_manager = CompanyManager()

def show_company_management():
    st.title("Gerenciamento de Empresas")
    
    # Exemplo de função para adicionar uma empresa
    new_company_name = st.text_input("Nome da empresa", key="new_company")
    if st.button("Adicionar Empresa"):
        if new_company_name:
            result = company_manager.add_company(new_company_name)
            st.success(result['message'])
        else:
            st.warning("Preencha o nome da empresa.")
    
    # Listar empresas
    companies = company_manager.list_companies()
    st.write("Empresas cadastradas:")
    for company in companies:
        st.write(company["company"])
