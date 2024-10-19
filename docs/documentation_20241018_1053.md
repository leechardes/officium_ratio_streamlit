# Documentação Unificada

## Estrutura do Projeto

```
./
├── config/
│   ├── categories.json
│   ├── users.json
│   └── settings.py
├── uploads/
├── utils/
│   ├── process_csv.py
│   └── helpers.py
├── docs/
│   ├── pivot (1).csv
│   └── pivot (2).csv
├── components/
│   └── sidebar.py
├── logs/
│   ├── update_log_20241007_122934.txt
│   └── update_log_20241007_190137.txt
├── scripts/
│   ├── config/
│   │   └── generate_documentation.json
│   ├── update_environment.py
│   ├── setup_environment.py
│   ├── generate_project_structure.py
│   └── generate_documentation.py
├── data/
│   ├── bkp/
│   │   ├── data.csv
│   │   └── dre_process.csv
│   ├── data_loader.py
│   └── data.csv
├── views/
│   ├── config.py
│   ├── version.py
│   ├── overview.py
│   └── login.py
├── assets/
│   ├── styles.css
│   └── logo.png
├── backups/
│   ├── data_backup_20241008_205856.csv
│   ├── data_backup_20241008_180833.csv
│   ├── data_backup_20241008_181654.csv
│   ├── data_backup_20241008_180204.csv
│   ├── data_backup_20241008_181721.csv
│   ├── data_backup_20241008_175339.csv
│   ├── data_backup_20241008_181939.csv
│   ├── data_backup_20241008_183643.csv
│   ├── data_backup_20241008_181444.csv
│   ├── data_backup_20241008_181525.csv
│   ├── data_backup_20241008_184313.csv
│   ├── data_backup_20241008_184139.csv
│   ├── data_backup_20241008_184339.csv
│   ├── data_backup_20241008_182615.csv
│   ├── data_backup_20241008_184112.csv
│   ├── data_backup_20241008_181019.csv
│   ├── data_backup_20241008_182935.csv
│   ├── data_backup_20241008_181637.csv
│   ├── data_backup_20241008_175416.csv
│   ├── data_backup_20241008_182659.csv
│   ├── data_backup_20241008_182856.csv
│   ├── data_backup_20241008_183813.csv
│   ├── data_backup_20241008_182728.csv
│   ├── data_backup_20241008_184010.csv
│   ├── data_backup_20241008_181814.csv
│   ├── data_backup_20241008_183742.csv
│   ├── data_backup_20241008_180920.csv
│   ├── data_backup_20241008_183346.csv
│   ├── data_backup_20241008_183622.csv
│   ├── data_backup_20241008_180910.csv
│   ├── data_backup_20241008_183821.csv
│   ├── data_backup_20241008_182524.csv
│   ├── data_backup_20241008_175435.csv
│   ├── data_backup_20241008_175430.csv
│   ├── data_backup_20241008_180903.csv
│   ├── data_backup_20241008_175222.csv
│   ├── data_backup_20241008_184026.csv
│   ├── data_backup_20241008_180240.csv
│   ├── data_backup_20241008_184032.csv
│   ├── data_backup_20241008_182905.csv
│   ├── data_backup_20241008_193014.csv
│   ├── data_backup_20241008_182737.csv
│   ├── data_backup_20241008_181649.csv
│   ├── data_backup_20241008_182625.csv
│   ├── data_backup_20241008_184125.csv
│   ├── data_backup_20241008_183717.csv
│   ├── data_backup_20241008_184044.csv
│   ├── data_backup_20241008_181704.csv
│   ├── data_backup_20241008_175519.csv
│   ├── data_backup_20241008_184251.csv
│   └── data_backup_20241008_182542.csv
├── requirements.txt
├── processamento.log
└── main.py
```
## Conteúdo dos Arquivos

