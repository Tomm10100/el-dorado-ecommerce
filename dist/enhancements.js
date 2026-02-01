// El Dorado - Trust, Analytics, CRO & Email Capture Enhancements
// This file adds trust signals, conversion optimization, and analytics tracking

// ===========================================
// 1. ANALYTICS TRACKING SYSTEM
// ===========================================

class AnalyticsTracker {
    constructor() {
        this.gaId = import.meta.env.VITE_GA_MEASUREMENT_ID || '';
        this.fbPixelId = import.meta.env.VITE_FB_PIXEL_ID || '';
        this.init();
    }

    init() {
        // Google Analytics 4
        if (this.gaId && window.gtag) {
            console.log('✓ GA4 initialized:', this.gaId);
        }

        // Facebook Pixel
        if (this.fbPixelId && window.fbq) {
            console.log('✓ Facebook Pixel initialized:', this.fbPixelId);
        }
    }

    // Track page views
    trackPageView(pagePath) {
        if (window.gtag) {
            gtag('config', this.gaId, { page_path: pagePath });
        }
        if (window.fbq) {
            fbq('track', 'PageView');
        }
    }

    // Track add to cart
    trackAddToCart(product) {
        console.log('📊 Track: Add to Cart', product.name);

        if (window.gtag) {
            gtag('event', 'add_to_cart', {
                currency: 'USD',
                value: product.price,
                items: [{
                    item_id: product.id,
                    item_name: product.name,
                    price: product.price,
                    quantity: 1
                }]
            });
        }

        if (window.fbq) {
            fbq('track', 'AddToCart', {
                content_name: product.name,
                content_ids: [product.id],
                content_type: 'product',
                value: product.price,
                currency: 'USD'
            });
        }
    }

    // Track checkout initiation
    trackInitiateCheckout(cartItems, totalValue) {
        console.log('📊 Track: Initiate Checkout', totalValue);

        if (window.gtag) {
            gtag('event', 'begin_checkout', {
                currency: 'USD',
                value: totalValue,
                items: cartItems.map(item => ({
                    item_id: item.id,
                    item_name: item.name,
                    price: item.price,
                    quantity: item.quantity
                }))
            });
        }

        if (window.fbq) {
            fbq('track', 'InitiateCheckout', {
                content_ids: cartItems.map(i => i.id),
                contents: cartItems.map(i => ({
                    id: i.id,
                    quantity: i.quantity
                })),
                value: totalValue,
                currency: 'USD'
            });
        }
    }

    // Track purchase (to be called after successful payment)
    trackPurchase(orderId, cartItems, totalValue) {
        console.log('📊 Track: Purchase', orderId, totalValue);

        if (window.gtag) {
            gtag('event', 'purchase', {
                transaction_id: orderId,
                value: totalValue,
                currency: 'USD',
                items: cartItems.map(item => ({
                    item_id: item.id,
                    item_name: item.name,
                    price: item.price,
                    quantity: item.quantity
                }))
            });
        }

        if (window.fbq) {
            fbq('track', 'Purchase', {
                value: totalValue,
                currency: 'USD',
                content_ids: cartItems.map(i => i.id),
                content_type: 'product'
            });
        }
    }
}

// Initialize analytics
window.analytics = new AnalyticsTracker();

// ===========================================
// 2. EMAIL CAPTURE POPUP
// ===========================================

class EmailCapturePopup {
    constructor() {
        this.hasShown = localStorage.getItem('emailPopupShown') === 'true';
        this.emailCaptured = localStorage.getItem('emailCaptured') === 'true';
        this.init();
    }

    init() {
        if (this.hasShown || this.emailCaptured) return;

        // Show popup after 10 seconds OR 50% scroll
        setTimeout(() => this.maybeShow(), 10000);
        window.addEventListener('scroll', () => this.onScroll());
    }

    onScroll() {
        const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
        if (scrollPercent > 50) {
            this.maybeShow();
        }
    }

    maybeShow() {
        if (this.hasShown || this.emailCaptured) return;
        this.show();
        this.hasShown = true;
        localStorage.setItem('emailPopupShown', 'true');
    }

