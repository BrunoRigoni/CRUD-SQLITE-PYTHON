from datetime import datetime
from src.database.connection import get_db_connection
from src.utils.file_utils import save_image, delete_image


class Product:
    def __init__(self, id=None, nome=None, preco=None, quantidade=None, categoria=None,
                 data_cadastro=None, usuario_email=None, image_path=None):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.categoria = categoria
        self.data_cadastro = data_cadastro
        self.usuario_email = usuario_email
        self.image_path = image_path

    @staticmethod
    def create(nome, preco, quantidade, categoria, usuario_email, image_file=None):
        """Cria um novo produto"""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            # Salvar imagem se fornecida
            image_path = None
            if image_file:
                image_path = save_image(image_file)
                if not image_path:
                    return None

            cursor = conn.execute('''
                INSERT INTO produtos (nome, preco, quantidade, categoria, usuario_email, image_path, data_cadastro)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nome, preco, quantidade, categoria, usuario_email, image_path, datetime.now()))

            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar produto: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_user(usuario_email):
        """Busca produtos de um usuário específico"""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.execute('''
                SELECT id, nome, preco, quantidade, categoria, data_cadastro, image_path
                FROM produtos
                WHERE usuario_email = ?
                ORDER BY data_cadastro DESC
            ''', (usuario_email,))

            products = []
            for row in cursor.fetchall():
                products.append(Product(
                    id=row['id'],
                    nome=row['nome'],
                    preco=row['preco'],
                    quantidade=row['quantidade'],
                    categoria=row['categoria'],
                    data_cadastro=row['data_cadastro'],
                    usuario_email=usuario_email,
                    image_path=row['image_path']
                ))
            return products
        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """Busca todos os produtos com informações do vendedor"""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.execute('''
                SELECT p.id, p.nome, p.preco, p.quantidade, p.categoria, p.image_path, 
                       p.data_cadastro, p.usuario_email, u.name as vendedor_nome
                FROM produtos p
                LEFT JOIN users u ON p.usuario_email = u.email
                ORDER BY p.data_cadastro DESC
            ''')

            products = []
            for row in cursor.fetchall():
                products.append({
                    'id': row[0],
                    'nome': row[1],
                    'preco': float(row[2]),
                    'quantidade': row[3],
                    'categoria': row[4],
                    'image_path': row[5],
                    'data_cadastro': row[6],
                    'usuario_email': row[7],
                    'vendedor_nome': row[8] or 'Vendedor'
                })
            return products
        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_categories():
        """Busca todas as categorias únicas"""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.execute('''
                SELECT DISTINCT categoria 
                FROM produtos 
                WHERE categoria IS NOT NULL AND categoria != ''
                ORDER BY categoria
            ''')

            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Erro ao buscar categorias: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def delete(product_id, usuario_email):
        """Deleta um produto"""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            # Verificar se o produto pertence ao usuário
            cursor = conn.execute('''
                SELECT image_path FROM produtos 
                WHERE id = ? AND usuario_email = ?
            ''', (product_id, usuario_email))

            product = cursor.fetchone()
            if not product:
                return False

            # Deletar imagem se existir
            if product['image_path']:
                delete_image(product['image_path'])

            # Deletar produto
            conn.execute('DELETE FROM produtos WHERE id = ?', (product_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar produto: {e}")
            return False
        finally:
            conn.close()