### ./requirements.txt
```
streamlit
pandas
plotly
setuptools
xlsxwriter
openpyxl
babel
```
### ./.gitignore
```
# Python #
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Virtual environment
venv/
env/
ENV/
.env
.venv
venv.bak/

# Streamlit config and cache
.streamlit/
# Cache files
*.pkl
*.cache

# Jupyter Notebook checkpoints
.ipynb_checkpoints

# Logs and local files
*.log
*.sqlite3

# VS Code settings
.vscode/
*.csv
data/data.csv
categories.json
users.json

# macOS
.DS_Store

```
### ./main.py
```python
import streamlit as st
from components.sidebar import create_sidebar
from views.overview import show_overview
from views.config import show_config
from views.login import show_login
from views.version import show_version

from utils.helpers import apply_filters
from config.settings import set_page_config

def main():
    
    if show_login():  # O login só retorna True quando o login for bem-sucedido
        create_sidebar()  # Cria a sidebar e armazena as seleções no session_state
        
        apply_filters()  # Aplica os filtros ao df no session_state
        
        if st.session_state.page == "Visão Geral":
            show_overview()
        elif st.session_state.page == "Configuração":
            show_config()
        elif st.session_state.page == "Versão":
            show_version()
        else:
            st.write("Página em desenvolvimento")
    else:
        st.write("Você precisa fazer login para acessar o sistema")

if __name__ == "__main__":
    
    set_page_config()
    main()

```
### assets/styles.css
```css
/* Adicione seus estilos personalizados aqui */
body {
    font-family: Arial, sans-serif;
}
```
### assets/logo.png
```

```
### components/sidebar.py
```python
import streamlit as st
from data.data_loader import load_data

def create_sidebar():
    st.sidebar.title("Menu")
    st.session_state.df = load_data()  # Carrega o dataframe no session_state
    
    # Pergunta sobre exibição de gráfico e cálculo de percentual
    st.sidebar.selectbox("Exibe gráfico?", ["Sim", "Não"], key="exibe_grafico")
    st.sidebar.selectbox("Exibe por trimestre ou mês?", ["Trimestre", "Mês"], key="exibe_trimestre")
    st.sidebar.selectbox("Calcular percentual?", ["Sim", "Não"], key="calcula_percentual")
    st.sidebar.selectbox("Escolha uma página", ["Visão Geral", "Configuração", "Versão"], key="page")

    # Filtros
    trimestre = sorted(st.session_state.df['Trimestre'].unique())
    meses_anos = sorted(st.session_state.df['Mês/Ano'].unique())
    grupos = sorted(st.session_state.df['Descrição Grupo'].unique())
    subgrupos = sorted(st.session_state.df['Descrição SubGrupo'].unique())
    categorias = sorted(st.session_state.df['Descrição Categoria'].unique())

    # Armazenando os filtros no session_state
    st.sidebar.multiselect('Selecione o(s) Trimestre(es)', trimestre, default=trimestre, key="trimestre_selecionado")
    st.sidebar.multiselect('Selecione o(s) Mês(es)/Ano(s)', meses_anos, default=meses_anos, key="mes_ano_selecionado")
    st.sidebar.multiselect('Selecione o(s) Grupo(s)', grupos, default=grupos, key="grupo_selecionado")
    st.sidebar.multiselect('Selecione o(s) Subgrupo(s)', subgrupos, default=subgrupos, key="subgrupo_selecionado")
    st.sidebar.multiselect('Selecione a(s) Categoria(s)', categorias, default=categorias, key="categoria_selecionada")

```
### components/__pycache__/sidebar.cpython-312.pyc
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xcb in position 0: invalid continuation byte
### config/categories.json
```json
{
    "categories": [
        {
            "title": "3.01 Receitas de Vendas e de Servi\u00e7os",
            "description_category": [
                "Receita de conv\u00eanios",
                "Receitas de Servi\u00e7os Cart\u00e3o C/D",
                "Receitas de Servi\u00e7os em Esp\u00e9cie",
                "Receitas de Servi\u00e7os PIX"
            ]
        },
        {
            "title": "4.01 Impostos sobre Vendas e Servi\u00e7os",
            "description_category": [
                "COFINS",
                "CSL",
                "IRPJ",
                "ISS sobre Faturamento",
                "Parcelamento do Simples Nacional",
                "PIS",
                "Simples Nacional - DAS"
            ]
        },
        {
            "title": "4.02 Despesas com Vendas e Servi\u00e7os",
            "description_category": [
                "Aluguel de Maquinas e Equipamentos",
                "DEVOLU\u00c7\u00c3O DE SERVI\u00c7O",
                "Documentos Odonto",
                "Laudos de Exames Terceirizados",
                "Materiais Aplicados na Presta\u00e7\u00e3o de Servi\u00e7os",
                "Material M\u00e9dico Hospitalar",
                "Reembolso M\u00e9dicos ref NFE",
                "Repasse M\u00e9dicos"
            ]
        },
        {
            "title": "4.03 Despesas com Sal\u00e1rios e Encargos",
            "description_category": [
                "Ajuda de Custo",
                "F\u00e9rias",
                "FGTS e Multa de FGTS",
                "INSS sobre Sal\u00e1rios - GPS",
                "Rescis\u00f5es",
                "Reten\u00e7\u00e3o - Darf 5952 - PIS/COFINS/CSLL",
                "Sal\u00e1rios",
                "Contribui\u00e7\u00e3o Sindical",
                "Fardamento",
                "Gratifica\u00e7\u00f5es",
                "Plano Odontol\u00f3gico Colaboradores",
                "Vale-Transporte"
            ]
        },
        {
            "title": "4.05 Despesas Administrativas",
            "description_category": [
                "Coleta de Lixo Hospitalar",
                "Combust\u00edveis",
                "Copa e Cozinha",
                "Correios",
                "Despesas a identificar",
                "Fatura Cart\u00e3o",
                "Honor\u00e1rios (outros)",
                "Honor\u00e1rios Advocat\u00edcios",
                "Honor\u00e1rios Cont\u00e1beis",
                "Lanches e Refei\u00e7\u00f5es",
                "Manuten\u00e7\u00e3o de Equipamentos",
                "Materiais de Escrit\u00f3rio",
                "Materiais de Limpeza e Higiene",
                "Material de Expediente",
                "Mensalidade CIEE",
                "Mensalidade Sistema",
                "Presta\u00e7\u00e3o de Servi\u00e7os",
                "Rastreamento",
                "Reten\u00e7\u00e3o - ISS Servi\u00e7os Tomados",
                "Seguros de Ve\u00edculos",
                "Taxa",
                "Telefonia e Internet",
                "Telefonia M\u00f3vel",
                "Transporte Urbano (t\u00e1xi, Uber)",
                "Despesas a identificar"
            ]
        },
        {
            "title": "4.06 Despesas Comerciais",
            "description_category": [
                "Brindes para Clientes",
                "Marketing e Publicidade"
            ]
        },
        {
            "title": "4.07 Despesas com Im\u00f3vel",
            "description_category": [
                "\u00c1gua e Saneamento",
                "Aluguel",
                "Energia El\u00e9trica",
                "IPTU",
                "Manuten\u00e7\u00e3o Predial",
                "Material de Constru\u00e7\u00e3o",
                "Seguro de Im\u00f3veis",
                "TCR",
                "Vigil\u00e2ncia e Seguran\u00e7a Patrimonial"
            ]
        },
        {
            "title": "4.10 Despesas Financeiras",
            "description_category": [
                "Tarifas Banc\u00e1rias",
                "Tarifas de Antecipa\u00e7\u00e3o Parcele j\u00e1",
                "Tarifas de Cart\u00f5es de Cr\u00e9dito Sicredi",
                "Tarifas DOC / TED"
            ]
        },
        {
            "title": "3.03 Outras Receitas e Entradas",
            "description_category": [
                "Empr\u00e9stimos de S\u00f3cios",
                "Receitas a Identificar",
                "Repasse laborat\u00f3rio Dore"
            ]
        },
        {
            "title": "4.09 Despesas com Diretoria",
            "description_category": [
                "Distribui\u00e7\u00e3o de Lucro Laborat\u00f3rio",
                "Antecipa\u00e7\u00e3o de Lucros",
                "Plano Odontol\u00f3gico S\u00f3cios"
            ]
        },
        {
            "title": "5.01 Bens Imobilizados da Empresa",
            "description_category": [
                "M\u00e1quinas, Equipamentos e Instala\u00e7\u00f5es Industriais",
                "M\u00f3veis, Utens\u00edlios e Instala\u00e7\u00f5es Administrativos"
            ]
        },
        {
            "title": "5.02 Empr\u00e9stimos e Financiamentos",
            "description_category": [
                "Devolu\u00e7\u00e3o de Empr\u00e9stimo S\u00f3cios",
                "Empr\u00e9stimos de Bancos"
            ]
        },
        {
            "title": "Repasse Laboratoriais",
            "description_category": [
                "Repasse laborat\u00f3rio Dore",
                "Distrib. Lucro Laborat\u00f3rio"
            ]
        }
    ],
    "excluded_categories": [
        "Repasse laborat\u00f3rio Dore",
        "Distrib. Lucro Laborat\u00f3rio"
    ]
}
```
### config/users.json
```json
[
    {
        "username": "admin",
        "password": "senha123",
        "nome": "Administrador",
        "grupo": "admin"
    },
    {
        "username": "heraclito",
        "password": "hera123",
        "nome": "Her\u00e1rclito",
        "grupo": "admin"
    },
    {
        "username": "lee",
        "password": "lee123",
        "nome": "Lee Chardes",
        "grupo": "admin"
    }
]
```
### config/settings.py
```python
import streamlit as st

def set_page_config():
    st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
```
### config/__pycache__/settings.cpython-312.pyc
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xcb in position 0: invalid continuation byte
### utils/process_csv.py
```python
import csv
import os
import argparse
from datetime import datetime

# Dicionário para mapear abreviações de meses para seus números correspondentes
meses_nomes = {
    'Jan': '01', 'Fev': '02', 'Mar': '03', 'Abr': '04', 'Mai': '05', 'Jun': '06',
    'Jul': '07', 'Ago': '08', 'Set': '09', 'Out': '10', 'Nov': '11', 'Dez': '12'
}

def get_trimester(month):
    """Função para calcular o trimestre com base no mês."""
    month = int(month)
    if month in [1, 2, 3]:
        return '1 Trimestre'
    elif month in [4, 5, 6]:
        return '2 Trimestre'
    elif month in [7, 8, 9]:
        return '3 Trimestre'
    else:
        return '4 Trimestre'

def process_csv(input_file, writer, months):
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)

        # Desconsiderar as duas primeiras linhas
        next(reader)
        next(reader)

        rows = list(reader)
        # Desconsiderar a última linha
        rows = rows[:-1]

        sequence = 0  # Variável para a sequência
        current_group = None  # Armazenar o grupo atual
        current_subgroup = None  # Armazenar o subgrupo atual
        group_description = ""  # Descrição do grupo
        subgroup_description = ""  # Descrição do subgrupo

        for i, row in enumerate(rows):
            if i == 0:
                # Se os meses ainda não foram capturados, capturar da segunda até a penúltima coluna
                if not months:
                    months.extend(row[1:-1])
                continue

            # Verificar se a linha é um grupo, subgrupo ou item (grupo)
            first_col = row[0].strip()

            # Grupo: inicia com número seguido de "."
            if first_col[0].isdigit() and first_col[1] == '.':
                group = first_col.split('.')[0]  # Pegar apenas o número do grupo
                group_description = first_col  # Atualizar a descrição do grupo
                subgroup = None
                item = None

                # Reiniciar a sequência se o grupo mudar
                if group != current_group:
                    sequence = 0
                    current_group = group

            # SubGrupo: inicia com número e o ponto está na terceira posição
            elif first_col[0].isdigit() and first_col[2] == '.':
                subgroup = first_col.split('.')[0]  # Pegar apenas o número do subgrupo
                subgroup_description = first_col  # Atualizar a descrição do subgrupo
                item = None

            # Item (Grupo): não segue os padrões anteriores
            else:
                item = first_col

                # Incrementar sequência apenas quando o item mudar
                if item != "":
                    sequence += 1

                # Para cada mês, adicionar uma linha com o valor correspondente
                for month, value in zip(months, row[1:-1]):
                    # Remover aspas e converter valor
                    value = value.replace('"', '').replace('.', '').replace(',', '.')
                    value = float(value) if value else 0.0

                    # Substituir a abreviação do mês pelo número correspondente usando o dicionário
                    try:
                        month_name, year = month.split('/')  # Separar mês e ano
                        if month_name in meses_nomes:
                            formatted_month = f"{year}-{meses_nomes[month_name]}-01"  # Formato AAAA-MM-DD
                            trimestre = get_trimester(meses_nomes[month_name])  # Calcular o trimestre
                        else:
                            print(f"Mês desconhecido: {month_name}")
                            continue
                    except ValueError:
                        # Se houver um erro de formatação, ignorar a linha ou tratar como necessário
                        print(f"Erro ao converter o mês: {month}")
                        continue

                    # Escrever a nova linha no formato desejado
                    writer.writerow([
                        group, group_description, 
                        subgroup if subgroup else '', subgroup_description, 
                        sequence, item, 
                        month, formatted_month, value, trimestre  # Adiciona o trimestre na linha
                    ])

def process_folder(input_folder):
    output_file = 'data.csv'
    months = []

    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=';')

        # Escrever o cabeçalho no arquivo de saída com os nomes atualizados
        writer.writerow([
            'Código Grupo', 'Descrição Grupo', 
            'Código SubGrupo', 'Descrição SubGrupo', 
            'Sequência Grupo', 'Descrição Categoria', 
            'Mês/Ano', 'Ano-Mês-Dia', 'Valor', 'Trimestre'  # Adiciona o cabeçalho para o Trimestre
        ])

        # Percorrer todos os arquivos da pasta
        for filename in os.listdir(input_folder):
            if filename.endswith('.csv'):
                file_path = os.path.join(input_folder, filename)
                print(f"Processando arquivo: {file_path}")
                process_csv(file_path, writer, months)

if __name__ == "__main__":
    # Configurar argparse para aceitar a pasta como argumento
    parser = argparse.ArgumentParser(description='Processar todos os arquivos CSV de uma pasta.')
    parser.add_argument('input_folder', help='Caminho da pasta contendo os arquivos CSV a serem processados')
    args = parser.parse_args()
    
    # Chamar a função passando a pasta recebida
    process_folder(args.input_folder)

```
### utils/helpers.py
```python
import pandas as pd
from babel.numbers import format_currency
import streamlit as st

def format_real(value):
    return format_currency(value, 'BRL', locale='pt_BR')

def apply_filters():
    """
    Aplica os filtros selecionados ao DataFrame no session_state.
    
    :return: DataFrame filtrado
    """
    st.session_state.df = st.session_state.df[
        (st.session_state.df['Trimestre'].isin(st.session_state.trimestre_selecionado)) &
        (st.session_state.df['Mês/Ano'].isin(st.session_state.mes_ano_selecionado)) &
        (st.session_state.df['Descrição Grupo'].isin(st.session_state.grupo_selecionado)) &
        (st.session_state.df['Descrição SubGrupo'].isin(st.session_state.subgrupo_selecionado)) &
        (st.session_state.df['Descrição Categoria'].isin(st.session_state.categoria_selecionada))
    ]


```
### utils/__pycache__/helpers.cpython-312.pyc
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xcb in position 0: invalid continuation byte
### utils/__pycache__/process_csv.cpython-312.pyc
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xcb in position 0: invalid continuation byte
### views/config.py
```python
import json
import os
import streamlit as st
import csv
import os
import shutil
import logging
import pandas as pd
import streamlit as st
from datetime import datetime
from utils.process_csv import process_csv  # Usando o script que você forneceu
from data.data_loader import load_data

# Configurar logging
log_file = "processamento.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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

# Função para adicionar novo subgrupos
def add_category(categories):
    st.subheader("Adicionar novo subgrupo")
    new_category_title = st.text_input("Título da subgrupo", key="new_category_title")
    new_category_description = st.text_input("Descrição da subgrupo", key="new_category_description")
    
    def add_category_action():
        new_category = {
            "title": st.session_state["new_category_title"],
            "description_category": [st.session_state["new_category_description"]]
        }
        if new_category["title"] not in [cat["title"] for cat in categories["categories"]]:
            categories["categories"].append(new_category)
            save_categories(categories)
            st.success("Subgrupo adicionado com sucesso!")
        else:
            st.warning("Esse subgrupo já existe.")
        # Limpar campos
        st.session_state["new_category_title"] = ""
        st.session_state["new_category_description"] = ""

    st.button("Adicionar", on_click=add_category_action)

# Função para editar subgrupos
def edit_category(categories):
    st.subheader("Editar subgrupos existentes")
    category_titles = [category["title"] for category in categories["categories"]]
    selected_category = st.selectbox("Selecione a subgrupo para editar", category_titles)

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
                category_title = st.text_input("Título da subgrupo", value=category["title"])
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

# Função para excluir subgrupos
def delete_category(categories):
    st.subheader("Excluir subgrupos existentes")
    category_titles = [category["title"] for category in categories["categories"]]
    selected_category_to_delete = st.selectbox("Selecione o subgrupo para excluir", category_titles, key="selected_category_to_delete")
    
    if selected_category_to_delete:
        def delete_action():
            for category in categories["categories"]:
                if category["title"] == selected_category_to_delete:
                    categories["categories"].remove(category)
                    save_categories(categories)
                    st.success("Subgrupo excluída com sucesso!")
        
        st.button("Excluir", on_click=delete_action)

def edit_excluded_categories(categories):
    st.subheader("Editar subgrupos excluídos")
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

def manage_users():
    st.title("Gerenciamento de Usuários")
    users = load_users()

    # Lista de usuários
    st.subheader("Editar ou Excluir Usuários Existentes")
    col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 2, 2, 1, 1])  # Adiciona uma terceira coluna para o botão de deletar
    with col1:
        st.write("Usuário")
    with col2:
        st.write("Nome")
    with col3:
        st.write("Senha")
    with col4:
        st.write("Grupo")

    for i, user in enumerate(users):
        col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 2, 2, 1, 1])  # Adiciona mais colunas

        # O campo username é fixo, não pode ser alterado
        with col1:
            st.text_input(f"Usuário {i+1}", value=user['username'], key=f"username_{i}", disabled=True, label_visibility="collapsed")

        # Campo Nome
        with col2:
            nome = st.text_input(f"Nome {i+1}", value=user['nome'], key=f"nome_{i}", label_visibility="collapsed")

        # Campo Senha
        with col3:
            password = st.text_input(f"Senha {i+1}", value=user['password'], key=f"password_{i}", type="password", label_visibility="collapsed")

        # Campo Grupo (seleção de grupo)
        with col4:
            grupo = st.selectbox(f"Grupo {i+1}", options=["admin", "usuario"], index=["admin", "usuario"].index(user['grupo']), key=f"grupo_{i}", label_visibility="collapsed")

        # Botão de salvar
        with col5:
            if st.button("Salvar", key=f"save_user_{i}"):
                # Atualiza as informações do usuário, exceto o username
                users[i]["nome"] = nome
                users[i]["password"] = password
                users[i]["grupo"] = grupo
                save_users(users)
                st.success(f"Informações do usuário {user['username']} atualizadas com sucesso!")

        # Botão de deletar
        with col6:
            if st.button("Deletar", key=f"delete_user_{i}"):
                users.pop(i)
                save_users(users)
                st.success(f"Usuário {user['username']} excluído com sucesso!")

    # Adicionar novo usuário
    st.subheader("Adicionar novo usuário")
    new_username = st.text_input("Nome de Usuário", key="new_username")
    new_password = st.text_input("Senha", type="password", key="new_password")
    new_nome = st.text_input("Nome", key="new_nome")
    new_grupo = st.selectbox("Grupo", ["admin", "usuario"], key="new_grupo")

    def add_user_action():
        new_user = {
            "username": new_username,
            "password": new_password,
            "nome": new_nome,
            "grupo": new_grupo
        }
        users.append(new_user)
        save_users(users)
        st.success("Usuário adicionado com sucesso!")
        # Limpar os campos após adicionar
        st.session_state["new_username"] = ""
        st.session_state["new_password"] = ""
        st.session_state["new_nome"] = ""
        st.session_state["new_grupo"] = "usuario"

    st.button("Adicionar Usuário", on_click=add_user_action)

def load_users():
    with open('config/users.json', 'r') as f:
        users = json.load(f)
    return users


def save_users(users):
    with open('config/users.json', 'w') as f:
        json.dump(users, f, indent=4)

# Função para backup do arquivo
def backup_file(file_path):
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Gerar nome do backup com data e hora
    backup_filename = f"data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    shutil.copy(file_path, backup_path)
    logging.info(f"Backup criado: {backup_path}")

# Função para processar o arquivo CSV
def process_uploaded_files(files):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Backup do arquivo atual antes da atualização
    data_file = "data/data.csv"
    if os.path.exists(data_file):
        backup_file(data_file)

    output_file = 'data/data.csv'  # O arquivo final processado
    months = []

    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=';')

        # Escrever o cabeçalho no arquivo de saída com os nomes atualizados
        writer.writerow([
            'Código Grupo', 'Descrição Grupo', 
            'Código SubGrupo', 'Descrição SubGrupo', 
            'Sequência Grupo', 'Descrição Categoria', 
            'Mês/Ano', 'Ano-Mês-Dia', 'Valor', 'Trimestre'  # Adiciona o cabeçalho para o Trimestre
        ])

        # Loop pelos arquivos selecionados para processamento
        for file in files:
            file_path = os.path.join(upload_dir, file.name)
            
            # Salvar o arquivo na pasta uploads
            with open(file_path, "wb") as f:
                f.write(file.read())
            logging.info(f"Arquivo carregado: {file_path}")

            # Processar o arquivo CSV
            try:
                process_csv(file_path, writer, months)
                logging.info(f"Arquivo processado com sucesso: {file_path}")
            except Exception as e:
                logging.error(f"Erro ao processar o arquivo {file.name}: {e}")
                st.error(f"Erro ao processar o arquivo {file.name}: {e}")

    st.success("Processamento e backup concluídos com sucesso!")
    logging.info("Processamento concluído com sucesso.")

def reset_uploader():
    # Resetar o file_uploader
    st.session_state['uploaded_files'] = []

# Função para limpar o diretório de uploads
def clear_upload_folder(upload_dir):
    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)  # Remove todo o diretório de upload
    os.makedirs(upload_dir) 

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
    manage_users()

    # Interface com o usuário
    st.write("### Upload e Processamento de Arquivos CSV")

    # Inicialize uma chave única para o file_uploader no session_state
    if 'uploader_key' not in st.session_state:
        st.session_state['uploader_key'] = 0

    # Criar uma opção de upload de arquivos CSV
    uploaded_files = st.file_uploader("Selecione um ou mais arquivos CSV", type=["csv"], accept_multiple_files=True, key=f"uploader_{st.session_state['uploader_key']}")

    # Verificar se algum arquivo foi selecionado
    # Processar arquivos quando o botão for clicado
    if st.button("Processar"):
        if uploaded_files:
            # Definir o diretório de upload
            upload_dir = "uploads"
            process_uploaded_files(uploaded_files)  # Processar os arquivos
            reset_uploader()  # Reiniciar o file uploader
            clear_upload_folder(upload_dir)  # Limpar a pasta de uploads
            st.cache_data.clear()  # Limpar o cache
            st.session_state.df = load_data()  # Recarregar os dados
            st.session_state['uploader_key'] += 1  # Incrementar a chave
            # st.rerun()
        else:
            st.warning("Por favor, selecione pelo menos um arquivo CSV para processar.")

    data_json = json.dumps(categories)
    data_bytes = data_json.encode("utf-8")
    # Download do arquivo de configuração de categorias
    st.download_button(
        label="Download do arquivo de configuração de categorias",
        data=data_bytes,
        file_name="config_categories.json",
        mime="json",
    )

```
### views/version.py
```python
import streamlit as st

def show_version():
    st.title("Versão Atual")
    st.write("Número da versão: 1.0.2")
    st.write("Data de lançamento: 08/10/2024")
    st.write("Alterações:")
    st.write("* Correção de bugs")
    st.write("* Adição de recursos novos")

    st.title("Histórico de Versões")
    st.write("Versão 1.0.1: 08/10/2024")
    st.write("* Login de acesso")
    st.write("* Gerenciamento de usuário")

    st.title("Histórico de Versões")
    st.write("Versão 1.0.2: 08/10/2024")
    st.write("* Upload e processamento de arquivos CSV")

    st.title("Notas de Lançamento")
    st.write("Versão 1.0.2: 08/10/2024")
    st.write("* Melhorias..")
```
### views/overview.py
```python
from io import BytesIO
import json
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import format_real
import uuid 
import xlsxwriter

# Função para carregar o arquivo JSON
def load_categories():
    with open('config/categories.json', 'r') as f:
        return json.load(f)
    
def show_overview():
    st.title("Dashboard Financeiro - Visão Geral")

    # Carrega as categorias a partir do arquivo JSON
    categories = load_categories()

    # Aplicar o filtro para remover as categorias excluídas
    excluded_categories = categories["excluded_categories"]

    # Remover as linhas que contenham as categorias excluídas
    df_filtered = st.session_state.df[~st.session_state.df['Descrição Categoria'].isin(excluded_categories)]
    df_ignored_excluded = st.session_state.df

    # Agrupa por Ano-Mês-Dia e Trimestre
    st.session_state.total_grupo_1_ymd = df_filtered[df_filtered['Código Grupo'] == 1].groupby('Mês/Ano')['Valor'].sum()
    st.session_state.total_grupo_1_trimestre = df_filtered[df_filtered['Código Grupo'] == 1].groupby('Trimestre')['Valor'].sum()
        
    # Filtros
    st.session_state.is_quarterly = st.session_state.exibe_trimestre == "Trimestre"
    st.session_state.is_percent = st.session_state.calcula_percentual == "Sim"
    st.session_state.is_graph = st.session_state.exibe_grafico == "Sim" and  st.session_state.is_percent

    show_main_metrics(df_filtered)
    show_bar_chart(df_filtered, 'Descrição Grupo')

    show_summary(df_filtered, title='Resumo por Grupo', x_field='Descrição Grupo')
    show_summary(df_filtered, title='Resumo por Grupo Detalhado', x_field='Descrição Grupo', is_quarterly=not st.session_state.is_quarterly)

    # Lista para armazenar todas as descrições de categoria do JSON
    all_defined_categories = []

    for category in categories['categories']:
        title = category['title']
        description_category = category['description_category']
        all_defined_categories.extend(description_category)

        # Filtra o DataFrame com base nas descrições de categoria
        df_filtered_category = df_ignored_excluded[df_ignored_excluded['Descrição Categoria'].isin(description_category)]
        show_summary(df_filtered_category, title=title, x_field='Descrição Categoria')
     
    # Gera o df_outros filtrando todas as categorias que não estão no JSON
    df_outros = df_filtered[~df_filtered['Descrição Categoria'].isin(all_defined_categories)]
    show_summary(df_outros, title='Outros', x_field='Descrição Categoria')

def show_dataframe(df):
    st.write(df)

def show_main_metrics(df):
    col1, col2, col3 = st.columns(3)
    total_geral = df['Valor'].sum()
    total_receitas = df[df['Valor'] > 0]['Valor'].sum()
    total_despesas = df[df['Valor'] < 0]['Valor'].sum()

    col1.metric("Total Geral", format_real(total_geral))
    col2.metric("Total de Receitas", format_real(total_receitas))
    col3.metric("Total de Despesas", format_real(total_despesas))

def show_bar_chart(df, x_field):
    fig_bar = px.bar(
        df.groupby(x_field)['Valor'].sum().reset_index(),
        x=x_field,
        y='Valor',
        title='Valores por ' + x_field.capitalize(),
        labels={'Valor': 'Valor Total', x_field: x_field.capitalize()},
        color='Valor',
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

def show_line_chart(df, x_field, group_field):
    df_time = df.groupby([x_field, group_field])['Valor'].sum().reset_index()
    fig_line = px.line(
        df_time,
        x=x_field,
        y='Valor',
        color=group_field,
        title='Evolução Temporal por ' + group_field.capitalize(),
        labels={'Valor': 'Valor Total', x_field: x_field.capitalize()}
    )
    st.plotly_chart(fig_line, use_container_width=True)

def show_summary(df, x_field, title, is_quarterly = st.session_state.get('is_quarterly', False) ,group_1=None,group_2=None,description_1=None,description_2=None):
    if is_quarterly:
        df = df.groupby(['Trimestre', x_field])['Valor'].sum().reset_index()
    else:
        df = df.groupby(['Ano-Mês-Dia', x_field, 'Mês/Ano'])['Valor'].sum().reset_index()

    pivot = create_pivot_table(df, x_field, is_quarterly)
    pivot_combined = create_combined_pivot(pivot, is_quarterly, group_1, group_2, description_1, description_2)

    pivot_combined.index.name = title
    display_pivot_table(pivot_combined)

    if st.session_state.is_graph:
        display_percentage_chart(pivot_combined, is_quarterly)

    df_excel = pivot_combined.copy()

    unique_id = str(uuid.uuid4())
    st.download_button(
        label="Download em Excel",
        data=to_excel(df_excel),
        file_name="dados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"download_button_{unique_id}"
    )

def create_pivot_table(df, x_field, is_quarterly):

    if is_quarterly:
        x_field_pivot = 'Trimestre'
    else:
        x_field_pivot = 'Ano-Mês-Dia'

    pivot = pd.pivot_table(
        df,
        values='Valor',
        index=[x_field],
        columns=[x_field_pivot],
        aggfunc='sum',
        fill_value=0
    )
    if not is_quarterly:
        ordered_columns = sorted(df['Ano-Mês-Dia'].unique())
        pivot = pivot[ordered_columns]
        pivot.columns = df['Mês/Ano'].unique()
    return pivot

def create_combined_pivot(pivot, is_quarterly, group_1, group_2, description_1, description_2):
    
    if st.session_state.is_percent:
        pivot_percent = calculate_percentages(pivot, is_quarterly)
        pivot_combined = combine_pivot_and_percent(pivot, pivot_percent)
    else:
        pivot_combined = pivot.copy()
    
    pivot_combined = add_totals(pivot_combined,group_1,group_2,description_1,description_2)
    return pivot_combined

def calculate_percentages(pivot, is_quarterly):
    pivot_percent = pivot.copy()
    for col in pivot.columns:
        if is_quarterly:
            first_row_value = st.session_state.total_grupo_1_trimestre[col]
        else:
            first_row_value = st.session_state.total_grupo_1_ymd[col]   
        pivot_percent[col] = pivot[col] / first_row_value * 100 if first_row_value != 0 else 0
    return pivot_percent

def combine_pivot_and_percent(pivot, pivot_percent):
    pivot_combined = pd.DataFrame()
    for col in pivot.columns:
        pivot_combined[f'{col}'] = pivot[col]
        pivot_combined[f'{col} %'] = pivot_percent[col]
    new_order = [item for pair in zip(pivot.columns, [f'{col} %' for col in pivot.columns]) for item in pair]
    return pivot_combined[new_order]

def add_totals(pivot_combined,group_1=None,group_2=None,description_1=None,description_2=None):

    if group_1 is not None and description_1 is not None:
        grupo_1_total = pivot_combined.loc[group_1].sum()
        grupo_1_total.name = description_1

    if group_2 is not None and description_2 is not None:
        grupo_2_total = pivot_combined.loc[group_2].sum()
        grupo_2_total.name = description_2
    

    if group_1 is not None and group_2 is not None:
        pivot_combined = pd.concat([
            pivot_combined.loc[group_1],
            pd.DataFrame([grupo_1_total]),
            pivot_combined.loc[group_2],
            pd.DataFrame([grupo_2_total]),
            pivot_combined.drop(group_1 + group_2)
        ])
    elif group_1 is not None:
        pivot_combined = pd.concat([
            pivot_combined.loc[group_1],
            pd.DataFrame([grupo_1_total]),
            pivot_combined.drop(group_1)
        ])
    elif group_2 is not None:
        pivot_combined = pd.concat([
            pivot_combined.loc[group_2],
            pd.DataFrame([grupo_2_total]),
            pivot_combined.drop(group_2)
        ])

    total_geral = pivot_combined.sum()
    total_geral.name = 'Total Geral'
    pivot_combined = pd.concat([pivot_combined, pd.DataFrame([total_geral])])
    
    pivot_combined['Total por Linha'] = pivot_combined[[col for col in pivot_combined.columns if "%" not in col]].sum(axis=1)
    
    return pivot_combined

def display_pivot_table(pivot_combined):
    column_configs = {
        col: st.column_config.NumberColumn(
            label=col,
            format="%.2f%%"
        )
        for col in pivot_combined.columns if "%" in col
    }
    st.dataframe(
        pivot_combined,
        column_config=column_configs,
        use_container_width=True
    )

def display_percentage_chart(pivot_combined, is_quarterly):
    percent_columns = [col for col in pivot_combined.columns if '%' in col]
    df_percentual = pivot_combined[percent_columns].transpose()

    title = 'Evolução Percentual / ' + ('Trimestre' if is_quarterly else 'Mês')
    labels = {'value': 'Percentual (%)', 'index': 'Trimestres' if is_quarterly else 'Meses'}

    fig = px.line(
        df_percentual, 
        title=title,
        labels=labels
    )
    st.plotly_chart(fig, use_container_width=True)

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    df = df.reset_index()
    
    # Escreve o DataFrame no Excel
    df.to_excel(writer, sheet_name='Dados', index=False)
    
    # Obtém o workbook e worksheet do XlsxWriter para formatação
    workbook = writer.book
    worksheet = writer.sheets['Dados']

    # Formatação das células (opcional, mas recomendada para visualização)
    format1 = workbook.add_format({'bg_color': '#CCCCCC'})
    format2 = workbook.add_format({'bg_color': '#FFFFFF'})

    # Alterna as cores das linhas (se necessário)
    for i, row in enumerate(df.index):
        if i % 2 == 0:
            worksheet.set_row(i + 1, None, format1)
        else:
            worksheet.set_row(i + 1, None, format2)

    # Formata a primeira linha como negrito
    worksheet.set_row(0, None, workbook.add_format({'bold': True}))

    writer.close()
    processed_data = output.getvalue()
    return processed_data




```
### views/login.py
```python
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
```
### views/__pycache__/login.cpython-312.pyc
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xcb in position 0: invalid continuation byte
### views/__pycache__/config.cpython-312.pyc
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xcb in position 0: invalid continuation byte
### views/__pycache__/overview.cpython-312.pyc
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xcb in position 0: invalid continuation byte
### views/__pycache__/version.cpython-312.pyc
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xcb in position 0: invalid continuation byte
### scripts/update_environment.py
```python
import os
import subprocess
import sys
import pkg_resources
from pkg_resources import parse_version
import datetime

def get_latest_version(package_name):
    try:
        latest_version = subprocess.check_output([sys.executable, '-m', 'pip', 'install', f'{package_name}==random'], stderr=subprocess.STDOUT)
        latest_version = latest_version.decode('utf-8')
        latest_version = latest_version.split('(from versions:')[1].split(')')[0].strip().split(',')[-1].strip()
        return latest_version
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8')
        if "Could not find a version that satisfies the requirement" in output:
            versions = output.split('(from versions:')[1].split(')')[0].strip().split(',')
            return versions[-1].strip()
    return None

def update_requirements():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    requirements_path = os.path.join(project_root, 'requirements.txt')
    log_dir = os.path.join(project_root, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f'update_log_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')

    updated_requirements = []
    updates = []

    with open(requirements_path, 'r') as file:
        requirements = file.readlines()

    for req in requirements:
        package_name = req.strip().split('==')[0]
        current_version = req.strip().split('==')[1] if '==' in req else None
        latest_version = get_latest_version(package_name)

        if latest_version and (not current_version or parse_version(latest_version) > parse_version(current_version)):
            updated_requirements.append(f'{package_name}=={latest_version}\n')
            updates.append(f'Updated {package_name}: {current_version or "Not specified"} -> {latest_version}')
        else:
            updated_requirements.append(req)

    with open(requirements_path, 'w') as file:
        file.writelines(updated_requirements)

    with open(log_path, 'w') as log_file:
        log_file.write(f'Update performed on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        if updates:
            log_file.write('\n'.join(updates))
        else:
            log_file.write('No updates were necessary. All packages are up to date.')

    print(f'Requirements updated. Log file created at {log_path}')

if __name__ == '__main__':
    update_requirements()
```
### scripts/setup_environment.py
```python
import os
import subprocess
import sys
import venv

# Obtém o caminho do diretório raiz do projeto
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_venv():
    venv_path = os.path.join(ROOT_DIR, "venv")
    if not os.path.exists(venv_path):
        print("Criando o ambiente virtual...")
        venv.create(venv_path, with_pip=True)
        print("Ambiente virtual criado com sucesso.")
    return venv_path


def get_venv_python(venv_path):
    if os.name == "nt":  # Windows
        return os.path.join(venv_path, "Scripts", "python.exe")
    else:  # macOS/Linux
        return os.path.join(venv_path, "bin", "python")


def install_requirements(venv_python):
    requirements_path = os.path.join(ROOT_DIR, "requirements.txt")
    if os.path.exists(requirements_path):
        print("Instalando pacotes do requirements.txt...")
        subprocess.run([venv_python, "-m", "pip", "install", "-r", requirements_path])
        print("Instalação dos pacotes concluída.")
    else:
        print("Arquivo requirements.txt não encontrado.")


def install_odbc_driver():
    if os.name == "nt":
        print(
            "Você está no Windows. Certifique-se de ter o driver ODBC instalado manualmente."
        )
        return

    if sys.platform == "darwin":
        print("Instalando o driver ODBC no macOS...")
        subprocess.run(["brew", "install", "unixodbc"])
    elif sys.platform == "linux":
        print("Instalando o driver ODBC no Linux...")
        subprocess.run(["sudo", "apt-get", "install", "unixodbc", "unixodbc-dev"])


def check_and_install_odbc_driver():
    try:
        output = subprocess.run(["odbcinst", "-j"], capture_output=True, text=True)
        print(output.stdout)
    except FileNotFoundError:
        print("odbcinst não encontrado, instalando driver ODBC...")
        install_odbc_driver()


def start_streamlit(venv_python):
    print("Iniciando o dashboard I9 Smart PDV com Streamlit...")
    streamlit_path = os.path.join(ROOT_DIR, "main.py")
    subprocess.run([venv_python, "-m", "streamlit", "run", streamlit_path])


if __name__ == "__main__":
    os.chdir(ROOT_DIR)  # Muda o diretório de trabalho para a raiz do projeto

    venv_path = create_venv()
    venv_python = get_venv_python(venv_path)

    install_requirements(venv_python)
    # check_and_install_odbc_driver()

    print("Configuração do ambiente concluída.")
    print(f"Para ativar o ambiente virtual, use:")
    if os.name == "nt":
        print(f"    {os.path.join(venv_path, 'Scripts', 'activate')}")
    else:
        print(f"    source {os.path.join(venv_path, 'bin', 'activate')}")
    print(
        "Para iniciar o dashboard, execute 'streamlit run main.py' na raiz do projeto."
    )

    # Descomente a linha abaixo se quiser iniciar o Streamlit automaticamente
    # start_streamlit(venv_python)

```
### scripts/generate_project_structure.py
```python
import os
import shutil

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def create_file(path, content):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

def generate_project_structure():
    # Define the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Create directories
    directories = [
        'assets',
        'components',
        'config',
        'data',
        'utils',
        'views',
    ]
    for directory in directories:
        create_directory(os.path.join(project_root, directory))

    # Create files with content
    files_content = {
        'main.py': '''
import streamlit as st
from components.sidebar import create_sidebar
from views.overview import show_overview
from data.data_loader import load_data
from config.settings import set_page_config

def main():
    set_page_config()
    df = load_data()
    
    page = create_sidebar(df)
    
    if page == "Visão Geral":
        show_overview(df)
    else:
        st.write("Página em desenvolvimento")

if __name__ == "__main__":
    main()
''',
        'components/sidebar.py': '''
import streamlit as st

def create_sidebar(df):
    st.sidebar.title("Menu")
    page = st.sidebar.selectbox("Escolha uma página", ["Visão Geral"])

    # Filtros
    trimestre = sorted(df['Trimestre'].unique())
    meses_anos = sorted(df['Mês/Ano'].unique())
    grupos = sorted(df['Descrição Grupo'].unique())
    subgrupos = sorted(df['Descrição SubGrupo'].unique())
    categorias = sorted(df['Descrição Categoria'].unique())

    trimestre_selecionado = st.sidebar.multiselect('Selecione o(s) Trimestre(es)', trimestre, default=trimestre)
    mes_ano_selecionado = st.sidebar.multiselect('Selecione o(s) Mês(es)/Ano(s)', meses_anos, default=meses_anos)
    grupo_selecionado = st.sidebar.multiselect('Selecione o(s) Grupo(s)', grupos, default=grupos)
    subgrupo_selecionado = st.sidebar.multiselect('Selecione o(s) Subgrupo(s)', subgrupos, default=subgrupos)
    categoria_selecionada = st.sidebar.multiselect('Selecione a(s) Categoria(s)', categorias, default=categorias)

    return page, trimestre_selecionado, mes_ano_selecionado, grupo_selecionado, subgrupo_selecionado, categoria_selecionada
''',
        'data/data_loader.py': '''
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('/Users/leechardes/Python/dashboard/heraclito/dre_process.csv',
                         sep=';',
                         encoding='utf-8',
                         quotechar='"',
                         escapechar='\\',
                         on_bad_lines='warn')
        
        # Converter a coluna 'Valor' para numérico, tratando erros
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {str(e)}")
        return pd.DataFrame()
''',
        'config/settings.py': '''
import streamlit as st
import locale

def set_page_config():
    st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
    locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
''',
        'utils/helpers.py': '''
import locale

def format_real(value):
    return locale.currency(value, grouping=True, symbol=None)
''',
        'views/overview.py': '''
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import format_real

def show_overview(df):
    st.title("Dashboard Financeiro - Visão Geral")

    # Métricas principais
    col1, col2, col3 = st.columns(3)
    total_geral = df['Valor'].sum()
    total_receitas = df[df['Valor'] > 0]['Valor'].sum()
    total_despesas = df[df['Valor'] < 0]['Valor'].sum()

    col1.metric("Total Geral", format_real(total_geral))
    col2.metric("Total de Receitas", format_real(total_receitas))
    col3.metric("Total de Despesas", format_real(total_despesas))

    # Gráfico de barras por grupo
    fig_bar = px.bar(
        df.groupby('Descrição Grupo')['Valor'].sum().reset_index(),
        x='Descrição Grupo',
        y='Valor',
        title='Valores por Grupo',
        labels={'Valor': 'Valor Total', 'Descrição Grupo': 'Grupo'},
        color='Valor',
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Gráfico de linha temporal
    df_time = df.groupby(['Ano-Mês-Dia', 'Descrição Grupo'])['Valor'].sum().reset_index()
    fig_line = px.line(
        df_time,
        x='Ano-Mês-Dia',
        y='Valor',
        color='Descrição Grupo',
        title='Evolução Temporal por Grupo (Mês/Ano)',
        labels={'Valor': 'Valor Total', 'Ano-Mês-Dia': 'Período'}
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # ... (resto do código para a visão geral)
''',
        'assets/styles.css': '''
/* Adicione seus estilos personalizados aqui */
body {
    font-family: Arial, sans-serif;
}
''',
    }

    for file_path, content in files_content.items():
        create_file(os.path.join(project_root, file_path), content.strip())

    # Create an empty logo.png file
    open(os.path.join(project_root, 'assets', 'logo.png'), 'w').close()

    print("Estrutura do projeto gerada com sucesso!")

if __name__ == "__main__":
    generate_project_structure()
```
### scripts/generate_documentation.py
```python
import os
import json
from datetime import datetime


# Função para carregar o arquivo de configuração
def load_config(config_path="scripts/config/generate_documentation.json"):
    with open(config_path, "r") as config_file:
        return json.load(config_file)


# Função para mapear extensões para linguagens
def detect_language(file_name):
    extension_mapping = {
        ".py": "python",
        ".json": "json",
        ".html": "html",
        ".js": "javascript",
        ".css": "css",
        ".md": "markdown",
        ".sh": "bash",
        ".yml": "yaml",
        ".yaml": "yaml",
    }
    ext = os.path.splitext(file_name)[1]  # Obter a extensão do arquivo
    return extension_mapping.get(
        ext, ""
    )  # Retornar a linguagem correspondente ou vazio se não mapeado


# Função para gerar a estrutura do projeto, considerando as configurações e identificando o último item
def generate_file_structure(
    startpath, folders_to_check, ignore_dirs, extensions_to_ignore, ignore_files_root
):
    content = "## Estrutura do Projeto\n\n```\n"

    # Processar arquivos na raiz
    root_dirs = []
    root_files = []

    for item in os.listdir(startpath):
        if item in ignore_files_root or item in ignore_dirs or item.startswith("."):
            continue
        if os.path.isdir(os.path.join(startpath, item)):
            root_dirs.append(item)
        else:
            root_files.append(item)

    # Escrever a raiz do projeto
    content += f"{os.path.basename(startpath)}/\n"

    # Processar diretórios e arquivos na raiz do projeto
    for i, item in enumerate(root_dirs + root_files):
        is_last = i == len(root_dirs) + len(root_files) - 1
        if is_last:
            content += f"└── {item}"
        else:
            content += f"├── {item}"

        if item in root_dirs:
            content += "/\n"
            content += generate_subtree(
                startpath, item, ignore_dirs, extensions_to_ignore, 1, is_last
            )
        else:
            content += "\n"

    content += "```\n"
    return content


