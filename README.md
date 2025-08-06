# CRUD SQLite Python - Flask App

Sistema de gerenciamento de produtos com autenticação de usuários.

## Deploy no Render.com

### Configurações Necessárias

1. **Root Directory**: Deixe vazio (usar diretório raiz do repositório)

2. **Build Command**: 
```
pip install -r requirements.txt
```

3. **Start Command**: 
```
gunicorn app:app
```

4. **Environment Variables**:
   - `FLASK_ENV`: `production`
   - `FLASK_APP`: `app.py`
   - `SECRET_KEY`: `33d4a5d98ad218beebc1a5acfd22cccd`
   - `PORT`: `10000` (Render.com usa esta porta por padrão)

### Estrutura do Projeto

```
CRUD SQLITE PYTHON/
├── app.py                 # Aplicação principal Flask
├── wsgi.py               # Arquivo WSGI para Gunicorn
├── requirements.txt      # Dependências Python
├── render.yaml          # Configuração do Render.com
├── src/                 # Código fonte
│   ├── controllers/     # Controladores
│   ├── database/        # Conexão com banco
│   ├── models/          # Modelos
│   └── utils/           # Utilitários
├── static/              # Arquivos estáticos
├── templates/           # Templates HTML
└── README.md           # Este arquivo
```

### Funcionalidades

- ✅ Autenticação de usuários
- ✅ CRUD de produtos
- ✅ Gerenciamento de clientes
- ✅ Sistema de vendas
- ✅ Relatórios
- ✅ Upload de imagens
- ✅ Dashboard administrativo

### Tecnologias

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Deploy**: Render.com
- **WSGI Server**: Gunicorn

### Acesso

Após o deploy, a aplicação estará disponível em:
`https://seu-app-name.onrender.com`

### Notas Importantes

1. O banco SQLite será criado automaticamente na primeira execução
2. As imagens são salvas em `static/uploads/`
3. O sistema usa sessões para autenticação
4. CORS está configurado para desenvolvimento local 