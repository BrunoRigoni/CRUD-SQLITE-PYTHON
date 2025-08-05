import sqlite3
import os
from datetime import datetime


class ProdutosDB:
    """Classe para gerenciar o banco de dados de produtos por usuário"""
    
    def __init__(self, user_email):
        """Inicializa o banco de dados para um usuário específico"""
        self.user_email = user_email
        self.db_name = f"produtos_{user_email.replace('@', '_').replace('.', '_')}.db"
        self.connect = sqlite3.connect(self.db_name)
        self.create_tables()
    
    def create_tables(self):
        """Cria as tabelas necessárias para o usuário"""
        # Tabela de produtos do usuário
        self.connect.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL,
                categoria TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_email TEXT NOT NULL
            )
        ''')
        
        # Tabela de clientes do usuário
        self.connect.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT,
                telefone TEXT,
                endereco TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_email TEXT NOT NULL
            )
        ''')
        
        # Tabela de vendas do usuário
        self.connect.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                produto_id INTEGER,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                total REAL NOT NULL,
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_email TEXT NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        ''')
        
        self.connect.commit()
    
    def get_connection(self):
        """Retorna a conexão com o banco de dados"""
        return self.connect
    
    def close_connection(self):
        """Fecha a conexão com o banco de dados"""
        self.connect.close()
    
    def get_user_email(self):
        """Retorna o email do usuário"""
        return self.user_email
    
    def get_db_name(self):
        """Retorna o nome do arquivo do banco de dados"""
        return self.db_name


def create_produtos_db(user_email):
    """Função para criar e retornar uma instância do banco de dados de produtos"""
    return ProdutosDB(user_email)


def list_user_databases():
    """Lista todos os bancos de dados de produtos de usuários"""
    databases = []
    for file in os.listdir('.'):
        if file.startswith('produtos_') and file.endswith('.db'):
            user_email = file.replace('produtos_', '').replace('.db', '').replace('_', '.')
            databases.append({
                'file': file,
                'user_email': user_email
            })
    return databases


def delete_user_database(user_email):
    """Remove o banco de dados de produtos de um usuário"""
    db_name = f"produtos_{user_email.replace('@', '_').replace('.', '_')}.db"
    if os.path.exists(db_name):
        os.remove(db_name)
        return True
    return False 