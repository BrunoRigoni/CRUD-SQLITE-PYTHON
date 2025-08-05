from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import hashlib
import os
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

CORS(app, origins=['http://127.0.0.1:5500', 'http://localhost:5500',
     'http://127.0.0.1:3000', 'http://localhost:3000'])

DATABASE = 'database.db'


def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Erro ao conectar com banco: {e}")
        return None


def init_db():
    conn = get_db_connection()
    if not conn:
        print("Não foi possível conectar ao banco de dados")
        return

    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.execute('''
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/seller_login', methods=['GET', 'POST'])
def seller_login():
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                email = data.get('email', '').strip().lower()
                password = data.get('password', '').strip()
            else:
                email = request.form.get('email', '').strip().lower()
                password = request.form.get('password', '').strip()

            if not email or not password:
                return jsonify({
                    'success': False,
                    'message': 'Email e senha são obrigatórios!'
                }), 400

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            conn = get_db_connection()
            if not conn:
                return jsonify({
                    'success': False,
                    'message': 'Erro de conexão com banco de dados!'
                }), 500

            cursor = conn.execute('''
                SELECT id, name, email, is_admin FROM users 
                WHERE email = ? AND password = ?
            ''', (email, hashed_password))

            user = cursor.fetchone()
            conn.close()

            if user:
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_email'] = user['email']
                session['is_admin'] = user['is_admin']

                return jsonify({
                    'success': True,
                    'message': f'Bem-vindo, {user["name"]}!',
                    'user': {
                        'id': user['id'],
                        'name': user['name'],
                        'email': user['email'],
                        'is_admin': user['is_admin']
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Email ou senha incorretos!'
                }), 401

        except Exception as e:
            print(f"Erro no login: {e}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor!'
            }), 500

    return render_template('seller_login.html')


@app.route('/seller_register', methods=['GET', 'POST'])
def seller_register():
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                name = data.get('name', '').strip()
                email = data.get('email', '').strip().lower()
                password = data.get('password', '').strip()
                confirm_password = data.get('confirm_password', '').strip()
            else:
                name = request.form.get('name', '').strip()
                email = request.form.get('email', '').strip().lower()
                password = request.form.get('password', '').strip()
                confirm_password = request.form.get(
                    'confirm_password', '').strip()

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

            conn = get_db_connection()
            if not conn:
                return jsonify({
                    'success': False,
                    'message': 'Erro de conexão com banco de dados!'
                }), 500

            cursor = conn.execute(
                'SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                conn.close()
                return jsonify({
                    'success': False,
                    'message': 'Email já cadastrado!'
                }), 400

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            try:
                conn.execute('''
                    INSERT INTO users (name, email, password)
                    VALUES (?, ?, ?)
                ''', (name, email, hashed_password))
                conn.commit()
                conn.close()

                return jsonify({
                    'success': True,
                    'message': 'Usuário cadastrado com sucesso!'
                })
            except Exception as e:
                conn.close()
                print(f"Erro ao cadastrar usuário: {e}")
                return jsonify({
                    'success': False,
                    'message': f'Erro ao cadastrar usuário: {str(e)}'
                }), 500

        except Exception as e:
            print(f"Erro no registro: {e}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor!'
            }), 500

    return render_template('seller_register.html')

# Rotas do Dashboard


@app.route('/overview')
def overview():
    return render_template('overview.html')


@app.route('/products')
def products():
    return render_template('products.html')


@app.route('/customers')
def customers():
    return render_template('customers.html')


@app.route('/sales')
def sales():
    return render_template('sales.html')


@app.route('/reports')
def reports():
    return render_template('reports.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/api/validate_user', methods=['POST'])
def validate_user():
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

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        if not conn:
            return jsonify({
                'valid': False,
                'message': 'Erro de conexão com banco de dados!'
            }), 500

        cursor = conn.execute('''
            SELECT id, name, email, is_admin FROM users 
            WHERE email = ? AND password = ?
        ''', (email, hashed_password))

        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify({
                'valid': True,
                'message': 'Login válido!',
                'user': {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'is_admin': user['is_admin']
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


@app.route('/api/dashboard_stats')
def dashboard_stats():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'message': 'Erro de conexão com banco de dados!'
            }), 500

        # Contar produtos
        cursor = conn.execute('SELECT COUNT(*) FROM produtos')
        total_products = cursor.fetchone()[0]

        # Contar clientes
        cursor = conn.execute('SELECT COUNT(*) FROM clientes')
        total_customers = cursor.fetchone()[0]

        # Contar vendas
        cursor = conn.execute('SELECT COUNT(*) FROM vendas')
        total_sales = cursor.fetchone()[0]

        # Calcular receita total
        cursor = conn.execute('SELECT SUM(total) FROM vendas')
        total_revenue = cursor.fetchone()[0] or 0

        conn.close()

        return jsonify({
            'success': True,
            'total_products': total_products,
            'total_customers': total_customers,
            'total_sales': total_sales,
            'total_revenue': total_revenue
        })

    except Exception as e:
        print(f"Erro ao carregar estatísticas: {e}")
        return jsonify({
            'success': False,
            'message': 'Erro ao carregar estatísticas!'
        }), 500


@app.route('/api/check_db')
def check_db():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.execute('SELECT COUNT(*) FROM users')
            count = cursor.fetchone()[0]
            conn.close()
            return jsonify({
                'success': True,
                'message': f'Banco conectado! {count} usuários encontrados.',
                'user_count': count
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Não foi possível conectar ao banco de dados!'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao verificar banco: {str(e)}'
        }), 500


if __name__ == '__main__':
    init_db()
    print("🚀 Servidor Flask iniciado!")
    print("📊 Banco de dados: database.db")
    print("🌐 URLs: http://localhost:5000")
    print("💡 Use Live Server para acessar as páginas HTML")
    app.run(debug=True, host='0.0.0.0', port=5000)