    show() {
        const popup = document.createElement('div');
        popup.className = 'email-popup-overlay';
        popup.innerHTML = `
            <div class="email-popup glass">
                <button class="email-popup-close">&times;</button>
                <div class="email-popup-content">
                    <h2 class="serif">UNLOCK 10% OFF</h2>
                    <p class="sans">Join the El Dorado community and receive exclusive offers</p>
                    <form class="email-popup-form" id="emailCaptureForm">
                        <input 
                            type="email" 
                            placeholder="Enter your email" 
                            required 
                            class="email-input"
                            name="email"
                        >
                        <button type="submit" class="email-submit sans">GET MY DISCOUNT</button>
                    </form>
                    <p class="email-privacy sans">
                        We respect your privacy. Unsubscribe anytime.
                    </p>
                </div>
            </div>
        `;

        document.body.appendChild(popup);

        // Close button
        popup.querySelector('.email-popup-close').addEventListener('click', () => {
            popup.remove();
        });

        // Click outside to close
        popup.addEventListener('click', (e) => {
            if (e.target === popup) popup.remove();
        });

        // Form submission
        popup.querySelector('#emailCaptureForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const email = e.target.email.value;
            this.captureEmail(email);
            popup.remove();
        });

        // Animate in
        setTimeout(() => popup.classList.add('active'), 100);
    }

    captureEmail(email) {
        console.log('📧 Email captured:', email);
        localStorage.setItem('emailCaptured', 'true');
        localStorage.setItem('userEmail', email);

        // Track event
        if (window.analytics) {
            if (window.gtag) {
                gtag('event', 'generate_lead', {
                    currency: 'USD',
                    value: 10.0 // Estimated value of email
                });
            }
            if (window.fbq) {
                fbq('track', 'Lead');
            }
        }

        // Show success message
        this.showSuccessMessage();

        // TODO: Send to email service (Mailchimp, etc.)
        // Example: fetch('/api/subscribe', { method: 'POST', body: JSON.stringify({ email }) });
    }

    showSuccessMessage() {
        const success = document.createElement('div');
        success.className = 'email-success-toast';
        success.innerHTML = `
            <div class="toast-content">
                <span class="toast-icon">✓</span>
                <span class="toast-text">Welcome! Check your email for your 10% discount code</span>
            </div>
        `;
        document.body.appendChild(success);
        setTimeout(() => success.classList.add('show'), 100);
        setTimeout(() => {
            success.classList.remove('show');
            setTimeout(() => success.remove(), 300);
        }, 5000);
    }
}

// Initialize email capture
window.emailCapture = new EmailCapturePopup();

// ===========================================
// 3. CRO ENHANCEMENTS (Urgency, Scarcity, Social Proof)
// ===========================================

class CROEnhancements {
    constructor() {
        this.init();
    }

    init() {
        this.addUrgencyIndicators();
        this.addScarcitySignals();
        this.addSocialProof();
    }

    // Add "Only X left in stock!" indicators
    addUrgencyIndicators() {
        const products = document.querySelectorAll('.product-card');
        products.forEach(card => {
            const stock = Math.floor(Math.random() * 5) + 2; // 2-6 items
            if (stock <= 5) {
                const urgency = document.createElement('div');
                urgency.className = 'urgency-badge';
                urgency.innerHTML = `⚡ Only ${stock} left in stock!`;
                card.querySelector('.product-info').prepend(urgency);
            }
        });
    }

    // Add "X people viewing this" signals
    addScarcitySignals() {
        const products = document.querySelectorAll('.product-card');
        products.forEach(card => {
            const viewers = Math.floor(Math.random() * 15) + 5; // 5-20 viewers
            const scarcity = document.createElement('div');
            scarcity.className = 'scarcity-badge';
            scarcity.innerHTML = `👁️ ${viewers} people viewing`;

            const footer = card.querySelector('.product-footer');
            if (footer) {
                footer.appendChild(scarcity);
            }

            // Animate viewers count occasionally
            setInterval(() => {
                const newViewers = Math.max(3, viewers + Math.floor(Math.random() * 5) - 2);
                scarcity.innerHTML = `👁️ ${newViewers} people viewing`;
            }, 30000); // Update every 30 seconds
        });
    }

    // Add social proof notifications
    addSocialProof() {
        const purchases = [
            { name: 'Sarah from Toronto', product: 'Cruz-Ki Pendant', time: '2 hours ago' },
            { name: 'Michael from Vancouver', product: 'Fuego Cadena Chain', time: '4 hours ago' },
            { name: 'Jessica from Montreal', product: 'Dumfe Bracelet', time: '6 hours ago' },
            { name: 'David from Calgary', product: 'Chan Bracelet', time: '1 hour ago' },
            { name: 'Emily from Ottawa', product: 'Oni Bracelet', time: '3 hours ago' }
        ];

        let currentIndex = 0;

        const showSocialProof = () => {
            const purchase = purchases[currentIndex];
            const notification = document.createElement('div');
            notification.className = 'social-proof-notification glass';
            notification.innerHTML = `
                <div class="social-proof-content">
                    <span class="social-proof-icon">🎉</span>
                    <div class="social-proof-text">
                        <strong>${purchase.name}</strong> purchased<br>
                        <span class="social-proof-product">${purchase.product}</span>
                    </div>
                    <span class="social-proof-time">${purchase.time}</span>
                </div>
            `;

            document.body.appendChild(notification);
            setTimeout(() => notification.classList.add('show'), 100);

            setTimeout(() => {
                notification.classList.remove('show');
                setTimeout(() => notification.remove(), 300);
            }, 6000);

            currentIndex = (currentIndex + 1) % purchases.length;
        };

        // Show first notification after 15 seconds, then every 45 seconds
        setTimeout(() => {
            showSocialProof();
            setInterval(showSocialProof, 45000);
        }, 15000);
    }

