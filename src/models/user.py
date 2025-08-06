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
    def create(name, email, password):
        """Cria um novo usuário"""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor = conn.execute('''
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
            ''', (name, email, hashed_password))
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
            return None

        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor = conn.execute('''
                SELECT id, name, email, is_admin FROM users 
                WHERE email = ? AND password = ?
            ''', (email, hashed_password))

            user_data = cursor.fetchone()
            if user_data:
                return User(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    is_admin=user_data['is_admin']
                )
            return None
        except Exception as e:
            print(f"Erro ao autenticar usuário: {e}")
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
                return User(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    is_admin=user_data['is_admin']
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