# Função para gerar a árvore de subdiretórios e arquivos
def generate_subtree(
    startpath, directory, ignore_dirs, extensions_to_ignore, level, is_last_parent
):
    path = os.path.join(startpath, directory)
    items = os.listdir(path)
    items = [
        item for item in items if item not in ignore_dirs and not item.startswith(".")
    ]
    dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
    files = [
        item
        for item in items
        if os.path.isfile(os.path.join(path, item))
        and not any(item.endswith(ext) for ext in extensions_to_ignore)
    ]

    subtree_content = ""

    for i, item in enumerate(dirs + files):
        is_last = i == len(dirs) + len(files) - 1
        if is_last_parent:
            indent = "    " * (level - 1) + "    "
        else:
            indent = "│   " * level

        if is_last:
            subtree_content += f"{indent}└── {item}"
        else:
            subtree_content += f"{indent}├── {item}"

        if item in dirs:
            subtree_content += "/\n"
            subtree_content += generate_subtree(
                path,
                item,
                ignore_dirs,
                extensions_to_ignore,
                level + 1,
                is_last and is_last_parent,
            )
        else:
            subtree_content += "\n"

    return subtree_content


# Função para gerar o arquivo .md com a data e hora atual no nome
def generate_md_file(content, output_dir="docs"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    file_name = f"documentation_{timestamp}.md"
    file_path = os.path.join(output_dir, file_name)

    with open(file_path, "w") as md_file:
        md_file.write(content)

    print(f"Arquivo de documentação gerado: {file_path}")


# Função para obter o conteúdo dos arquivos
def get_file_content(files):
    content = "## Conteúdo dos Arquivos\n\n"
    for file in files:
        language = detect_language(file)  # Detectar a linguagem com base na extensão
        content += f"### {file}\n"
        try:
            with open(file, "r") as f:
                file_content = f.read()
                if language:
                    content += f"```{language}\n{file_content}\n```\n"
                else:
                    content += f"```\n{file_content}\n```\n"
        except Exception as e:
            content += f"Erro ao ler o arquivo: {e}\n"
    return content


# Aqui começa a unificação dos três scripts
def execute_scripts(config):
    folders_to_check = config["folders_to_check"]
    ignore_dirs = config.get("ignore_dirs", [])
    extensions_to_ignore = config.get("extensions_to_ignore", [".md"])
    ignore_files_root = config.get("ignore_files_root", [])

    content = "# Documentação Unificada\n\n"

    # Gerar estrutura dos arquivos e pastas, começando da raiz
    content += generate_file_structure(
        ".", folders_to_check, ignore_dirs, extensions_to_ignore, ignore_files_root
    )

    # Obter os arquivos a serem processados
    files_to_process = get_files_to_process(
        folders_to_check, extensions_to_ignore, ignore_files_root
    )  # Ignorar as extensões configuradas
    content += get_file_content(files_to_process)

    return content


# Função para verificar arquivos ignorando as extensões definidas
def get_files_to_process(folders_to_check, extensions_to_ignore, ignore_files_root):
    files_to_process = []

    # Processar os arquivos na raiz do projeto
    for file in os.listdir("."):
        if (
            os.path.isfile(file)
            and file not in ignore_files_root
            and not any(file.endswith(ext) for ext in extensions_to_ignore)
        ):
            files_to_process.append(os.path.join(".", file))

    # Processar as pastas configuradas
    for folder in folders_to_check:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if not any(file.endswith(ext) for ext in extensions_to_ignore):
                    files_to_process.append(os.path.join(root, file))
    return files_to_process


# Função principal
def main():
    # Carregar as configurações
    config = load_config()

    # Executar os scripts e obter o conteúdo
    md_content = execute_scripts(config)

    # Gerar o arquivo de documentação
    generate_md_file(md_content)


if __name__ == "__main__":
    main()

```
### scripts/config/generate_documentation.json
```json
{
    "folders_to_check": [
        "assets",
        "components",
        "config",
        "utils",
        "views",
        "scripts"
    ],
    "ignore_dirs": [
        ".git",
        "venv",
        "__pycache__"
    ],
    "extensions_to_ignore": [
        ".md",
        ".log"
    ],
    "ignore_files_root": [
        "README.md",
        "LICENSE"
    ]
}

```