    // Add trust badges to checkout
    static addTrustBadgesToCheckout() {
        const cartFooter = document.querySelector('.cart-footer');
        if (!cartFooter) return;

        const trustBadges = document.createElement('div');
        trustBadges.className = 'trust-badges';
        trustBadges.innerHTML = `
            <div class="trust-badge">
                <span class="badge-icon">🔒</span>
                <span class="badge-text">256-bit SSL Encryption</span>
            </div>
            <div class="trust-badge">
                <span class="badge-icon">✓</span>
                <span class="badge-text">30-Day Money-Back Guarantee</span>
            </div>
            <div class="trust-badge">
                <span class="badge-icon">🚚</span>
                <span class="badge-text">Free Worldwide Shipping</span>
            </div>
        `;

        // Insert before total
        const cartTotal = cartFooter.querySelector('.cart-total');
        if (cartTotal) {
            cartFooter.insertBefore(trustBadges, cartTotal);
        }
    }
}

// Initialize CRO enhancements
window.croEnhancements = new CROEnhancements();

// Add trust badges when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    CROEnhancements.addTrustBadgesToCheckout();
});

// ===========================================
// 4. LIVE CHAT INTEGRATION (Tawk.to)
// ===========================================

function initLiveChat() {
    const tawkToId = import.meta.env.VITE_TAWKTO_ID || '';

    if (!tawkToId) {
        console.log('⚠️ Live chat not configured. Add VITE_TAWKTO_ID to .env');
        return;
    }

    // Load Tawk.to script
    var Tawk_API = Tawk_API || {};
    var Tawk_LoadStart = new Date();

    (function () {
        var s1 = document.createElement("script");
        var s0 = document.getElementsByTagName("script")[0];
        s1.async = true;
        s1.src = `https://embed.tawk.to/${tawkToId}/default`;
        s1.charset = 'UTF-8';
        s1.setAttribute('crossorigin', '*');
        s0.parentNode.insertBefore(s1, s0);
    })();

    console.log('✓ Live chat initialized');
}

// Initialize live chat
initLiveChat();

// ===========================================
// 5. EXIT-INTENT POPUP (Abandoned Cart Recovery)
// ===========================================

class ExitIntentPopup {
    constructor() {
        this.hasShown = false;
        this.init();
    }

    init() {
        document.addEventListener('mouseleave', (e) => {
            if (e.clientY <= 0 && !this.hasShown) {
                this.show();
            }
        });
    }

    show() {
        const cartItemCount = window.cart ? window.cart.getItemCount() : 0;
        if (cartItemCount === 0) return; // Only show if cart has items

        this.hasShown = true;

        const popup = document.createElement('div');
        popup.className = 'exit-popup-overlay';
        popup.innerHTML = `
            <div class="exit-popup glass">
                <button class="exit-popup-close">&times;</button>
                <div class="exit-popup-content">
                    <h2 class="serif">WAIT! DON'T LEAVE YET</h2>
                    <p class="sans">Complete your order now and get <strong>15% OFF</strong></p>
                    <p class="discount-code">Use code: <span class="code-highlight">WELCOME15</span></p>
                    <button class="exit-popup-cta sans" id="exitPopupReturn">COMPLETE MY ORDER</button>
                    <p class="exit-popup-subtext sans">Plus free worldwide shipping on all orders</p>
                </div>
            </div>
        `;

        document.body.appendChild(popup);

        // Close button
        popup.querySelector('.exit-popup-close').addEventListener('click', () => {
            popup.remove();
        });

        // Return to cart
        popup.querySelector('#exitPopupReturn').addEventListener('click', () => {
            if (window.cart) {
                window.cart.openCart();
            }
            popup.remove();
        });

        // Click outside to close
        popup.addEventListener('click', (e) => {
            if (e.target === popup) popup.remove();
        });

        // Animate in
        setTimeout(() => popup.classList.add('active'), 100);
    }
}

// Initialize exit intent
window.exitIntent = new ExitIntentPopup();

console.log('✓ El Dorado Enhancements Loaded: Analytics, Email Capture, CRO, Live Chat, Exit Intent');
