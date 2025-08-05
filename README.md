# 🚀 Sistema de Login - Live Server

Sistema web completo para login e registro de vendedores, integrado com Flask e SQLite.

## 🎯 Como Usar

### 1. Ativar Ambiente Virtual
```bash
.venv\Scripts\Activate.ps1
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar Servidor Flask
```bash
python app.py
```

### 4. Acessar com Live Server
- **VS Code**: Clique direito em `templates/seller_login.html` → "Open with Live Server"
- **URL**: `http://127.0.0.1:5500/templates/seller_login.html`

## 📁 Estrutura

```
CRUD SQLITE PYTHON/
├── app.py                          # Servidor Flask
├── database.db                     # Banco SQLite
├── static/
│   ├── seller_style.css           # Estilos
│   ├── seller_login.js            # JS Login
│   └── seller_register.js         # JS Registro
├── templates/
│   ├── seller_login.html          # Login
│   └── seller_register.html       # Registro
└── requirements.txt               # Dependências
```

## 🎨 Funcionalidades

- ✅ **Login/Registro** com validação em tempo real
- ✅ **Conexão com banco** `database.db`
- ✅ **Design moderno** Apple-style
- ✅ **Live Server** compatível
- ✅ **CORS habilitado** para desenvolvimento

## 🔧 URLs

- **Flask**: `http://localhost:5000`
- **Live Server**: `http://127.0.0.1:5500`
- **Login**: `http://127.0.0.1:5500/templates/seller_login.html`
- **Registro**: `http://127.0.0.1:5500/templates/seller_register.html`

---

**✅ Sistema pronto para uso!** 