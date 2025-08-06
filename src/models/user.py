import hashlib
from src.database.connection import get_db_connection


class User:
    def __init__(self, id=None, name=None, email=None, password=None, is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    @staticmethod
    def create(name, email, password, is_admin=False):
        """Cria um novo usuário"""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            # Converter is_admin para inteiro (0 ou 1) para SQLite
            is_admin_int = 1 if is_admin else 0

            cursor = conn.execute('''
                INSERT INTO users (name, email, password, is_admin)
                VALUES (?, ?, ?, ?)
            ''', (name, email, hashed_password, is_admin_int))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def authenticate(email, password):
        """Autentica um usuário"""
        conn = get_db_connection()
        if not conn:
            print("DEBUG: Falha ao conectar com o banco de dados")
            return None

        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            print(f"DEBUG: Tentativa de autenticação para email: {email}")

            cursor = conn.execute('''
                SELECT id, name, email, is_admin FROM users 
                WHERE email = ? AND password = ?
            ''', (email, hashed_password))

            user_data = cursor.fetchone()
            print(f"DEBUG: Dados do usuário encontrados: {user_data}")

            if user_data:
                # Tratar o campo is_admin corretamente (SQLite retorna 0/1)
                is_admin = bool(
                    user_data['is_admin']) if user_data['is_admin'] is not None else False
                print(f"DEBUG: is_admin tratado: {is_admin}")

                user = User(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    is_admin=is_admin
                )
                print(
                    f"DEBUG: Usuário criado: {user.name} (admin: {user.is_admin})")
                return user
            else:
                print("DEBUG: Nenhum usuário encontrado com essas credenciais")
            return None
        except Exception as e:
            print(f"Erro ao autenticar usuário: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_email(email):
        """Busca usuário por email"""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.execute('''
                SELECT id, name, email, is_admin FROM users 
                WHERE email = ?
            ''', (email,))

            user_data = cursor.fetchone()
            if user_data:
                # Tratar o campo is_admin corretamente (SQLite retorna 0/1)
                is_admin = bool(
                    user_data['is_admin']) if user_data['is_admin'] is not None else False

                return User(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    is_admin=is_admin
                )
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def email_exists(email):
        """Verifica se um email já existe"""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.execute(
                'SELECT id FROM users WHERE email = ?', (email,))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Erro ao verificar email: {e}")
            return False
        finally:
            conn.close()
