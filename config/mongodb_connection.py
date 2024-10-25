import os
from pymongo import MongoClient
import json

def initialize_mongodb():
    # Define o caminho para o arquivo de configuração dentro da pasta config
    config_path = os.path.join('config', 'mongodb_config.json')
    
    # Lê as configurações do arquivo
    with open(config_path) as config_file:
        config = json.load(config_file)
    
    # Extrai as informações de conexão do arquivo de configuração
    username = config['username']
    password = config['password']
    host = config['host']
    database_name = config['database']
    port = config['port'] 
    auth_source = config['auth_source']

    # Monta a URI de conexão
    mongo_uri = f"mongodb://{username}:{password}@{host}:{port}?authSource={auth_source}"
    
    client = MongoClient(mongo_uri) 

    # Testa a conexão
    try:

        dbs = client.list_database_names()
        print("Conexão com MongoDB estabelecida!")
        print("Bancos de dados disponíveis:", dbs)
        # Ping the database to check the connection
        client.admin.command('ping')
        print("Conexão com MongoDB estabelecida com sucesso!")
        return client[database_name]
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return None

# Função para obter a conexão com o banco de dados
def get_db():
    db = initialize_mongodb()
    if db is not None:
        return db
    else:
        raise ConnectionError("Falha ao conectar ao MongoDB")