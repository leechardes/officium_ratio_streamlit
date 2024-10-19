import json
import os
from pymongo import MongoClient
from config.mongodb_connection import get_db
from utils.helpers import format_real

class CategoryManager:
    def __init__(self):
        # Inicializa a conexão com o banco de dados
        self.db = get_db()
        # Coleções para as categorias e categorias excluídas
        self.categories_collection = self.db['categories']
        self.excluded_categories_collection = self.db['excluded_categories']

    def migrate_categories_from_file(self, company):
        """Migra os dados de categorias do arquivo JSON para o MongoDB para uma empresa específica."""
        file_path = os.path.join('config', 'categories.json')
        
        if not os.path.exists(file_path):
            print(f"Arquivo {file_path} não encontrado. Nenhuma migração realizada.")
            return

        if self.categories_collection.count_documents({}) > 0:
            print("Nenhum usuário encontrado na coleção. Migrando usuários do arquivo.")
            return
        
        # Carregar o arquivo JSON
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Migrar as categorias
        categories = data.get("categories", [])
        for category in categories:
            # Inserir cada categoria como um documento separado no MongoDB, associando à empresa
            category['company'] = company
            self.categories_collection.insert_one(category)

        # Migrar as categorias excluídas
        excluded_categories = data.get("excluded_categories", [])
        for excluded in excluded_categories:
            # Inserir cada categoria excluída na coleção apropriada, associando à empresa
            self.excluded_categories_collection.insert_one({"category": excluded, "company": company})

        print(f"Migração concluída para a empresa '{company}': {len(categories)} categorias e {len(excluded_categories)} categorias excluídas.")

    def add_category(self, title, description_category, company):
        """Adiciona uma nova categoria associada a uma empresa."""
        category = {
            "title": title,
            "description_category": description_category,
            "company": company
        }
        self.categories_collection.insert_one(category)
        return {"status": "success", "message": "Categoria adicionada com sucesso!"}

    def get_category(self, title, company):
        """Obtém uma categoria pelo título e empresa."""
        category = self.categories_collection.find_one({"title": title, "company": company}, {"_id": 0})
        if category:
            return {"status": "success", "category": category}
        return {"status": "error", "message": "Categoria não encontrada!"}

    def update_category(self, title, description_category, company):
        """Atualiza a descrição de uma categoria associada a uma empresa."""
        result = self.categories_collection.update_one(
            {"title": title, "company": company},
            {"$set": {"description_category": description_category}}
        )
        if result.modified_count > 0:
            return {"status": "success", "message": "Categoria atualizada com sucesso!"}
        return {"status": "error", "message": "Nenhuma modificação realizada ou categoria não encontrada."}

    def delete_category(self, title, company):
        """Remove uma categoria associada a uma empresa."""
        result = self.categories_collection.delete_one({"title": title, "company": company})
        if result.deleted_count > 0:
            return {"status": "success", "message": "Categoria removida com sucesso!"}
        return {"status": "error", "message": "Categoria não encontrada."}

    def list_categories(self, company):
        """Lista todas as categorias associadas a uma empresa."""
        categories = self.categories_collection.find({"company": company}, {"_id": 0})
        return list(categories)

    def list_excluded_categories(self, company):
        """Lista todas as categorias excluídas associadas a uma empresa."""
        excluded_categories = self.excluded_categories_collection.find({"company": company}, {"_id": 0})
        return [category["category"] for category in excluded_categories]

    def add_excluded_category(self, category_name, company):
        """Adiciona uma categoria à lista de excluídas para uma empresa."""
        if not self.excluded_categories_collection.find_one({"category": category_name, "company": company}):
            self.excluded_categories_collection.insert_one({"category": category_name, "company": company})
            return {"status": "success", "message": "Categoria excluída adicionada com sucesso!"}
        return {"status": "error", "message": "Categoria já está na lista de excluídas!"}

    def remove_excluded_category(self, category_name, company):
        """Remove uma categoria da lista de excluídas para uma empresa."""
        result = self.excluded_categories_collection.delete_many({"category": category_name, "company": company})
        if result.deleted_count > 0:
            return {"status": "success", "message": "Categoria removida da lista de excluídas!"}
        return {"status": "error", "message": "Categoria não encontrada na lista de excluídas!"}
