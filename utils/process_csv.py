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
