// Products JavaScript

class ProductsManager {
    constructor() {
        this.productsContainer = document.getElementById('products-container');
        this.init();
    }

    init() {
        this.loadUserInfo();
        this.loadProducts();
    }

    loadUserInfo() {
        const userData = localStorage.getItem('user');
        if (userData) {
            const user = JSON.parse(userData);
            const userNameElement = document.getElementById('user-name');
            if (userNameElement) {
                userNameElement.textContent = `Welcome, ${user.name}`;
            }
        }
    }

    async loadProducts() {
        try {
            const response = await fetch('/api/get_products');
            const data = await response.json();

            if (response.ok && data.success) {
                this.displayProducts(data.products);
            } else {
                this.showError('Error loading products');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Error connecting to server');
        }
    }

    displayProducts(products) {
        if (!products || products.length === 0) {
            this.productsContainer.innerHTML = `
                <div class="no-products">
                    <h3>No products found</h3>
                    <p>Start by adding your first product!</p>
                </div>
            `;
            return;
        }

        const productsHTML = products.map(product => this.createProductCard(product)).join('');
        this.productsContainer.innerHTML = `
            <div class="products-grid">
                ${productsHTML}
            </div>
        `;
    }

    createProductCard(product) {
        const imageUrl = product.image_path ? `/static/uploads/${product.image_path}` : '/static/img/default-product.png';
        
        return `
            <div class="product-card" data-product-id="${product.id}">
                <img src="${imageUrl}" alt="${product.nome}" class="product-image" onerror="this.src='/static/img/default-product.png'">
                <div class="product-info">
                    <h3>${product.nome}</h3>
                    <div class="product-price">R$ ${product.preco.toFixed(2)}</div>
                    <div class="product-details">
                        <p><strong>Quantity:</strong> ${product.quantidade}</p>
                        <p><strong>Category:</strong> ${product.categoria || 'N/A'}</p>
                        <p><strong>Added:</strong> ${new Date(product.data_cadastro).toLocaleDateString()}</p>
                    </div>
                    <div class="product-actions">
                        <button class="btn btn-warning" onclick="productsManager.editProduct(${product.id})">
                            <i class="icon">✏️</i> Edit
                        </button>
                        <button class="btn btn-danger" onclick="productsManager.deleteProduct(${product.id})">
                            <i class="icon">🗑️</i> Delete
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    async editProduct(productId) {
        // Redirect to edit page (to be implemented)
        window.location.href = `/edit_product/${productId}`;
    }

    async deleteProduct(productId) {
        if (!confirm('Are you sure you want to delete this product?')) {
            return;
        }

        try {
            const response = await fetch(`/api/delete_product/${productId}`, {
                method: 'DELETE'
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Reload products
                this.loadProducts();
            } else {
                this.showError(data.message || 'Error deleting product');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Error connecting to server');
        }
    }

    showError(message) {
        this.productsContainer.innerHTML = `
            <div class="error-message">
                <h3>Error</h3>
                <p>${message}</p>
            </div>
        `;
    }
}

// Initialize when DOM is loaded
let productsManager;
document.addEventListener('DOMContentLoaded', function() {
    productsManager = new ProductsManager();
}); 