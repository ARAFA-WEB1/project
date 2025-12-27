// Medical Store Main JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Cart functionality
    const cartSidebar = document.querySelector('.cart-sidebar');
    const cartOverlay = document.querySelector('.cart-overlay');
    const cartButtons = document.querySelectorAll('.cart-icon, .add-to-cart');
    const closeCartBtn = document.querySelector('.close-cart');
    
    // Toggle cart sidebar
    function toggleCart() {
        cartSidebar.classList.toggle('active');
        cartOverlay.classList.toggle('active');
        updateCartCount();
        loadCartItems();
    }
    
    // Update cart count in header
    function updateCartCount() {
        const cartItems = JSON.parse(localStorage.getItem('cart')) || [];
        const cartCount = document.querySelectorAll('.cart-count');
        const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);
        
        cartCount.forEach(count => {
            count.textContent = totalItems || '';
        });
    }
    
    // Load cart items into sidebar
    function loadCartItems() {
        const cartItems = JSON.parse(localStorage.getItem('cart')) || [];
        const cartItemsContainer = document.querySelector('.cart-items');
        const totalPriceElement = document.querySelector('.total-price');
        
        cartItemsContainer.innerHTML = '';
        
        if (cartItems.length === 0) {
            cartItemsContainer.innerHTML = `
                <div class="empty-cart">
                    <i class="fas fa-shopping-cart"></i>
                    <p>Your cart is empty</p>
                    <a href="products.html" class="btn btn-primary">Start Shopping</a>
                </div>
            `;
            totalPriceElement.textContent = 'EGP 0.00';
            return;
        }
        
        let total = 0;
        
        cartItems.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            
            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item';
            cartItem.innerHTML = `
                <div class="cart-item-image">
                    <img src="${item.image}" alt="${item.name}">
                </div>
                <div class="cart-item-info">
                    <h4 class="cart-item-title">${item.name}</h4>
                    <div class="cart-item-price">EGP ${item.price.toFixed(2)}</div>
                    <div class="cart-item-actions">
                        <button class="quantity-btn minus" data-id="${item.id}">-</button>
                        <span class="quantity">${item.quantity}</span>
                        <button class="quantity-btn plus" data-id="${item.id}">+</button>
                        <button class="remove-item" data-id="${item.id}">Remove</button>
                    </div>
                </div>
            `;
            cartItemsContainer.appendChild(cartItem);
        });
        
        totalPriceElement.textContent = `EGP ${total.toFixed(2)}`;
        
        // Add event listeners to new buttons
        document.querySelectorAll('.quantity-btn.minus').forEach(btn => {
            btn.addEventListener('click', updateCartItem);
        });
        
        document.querySelectorAll('.quantity-btn.plus').forEach(btn => {
            btn.addEventListener('click', updateCartItem);
        });
        
        document.querySelectorAll('.remove-item').forEach(btn => {
            btn.addEventListener('click', removeCartItem);
        });
    }
    
    // Add to cart functionality
    function addToCart(productId) {
        // Sample product data - in real app, this would come from a database
        const products = {
            1: {
                id: 1,
                name: 'Digital Blood Pressure Monitor',
                price: 1299,
                image: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'
            },
            2: {
                id: 2,
                name: 'Portable Oxygen Concentrator',
                price: 18500,
                image: 'https://images.unsplash.com/photo-1551601651-2a8555f1a136?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'
            },
            3: {
                id: 3,
                name: 'Infrared Digital Thermometer',
                price: 450,
                image: 'https://images.unsplash.com/photo-1559757175-0eb30cd8c063?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'
            },
            4: {
                id: 4,
                name: 'Electric Adjustable Hospital Bed',
                price: 32000,
                image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'
            }
        };
        
        const product = products[productId];
        if (!product) return;
        
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        const existingItem = cart.find(item => item.id === productId);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({
                id: product.id,
                name: product.name,
                price: product.price,
                image: product.image,
                quantity: 1
            });
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
        
        // Show success notification
        showNotification('Product added to cart!', 'success');
        updateCartCount();
        
        // Auto-open cart on mobile
        if (window.innerWidth < 768) {
            toggleCart();
        }
    }
    
    // Update cart item quantity
    function updateCartItem(e) {
        const productId = parseInt(e.target.dataset.id);
        const isPlus = e.target.classList.contains('plus');
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        const itemIndex = cart.findIndex(item => item.id === productId);
        
        if (itemIndex !== -1) {
            if (isPlus) {
                cart[itemIndex].quantity += 1;
            } else {
                cart[itemIndex].quantity -= 1;
                if (cart[itemIndex].quantity <= 0) {
                    cart.splice(itemIndex, 1);
                }
            }
            
            localStorage.setItem('cart', JSON.stringify(cart));
            loadCartItems();
            updateCartCount();
        }
    }
    
    // Remove cart item
    function removeCartItem(e) {
        const productId = parseInt(e.target.dataset.id);
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        cart = cart.filter(item => item.id !== productId);
        
        localStorage.setItem('cart', JSON.stringify(cart));
        loadCartItems();
        updateCartCount();
        showNotification('Item removed from cart', 'info');
    }
    
    // Show notification
    function showNotification(message, type = 'info') {
        // Remove any existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(n => n.remove());
        
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <p>${message}</p>
            <button class="close-notification">&times;</button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
        
        // Close button
        notification.querySelector('.close-notification').addEventListener('click', () => {
            notification.remove();
        });
    }
    
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
            navMenu.classList.toggle('active');
        });
    }
    
    // Newsletter form
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            
            // In a real app, you would send this to your server
            showNotification('Thank you for subscribing!', 'success');
            this.reset();
        });
    }
    
    // Initialize event listeners
    cartButtons.forEach(btn => {
        if (btn.classList.contains('add-to-cart')) {
            btn.addEventListener('click', function() {
                const productId = parseInt(this.dataset.id);
                addToCart(productId);
            });
        } else {
            btn.addEventListener('click', toggleCart);
        }
    });
    
    if (closeCartBtn) {
        closeCartBtn.addEventListener('click', toggleCart);
    }
    
    cartOverlay.addEventListener('click', toggleCart);
    
    // Prescription modal
    const prescriptionModal = document.getElementById('prescriptionModal');
    const prescriptionOverlay = document.querySelector('.modal-overlay');
    const uploadPrescriptionBtns = document.querySelectorAll('.upload-btn');
    const closeModalBtns = document.querySelectorAll('.close-modal, .cancel-upload');
    
    if (prescriptionModal) {
        uploadPrescriptionBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                prescriptionModal.classList.add('active');
                prescriptionOverlay.classList.add('active');
            });
        });
        
        closeModalBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                prescriptionModal.classList.remove('active');
                prescriptionOverlay.classList.remove('active');
            });
        });
        
        prescriptionOverlay.addEventListener('click', () => {
            prescriptionModal.classList.remove('active');
            prescriptionOverlay.classList.remove('active');
        });
        
        // File upload handling
        const uploadArea = document.querySelector('.upload-area');
        const fileInput = document.getElementById('prescriptionFile');
        const uploadSubmitBtn = document.querySelector('.upload-submit');
        
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
                
                // Add change file button listener
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
            
            // In real app, upload to server here
            showNotification('Prescription uploaded successfully! Our team will review it shortly.', 'success');
            prescriptionModal.classList.remove('active');
            prescriptionOverlay.classList.remove('active');
        });
    }
    
    // Add notification styles
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 1rem 1.5rem;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            z-index: 2000;
            animation: slideIn 0.3s ease;
            border-left: 4px solid var(--primary);
        }
        
        .notification.success {
            border-left-color: var(--secondary);
        }
        
        .notification.error {
            border-left-color: var(--accent);
        }
        
        .notification p {
            margin: 0;
            color: var(--dark);
        }
        
        .close-notification {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--gray);
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
        
        .empty-cart {
            text-align: center;
            padding: 3rem 1rem;
        }
        
        .empty-cart i {
            font-size: 3rem;
            color: var(--light-gray);
            margin-bottom: 1rem;
        }
        
        .empty-cart p {
            margin-bottom: 1.5rem;
            color: var(--gray);
        }
    `;
    document.head.appendChild(style);
    
    // Initialize cart count on page load
    updateCartCount();
});