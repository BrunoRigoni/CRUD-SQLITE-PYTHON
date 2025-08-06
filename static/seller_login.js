// Seller Login JavaScript - Validação e Conexão com Flask (Live Server)

class SellerLogin {
    constructor() {
        this.form = document.getElementById('loginForm');
        this.emailInput = document.getElementById('email');
        this.passwordInput = document.getElementById('password');
        this.messageDiv = document.getElementById('message');
        this.apiBaseUrl = window.location.origin;
        
        this.init();
    }

    init() {
        // Criar container para mensagens de erro
        this.createErrorContainer();
        
        // Adicionar event listeners
        this.addEventListeners();
        
        // Validação em tempo real
        this.setupRealTimeValidation();
        
        // Verificar conexão com banco
        this.checkDatabaseConnection();
    }

    createErrorContainer() {
        // Remover container de erro existente se houver
        const existingError = document.querySelector('.error-container');
        if (existingError) {
            existingError.remove();
        }

        // Criar novo container de erro
        this.errorContainer = document.createElement('div');
        this.errorContainer.className = 'error-container';
        this.errorContainer.style.cssText = `
            margin-top: 1rem;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 400;
            letter-spacing: -0.01em;
            display: none;
        `;
        
        // Inserir após o formulário
        this.form.parentNode.insertBefore(this.errorContainer, this.form.nextSibling);
    }

