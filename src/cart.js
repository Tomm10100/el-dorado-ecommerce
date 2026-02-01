// Shopping Cart System for El Dorado
export class ShoppingCart {
  constructor() {
    this.items = this.loadCart();
    this.init();
  }

  init() {
    this.createCartUI();
    this.updateCartCount();
  }

  loadCart() {
    const saved = localStorage.getItem('eldorado-cart');
    return saved ? JSON.parse(saved) : [];
  }

  saveCart() {
    localStorage.setItem('eldorado-cart', JSON.stringify(this.items));
    this.updateCartCount();
  }

  addItem(product) {
    const existing = this.items.find(item => item.id === product.id);
    if (existing) {
      existing.quantity += 1;
    } else {
      this.items.push({ ...product, quantity: 1 });
    }
    this.saveCart();
    this.showNotification(`${product.name} added to cart`);
    this.renderCart();

    // Track add to cart event
    if (window.analytics) {
      window.analytics.trackAddToCart(product);
    }
  }

  removeItem(productId) {
    this.items = this.items.filter(item => item.id !== productId);
    this.saveCart();
    this.renderCart();
  }

  updateQuantity(productId, quantity) {
    const item = this.items.find(item => item.id === productId);
    if (item) {
      item.quantity = Math.max(1, quantity);
      this.saveCart();
      this.renderCart();
    }
  }

  getTotal() {
    return this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  }

  getItemCount() {
    return this.items.reduce((sum, item) => sum + item.quantity, 0);
  }

  updateCartCount() {
    const badge = document.querySelector('#cart-count');
    const count = this.getItemCount();
    if (badge) {
      badge.textContent = count;
      badge.style.display = count > 0 ? 'flex' : 'none';
    }
  }

  createCartUI() {
    // Create cart sidebar overlay
    const cartHTML = `
      <div id="cart-overlay" class="cart-overlay">
        <div class="cart-sidebar glass">
          <div class="cart-header">
            <h3 class="serif">YOUR CART</h3>
            <button id="close-cart" class="close-btn">&times;</button>
          </div>
          <div id="cart-items" class="cart-items"></div>
          <div class="cart-footer">
            <div class="cart-total">
              <span class="sans">TOTAL:</span>
              <span class="serif" id="cart-total">$0</span>
            </div>
            <button id="checkout-stripe" class="checkout-btn sans">
              CHECKOUT WITH CARD
            </button>
            <button id="checkout-crypto" class="checkout-btn crypto-btn sans">
              PAY WITH XRP
            </button>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', cartHTML);

    // Event listeners
    document.querySelector('#close-cart').addEventListener('click', () => this.closeCart());
    document.querySelector('#cart-overlay').addEventListener('click', (e) => {
      if (e.target.id === 'cart-overlay') this.closeCart();
    });

    document.querySelector('#checkout-stripe').addEventListener('click', () => this.checkoutStripe());
    document.querySelector('#checkout-crypto').addEventListener('click', () => this.checkoutCrypto());
  }

  openCart() {
    this.renderCart();
    document.querySelector('#cart-overlay').classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  closeCart() {
    document.querySelector('#cart-overlay').classList.remove('active');
    document.body.style.overflow = '';
  }

  renderCart() {
    const container = document.querySelector('#cart-items');

    if (this.items.length === 0) {
      container.innerHTML = `
        <div class="empty-cart sans">
          <p>Your cart is empty</p>
        </div>
      `;
      document.querySelector('#cart-total').textContent = '$0';
      return;
    }

    container.innerHTML = this.items.map(item => `
      <div class="cart-item">
        <img src="${item.img}" alt="${item.name}" class="cart-item-img">
        <div class="cart-item-details">
          <h4 class="serif">${item.name}</h4>
          <p class="sans">$${item.price}</p>
          <div class="quantity-controls">
            <button class="qty-btn" onclick="window.cart.updateQuantity(${item.id}, ${item.quantity - 1})">-</button>
            <span class="quantity">${item.quantity}</span>
            <button class="qty-btn" onclick="window.cart.updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
          </div>
        </div>
        <button class="remove-btn sans" onclick="window.cart.removeItem(${item.id})">
          &times;
        </button>
      </div>
    `).join('');

    document.querySelector('#cart-total').textContent = `$${this.getTotal()}`;
  }

  async checkoutStripe() {
    if (this.items.length === 0) {
      alert('Your cart is empty');
      return;
    }

    const stripePublicKey = import.meta.env.VITE_STRIPE_PUBLIC_KEY;
    if (!stripePublicKey || stripePublicKey.includes('YOUR_')) {
      alert('Stripe is not configured. Please set VITE_STRIPE_PUBLIC_KEY in .env');
      return;
    }

    try {
      // Dynamic import to keep initial bundle size low
      const { loadStripe } = await import('@stripe/stripe-js');
      const stripe = await loadStripe(stripePublicKey);

      // Track checkout initiation
      if (window.analytics) {
        window.analytics.trackInitiateCheckout(this.items, this.getTotal());
      }

      this.showNotification('Redirecting to secure checkout...');

      // MOCK IMPLEMENTATION FOR NOW - Needs manual Price ID updates
      // We will alert the user to mapped fields if Price IDs are missing

      alert('Redirecting to Stripe... (Requires Price IDs in production)');

      // To actually process payments securely without a backend, we need
      // "Client-only Checkout" which requires creating Products in Stripe Dashboard
      // and using their price_123 IDs.

    } catch (err) {
      console.error('Checkout failed:', err);
      alert('Unable to initiate checkout. Please try again.');
    }
  }

  checkoutCrypto() {
    if (this.items.length === 0) {
      alert('Your cart is empty');
      return;
    }

    // Show XRP payment modal
    this.showCryptoPayment();
  }

  showCryptoPayment() {
    const total = this.getTotal();
    // Example XRP conversion (you'll need real-time rate)
    const xrpAmount = (total / 0.50).toFixed(2); // Assuming XRP = $0.50 (UPDATE WITH REAL RATE)

    const modal = document.createElement('div');
    modal.className = 'crypto-modal';
    modal.innerHTML = `
      <div class="crypto-content glass">
        <h3 class="serif">Pay with XRP</h3>
        <div class="crypto-details">
          <p class="sans">Order Total: <strong>$${total} USD</strong></p>
          <p class="sans">XRP Amount: <strong>${xrpAmount} XRP</strong></p>
          <div class="xrp-address">
            <p class="sans">Send XRP to:</p>
            <code id="xrp-address">rYOUR_XRP_ADDRESS_HERE</code>
            <button class="copy-btn sans" onclick="navigator.clipboard.writeText(document.getElementById('xrp-address').textContent)">
              COPY ADDRESS
            </button>
          </div>
          <p class="sans" style="font-size: 0.75rem; opacity: 0.6; margin-top: 2rem;">
            After sending, email tommy@innovlead.ca with your transaction ID
          </p>
        </div>
        <button class="close-modal-btn sans" onclick="this.parentElement.parentElement.remove()">
          CLOSE
        </button>
      </div>
    `;

    document.body.appendChild(modal);
  }

  showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'cart-notification glass';
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => notification.classList.add('show'), 100);
    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => notification.remove(), 300);
    }, 2000);
  }

  clear() {
    this.items = [];
    this.saveCart();
    this.renderCart();
  }
}

// Initialize cart globally
window.cart = new ShoppingCart();
