// Seller Register JavaScript - Validação e Conexão com Flask (Live Server)

class SellerRegister {
    constructor() {
        this.form = document.getElementById('registerForm');
        this.nameInput = document.getElementById('name');
        this.emailInput = document.getElementById('email');
        this.passwordInput = document.getElementById('password');
        this.confirmPasswordInput = document.getElementById('confirmPassword');
        this.messageDiv = document.getElementById('message');
        this.apiBaseUrl = '';
        
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
        this.nameInput.addEventListener('blur', () => this.validateName());
        this.emailInput.addEventListener('blur', () => this.validateEmail());
        this.passwordInput.addEventListener('blur', () => this.validatePassword());
        this.confirmPasswordInput.addEventListener('blur', () => this.validateConfirmPassword());
        
        // Event listeners para limpar erros ao digitar
        this.nameInput.addEventListener('input', () => this.clearError());
        this.emailInput.addEventListener('input', () => this.clearError());
        this.passwordInput.addEventListener('input', () => this.clearError());
        this.confirmPasswordInput.addEventListener('input', () => this.clearError());
    }

    setupRealTimeValidation() {
        // Validação de nome em tempo real
        this.nameInput.addEventListener('input', (e) => {
            const name = e.target.value.trim();
            if (name && name.length < 2) {
                this.showFieldError(this.nameInput, 'Nome deve ter pelo menos 2 caracteres');
            } else {
                this.clearFieldError(this.nameInput);
            }
        });

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
            } else if (password && password.includes(' ')) {
                this.showFieldError(this.passwordInput, 'Senha não pode conter espaços');
            } else {
                this.clearFieldError(this.passwordInput);
            }
            
            // Validar confirmação de senha
            if (this.confirmPasswordInput.value) {
                this.validateConfirmPassword();
            }
        });

        // Validação de confirmação de senha em tempo real
        this.confirmPasswordInput.addEventListener('input', (e) => {
            if (e.target.value && e.target.value !== this.passwordInput.value) {
                this.showFieldError(this.confirmPasswordInput, 'Senhas não coincidem');
            } else {
                this.clearFieldError(this.confirmPasswordInput);
            }
        });
    }

    validateName() {
        const name = this.nameInput.value.trim();
        
        if (!name) {
            this.showFieldError(this.nameInput, 'Nome é obrigatório');
            return false;
        }
        
        if (name.length < 2) {
            this.showFieldError(this.nameInput, 'Nome deve ter pelo menos 2 caracteres');
            return false;
        }
        
        this.clearFieldError(this.nameInput);
        return true;
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

    validateConfirmPassword() {
        const confirmPassword = this.confirmPasswordInput.value;
        const password = this.passwordInput.value;
        
        if (!confirmPassword) {
            this.showFieldError(this.confirmPasswordInput, 'Confirmação de senha é obrigatória');
            return false;
        }
        
        if (confirmPassword !== password) {
            this.showFieldError(this.confirmPasswordInput, 'Senhas não coincidem');
            return false;
        }
        
        this.clearFieldError(this.confirmPasswordInput);
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
        const isNameValid = this.validateName();
        const isEmailValid = this.validateEmail();
        const isPasswordValid = this.validatePassword();
        const isConfirmPasswordValid = this.validateConfirmPassword();
        
        if (!isNameValid || !isEmailValid || !isPasswordValid || !isConfirmPasswordValid) {
            return;
        }
        
        // Desabilitar botão durante a requisição
        this.submitButton.disabled = true;
        this.submitButton.textContent = 'Registrando...';
        
        try {
            // Preparar dados
            const formData = {
                name: this.nameInput.value.trim(),
                email: this.emailInput.value.trim().toLowerCase(),
                password: this.passwordInput.value,
                confirm_password: this.confirmPasswordInput.value
            };
            
            // Fazer requisição para registro
            const response = await this.registerWithServer(formData);
            
            if (response.success) {
                // Registro bem-sucedido
                this.showError('Usuário registrado com sucesso! Redirecionando para login...', 'success');
                
                // Redirecionar após 2 segundos
                setTimeout(() => {
                    window.location.href = '/seller_login.html';
                }, 2000);
                
            } else {
                // Registro falhou
                this.showError(response.message || 'Erro ao registrar usuário');
            }
            
        } catch (error) {
            console.error('Erro no registro:', error);
            this.showError('Erro de conexão. Verifique se o servidor Flask está rodando (python app.py)');
        } finally {
            // Reabilitar botão
            this.submitButton.disabled = false;
            this.submitButton.textContent = 'Register';
        }
    }

    async registerWithServer(formData) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/seller_register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Erro na requisição');
            }
            
            return data;
            
        } catch (error) {
            console.error('Erro na requisição:', error);
            throw error;
        }
    }
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se estamos na página de registro
    if (document.querySelector('.login-form') && document.querySelector('input[name="name"]')) {
        new SellerRegister();
    }
}); 