    addEventListeners() {
        // Event listener para submit do formulário
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });

        // Event listeners para validação em tempo real
        this.emailInput.addEventListener('blur', () => this.validateEmail());
        this.passwordInput.addEventListener('blur', () => this.validatePassword());
        
        // Event listeners para limpar erros ao digitar
        this.emailInput.addEventListener('input', () => this.clearError());
        this.passwordInput.addEventListener('input', () => this.clearError());
    }

    setupRealTimeValidation() {
        // Validação de email em tempo real
        this.emailInput.addEventListener('input', (e) => {
            const email = e.target.value.trim();
            if (email && !this.isValidEmail(email)) {
                this.showFieldError(this.emailInput, 'Email inválido');
            } else {
                this.clearFieldError(this.emailInput);
            }
        });

        // Validação de senha em tempo real
        this.passwordInput.addEventListener('input', (e) => {
            const password = e.target.value;
            if (password && password.length < 8) {
                this.showFieldError(this.passwordInput, 'Senha deve ter pelo menos 8 caracteres');
            } else {
                this.clearFieldError(this.passwordInput);
            }
        });
    }

    validateEmail() {
        const email = this.emailInput.value.trim();
        
        if (!email) {
            this.showFieldError(this.emailInput, 'Email é obrigatório');
            return false;
        }
        
        if (!this.isValidEmail(email)) {
            this.showFieldError(this.emailInput, 'Email inválido');
            return false;
        }
        
        this.clearFieldError(this.emailInput);
        return true;
    }

    validatePassword() {
        const password = this.passwordInput.value;
        
        if (!password) {
            this.showFieldError(this.passwordInput, 'Senha é obrigatória');
            return false;
        }
        
        if (password.length < 8) {
            this.showFieldError(this.passwordInput, 'Senha deve ter pelo menos 8 caracteres');
            return false;
        }
        
        if (password.includes(' ')) {
            this.showFieldError(this.passwordInput, 'Senha não pode conter espaços');
            return false;
        }
        
        this.clearFieldError(this.passwordInput);
        return true;
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    showFieldError(field, message) {
        // Remover erro anterior
        this.clearFieldError(field);
        
        // Adicionar classe de erro
        field.style.borderColor = '#ff3b30';
        field.style.boxShadow = '0 0 0 3px rgba(255, 59, 48, 0.1)';
        
        // Criar elemento de erro
        const errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        errorElement.textContent = message;
        errorElement.style.cssText = `
            color: #ff3b30;
            font-size: 0.75rem;
            margin-top: 0.25rem;
            font-weight: 400;
        `;
        
        // Inserir após o campo
        field.parentNode.insertBefore(errorElement, field.nextSibling);
    }

    clearFieldError(field) {
        // Remover estilo de erro
        field.style.borderColor = '';
        field.style.boxShadow = '';
        
        // Remover elemento de erro
        const errorElement = field.parentNode.querySelector('.field-error');
        if (errorElement) {
            errorElement.remove();
        }
    }

    showError(message, type = 'error') {
        this.errorContainer.textContent = message;
        this.errorContainer.style.display = 'block';
        
        if (type === 'error') {
            this.errorContainer.style.backgroundColor = 'rgba(255, 59, 48, 0.1)';
            this.errorContainer.style.color = '#ff3b30';
            this.errorContainer.style.border = '1px solid rgba(255, 59, 48, 0.2)';
        } else if (type === 'success') {
            this.errorContainer.style.backgroundColor = 'rgba(52, 199, 89, 0.1)';
            this.errorContainer.style.color = '#34c759';
            this.errorContainer.style.border = '1px solid rgba(52, 199, 89, 0.2)';
        } else if (type === 'info') {
            this.errorContainer.style.backgroundColor = 'rgba(0, 113, 227, 0.1)';
            this.errorContainer.style.color = '#0071e3';
            this.errorContainer.style.border = '1px solid rgba(0, 113, 227, 0.2)';
        }
    }

    clearError() {
        this.errorContainer.style.display = 'none';
    }

    async checkDatabaseConnection() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/check_db`);
            const data = await response.json();
            
            if (data.success) {
                console.log('✅ Banco de dados conectado:', data.message);
            } else {
                console.warn('⚠️ Problema com banco de dados:', data.message);
                this.showError('Aviso: Problema de conexão com banco de dados', 'info');
            }
        } catch (error) {
            console.warn('⚠️ Não foi possível verificar banco de dados:', error.message);
            this.showError('Aviso: Servidor Flask não está rodando. Execute "python app.py"', 'info');
        }
    }

    async handleSubmit() {
        // Limpar erros anteriores
        this.clearError();
        
        // Validar campos
        const isEmailValid = this.validateEmail();
        const isPasswordValid = this.validatePassword();
        
        if (!isEmailValid || !isPasswordValid) {
            return;
        }
        
        // Desabilitar botão durante a requisição
        this.submitButton.disabled = true;
        this.submitButton.textContent = 'Entrando...';
        
        try {
            // Preparar dados
            const formData = {
                email: this.emailInput.value.trim().toLowerCase(),
                password: this.passwordInput.value
            };
            
            // Fazer requisição para validação
            const response = await this.validateWithServer(formData);
            
            if (response.valid) {
                // Login bem-sucedido
                console.log('Login realizado com sucesso!');
                console.log('Resposta do servidor:', response);
                
                // Armazenar dados do usuário
                localStorage.setItem('user', JSON.stringify(response.user));
                
                // Redirecionar para o dashboard
                console.log('Redirecionando para /overview...');
                window.location.href = '/overview';
                
            } else {
                // Login falhou
                console.log('Login falhou:', response);
                this.showError(response.message || 'Erro ao fazer login');
            }
            
        } catch (error) {
            console.error('Erro na validação:', error);
            this.showError('Erro de conexão. Verifique se o servidor Flask está rodando (python app.py)');
        } finally {
            // Reabilitar botão
            this.submitButton.disabled = false;
            this.submitButton.textContent = 'Login';
        }
    }

    async validateWithServer(formData) {
        try {
            console.log('Enviando requisição para:', `${this.apiBaseUrl}/api/validate_user`);
            console.log('Dados enviados:', formData);
            
            const response = await fetch(`${this.apiBaseUrl}/api/validate_user`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(formData)
            });
            
            console.log('Resposta recebida:', response);
            const data = await response.json();
            console.log('Dados da resposta:', data);
            
            if (!response.ok) {
                throw new Error(data.message || 'Erro na requisição');
            }
            
            return data;
            
        } catch (error) {
            console.error('Erro na requisição:', error);
            throw error;
        }
    }

    // Método para validar dados do banco de dados
    async validateDatabaseCredentials(email, password) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/validate_user`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            return data;
            
        } catch (error) {
            console.error('Erro na validação do banco:', error);
            return {
                valid: false,
                message: 'Erro de conexão com o banco de dados'
            };
        }
    }
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se estamos na página de login
    if (document.querySelector('.login-form')) {
        new SellerLogin();
    }
});

// Função global para validação externa
window.validateSellerLogin = function(email, password) {
    const validator = new SellerLogin();
    return validator.validateDatabaseCredentials(email, password);
};

// Função para limpar dados do usuário (logout)
window.clearUserData = function() {
    localStorage.removeItem('user');
    sessionStorage.clear();
};

// Função para obter dados do usuário logado
window.getCurrentUser = function() {
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
};

// Função para verificar se usuário está logado
window.isUserLoggedIn = function() {
    return getCurrentUser() !== null;
};
