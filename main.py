import sqlite3
import hashlib
import admin_view
import config


def create_white_list_table(connect):
    """Cria a tabela white_list se não existir"""
    connect.execute(
        'CREATE TABLE IF NOT EXISTS white_list (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE)')
    connect.commit()


def create_master_admin(connect):
    """Cria o admin mestre padrão se não existir"""
    master_email = config.MASTER_ADMIN_EMAIL
    master_password = config.MASTER_ADMIN_PASSWORD
    master_name = config.MASTER_ADMIN_NAME
    master_security = config.MASTER_ADMIN_SECURITY_QUESTION

    # Verificar se o admin mestre já existe
    cursor = connect.execute(
        'SELECT * FROM users WHERE email = ?', (master_email,))
    if cursor.fetchone():
        print("Admin mestre já existe!")
        return

    # Criar admin mestre
    hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
    connect.execute(
        'INSERT INTO users (name, email, password, security_question) VALUES (?, ?, ?, ?)',
        (master_name, master_email, hashed_password, master_security))

    # Adicionar à white list
    try:
        connect.execute(
            'INSERT INTO white_list (email) VALUES (?)', (master_email,))
    except sqlite3.IntegrityError:
        pass  # Já está na white list

    connect.commit()
    print("Admin mestre criado com sucesso!")
    print(f"Email: {master_email}")
    print(f"Senha: {master_password}")


def add_to_white_list(connect):
    """Adiciona um email à white list"""
    print("ADICIONAR À WHITE LIST")
    email = input("Digite o email para adicionar à white list: ").strip()

    if not email:
        print("Email é obrigatório!")
        return

    try:
        connect.execute('INSERT INTO white_list (email) VALUES (?)', (email,))
        connect.commit()
        print(f"Email {email} adicionado à white list com sucesso!")
    except sqlite3.IntegrityError:
        print("Email já está na white list!")


def list_users(connect):
    """Lista todos os usuários cadastrados"""
    print("USUÁRIOS CADASTRADOS:")
    print("-" * 50)
    cursor = connect.execute('SELECT id, name, email FROM users')
    users = cursor.fetchall()

    if not users:
        print("Nenhum usuário cadastrado!")
        return

    for user in users:
        print(f"ID: {user[0]}")
        print(f"Nome: {user[1]}")
        print(f"Email: {user[2]}")
        print("-" * 30)


def is_admin(connect, email):
    """Verifica se o email está na white list (é admin) ou é o admin mestre"""
    # Verificar se é o admin mestre
    if email == config.MASTER_ADMIN_EMAIL:
        return True

    # Verificar se está na white list
    cursor = connect.execute(
        'SELECT * FROM white_list WHERE email = ?', (email,))
    return cursor.fetchone() is not None


def login(connect):
    print("LOGIN")
    email = input("Digite o email: ").strip()
    password = input("Digite a senha: ").strip()

    if not email or not password:
        print("Email e senha são obrigatórios!")
        return

    # Verificar se o email existe primeiro
    cursor = connect.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()

    if not user:
        print("Email não encontrado!")
        return

    # Agora verificar a senha
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    stored_password = user[3]  # password está na posição 3 da tupla

    if hashed_password == stored_password:
        print(config.LOGIN_SUCCESS)
        print(f"Bem-vindo, {user[1]}!")  # nome está na posição 1

        # Verificar se é admin (está na white list)
        if is_admin(connect, email):
            print(config.ADMIN_ACCESS_DETECTED)
            input("Pressione Enter para acessar o painel de administração...")
            admin_view.admin_panel(connect)
        else:
            print(config.USER_ACCESS)
    else:
        print("Senha incorreta!")
        print("Verifique se digitou a senha corretamente.")


def register(connect):
    print("CADASTRAR USUÁRIO")
    name = input("Digite o nome: ").strip()
    email = input("Digite o email: ").strip()
    password = input("Digite a senha: ").strip()
    security_question = input("Qual cidade você nasceu: ").strip()

    if not name or not email or not password:
        print("Nome, email e senha são obrigatórios!")
        return
    elif email.count("@") != 1:
        print("Email inválido!")
        return
    elif len(password) < 8:
        print("Senha deve ter pelo menos 8 caracteres!")
        return
    elif " " in password:
        print("Senha não pode conter espaços!")
        return

    # Verificar se email já existe
    cursor = connect.execute(
        'SELECT email FROM users WHERE email = ?', (email,))
    if cursor.fetchone():
        print("Email já cadastrado!")
        return

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    connect.execute(
        'INSERT INTO users (name, email, password, security_question) VALUES (?, ?, ?, ?)', (name, email, hashed_password, security_question))
    connect.commit()
    print("Usuário cadastrado com sucesso!")


def change_password(connect):
    print("REDEFINIR SENHA")
    email = input("Digite o email: ").strip()

    if not email:
        print("Email é obrigatório!")
        return

    # Verificar se o email existe
    cursor = connect.execute(
        'SELECT security_question FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()

    if not user:
        print("Email não encontrado!")
        return

    security_question = user[0]
    print(f"Pergunta de segurança: Qual cidade você nasceu?")
    answer = input("Digite sua resposta: ").strip()

    if answer.lower() != security_question.lower():
        print("Resposta incorreta!")
        return

    new_password = input("Digite a nova senha: ").strip()

    # Validar nova senha
    if not new_password:
        print("Nova senha é obrigatória!")
        return
    elif len(new_password) < 8:
        print("Senha deve ter pelo menos 8 caracteres!")
        return
    elif " " in new_password:
        print("Senha não pode conter espaços!")
        return

    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    connect.execute(
        'UPDATE users SET password = ? WHERE email = ?', (hashed_password, email))
    connect.commit()
    print("Senha redefinida com sucesso!")


def check_and_fix_table(connect):
    """Verifica se a tabela tem a coluna security_question e adiciona se necessário"""
    try:
        # Verificar se a coluna security_question existe
        cursor = connect.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'security_question' not in columns:
            print("Adicionando coluna security_question à tabela...")
            connect.execute(
                "ALTER TABLE users ADD COLUMN security_question TEXT")
            connect.commit()
            print("Coluna adicionada com sucesso!")
    except Exception as e:
        print(f"Erro ao verificar/corrigir tabela: {e}")


def main():
    connect = sqlite3.connect(config.DATABASE_NAME)
    connect.execute(
        'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, password TEXT, security_question TEXT)')

    # Criar tabela white_list
    create_white_list_table(connect)

    # Verificar e corrigir estrutura da tabela se necessário
    check_and_fix_table(connect)

    # Criar admin mestre se não existir
    create_master_admin(connect)

    options = 0
    while options != 4:
        try:
            print(
                f"{config.WELCOME_MESSAGE}: \n Digite [1] para login \n Digite [2] para cadastro \n Digite [3] para redefinir senha \n Digite [4] Sair")
            options = int(input("Digite a opção desejada: "))

            if options == 1:
                login(connect)
                input('Digite enter para voltar ao menu')

            elif options == 2:
                register(connect)
                input('Digite enter para voltar ao menu')

            elif options == 3:
                change_password(connect)
                input('Digite enter para voltar ao menu')

            elif options == 4:
                print("Saindo do sistema...")
                connect.close()
                input('Digite enter para sair')
            else:
                print("Opção inválida! Digite 1, 2, 3 ou 4.")

        except ValueError:
            print("Erro: Digite apenas números para as opções!")
        except Exception as e:
            print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()
