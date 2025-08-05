import sqlite3
import hashlib
import admin_view
import user_view
import config


def create_tables(connect):
    """Cria as tabelas necessárias no banco de dados"""
    # Tabela de usuários
    connect.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela de produtos (centralizada)
    connect.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            categoria TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            usuario_email TEXT NOT NULL,
            FOREIGN KEY (usuario_email) REFERENCES users (email)
        )
    ''')

    # Tabela de clientes (centralizada)
    connect.execute('''
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

    # Tabela de vendas (centralizada)
    connect.execute('''
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

    connect.commit()


def is_admin(connect, email):
    """Verifica se o usuário é administrador"""
    cursor = connect.execute(
        'SELECT is_admin FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    return result and result[0]


def register(connect):
    """Registra um novo usuário"""
    print("\n" + "="*50)
    print("CADASTRO DE USUÁRIO")
    print("="*50)

    name = input("Nome completo: ").strip()
    if not name:
        print("Nome é obrigatório!")
        return

    email = input("Email: ").strip().lower()
    if not email:
        print("Email é obrigatório!")
        return

    # Verificar se o email já existe
    cursor = connect.execute('SELECT id FROM users WHERE email = ?', (email,))
    if cursor.fetchone():
        print("Email já cadastrado!")
        return

    password = input("Senha: ").strip()
    if not password:
        print("Senha é obrigatória!")
        return

    if ' ' in password:
        print("Senha não pode conter espaços!")
        return

    # Hash da senha
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        connect.execute('''
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        ''', (name, email, hashed_password))
        connect.commit()
        print("Usuário cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")


def login(connect):
    """Realiza o login do usuário"""
    print("\n" + "="*50)
    print("LOGIN")
    print("="*50)

    email = input("Email: ").strip().lower()
    if not email:
        print("Email é obrigatório!")
        return

    password = input("Senha: ").strip()
    if not password:
        print("Senha é obrigatória!")
        return

    # Hash da senha
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Verificar credenciais
    cursor = connect.execute('''
        SELECT id, name, email, password FROM users 
        WHERE email = ? AND password = ?
    ''', (email, hashed_password))

    user = cursor.fetchone()

    if user:
        print(config.LOGIN_SUCCESS)
        print(f"Bem-vindo, {user[1]}!")

        if is_admin(connect, email):
            print(config.ADMIN_ACCESS_DETECTED)
            input("Pressione Enter para acessar o painel de administração...")
            admin_view.admin_panel(connect)
        else:
            print(config.USER_ACCESS)
            input("Pressione Enter para acessar o painel de usuário...")
            # Passa nome e email do usuário
            user_view.user_panel(connect, user[1], email)
    else:
        print("Email ou senha incorretos!")
        print("Verifique se digitou as credenciais corretamente.")


def main():
    """Função principal"""
    print(config.WELCOME_MESSAGE)

    # Conectar ao banco de dados
    connect = sqlite3.connect('database.db')

    # Criar tabelas
    create_tables(connect)

    while True:
        try:
            print("\n" + "="*50)
            print("SISTEMA DE GERENCIAMENTO")
            print("="*50)
            print("1. Login")
            print("2. Cadastro")
            print("3. Sair")
            print("-"*50)

            option = int(input("Digite a opção desejada: "))

            if option == 1:
                login(connect)
            elif option == 2:
                register(connect)
            elif option == 3:
                print("Saindo do sistema...")
                connect.close()
                break
            else:
                print("Opção inválida! Digite 1, 2 ou 3.")

        except ValueError:
            print("Erro: Digite apenas números para as opções!")
        except Exception as e:
            print(f"Erro inesperado: {e}")
            input('Digite enter para continuar...')


if __name__ == "__main__":
    main()
