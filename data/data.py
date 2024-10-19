from pymongo import MongoClient
from config.mongodb_connection import get_db
import pandas as pd

class DataManager:
    def __init__(self):
        # Conecta ao banco de dados e à coleção 'data'
        self.db = get_db()
        self.collection = self.db['data']

    def insert_group_data(self, group_data, company):
        """Insere os dados de um grupo de empresa no MongoDB, incluindo o identificador da empresa."""
        # Adiciona o identificador da empresa a cada documento
        for data in group_data:
            data['company'] = company

        # Insere os dados no MongoDB
        result = self.collection.insert_many(group_data)
        return {"status": "success", "inserted_ids": result.inserted_ids}

    def get_group_data(self, group_code, company):
        """Recupera os dados de um grupo de empresa pelo código do grupo e empresa."""
        return list(self.collection.find({"group_code": group_code, "company": company}))
    
    def get_company_data(self, company):
        """Recupera os dados de um grupo de empresa pelo código do grupo e empresa."""
        return list(self.collection.find({"company": company}))

    def get_all_groups(self):
        """Retorna todos os grupos de empresas armazenados."""
        return list(self.collection.find())

    def update_group_data(self, group_code, updated_data, company):
        """Atualiza os dados de um grupo de empresa, usando o código do grupo e o identificador da empresa."""
        result = self.collection.update_many({"group_code": group_code, "company": company}, {"$set": updated_data})
        if result.modified_count > 0:
            return {"status": "success", "modified_count": result.modified_count}
        return {"status": "error", "message": "Nenhum dado atualizado"}

    def delete_group_data(self, group_code, company):
        """Deleta os dados de um grupo de empresa pelo código e identificador da empresa."""
        result = self.collection.delete_many({"group_code": group_code, "company": company})
        if result.deleted_count > 0:
            return {"status": "success", "deleted_count": result.deleted_count}
        return {"status": "error", "message": "Nenhum dado encontrado para deletar"}
    
    def delete_company_data(self, company):
        """Deleta os dados de um grupo de empresa pelo código e identificador da empresa."""
        result = self.collection.delete_many({"company": company})
        if result.deleted_count > 0:
            return {"status": "success", "deleted_count": result.deleted_count}
        return {"status": "error", "message": "Nenhum dado encontrado para deletar"}
    
    def get_company_dataframe(self, company):
        """Retorna um DataFrame com os dados da empresa e nomes de colunas específicos."""
        # Recuperar os dados da empresa
        company_data = self.get_company_data(company)
        
        if not company_data:
            print(f"Nenhum dado encontrado para a empresa: {company}")
            return pd.DataFrame()  # Retorna um DataFrame vazio se não houver dados
        
        # Converte os dados em um DataFrame
        df = pd.DataFrame(company_data)
     
        # Renomeia as colunas
        df = df.rename(columns={
            '_id': '_id',
            'group_code': 'Código Grupo',
            'group_description': 'Descrição Grupo',
            'subgroup_code': 'Código SubGrupo',
            'subgroup_description': 'Descrição SubGrupo',
            'sequence_group': 'Sequência Grupo',
            'category_description': 'Descrição Categoria',
            'month_year': 'Mês/Ano',
            'date': 'Ano-Mês-Dia',
            'value': 'Valor',
            'quarter': 'Trimestre',
            'company': 'company'
        })

        # Remove as colunas '_id' e 'company' se não forem necessárias
        df.drop(columns=['_id', 'company'], inplace=True)

        return df
