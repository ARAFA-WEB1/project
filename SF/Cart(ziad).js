document.addEventListener('DOMContentLoaded', function () {

    /* =======================
       STATE
    ======================== */
    let cartItems = [];
    let appliedDiscount = 0;
    let activePrescriptionIndex = null;

    /* =======================
       DOM ELEMENTS
    ======================== */
    const cartTable = document.querySelector('.cart-table');
    const cartHeaderCount = document.querySelector('.cart-header h2');
    const clearCartBtn = document.querySelector('.clear-cart');
    const updateCartBtn = document.querySelector('.update-cart');
    const promoInput = document.querySelector('.promo-input input');
    const applyPromoBtn = document.querySelector('.promo-input button');
    const checkoutBtn = document.querySelector('.checkout-btn');

    /* =======================
       LOAD CART
    ======================== */
    function loadCart() {
        const savedCart = JSON.parse(localStorage.getItem('cart'));

        cartItems = savedCart && savedCart.length
            ? savedCart
            : [
                {
                    id: 1,
                    name: 'Digital Blood Pressure Monitor',
                    category: 'Monitoring Devices',
                    price: 1299,
                    quantity: 1,
                    image: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56',
                    sku: 'BP-2023-01'
                },
                {
                    id: 3,
                    name: 'Infrared Digital Thermometer',
                    category: 'Diagnostic Tools',
                    price: 450,
                    quantity: 2,
                    image: 'https://images.unsplash.com/photo-1559757175-0eb30cd8c063',
                    sku: 'TH-2023-05'
                },
                {
                    id: 2,
                    name: 'Portable Oxygen Concentrator',
                    category: 'Respiratory Care',
                    price: 18500,
                    quantity: 1,
                    image: 'https://images.unsplash.com/photo-1551601651-2a8555f1a136',
                    sku: 'OX-2023-12',
                    requiresPrescription: true,
                    prescriptionUploaded: false
                }
            ];
    }

    /* =======================
       SAVE CART
    ======================== */
    function saveCart() {
        localStorage.setItem('cart', JSON.stringify(cartItems));
    }

    /* =======================
       TOTALS
    ======================== */
    function calculateTotals() {
        const subtotal = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
        const shipping = cartItems.length ? 200 : 0;
        const tax = Math.round(subtotal * 0.14);
        const total = subtotal + shipping + tax - appliedDiscount;

        document.querySelector('.summary-row:nth-child(1) span:last-child').textContent =
            `EGP ${subtotal.toLocaleString()}`;
        document.querySelector('.summary-row:nth-child(2) span:last-child').textContent =
            `EGP ${shipping.toLocaleString()}`;
        document.querySelector('.summary-row:nth-child(3) span:last-child').textContent =
            `EGP ${tax.toLocaleString()}`;
        document.querySelector('.summary-row.total span:last-child').textContent =
            `EGP ${total.toLocaleString()}`;

        const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);
        cartHeaderCount.textContent = `Your Cart Items (${totalItems})`;
    }

    /* =======================
       RENDER CART
    ======================== */
    function renderCartItems() {
        cartTable.querySelectorAll('.cart-item-row').forEach(row => row.remove());

        cartItems.forEach((item, index) => {
            const row = document.createElement('div');
            row.className = 'cart-item-row';

            row.innerHTML = `
                <div class="cart-col product">
                    <img src="${item.image}" alt="${item.name}">
                    <div>
                        <h4>${item.name}</h4>
                        <div>SKU: ${item.sku}</div>
                        ${item.requiresPrescription ? `
                            <div class="prescription-notice">
                                ${item.prescriptionUploaded ? 'Prescription uploaded ✔' : 'Prescription required'}
                            </div>
                        ` : ''}
                    </div>
                </div>

                <div class="cart-col price">EGP ${item.price.toLocaleString()}</div>

                <div class="cart-col quantity">
                    <button class="minus" data-index="${index}">-</button>
                    <input type="number" min="1" max="10" value="${item.quantity}" data-index="${index}">
                    <button class="plus" data-index="${index}">+</button>
                </div>

                <div class="cart-col total">
                    EGP ${(item.price * item.quantity).toLocaleString()}
                </div>

                <div class="cart-col actions">
                    <button class="remove" data-index="${index}">🗑</button>
                    ${item.requiresPrescription ? `
                        <button class="upload" data-index="${index}">Upload Prescription</button>
                    ` : ''}
                </div>
            `;

            cartTable.appendChild(row);
        });

        addCartEventListeners();
        calculateTotals();
    }

    /* =======================
       EVENTS
    ======================== */
    function addCartEventListeners() {

        document.querySelectorAll('.plus').forEach(btn => {
            btn.onclick = () => {
                cartItems[btn.dataset.index].quantity++;
                saveCart();
                renderCartItems();
            };
        });

        document.querySelectorAll('.minus').forEach(btn => {
            btn.onclick = () => {
                if (cartItems[btn.dataset.index].quantity > 1) {
                    cartItems[btn.dataset.index].quantity--;
                    saveCart();
                    renderCartItems();
                }
            };
        });

        document.querySelectorAll('.remove').forEach(btn => {
            btn.onclick = () => {
                cartItems.splice(btn.dataset.index, 1);
                saveCart();
                renderCartItems();
            };
        });

        document.querySelectorAll('.upload').forEach(btn => {
            btn.onclick = () => {
                activePrescriptionIndex = btn.dataset.index;
                document.getElementById('prescriptionModal').classList.add('active');
                document.querySelector('.modal-overlay').classList.add('active');
            };
        });
    }

    /* =======================
       PROMO CODES
    ======================== */
    function applyPromoCode() {
        const codes = {
            MEDICAL10: 1000,
            HEALTH15: 1500,
            NEWCUSTOMER: 500
        };

        const code = promoInput.value.trim().toUpperCase();

        if (!codes[code]) {
            showNotification('Invalid promo code', 'error');
            return;
        }

        appliedDiscount = codes[code];
        promoInput.value = '';
        calculateTotals();
        showNotification(`Promo applied! You saved EGP ${appliedDiscount}`, 'success');
    }

    /* =======================
       CHECKOUT
    ======================== */
    function proceedToCheckout() {
        if (!cartItems.length) {
            showNotification('Your cart is empty', 'error');
            return;
        }

        const missingPrescription = cartItems.some(
            item => item.requiresPrescription && !item.prescriptionUploaded
        );

        if (missingPrescription) {
            showNotification('Upload all required prescriptions first', 'error');
            return;
        }

        localStorage.setItem('checkoutCart', JSON.stringify(cartItems));
        window.location.href = 'checkout.html';
    }

    /* =======================
       PRESCRIPTION MODAL
    ======================== */
    function initPrescriptionModal() {
        const modal = document.getElementById('prescriptionModal');
        const overlay = document.querySelector('.modal-overlay');
        const fileInput = document.getElementById('prescriptionFile');

        document.querySelector('.upload-submit').onclick = () => {
            if (!fileInput.files.length) {
                showNotification('Select a file first', 'error');
                return;
            }

            cartItems[activePrescriptionIndex].prescriptionUploaded = true;
            saveCart();
            renderCartItems();

            modal.classList.remove('active');
            overlay.classList.remove('active');

            showNotification('Prescription uploaded successfully', 'success');
        };

        overlay.onclick = () => {
            modal.classList.remove('active');
            overlay.classList.remove('active');
        };
    }

    /* =======================
       INIT
    ======================== */
    loadCart();
    renderCartItems();
    initPrescriptionModal();

    applyPromoBtn?.addEventListener('click', applyPromoCode);
    checkoutBtn?.addEventListener('click', proceedToCheckout);
    clearCartBtn?.addEventListener('click', () => {
        cartItems = [];
        saveCart();
        renderCartItems();
    });

});
