from flask import jsonify, request, session
from src.models.user import User


class AuthController:
    @staticmethod
    def login():
        """Controlador para login de usuários"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({
                    'valid': False,
                    'message': 'Dados inválidos!'
                }), 400

            email = data.get('email', '').strip().lower()
            password = data.get('password', '').strip()

            if not email or not password:
                return jsonify({
                    'valid': False,
                    'message': 'Email e senha são obrigatórios!'
                }), 400

            user = User.authenticate(email, password)
            if user:
                # Criar sessão do usuário
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['user_email'] = user.email
                session['is_admin'] = user.is_admin

                return jsonify({
                    'valid': True,
                    'message': 'Login válido!',
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'is_admin': user.is_admin
                    }
                })
            else:
                return jsonify({
                    'valid': False,
                    'message': 'Email ou senha incorretos!'
                }), 401

        except Exception as e:
            print(f"Erro na validação: {e}")
            return jsonify({
                'valid': False,
                'message': 'Erro interno do servidor!'
            }), 500

    @staticmethod
    def register():
        """Controlador para registro de usuários"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'Dados inválidos!'
                }), 400

            name = data.get('name', '').strip()
            email = data.get('email', '').strip().lower()
            password = data.get('password', '').strip()
            confirm_password = data.get('confirm_password', '').strip()

            if not name or not email or not password:
                return jsonify({
                    'success': False,
                    'message': 'Todos os campos são obrigatórios!'
                }), 400

            if password != confirm_password:
                return jsonify({
                    'success': False,
                    'message': 'As senhas não coincidem!'
                }), 400

            if len(password) < 8:
                return jsonify({
                    'success': False,
                    'message': 'A senha deve ter pelo menos 8 caracteres!'
                }), 400

            if ' ' in password:
                return jsonify({
                    'success': False,
                    'message': 'A senha não pode conter espaços!'
                }), 400

            if User.email_exists(email):
                return jsonify({
                    'success': False,
                    'message': 'Email já cadastrado!'
                }), 400

            user_id = User.create(name, email, password)
            if user_id:
                return jsonify({
                    'success': True,
                    'message': 'Usuário cadastrado com sucesso!'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Erro ao cadastrar usuário!'
                }), 500

        except Exception as e:
            print(f"Erro no registro: {e}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor!'
            }), 500

    @staticmethod
    def logout():
        """Controlador para logout de usuários"""
        session.clear()
        return jsonify({
            'success': True,
            'message': 'Logout realizado com sucesso!'
        })

    @staticmethod
    def client_login():
        """Controlador para login de clientes"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'Dados inválidos!'
                }), 400

            email = data.get('email', '').strip().lower()
            password = data.get('password', '').strip()

            if not email or not password:
                return jsonify({
                    'success': False,
                    'message': 'Email e senha são obrigatórios!'
                }), 400

            # Verificar se é um cliente (usuário não-admin)
            user = User.authenticate(email, password)
            if user and not user.is_admin:
                # Criar sessão do cliente
                session['client_id'] = user.id
                session['client_name'] = user.name
                session['client_email'] = user.email

                return jsonify({
                    'success': True,
                    'message': 'Login realizado com sucesso!',
                    'client': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Email ou senha incorretos!'
                }), 401

        except Exception as e:
            print(f"Erro no login do cliente: {e}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor!'
            }), 500

    @staticmethod
    def client_register():
        """Controlador para registro de clientes"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'Dados inválidos!'
                }), 400

            name = data.get('name', '').strip()
            email = data.get('email', '').strip().lower()
            password = data.get('password', '').strip()

            if not name or not email or not password:
                return jsonify({
                    'success': False,
                    'message': 'Todos os campos são obrigatórios!'
                }), 400

            if len(password) < 6:
                return jsonify({
                    'success': False,
                    'message': 'A senha deve ter pelo menos 6 caracteres!'
                }), 400

            if User.email_exists(email):
                return jsonify({
                    'success': False,
                    'message': 'Email já cadastrado!'
                }), 400

            # Criar cliente (usuário não-admin)
            user_id = User.create(name, email, password, is_admin=False)
            if user_id:
                return jsonify({
                    'success': True,
                    'message': 'Conta criada com sucesso!'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Erro ao criar conta!'
                }), 500

        except Exception as e:
            print(f"Erro no registro do cliente: {e}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor!'
            }), 500
