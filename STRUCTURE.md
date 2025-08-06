# 📁 Estrutura do Projeto - Documentação Detalhada

## 🎯 Visão Geral

O projeto foi reorganizado seguindo princípios de **Arquitetura em Camadas** e **Separação de Responsabilidades**, tornando o código mais **maintainable**, **testable** e **escalável**.

## 🏗️ Estrutura de Pastas

```
CRUD-SQLITE-PYTHON/
├── 📁 src/                          # Código fonte organizado
│   ├── 📁 database/                 # Camada de banco de dados
│   │   ├── __init__.py
│   │   └── connection.py            # Conexão e inicialização do banco
│   ├── 📁 models/                   # Modelos de dados (Entidades)
│   │   ├── __init__.py
│   │   ├── user.py                  # Modelo de usuário
│   │   └── product.py               # Modelo de produto
│   ├── 📁 controllers/              # Controladores (Lógica de negócio)
│   │   ├── __init__.py
│   │   ├── auth_controller.py       # Controlador de autenticação
│   │   └── product_controller.py    # Controlador de produtos
│   └── 📁 utils/                    # Utilitários
│       ├── __init__.py
│       └── file_utils.py            # Utilitários para arquivos
├── 📁 static/                       # Arquivos estáticos
│   ├── 📁 css/                      # Folhas de estilo
│   ├── 📁 js/                       # JavaScript
│   ├── 📁 img/                      # Imagens
│   └── 📁 uploads/                  # Uploads de imagens
├── 📁 templates/                    # Templates HTML
├── 🐍 app.py                        # Aplicação principal Flask
├── 📄 requirements.txt              # Dependências Python
├── 📄 README.md                     # Documentação principal
└── 📄 STRUCTURE.md                  # Esta documentação
```

## 🔄 Fluxo de Dados

### 1. **Request Flow**
```
Cliente → app.py (Rotas) → Controller → Model → Database
```

### 2. **Response Flow**
```
Database → Model → Controller → app.py → Cliente
```

## 📂 Detalhamento das Camadas

### 🗄️ **Database Layer** (`src/database/`)

**Responsabilidade**: Gerenciar conexões e operações de banco de dados.

#### `connection.py`
- **Função**: Estabelecer conexões com SQLite
- **Métodos**:
  - `get_db_connection()`: Retorna conexão ativa
  - `init_db()`: Inicializa tabelas do banco

#### Características:
- ✅ Conexões seguras e gerenciadas
- ✅ Inicialização automática de tabelas
- ✅ Tratamento de erros robusto

### 🎯 **Models Layer** (`src/models/`)

**Responsabilidade**: Representar entidades de negócio e suas operações.

#### `user.py`
- **Entidade**: Usuário do sistema
- **Métodos**:
  - `create()`: Criar novo usuário
  - `authenticate()`: Autenticar usuário
  - `get_by_email()`: Buscar por email
  - `email_exists()`: Verificar existência

#### `product.py`
- **Entidade**: Produto do sistema
- **Métodos**:
  - `create()`: Criar novo produto
  - `get_by_user()`: Buscar produtos do usuário
  - `get_all()`: Buscar todos os produtos
  - `get_categories()`: Buscar categorias
  - `delete()`: Deletar produto

#### Características:
- ✅ Separação clara de responsabilidades
- ✅ Métodos estáticos para operações
- ✅ Validações integradas

### 🎮 **Controllers Layer** (`src/controllers/`)

**Responsabilidade**: Orquestrar lógica de negócio e validações.

#### `auth_controller.py`
- **Função**: Gerenciar autenticação
- **Métodos**:
  - `login()`: Processar login
  - `register()`: Processar registro
  - `logout()`: Processar logout

#### `product_controller.py`
- **Função**: Gerenciar produtos
- **Métodos**:
  - `create()`: Criar produto
  - `get_user_products()`: Buscar produtos do usuário
  - `get_all_products()`: Buscar todos os produtos
  - `get_categories()`: Buscar categorias
  - `delete()`: Deletar produto

#### Características:
- ✅ Validações robustas
- ✅ Tratamento de erros
- ✅ Respostas padronizadas

### 🛠️ **Utils Layer** (`src/utils/`)

**Responsabilidade**: Fornecer utilitários reutilizáveis.

#### `file_utils.py`
- **Função**: Manipulação de arquivos
- **Métodos**:
  - `allowed_file()`: Validar extensões
  - `save_image()`: Salvar imagens
  - `delete_image()`: Deletar imagens

#### Características:
- ✅ Funções reutilizáveis
- ✅ Validações de segurança
- ✅ Gerenciamento de arquivos

## 🎨 Benefícios da Nova Estrutura

### ✅ **Manutenibilidade**
- Código organizado por responsabilidade
- Fácil localização de funcionalidades
- Redução de acoplamento

### ✅ **Testabilidade**
- Camadas isoladas
- Dependências claras
- Fácil mock de componentes

### ✅ **Escalabilidade**
- Estrutura preparada para crescimento
- Fácil adição de novas funcionalidades
- Padrões consistentes

### ✅ **Legibilidade**
- Código auto-documentado
- Nomes descritivos
- Estrutura intuitiva

## 🔧 Como Adicionar Novas Funcionalidades

### 1. **Novo Modelo**
```python
# src/models/novo_modelo.py
from src.database.connection import get_db_connection

class NovoModelo:
    @staticmethod
    def create():
        # Implementação
        pass
```

### 2. **Novo Controller**
```python
# src/controllers/novo_controller.py
from flask import jsonify, request
from src.models.novo_modelo import NovoModelo

class NovoController:
    @staticmethod
    def create():
        # Implementação
        pass
```

### 3. **Nova Rota**
```python
# app.py
from src.controllers.novo_controller import NovoController

@app.route('/api/novo', methods=['POST'])
def novo_endpoint():
    return NovoController.create()
```

## 🚀 Próximos Passos

### 🔄 Melhorias Sugeridas

1. **Testes Unitários**
   - Criar testes para cada camada
   - Usar pytest ou unittest

2. **Logging**
   - Implementar sistema de logs
   - Rastreamento de erros

3. **Configuração**
   - Arquivo de configuração separado
   - Variáveis de ambiente

4. **Documentação**
   - Docstrings completas
   - Exemplos de uso

5. **Validação**
   - Schemas de validação
   - Sanitização de dados

## 📝 Convenções de Código

### 📋 **Nomenclatura**
- **Classes**: PascalCase (`User`, `ProductController`)
- **Métodos**: snake_case (`get_user_products`, `create_product`)
- **Variáveis**: snake_case (`user_email`, `product_name`)
- **Constantes**: UPPER_CASE (`DATABASE`, `UPLOAD_FOLDER`)

### 📋 **Estrutura de Arquivos**
- **Um arquivo por classe/entidade**
- **Nomes descritivos**
- **Organização por responsabilidade**

### 📋 **Documentação**
- **Docstrings em todas as funções**
- **Comentários explicativos**
- **README atualizado**

---

**🎯 Resultado**: Código mais organizado, maintainable e profissional! 