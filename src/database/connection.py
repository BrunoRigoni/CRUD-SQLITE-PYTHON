import sqlite3
import os

DATABASE = 'database.db'


def get_db_connection():
    """Estabelece conexão com o banco de dados SQLite"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Erro ao conectar com banco: {e}")
        return None


def init_db():
    """Inicializa o banco de dados criando as tabelas necessárias"""
    conn = get_db_connection()
    if not conn:
        print("Não foi possível conectar ao banco de dados")
        return

    try:
        # Tabela de usuários
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela de produtos
        conn.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL,
                categoria TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_email TEXT NOT NULL,
                image_path TEXT,
                FOREIGN KEY (usuario_email) REFERENCES users (email)
            )
        ''')

        # Tabela de clientes
        conn.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT,
                telefone TEXT,
                endereco TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_email TEXT NOT NULL,
                FOREIGN KEY (usuario_email) REFERENCES users (email)
            )
        ''')

        # Tabela de vendas
        conn.execute('''
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
                FOREIGN KEY (produto_id) REFERENCES produtos (id),
                FOREIGN KEY (usuario_email) REFERENCES users (email)
            )
        ''')

        conn.commit()
        print("Banco de dados inicializado com sucesso!")

    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")
    finally:
        conn.close()
