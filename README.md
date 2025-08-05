# Sistema de Login com White List e Painel de Administração

Este é um sistema de login em Python com SQLite que inclui funcionalidades de white list e painel de administração com um **admin mestre** padrão.

## Funcionalidades

### Sistema Principal (`main.py`)
- **Login**: Autenticação de usuários
- **Cadastro**: Registro de novos usuários
- **Redefinir senha**: Recuperação de senha via pergunta de segurança
- **Admin Mestre**: Usuário com acesso total ao sistema
- **Detecção automática de admin**: Usuários na white list acessam o painel de admin

### Painel de Administração (`admin_view.py`)
- **Listar usuários**: Visualizar todos os usuários cadastrados (apenas para admins)
- **Alterar senha**: Modificar senha de qualquer usuário
- **Cadastrar usuário**: Criar novos usuários
- **Remover usuário**: Excluir usuários do sistema
- **Adicionar à white list**: Dar privilégios de administrador

### Configuração (`config.py`)
- **Credenciais do admin mestre**: Email e senha padrão
- **Configurações de segurança**: Validações de senha
- **Mensagens do sistema**: Personalização de textos

## Admin Mestre

O sistema possui um **admin mestre** que é criado automaticamente na primeira execução:

### Credenciais Padrão:
- **Email**: `admin@admin.com`
- **Senha**: `admin123456`
- **Nome**: Administrador Mestre

### Características:
- ✅ **Acesso total** ao painel de administração
- ✅ **Sempre reconhecido** como admin (não precisa estar na white list)
- ✅ **Criado automaticamente** na primeira execução
- ✅ **Credenciais configuráveis** no arquivo `config.py`

## Como usar

### 1. Primeira execução
1. Execute `python main.py`
2. O admin mestre será criado automaticamente
3. Use as credenciais padrão para fazer login

### 2. Login como admin mestre
1. Escolha opção `1` para login
2. Digite: `admin@admin.com` / `admin123456`
3. Acesso direto ao painel de administração

### 3. Login como admin da white list
1. Cadastre um usuário (opção 2)
2. Faça login e acesse o painel de admin
3. No painel, use opção 5 para adicionar emails à white list
4. Agora outros usuários podem fazer login como admin

### 4. Menu Principal
- **Opção 1**: Login
- **Opção 2**: Cadastro de usuário
- **Opção 3**: Redefinir senha
- **Opção 4**: Sair do sistema

### 5. Funcionalidades do admin
- **Opção 1**: Listar todos os usuários
- **Opção 2**: Alterar senha de qualquer usuário
- **Opção 3**: Cadastrar novos usuários
- **Opção 4**: Remover usuários
- **Opção 5**: Adicionar usuários à white list
- **Opção 6**: Voltar ao menu principal

## Personalização

### Alterar credenciais do admin mestre:
Edite o arquivo `config.py`:

```python
# Credenciais do Admin Mestre
MASTER_ADMIN_EMAIL = "seu_email@exemplo.com"
MASTER_ADMIN_PASSWORD = "sua_senha_segura"
MASTER_ADMIN_NAME = "Seu Nome"
MASTER_ADMIN_SECURITY_QUESTION = "Sua resposta"
```

### Configurações de segurança:
```python
MIN_PASSWORD_LENGTH = 8  # Tamanho mínimo da senha
PASSWORD_ALLOW_SPACES = False  # Permitir espaços na senha
```

## Estrutura do banco de dados

### Tabela `users`
- `id`: ID único do usuário
- `name`: Nome completo
- `email`: Email (único)
- `password`: Hash da senha (SHA-256)
- `security_question`: Resposta para recuperação de senha

### Tabela `white_list`
- `id`: ID único
- `email`: Email do administrador (único)

## Segurança

- ✅ Senhas sempre hasheadas com SHA-256
- ✅ Validação de email e senha
- ✅ Admin mestre com acesso garantido
- ✅ White list para controle de acesso admin
- ✅ Não exibe senhas ou hashes em logs
- ✅ Validações de entrada de dados
- ✅ Listagem de usuários apenas para administradores

## Exemplo de uso

```
1. Primeira execução:
   → Admin mestre criado automaticamente
   → Email: admin@admin.com
   → Senha: admin123456

2. Login como admin mestre:
   → Acesso direto ao painel de administração
   → Pode gerenciar todos os usuários

3. Criar outros admins:
   → No painel, adicionar emails à white list
   → Outros usuários ganham privilégios de admin
```

## Arquivos do sistema

- `main.py`: Sistema principal
- `admin_view.py`: Painel de administração
- `config.py`: Configurações do sistema
- `database.db`: Banco de dados SQLite
- `README.md`: Documentação 