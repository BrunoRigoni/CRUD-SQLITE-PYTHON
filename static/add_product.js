// Add Product JavaScript

class AddProductManager {
    constructor() {
        this.form = document.getElementById('addProductForm');
        this.imageInput = document.getElementById('productImage');
        this.imagePreview = document.getElementById('imagePreview');
        this.messageDiv = document.getElementById('message');
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadUserInfo();
    }

    setupEventListeners() {
        // Image preview
        this.imageInput.addEventListener('change', (e) => {
            this.handleImagePreview(e);
        });

        // Form submission
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });

        // Real-time validation
        this.setupValidation();
    }

    handleImagePreview(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                this.imagePreview.src = e.target.result;
                this.imagePreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    }

    setupValidation() {
        const priceInput = document.getElementById('productPrice');
        const quantityInput = document.getElementById('productQuantity');

        // Price validation
        priceInput.addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            if (value < 0) {
                e.target.value = 0;
            }
        });

        // Quantity validation
        quantityInput.addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            if (value < 0) {
                e.target.value = 0;
            }
        });
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

    showMessage(message, type = 'error') {
        this.messageDiv.textContent = message;
        this.messageDiv.className = type === 'error' ? 'error-message' : 'success-message';
        this.messageDiv.style.display = 'block';
    }

    clearMessage() {
        this.messageDiv.style.display = 'none';
    }

    validateForm() {
        const name = document.getElementById('productName').value.trim();
        const price = parseFloat(document.getElementById('productPrice').value);
        const quantity = parseInt(document.getElementById('productQuantity').value);
        const category = document.getElementById('productCategory').value.trim();
        const image = this.imageInput.files[0];

        if (!name) {
            this.showMessage('Product name is required');
            return false;
        }

        if (isNaN(price) || price < 0) {
            this.showMessage('Please enter a valid price');
            return false;
        }

        if (isNaN(quantity) || quantity < 0) {
            this.showMessage('Please enter a valid quantity');
            return false;
        }

        if (!category) {
            this.showMessage('Category is required');
            return false;
        }

        if (!image) {
            this.showMessage('Product image is required');
            return false;
        }

        return true;
    }

    async handleSubmit() {
        this.clearMessage();

        if (!this.validateForm()) {
            return;
        }

        const submitButton = this.form.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Saving...';

        try {
            const formData = new FormData();
            
            // Add form data
            formData.append('name', document.getElementById('productName').value.trim());
            formData.append('price', parseFloat(document.getElementById('productPrice').value));
            formData.append('quantity', parseInt(document.getElementById('productQuantity').value));
            formData.append('category', document.getElementById('productCategory').value.trim());
            formData.append('image', this.imageInput.files[0]);

            const response = await fetch('/api/add_product', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.showMessage('Product added successfully!', 'success');
                setTimeout(() => {
                    window.location.href = '/products';
                }, 1500);
            } else {
                this.showMessage(data.message || 'Error adding product');
            }

        } catch (error) {
            console.error('Error:', error);
            this.showMessage('Error connecting to server');
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new AddProductManager();
}); 