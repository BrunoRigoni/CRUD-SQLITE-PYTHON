# CRUD SQLite Python - Sistema de Gerenciamento de Produtos

Sistema completo de gerenciamento de produtos com interface web, desenvolvido em Python usando Flask e SQLite.

## 🏗️ Estrutura do Projeto

```
CRUD-SQLITE-PYTHON/
├── src/                          # Código fonte organizado
│   ├── database/                 # Camada de banco de dados
│   │   ├── __init__.py
│   │   └── connection.py         # Conexão e inicialização do banco
│   ├── models/                   # Modelos de dados
│   │   ├── __init__.py
│   │   ├── user.py              # Modelo de usuário
│   │   └── product.py           # Modelo de produto
│   ├── controllers/              # Controladores
│   │   ├── __init__.py
│   │   ├── auth_controller.py   # Controlador de autenticação
│   │   └── product_controller.py # Controlador de produtos
│   └── utils/                    # Utilitários
│       ├── __init__.py
│       └── file_utils.py        # Utilitários para arquivos
├── static/                       # Arquivos estáticos
│   ├── css/                     # Folhas de estilo
│   ├── js/                      # JavaScript
│   ├── img/                     # Imagens
│   └── uploads/                 # Uploads de imagens
├── templates/                    # Templates HTML
├── app.py                       # Aplicação principal Flask
├── requirements.txt             # Dependências Python
└── README.md                    # Documentação
```

## 🚀 Funcionalidades

### ✨ Principais Recursos
- **Sistema de Autenticação**: Login e registro de usuários
- **Gerenciamento de Produtos**: CRUD completo de produtos
- **Upload de Imagens**: Suporte a imagens de produtos
- **Carrossel Dinâmico**: Exibição de produtos em carrossel
- **Interface Responsiva**: Design moderno e responsivo
- **Dashboard**: Painel administrativo completo

### 🎯 Funcionalidades Específicas
- **Login/Registro**: Sistema completo de autenticação
- **Adicionar Produtos**: Formulário com upload de imagem
- **Visualizar Produtos**: Lista dinâmica de produtos
- **Categorias**: Filtros por categoria
- **Busca**: Sistema de busca de produtos
- **Carrossel**: Banner dinâmico com produtos
- **Dashboard**: Estatísticas e gerenciamento

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.x, Flask
- **Banco de Dados**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Upload**: Werkzeug
- **CORS**: Flask-CORS

## 📦 Instalação

### Pré-requisitos
- Python 3.7+
- pip

### Passos para Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd CRUD-SQLITE-PYTHON
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**
```bash
python app.py
```

4. **Acesse a aplicação**
- **Frontend**: http://localhost:5000
- **Dashboard**: http://localhost:5000/seller_login

## 🎨 Estrutura de Código

### 📁 Organização por Camadas

#### **Database Layer** (`src/database/`)
- `connection.py`: Gerencia conexões com SQLite
- Inicialização automática do banco
- Configuração de tabelas

#### **Models Layer** (`src/models/`)
- `user.py`: Modelo de usuário com autenticação
- `product.py`: Modelo de produto com CRUD
- Separação clara de responsabilidades

#### **Controllers Layer** (`src/controllers/`)
- `auth_controller.py`: Lógica de autenticação
- `product_controller.py`: Lógica de produtos
- Validações e regras de negócio

#### **Utils Layer** (`src/utils/`)
- `file_utils.py`: Manipulação de arquivos
- Upload e exclusão de imagens
- Validações de arquivo

### 🔄 Fluxo de Dados

1. **Request** → `app.py` (Rotas)
2. **Controller** → Validação e lógica
3. **Model** → Interação com banco
4. **Response** → JSON/HTML

## 🎯 Como Usar

### 👤 Sistema de Autenticação
1. Acesse `/seller_register` para criar conta
2. Faça login em `/seller_login`
3. Acesse o dashboard

### 📦 Gerenciamento de Produtos
1. **Adicionar Produto**:
   - Acesse `/products`
   - Clique em "Add Product"
   - Preencha o formulário
   - Faça upload da imagem

2. **Visualizar Produtos**:
   - Acesse `/` para ver produtos públicos
   - Use filtros por categoria
   - Utilize a busca

3. **Gerenciar Produtos**:
   - Acesse `/products` no dashboard
   - Visualize, edite ou delete produtos

### 🎠 Carrossel Dinâmico
- Produtos com imagens aparecem automaticamente
- Navegação automática e manual
- Pausa no hover

## 🔧 Configuração

### Variáveis de Ambiente
```python
# app.py
app.secret_key = 'your-secret-key-here'  # Altere para produção
```

### Banco de Dados
- Criado automaticamente na primeira execução
- Localizado em `database.db`
- Tabelas criadas automaticamente

## 🐛 Solução de Problemas

### Problemas Comuns

1. **Erro de CORS**:
   - Verifique se o Flask-CORS está instalado
   - Confirme as origens permitidas

2. **Upload de Imagens**:
   - Verifique se a pasta `static/uploads` existe
   - Confirme permissões de escrita

3. **Banco de Dados**:
   - Delete `database.db` para recriar
   - Verifique permissões de escrita

## 📝 Licença

Este projeto está sob a licença MIT.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para suporte, entre em contato através dos issues do GitHub. 