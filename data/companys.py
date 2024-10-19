from pymongo import MongoClient
from bson.objectid import ObjectId
from config.mongodb_connection import get_db

class CompanyManager:
    def __init__(self):
        # Conecta ao banco de dados e à coleção 'company'
        self.db = get_db()
        self.collection = self.db['company']

    def add_company(self, company_name):
        """Adiciona uma nova empresa na coleção."""
        if self.collection.find_one({"company": company_name}):
            return {"status": "error", "message": "Empresa já existe!"}

        result = self.collection.insert_one({"company": company_name})
        return {"status": "success", "message": "Empresa adicionada com sucesso!", "company_id": str(result.inserted_id)}

    def get_company_by_id(self, company_id):
        """Recupera uma empresa pelo seu ObjectId."""
        company = self.collection.find_one({"_id": ObjectId(company_id)}, {"_id": 0})
        if company:
            return {"status": "success", "company": company}
        return {"status": "error", "message": "Empresa não encontrada!"}

    def get_company_by_name(self, company_name):
        """Recupera uma empresa pelo seu nome."""
        company = self.collection.find_one({"company": company_name}, {"_id": 1, "company": 1})
        if company:
            return {"status": "success", "company": company}
        return {"status": "error", "message": "Empresa não encontrada!"}

    def update_company(self, company_id, new_company_name):
        """Atualiza o nome de uma empresa pelo seu ObjectId."""
        result = self.collection.update_one(
            {"_id": ObjectId(company_id)},
            {"$set": {"company": new_company_name}}
        )
        if result.modified_count > 0:
            return {"status": "success", "message": "Empresa atualizada com sucesso!"}
        return {"status": "error", "message": "Nenhuma modificação realizada ou empresa não encontrada."}

    def delete_company(self, company_id):
        """Remove uma empresa pelo seu ObjectId."""
        result = self.collection.delete_one({"_id": ObjectId(company_id)})
        if result.deleted_count > 0:
            return {"status": "success", "message": "Empresa removida com sucesso!"}
        return {"status": "error", "message": "Empresa não encontrada."}

    def list_companies(self):
        """Lista todas as empresas."""
        companies = self.collection.find({}, {"_id": 1, "company": 1})
        return list(companies)

