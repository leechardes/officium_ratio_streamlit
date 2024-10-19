import bcrypt
import json
import os
from pymongo import MongoClient
from config.mongodb_connection import get_db

class UserManager:
    def __init__(self):
        # Obtém a conexão com o banco de dados
        self.db = get_db()
        # Conecta-se à coleção 'users'
        self.users_collection = self.db['users']

        # Verifica se a coleção 'users' está vazia
        if self.users_collection.count_documents({}) == 0:
            print("Nenhum usuário encontrado na coleção. Migrando usuários do arquivo.")
            self.migrate_users_from_file()

    def hash_password(self, password):
        """Gera o hash da senha usando bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, hashed_password, plain_password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

    def migrate_users_from_file(self):
        """Migra os usuários do arquivo JSON para o MongoDB."""
        users_file_path = os.path.join('config', 'users.json')

        if not os.path.exists(users_file_path):
            print(f"Arquivo {users_file_path} não encontrado. Nenhum usuário foi migrado.")
            return

        # Carregar o arquivo JSON
        with open(users_file_path, 'r') as file:
            users = json.load(file)

        # Inserir os usuários no MongoDB, criptografando as senhas
        for user in users:
            user['password'] = self.hash_password(user['password'])  # Criptografa a senha
            self.users_collection.insert_one(user)

        print(f"{len(users)} usuários migrados para o MongoDB.")

    def add_user(self, username, password, nome, grupo):
        """Adiciona um novo usuário ao MongoDB."""
        # Verifica se o usuário já existe
        if self.users_collection.find_one({"username": username}):
            return {"status": "error", "message": "Usuário já existe!"}

        # Criptografa a senha
        hashed_password = self.hash_password(password)

        user = {
            "username": username,
            "password": hashed_password,
            "nome": nome,
            "grupo": grupo
        }

        # Insere o usuário na coleção
        self.users_collection.insert_one(user)
        return {"status": "success", "message": "Usuário adicionado com sucesso!"}

    def get_user(self, username):
        """Obtém um usuário pelo nome de usuário (username)."""
        user = self.users_collection.find_one({"username": username}, {"_id": 0})
        if user:
            return {"status": "success", "user": user}
        return {"status": "error", "message": "Usuário não encontrado!"}

    def authenticate_user(self, username, password):
        """Autentica um usuário verificando sua senha."""
        user = self.users_collection.find_one({"username": username})
        if user and self.check_password(user['password'], password):
            return {"status": "success", "message": "Autenticado com sucesso!"}
        return {"status": "error", "message": "Usuário ou senha incorretos!"}

    def update_user(self, username, **kwargs):
        """Atualiza as informações de um usuário."""
        update_fields = {}
        if "password" in kwargs and kwargs["password"]:
            # Se a senha estiver sendo atualizada, criptografe-a
            update_fields["password"] = self.hash_password(kwargs["password"])

        for key, value in kwargs.items():
            if key != "password" and value:  # Evita criptografar a senha duas vezes
                update_fields[key] = value

        result = self.users_collection.update_one(
            {"username": username},
            {"$set": update_fields}
        )

        if result.modified_count > 0:
            return {"status": "success", "message": "Usuário atualizado com sucesso!"}
        return {"status": "error", "message": "Nenhuma modificação realizada ou usuário não encontrado!"}

    def delete_user(self, username):
        """Deleta um usuário do banco de dados."""
        result = self.users_collection.delete_one({"username": username})
        if result.deleted_count > 0:
            return {"status": "success", "message": "Usuário deletado com sucesso!"}
        return {"status": "error", "message": "Usuário não encontrado!"}

    def list_users(self):
        """Lista todos os usuários na coleção."""
        users = self.users_collection.find({}, {"_id": 0})  # Ignora o campo _id
        return list(users)
