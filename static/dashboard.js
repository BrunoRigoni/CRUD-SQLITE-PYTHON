// Dashboard JavaScript - Navegação e Funcionalidades

class Dashboard {
    constructor() {
        this.currentUser = null;
        this.init();
    }

    init() {
        this.loadUserData();
        this.setupNavigation();
        this.loadDashboardData();
        this.setupEventListeners();
    }

    loadUserData() {
        // Carregar dados do usuário do localStorage
        const userData = localStorage.getItem('user');
        if (userData) {
            this.currentUser = JSON.parse(userData);
            this.updateUserInfo();
        } else {
            // Se não há dados do usuário, redirecionar para login
            window.location.href = '/seller_login.html';
        }
    }

    updateUserInfo() {
        const userNameElement = document.getElementById('user-name');
        if (userNameElement && this.currentUser) {
            userNameElement.textContent = `Welcome, ${this.currentUser.name}`;
        }
    }

    setupNavigation() {
        // Marcar item ativo no menu
        const currentPath = window.location.pathname;
        const navItems = document.querySelectorAll('.nav-item');
        
        navItems.forEach(item => {
            const link = item.querySelector('.nav-link');
            if (link && link.getAttribute('href') === currentPath) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });

        // Adicionar event listeners para navegação
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');
                if (href && href !== '#') {
                    e.preventDefault();
                    this.navigateTo(href);
                }
            });
        });
    }

    navigateTo(path) {
        // Navegar para a página especificada
        // Se estiver usando Live Server, fazer requisição AJAX para Flask
        if (window.location.port === '5500' || window.location.hostname === '127.0.0.1') {
            this.loadPageContent(path);
        } else {
            window.location.href = path;
        }
    }

    async loadPageContent(path) {
        try {
            const response = await fetch(`http://localhost:5000${path}`);
            if (response.ok) {
                const html = await response.text();
                // Extrair apenas o conteúdo do main
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newContent = doc.querySelector('.main-content');
                const currentContent = document.querySelector('.main-content');
                
                if (newContent && currentContent) {
                    currentContent.innerHTML = newContent.innerHTML;
                    // Atualizar título da página
                    document.title = doc.title;
                    // Atualizar navegação ativa
                    this.updateActiveNavigation(path);
                    // Atualizar dados do dashboard se necessário
                    if (path === '/overview') {
                        this.loadDashboardData();
                    }
                }
            } else {
                console.error('Erro ao carregar página:', response.status);
            }
        } catch (error) {
            console.error('Erro na navegação:', error);
            // Fallback: tentar redirecionamento direto
            window.location.href = `http://localhost:5000${path}`;
        }
    }

    updateActiveNavigation(path) {
        // Remover classe active de todos os itens
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => item.classList.remove('active'));
        
        // Adicionar classe active ao item correto
        const activeLink = document.querySelector(`.nav-link[href="${path}"]`);
        if (activeLink) {
            activeLink.closest('.nav-item').classList.add('active');
        }
    }

    async loadDashboardData() {
        try {
            // Carregar estatísticas do dashboard
            const response = await fetch('/api/dashboard_stats');
            if (response.ok) {
                const data = await response.json();
                this.updateStats(data);
            } else {
                // Se não há dados, usar valores padrão
                this.updateStats({
                    total_products: 0,
                    total_customers: 0,
                    total_sales: 0,
                    total_revenue: 0
                });
            }
        } catch (error) {
            console.log('Usando dados padrão do dashboard');
            this.updateStats({
                total_products: 0,
                total_customers: 0,
                total_sales: 0,
                total_revenue: 0
            });
        }
    }

    updateStats(data) {
        const elements = {
            'total-products': data.total_products || 0,
            'total-customers': data.total_customers || 0,
            'total-sales': data.total_sales || 0,
            'total-revenue': `$${(data.total_revenue || 0).toFixed(2)}`
        };

        Object.keys(elements).forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = elements[id];
            }
        });
    }

    setupEventListeners() {
        // Event listener para logout
        const logoutBtn = document.querySelector('.logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.logout();
            });
        }

        // Event listeners para botões de ação rápida
        const actionBtns = document.querySelectorAll('.action-btn');
        actionBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const href = btn.getAttribute('onclick');
                if (href) {
                    // Extrair URL do onclick
                    const urlMatch = href.match(/location\.href='([^']+)'/);
                    if (urlMatch) {
                        e.preventDefault();
                        this.navigateTo(urlMatch[1]);
                    }
                }
            });
        });
    }

    logout() {
        // Limpar dados do usuário
        localStorage.removeItem('user');
        sessionStorage.clear();
        
        // Redirecionar para login
        window.location.href = '/seller_login.html';
    }

    // Função para mostrar notificações
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Estilos da notificação
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            animation: slideIn 0.3s ease-out;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        `;

        // Cores baseadas no tipo
        const colors = {
            success: '#34c759',
            error: '#ff3b30',
            warning: '#ff9500',
            info: '#0071e3'
        };

        notification.style.backgroundColor = colors[type] || colors.info;

        document.body.appendChild(notification);

        // Remover após 3 segundos
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    // Função para carregar dados em tempo real
    startRealTimeUpdates() {
        // Atualizar dados a cada 30 segundos
        setInterval(() => {
            this.loadDashboardData();
        }, 30000);
    }
}

// Inicializar dashboard quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    window.dashboardInstance = new Dashboard();
});

// Adicionar estilos CSS para animações de notificação
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(notificationStyles);

// Funções globais para uso em outras páginas
window.Dashboard = Dashboard;

// Função para navegar entre páginas
window.navigateTo = function(path) {
    if (window.dashboardInstance) {
        window.dashboardInstance.navigateTo(path);
    } else {
        // Fallback se a instância não estiver disponível
        if (window.location.port === '5500' || window.location.hostname === '127.0.0.1') {
            window.location.href = `http://localhost:5000${path}`;
        } else {
            window.location.href = path;
        }
    }
};

// Função para mostrar notificações
window.showNotification = function(message, type) {
    if (window.dashboardInstance) {
        window.dashboardInstance.showNotification(message, type);
    }
}; 