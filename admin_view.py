import hashlib
import sqlite3


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


def change_user_password(connect):
    """Altera a senha de um usuário"""
    print("ALTERAR SENHA DE USUÁRIO")
    email = input("Digite o email do usuário: ").strip()

    if not email:
        print("Email é obrigatório!")
        return

    # Verificar se o usuário existe
    cursor = connect.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()

    if not user:
        print("Usuário não encontrado!")
        return

    new_password = input("Digite a nova senha: ").strip()

    if not new_password:
        print("Nova senha é obrigatória!")
        return
    elif len(new_password) < 8:
        print("Senha deve ter pelo menos 8 caracteres!")
        return
    elif " " in new_password:
        print("Senha não pode conter espaços!")
        return

    # Hash da nova senha
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

    connect.execute(
        'UPDATE users SET password = ? WHERE email = ?', (hashed_password, email))
    connect.commit()
    print("Senha alterada com sucesso!")


def create_user(connect):
    """Cria um novo usuário"""
    print("CADASTRO DE USUÁRIO")
    name = input("Digite o nome do usuário: ").strip()
    email = input("Digite o email do usuário: ").strip()
    password = input("Digite a senha do usuário: ").strip()
    security_question = input(
        "Digite a pergunta de segurança do usuário: ").strip()

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

    # Hash da senha
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    connect.execute('INSERT INTO users (name, email, password, security_question) VALUES (?, ?, ?, ?)',
                    (name, email, hashed_password, security_question))
    connect.commit()
    print("Usuário cadastrado com sucesso!")


def delete_user(connect):
    """Remove um usuário"""
    print("REMOVER USUÁRIO")
    email = input("Digite o email do usuário a ser removido: ").strip()

    if not email:
        print("Email é obrigatório!")
        return

    # Verificar se o usuário existe
    cursor = connect.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()

    if not user:
        print("Usuário não encontrado!")
        return

    confirm = input(
        f"Tem certeza que deseja remover o usuário {user[1]} ({email})? (s/n): ").strip().lower()

    if confirm == 's' or confirm == 'sim':
        connect.execute('DELETE FROM users WHERE email = ?', (email,))
        connect.commit()
        print("Usuário removido com sucesso!")
    else:
        print("Operação cancelada.")


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


def admin_panel(connect):
    """Painel principal de administração"""
    option = 0

    while option != 6:
        try:
            print("\n" + "="*50)
            print("PAINEL DE ADMINISTRAÇÃO")
            print("="*50)
            print("1. Listar usuários")
            print("2. Alterar senha de usuário")
            print("3. Cadastrar novo usuário")
            print("4. Remover usuário")
            print("5. Adicionar usuário à white list")
            print("6. Voltar ao menu principal")
            print("-"*50)

            option = int(input("Digite a opção desejada: "))

            if option == 1:
                list_users(connect)
                input('Digite enter para voltar ao menu')

            elif option == 2:
                change_user_password(connect)
                input('Digite enter para voltar ao menu')

            elif option == 3:
                create_user(connect)
                input('Digite enter para voltar ao menu')

            elif option == 4:
                delete_user(connect)
                input('Digite enter para voltar ao menu')

            elif option == 5:
                add_to_white_list(connect)
                input('Digite enter para voltar ao menu')

            elif option == 6:
                print("Retornando ao menu principal...")
                break

            else:
                print("Opção inválida! Digite 1, 2, 3, 4, 5 ou 6.")

        except ValueError:
            print("Erro: Digite apenas números para as opções!")
        except Exception as e:
            print(f"Erro inesperado: {e}")
            input('Digite enter para continuar...')
