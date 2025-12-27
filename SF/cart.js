// Cart Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Cart items data
    let cartItems = JSON.parse(localStorage.getItem('cart')) || [
        {
            id: 1,
            name: 'Digital Blood Pressure Monitor',
            category: 'Monitoring Devices',
            price: 1299,
            quantity: 1,
            image: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80',
            sku: 'BP-2023-01'
        },
        {
            id: 3,
            name: 'Infrared Digital Thermometer',
            category: 'Diagnostic Tools',
            price: 450,
            quantity: 2,
            image: 'https://images.unsplash.com/photo-1559757175-0eb30cd8c063?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80',
            sku: 'TH-2023-05'
        },
        {
            id: 2,
            name: 'Portable Oxygen Concentrator',
            category: 'Respiratory Care',
            price: 18500,
            quantity: 1,
            image: 'https://images.unsplash.com/photo-1551601651-2a8555f1a136?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80',
            sku: 'OX-2023-12',
            requiresPrescription: true
        }
    ];

    // DOM Elements
    const cartTable = document.querySelector('.cart-table');
    const cartHeaderCount = document.querySelector('.cart-header h2');
    const clearCartBtn = document.querySelector('.clear-cart');
    const updateCartBtn = document.querySelector('.update-cart');
    const promoInput = document.querySelector('.promo-input input');
    const applyPromoBtn = document.querySelector('.promo-input button');
    const checkoutBtn = document.querySelector('.checkout-btn');
    
    // Calculate totals
    function calculateTotals() {
        const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        const shipping = 200;
        const tax = subtotal * 0.14;
        const discount = 1000; // From promo code
        const total = subtotal + shipping + tax - discount;
        
        // Update UI
        document.querySelectorAll('.summary-row:nth-child(1) span:last-child').forEach(el => {
            el.textContent = `EGP ${subtotal.toLocaleString()}`;
        });
        
        document.querySelector('.summary-row:nth-child(2) span:last-child').textContent = `EGP ${shipping.toLocaleString()}`;
        document.querySelector('.summary-row:nth-child(3) span:last-child').textContent = `EGP ${tax.toLocaleString()}`;
        document.querySelector('.summary-row.total span:last-child').textContent = `EGP ${total.toLocaleString()}`;
        
        // Update header count
        const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);
        cartHeaderCount.textContent = `Your Cart Items (${totalItems})`;
    }
    
    // Render cart items
    function renderCartItems() {
        const cartItemsContainer = cartTable.querySelector('.cart-table-header').nextElementSibling;
        if (!cartItemsContainer) return;
        
        // Remove existing rows (except header)
        while (cartItemsContainer.nextElementSibling) {
            cartItemsContainer.nextElementSibling.remove();
        }
        
        cartItems.forEach((item, index) => {
            const row = document.createElement('div');
            row.className = `cart-item-row ${item.requiresPrescription ? 'prescription-item' : ''}`;
            
            row.innerHTML = `
                <div class="cart-col product">
                    <div class="product-info">
                        <img src="${item.image}" alt="${item.name}">
                        <div>
                            <h4>${item.name}</h4>
                            <span class="product-category">${item.category}</span>
                            <div class="product-sku">SKU: ${item.sku}</div>
                            ${item.requiresPrescription ? `
                                <div class="prescription-notice">
                                    <i class="fas fa-exclamation-triangle"></i>
                                    Requires prescription approval
                                </div>
                            ` : ''}
                        </div>
                    </div>
                </div>
                <div class="cart-col price">
                    <div class="price-amount">EGP ${item.price.toLocaleString()}</div>
                </div>
                <div class="cart-col quantity">
                    <div class="quantity-control">
                        <button class="quantity-btn minus" data-index="${index}">-</button>
                        <input type="number" value="${item.quantity}" min="1" max="10" class="quantity-input" data-index="${index}">
                        <button class="quantity-btn plus" data-index="${index}">+</button>
                    </div>
                </div>
                <div class="cart-col total">
                    <div class="total-amount">EGP ${(item.price * item.quantity).toLocaleString()}</div>
                </div>
                <div class="cart-col actions">
                    <button class="remove-btn" data-index="${index}"><i class="fas fa-trash"></i></button>
                    ${item.requiresPrescription ? `
                        <button class="upload-btn" data-index="${index}">
                            <i class="fas fa-upload"></i> Upload Prescription
                        </button>
                    ` : `
                        <button class="wishlist-btn" data-index="${index}"><i class="far fa-heart"></i></button>
                    `}
                </div>
            `;
            
            cartTable.appendChild(row);
        });
        
        // Add event listeners
        addCartEventListeners();
        calculateTotals();
    }
    
    // Add event listeners to cart items
    function addCartEventListeners() {
        // Quantity buttons
        document.querySelectorAll('.quantity-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                const isPlus = this.classList.contains('plus');
                
                if (isPlus) {
                    cartItems[index].quantity += 1;
                } else {
                    cartItems[index].quantity -= 1;
                    if (cartItems[index].quantity <= 0) {
                        cartItems.splice(index, 1);
                    }
                }
                
                renderCartItems();
                saveCartToLocalStorage();
                showNotification('Cart updated', 'success');
            });
        });
        
        // Quantity inputs
        document.querySelectorAll('.quantity-input').forEach(input => {
            input.addEventListener('change', function() {
                const index = parseInt(this.dataset.index);
                const newQuantity = parseInt(this.value);
                
                if (newQuantity >= 1 && newQuantity <= 10) {
                    cartItems[index].quantity = newQuantity;
                    renderCartItems();
                    saveCartToLocalStorage();
                } else {
                    this.value = cartItems[index].quantity;
                    showNotification('Quantity must be between 1 and 10', 'error');
                }
            });
        });
        
        // Remove buttons
        document.querySelectorAll('.remove-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                const itemName = cartItems[index].name;
                
                cartItems.splice(index, 1);
                renderCartItems();
                saveCartToLocalStorage();
                showNotification(`${itemName} removed from cart`, 'info');
            });
        });
        
        // Wishlist buttons
        document.querySelectorAll('.wishlist-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                const icon = this.querySelector('i');
                icon.classList.toggle('far');
                icon.classList.toggle('fas');
                
                showNotification('Added to wishlist!', 'success');
            });
        });
        
        // Upload prescription buttons
        document.querySelectorAll('.upload-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const modal = document.getElementById('prescriptionModal');
                if (modal) {
                    modal.classList.add('active');
                    document.querySelector('.modal-overlay').classList.add('active');
                }
            });
        });
    }
    
    // Save cart to localStorage
    function saveCartToLocalStorage() {
        localStorage.setItem('cart', JSON.stringify(cartItems));
    }
    
    // Clear cart
    function clearCart() {
        if (cartItems.length === 0) {
            showNotification('Cart is already empty', 'info');
            return;
        }
        
        if (confirm('Are you sure you want to clear your cart?')) {
            cartItems = [];
            renderCartItems();
            saveCartToLocalStorage();
            showNotification('Cart cleared', 'success');
        }
    }
    
    // Apply promo code
    function applyPromoCode() {
        const code = promoInput.value.trim().toUpperCase();
        
        if (!code) {
            showNotification('Please enter a promo code', 'error');
            return;
        }
        
        // Sample valid codes
        const validCodes = {
            'MEDICAL10': 1000,
            'HEALTH15': 1500,
            'NEWCUSTOMER': 500
        };
        
        if (validCodes[code]) {
            const discount = validCodes[code];
            showNotification(`Promo code applied! You saved EGP ${discount}`, 'success');
            promoInput.value = '';
            
            // In a real app, you would update the discount calculation
        } else {
            showNotification('Invalid promo code', 'error');
        }
    }
    
    // Proceed to checkout
    function proceedToCheckout() {
        if (cartItems.length === 0) {
            showNotification('Your cart is empty', 'error');
            return;
        }
        
        // Check if any prescription items have uploaded prescriptions
        const prescriptionItems = cartItems.filter(item => item.requiresPrescription);
        if (prescriptionItems.length > 0) {
            showNotification('Please upload prescriptions for prescription-required items before checkout', 'error');
            return;
        }
        
        // Save cart for checkout page
        localStorage.setItem('checkoutCart', JSON.stringify(cartItems));
        
        // Redirect to checkout page
        window.location.href = 'checkout.html';
    }
    
    // Show notification
    function showNotification(message, type = 'info') {
        // Reuse the notification function from app.js if available
        if (window.showNotification) {
            window.showNotification(message, type);
            return;
        }
        
        // Fallback notification
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <p>${message}</p>
            <button class="close-notification">&times;</button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
        
        notification.querySelector('.close-notification').addEventListener('click', () => {
            notification.remove();
        });
    }
    
    // Initialize cart
    function init() {
        // Load cart from localStorage if available
        const savedCart = JSON.parse(localStorage.getItem('cart'));
        if (savedCart && savedCart.length > 0) {
            cartItems = savedCart;
        }
        
        renderCartItems();
        
        // Event listeners
        if (clearCartBtn) {
            clearCartBtn.addEventListener('click', clearCart);
        }
        
        if (updateCartBtn) {
            updateCartBtn.addEventListener('click', () => {
                saveCartToLocalStorage();
                showNotification('Cart updated successfully', 'success');
            });
        }
        
        if (applyPromoBtn) {
            applyPromoBtn.addEventListener('click', applyPromoCode);
        }
        
        if (promoInput) {
            promoInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    applyPromoCode();
                }
            });
        }
        
        if (checkoutBtn) {
            checkoutBtn.addEventListener('click', proceedToCheckout);
        }
        
        // Initialize prescription modal if exists
        initPrescriptionModal();
    }
    
    // Initialize prescription modal
    function initPrescriptionModal() {
        const modal = document.getElementById('prescriptionModal');
        if (!modal) return;
        
        const closeModalBtns = document.querySelectorAll('.close-modal, .cancel-upload');
        const uploadArea = document.querySelector('.upload-area');
        const fileInput = document.getElementById('prescriptionFile');
        const uploadSubmitBtn = document.querySelector('.upload-submit');
        const modalOverlay = document.querySelector('.modal-overlay');
        
        uploadArea.addEventListener('click', () => fileInput.click());
        
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                const fileName = this.files[0].name;
                uploadArea.innerHTML = `
                    <i class="fas fa-check-circle"></i>
                    <h4>File Selected</h4>
                    <p>${fileName}</p>
                    <button class="btn btn-sm btn-outline change-file">Change File</button>
                `;
                
                document.querySelector('.change-file')?.addEventListener('click', (e) => {
                    e.stopPropagation();
                    fileInput.click();
                });
            }
        });
        
        uploadSubmitBtn.addEventListener('click', () => {
            if (!fileInput.files.length) {
                showNotification('Please select a prescription file', 'error');
                return;
            }
            
            // Here you would normally upload to server
            showNotification('Prescription uploaded successfully! Our team will review it shortly.', 'success');
            modal.classList.remove('active');
            modalOverlay.classList.remove('active');
        });
        
        closeModalBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                modal.classList.remove('active');
                modalOverlay.classList.remove('active');
            });
        });
        
        modalOverlay.addEventListener('click', () => {
            modal.classList.remove('active');
            modalOverlay.classList.remove('active');
        });
    }
    
    // Add necessary styles
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            z-index: 2000;
            animation: slideIn 0.3s ease;
            border-left: 4px solid #2a6e97;
        }
        
        .notification.success {
            border-left-color: #28a745;
        }
        
        .notification.error {
            border-left-color: #ff6b6b;
        }
        
        .notification.info {
            border-left-color: #17a2b8;
        }
        
        .notification p {
            margin: 0;
            color: #343a40;
        }
        
        .close-notification {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #6c757d;
        }
        
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
        
        .fade-out {
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        }
    `;
    document.head.appendChild(style);
    
    // Start the cart
    init();
});