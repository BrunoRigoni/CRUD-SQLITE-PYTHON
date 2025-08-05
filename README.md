# Sistema de Gerenciamento CRUD com SQLite e Python

Um sistema completo de gerenciamento de produtos, clientes e vendas com autenticação de usuários, painel administrativo e funcionalidades avançadas de importação/exportação.

## 📋 Índice

- [Funcionalidades Principais](#funcionalidades-principais)
- [Linha do Tempo de Desenvolvimento](#linha-do-tempo-de-desenvolvimento)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Usar](#como-usar)
- [Funcionalidades Detalhadas](#funcionalidades-detalhadas)
- [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
- [Segurança](#segurança)
- [Arquivos do Sistema](#arquivos-do-sistema)

## 🎯 Funcionalidades Principais

### Sistema de Autenticação
- ✅ Login e cadastro de usuários
- ✅ Painel administrativo com admin mestre
- ✅ Sistema de white list para administradores
- ✅ Banco de dados centralizado por usuário

### Gerenciamento de Produtos
- ✅ CRUD completo (Criar, Ler, Atualizar, Deletar)
- ✅ Busca por nome e categoria
- ✅ Relatórios em Excel
- ✅ Importação/exportação via planilhas
- ✅ Sistema organizado de pastas (download_base/upload_base)

### Gerenciamento de Clientes
- ✅ CRUD completo
- ✅ Busca por nome e email
- ✅ Dados completos (nome, email, telefone, endereço)

### Gerenciamento de Vendas
- ✅ Nova venda com seleção de cliente e produto
- ✅ Listagem e busca de vendas
- ✅ Relatórios detalhados em Excel
- ✅ Análise de vendas por período

### Relatórios e Análises
- ✅ Relatórios de produtos em Excel
- ✅ Relatórios de vendas com múltiplas planilhas
- ✅ Análise completa de vendas
- ✅ Produtos com baixo estoque
- ✅ Vendas por período

## 🕒 Linha do Tempo de Desenvolvimento

### **Fase 1: Sistema Base de Autenticação**
- ✅ **Sistema de login** com SQLite
- ✅ **Cadastro de usuários** com validações
- ✅ **Admin mestre** com credenciais padrão
- ✅ **Painel administrativo** básico
- ✅ **Sistema de white list** para administradores

### **Fase 2: Gerenciamento de Produtos**
- ✅ **CRUD de produtos** completo
- ✅ **Busca por nome e categoria**
- ✅ **Validações de dados**
- ✅ **Interface de usuário** organizada

### **Fase 3: Sistema de Usuários Individuais**
- ✅ **Banco de dados separado por usuário** (inicial)
- ✅ **Visão exclusiva** de produtos por usuário
- ✅ **Isolamento de dados** entre usuários

### **Fase 4: Melhorias na Interface**
- ✅ **Função limpar_terminal()** para melhor UX
- ✅ **Input de confirmação** antes de voltar ao menu
- ✅ **Interface mais limpa** e organizada

### **Fase 5: Sistema Centralizado**
- ✅ **Banco de dados centralizado** em `database.db`
- ✅ **Separação lógica** por `usuario_email`
- ✅ **Tabelas unificadas** para produtos, clientes e vendas
- ✅ **Remoção de arquivos** desnecessários (`produtos_db.py`)

### **Fase 6: Gerenciamento de Clientes**
- ✅ **CRUD completo de clientes**
- ✅ **Busca por nome e email**
- ✅ **Dados completos** (nome, email, telefone, endereço)
- ✅ **Interface integrada** ao sistema

### **Fase 7: Sistema de Vendas**
- ✅ **Nova venda** com seleção de cliente e produto
- ✅ **Cálculo automático** de totais
- ✅ **Listagem de vendas**
- ✅ **Busca de vendas**

### **Fase 8: Relatórios em Excel**
- ✅ **Relatórios de produtos** em Excel
- ✅ **Relatórios de vendas** com múltiplas planilhas
- ✅ **Análise completa de vendas**
- ✅ **Bibliotecas pandas e openpyxl** integradas

### **Fase 9: Sistema de Importação/Exportação**
- ✅ **Geração de planilhas base** para importação
- ✅ **Importação de produtos** via Excel
- ✅ **Validação completa** de dados
- ✅ **Relatórios de importação**

### **Fase 10: Organização de Pastas**
- ✅ **Pasta `relatorios/`** para relatórios Excel
- ✅ **Pasta `inventario/`** para modelos e templates
- ✅ **Subpastas organizadas**:
  - `inventario/download_base/` - Modelos gerados
  - `inventario/upload_base/` - Arquivos para importação
- ✅ **Exclusão automática** após importação

### **Fase 11: Simplificação e Otimização**
- ✅ **Remoção de importação manual** (opção 8 anterior)
- ✅ **Sistema unificado** de importação via upload_base
- ✅ **Interface simplificada** e mais intuitiva
- ✅ **Fluxo organizado** e consistente

## 📁 Estrutura do Projeto

```
CRUD SQLITE PYTHON/
├── main.py                          # Sistema principal
├── user_view.py                     # Interface do usuário
├── admin_view.py                    # Painel administrativo
├── config.py                        # Configurações
├── database.db                      # Banco de dados centralizado
├── requirements.txt                 # Dependências Python
├── .gitignore                       # Arquivos ignorados pelo Git
├── README.md                        # Documentação
├── relatorios/                      # Relatórios Excel gerados
│   └── *.xlsx
└── inventario/                      # Modelos e templates
    ├── download_base/               # Planilhas base geradas
    │   └── *.xlsx
    └── upload_base/                 # Arquivos para importação
        └── *.xlsx
```

## 🚀 Como Usar

### 1. Primeira Execução
```bash
# Instalar dependências
py -m pip install pandas openpyxl

# Executar o sistema
py main.py
```

### 2. Login Inicial
- **Email**: `admin@admin.com`
- **Senha**: `admin123456`

### 3. Menu Principal
```
SISTEMA DE GERENCIAMENTO
1. Produtos
2. Vendas
3. Clientes
4. Análise de vendas
5. Sair
```

### 4. Gerenciamento de Produtos
```
GERENCIAMENTO DE PRODUTOS
1. Listar produtos
2. Adicionar produto
3. Editar produto
4. Remover produto
5. Buscar produto
6. Gerar relatório Excel
7. Gerar planilha base para importação
8. Importar produtos da pasta upload_base
9. Voltar ao menu principal
```

## 🔧 Funcionalidades Detalhadas

### Sistema de Autenticação
- **Login seguro** com hash SHA-256
- **Cadastro com validações** de email e senha
- **Admin mestre** com acesso total
- **White list** para administradores adicionais

### Gerenciamento de Produtos
- **CRUD completo** com validações
- **Busca inteligente** por nome e categoria
- **Relatórios Excel** com formatação automática
- **Importação organizada** via pasta upload_base
- **Modelos base** gerados automaticamente

### Gerenciamento de Clientes
- **Dados completos** (nome, email, telefone, endereço)
- **Busca flexível** por nome e email
- **CRUD integrado** ao sistema

### Sistema de Vendas
- **Nova venda** com seleção de cliente e produto
- **Cálculo automático** de totais
- **Histórico completo** de vendas
- **Relatórios detalhados** em Excel

### Relatórios e Análises
- **Relatórios de produtos** com estatísticas
- **Relatórios de vendas** com múltiplas planilhas
- **Análise completa** de vendas por período
- **Produtos com baixo estoque**
- **Clientes mais valiosos**

## 🗄️ Estrutura do Banco de Dados

### Tabela `users`
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
```

### Tabela `produtos`
```sql
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    categoria TEXT,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario_email TEXT NOT NULL,
    FOREIGN KEY (usuario_email) REFERENCES users(email)
);
```

### Tabela `clientes`
```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT,
    telefone TEXT,
    endereco TEXT,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario_email TEXT NOT NULL,
    FOREIGN KEY (usuario_email) REFERENCES users(email)
);
```

### Tabela `vendas`
```sql
CREATE TABLE vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    total REAL NOT NULL,
    data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario_email TEXT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    FOREIGN KEY (usuario_email) REFERENCES users(email)
);
```

## 🔒 Segurança

- ✅ **Senhas hasheadas** com SHA-256
- ✅ **Validação de dados** em todas as entradas
- ✅ **Separação de dados** por usuário
- ✅ **Controle de acesso** administrativo
- ✅ **Confirmações** para operações críticas
- ✅ **Exclusão automática** de arquivos temporários

## 📊 Arquivos do Sistema

### Arquivos Principais
- `main.py` - Sistema principal de autenticação
- `user_view.py` - Interface completa do usuário
- `admin_view.py` - Painel administrativo
- `config.py` - Configurações do sistema

### Banco de Dados
- `database.db` - Banco SQLite centralizado

### Dependências
- `requirements.txt` - Bibliotecas Python necessárias

### Documentação
- `README.md` - Documentação completa do projeto

### Pastas Organizacionais
- `relatorios/` - Relatórios Excel gerados
- `inventario/download_base/` - Modelos base
- `inventario/upload_base/` - Arquivos para importação

## 🎉 Status do Projeto

**✅ PROJETO COMPLETO E FUNCIONAL**

- **Todas as funcionalidades** implementadas e testadas
- **Interface intuitiva** e organizada
- **Sistema robusto** de segurança
- **Documentação completa** e atualizada
- **Código limpo** e bem estruturado
- **Pronto para uso** em produção

---

**Desenvolvido com ❤️ em Python e SQLite** 