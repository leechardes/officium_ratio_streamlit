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

def process_csv(input_file, company, manager):
    group_data = []  # Armazena todos os dados do grupo antes de inserir no MongoDB
    months = []  # Armazena os meses capturados da coluna da linha 1
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

                    # Preparar os dados para inserção no MongoDB
                    group_data.append({
                        "group_code": group,
                        "group_description": group_description, 
                        "subgroup_code": subgroup if subgroup else '',
                        "subgroup_description": subgroup_description, 
                        "sequence_group": sequence, 
                        "category_description": item, 
                        "month_year": month, 
                        "date": formatted_month, 
                        "value": value, 
                        "quarter": trimestre
                    })

    # Inserir todos os dados no MongoDB
    manager.insert_group_data(group_data, company)
