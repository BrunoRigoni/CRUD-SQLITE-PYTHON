from flask import jsonify, request, session
from src.models.product import Product


class ProductController:
    @staticmethod
    def create():
        """Controlador para criar produtos"""
        try:
            # Verificar se o usuário está logado
            if 'user_id' not in session:
                return jsonify({
                    'success': False,
                    'message': 'Usuário não está logado!'
                }), 401

            # Obter dados do formulário
            name = request.form.get('name', '').strip()
            price = request.form.get('price', '')
            quantity = request.form.get('quantity', '')
            category = request.form.get('category', '').strip()
            image = request.files.get('image')

            # Validações
            if not name:
                return jsonify({
                    'success': False,
                    'message': 'Nome do produto é obrigatório!'
                }), 400

            try:
                price = float(price)
                if price < 0:
                    return jsonify({
                        'success': False,
                        'message': 'Preço deve ser maior ou igual a zero!'
                    }), 400
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Preço inválido!'
                }), 400

            try:
                quantity = int(quantity)
                if quantity < 0:
                    return jsonify({
                        'success': False,
                        'message': 'Quantidade deve ser maior ou igual a zero!'
                    }), 400
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Quantidade inválida!'
                }), 400

            if not category:
                return jsonify({
                    'success': False,
                    'message': 'Categoria é obrigatória!'
                }), 400

            if not image:
                return jsonify({
                    'success': False,
                    'message': 'Imagem é obrigatória!'
                }), 400

            # Criar produto
            product_id = Product.create(
                name, price, quantity, category, session['user_email'], image)

            if product_id:
                return jsonify({
                    'success': True,
                    'message': 'Produto adicionado com sucesso!'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Erro ao adicionar produto!'
                }), 500

        except Exception as e:
            print(f"Erro ao adicionar produto: {e}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor!'
            }), 500

    @staticmethod
    def get_user_products():
        """Controlador para buscar produtos do usuário logado"""
        try:
            if 'user_id' not in session:
                return jsonify({
                    'success': False,
                    'message': 'Usuário não está logado!'
                }), 401

            products = Product.get_by_user(session['user_email'])
            products_data = []

            for product in products:
                products_data.append({
                    'id': product.id,
                    'nome': product.nome,
                    'preco': product.preco,
                    'quantidade': product.quantidade,
                    'categoria': product.categoria,
                    'data_cadastro': product.data_cadastro,
                    'image_path': product.image_path
                })

            return jsonify({
                'success': True,
                'products': products_data
            })

        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor!'
            }), 500

    @staticmethod
    def get_all_products():
        """Controlador para buscar todos os produtos (público)"""
        try:
            products = Product.get_all()
            return jsonify({
                'success': True,
                'products': products
            })

        except Exception as e:
            print(f"Erro ao buscar produtos públicos: {e}")
            return jsonify({
                'success': False,
                'message': f'Erro ao buscar produtos: {str(e)}'
            }), 500

    @staticmethod
    def get_categories():
        """Controlador para buscar categorias"""
        try:
            categories = Product.get_categories()
            return jsonify({
                'success': True,
                'categories': categories
            })

        except Exception as e:
            print(f"Erro ao buscar categorias: {e}")
            return jsonify({
                'success': False,
                'message': f'Erro ao buscar categorias: {str(e)}'
            }), 500

    @staticmethod
    def delete(product_id):
        """Controlador para deletar produto"""
        try:
            if 'user_id' not in session:
                return jsonify({
                    'success': False,
                    'message': 'Usuário não está logado!'
                }), 401

            success = Product.delete(product_id, session['user_email'])

            if success:
                return jsonify({
                    'success': True,
                    'message': 'Produto deletado com sucesso!'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Produto não encontrado!'
                }), 404

        except Exception as e:
            print(f"Erro ao deletar produto: {e}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor!'
            }), 500
