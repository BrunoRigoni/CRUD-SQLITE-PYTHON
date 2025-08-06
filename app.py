from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import os
from src.database.connection import init_db
from src.controllers.auth_controller import AuthController
from src.controllers.product_controller import ProductController
from datetime import datetime

# Inicializar banco de dados se não existir
if not os.path.exists('database.db'):
    print("📊 Inicializando banco de dados...")
    init_db()
    print("📊 Banco de dados criado: database.db")
else:
    print("📊 Banco de dados já existe: database.db")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Configuração CORS
CORS(app, origins=[
    'http://127.0.0.1:5500', 'http://localhost:5500',
    'http://127.0.0.1:5000', 'http://localhost:5000',
    'http://127.0.0.1:3000', 'http://localhost:3000',
    'http://127.0.0.1:5501', 'http://localhost:5501',
    'https://crud-sqlite-python.onrender.com',
    'https://*.onrender.com',
    'https://*.render.com'
], supports_credentials=True)

# Rotas principais


@app.route('/')
def index():
    print("Acessando página inicial")
    return render_template('index.html')


@app.route('/seller_login', methods=['GET', 'POST'])
def seller_login():
    if request.method == 'POST':
        return AuthController.login()
    return render_template('seller_login.html')


@app.route('/seller_register', methods=['GET', 'POST'])
def seller_register():
    if request.method == 'POST':
        return AuthController.register()
    return render_template('seller_register.html')


@app.route('/client_login', methods=['GET', 'POST'])
def client_login():
    if request.method == 'POST':
        return AuthController.client_login()
    return render_template('client_login.html')


@app.route('/client_register', methods=['GET', 'POST'])
def client_register():
    if request.method == 'POST':
        return AuthController.client_register()
    return render_template('client_register.html')

# Rotas do Dashboard


@app.route('/overview')
def overview():
    if 'user_id' not in session:
        return redirect(url_for('seller_login'))
    return render_template('overview.html')


@app.route('/products')
def products():
    if 'user_id' not in session:
        return redirect(url_for('seller_login'))
    return render_template('products.html')


@app.route('/add_product')
def add_product():
    if 'user_id' not in session:
        return redirect(url_for('seller_login'))
    return render_template('add_product.html')


@app.route('/customers')
def customers():
    if 'user_id' not in session:
        return redirect(url_for('seller_login'))
    return render_template('customers.html')


@app.route('/sales')
def sales():
    if 'user_id' not in session:
        return redirect(url_for('seller_login'))
    return render_template('sales.html')


@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('seller_login'))
    return render_template('reports.html')


@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('seller_login'))
    return render_template('settings.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# APIs


@app.route('/api/validate_user', methods=['POST'])
def validate_user():
    return AuthController.login()


@app.route('/api/client_login', methods=['POST'])
def api_client_login():
    return AuthController.client_login()


@app.route('/api/client_register', methods=['POST'])
def api_client_register():
    return AuthController.client_register()


@app.route('/api/dashboard_stats')
def dashboard_stats():
    try:
        from src.database.connection import get_db_connection
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
        from src.database.connection import get_db_connection
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


@app.route('/api/debug')
def debug():
    """Rota de debug para verificar se a aplicação está funcionando"""
    return jsonify({
        'success': True,
        'message': 'Aplicação Flask funcionando!',
        'timestamp': datetime.now().isoformat(),
        'environment': os.environ.get('FLASK_ENV', 'development')
    })

# APIs de Produtos


@app.route('/api/add_product', methods=['POST'])
def api_add_product():
    return ProductController.create()


@app.route('/api/get_products')
def get_products():
    return ProductController.get_user_products()


@app.route('/api/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    return ProductController.delete(product_id)


@app.route('/api/public_products')
def get_public_products():
    print("Acessando /api/public_products")
    try:
        result = ProductController.get_all_products()
        print(f"Resultado: {result}")
        return result
    except Exception as e:
        print(f"Erro na rota /api/public_products: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao carregar produtos: {str(e)}'
        }), 500


@app.route('/api/categories')
def get_categories():
    print("Acessando /api/categories")
    try:
        result = ProductController.get_categories()
        print(f"Resultado: {result}")
        return result
    except Exception as e:
        print(f"Erro na rota /api/categories: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao carregar categorias: {str(e)}'
        }), 500


@app.route('/api/init_db')
def init_database():
    """Rota para inicializar o banco de dados"""
    try:
        init_db()
        return jsonify({
            'success': True,
            'message': 'Banco de dados inicializado com sucesso!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao inicializar banco: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("🚀 Servidor Flask iniciado!")
    print("🌐 URL: http://localhost:5000")
    print("💡 Use Live Server para acessar as páginas HTML")

    # Configuração para produção
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    app.run(debug=debug, host='0.0.0.0', port=port)
