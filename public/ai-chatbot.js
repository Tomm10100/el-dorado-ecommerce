// El Dorado AI Customer Support Chatbot
// Integrates with website to provide instant customer support

class ElDoradoChatbot {
    constructor() {
        this.isOpen = false;
        this.conversationHistory = [];
        this.init();
    }

    init() {
        this.injectStyles();
        this.createChatWidget();
        this.loadConversationHistory();
    }

    injectStyles() {
        const styles = `
            .eldorado-chatbot {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 10000;
                font-family: 'Inter', sans-serif;
            }

            /* Chat toggle button removed */

            .chat-window {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 350px;
                height: 500px;
                background: rgba(15, 15, 15, 0.95);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                border: 1px solid rgba(255, 215, 0, 0.2);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                transform: scale(0);
                opacity: 0;
                transition: all 0.3s ease;
            }

            .chat-window.open {
                transform: scale(1);
                opacity: 1;
            }

            .chat-header {
                background: linear-gradient(135deg, #FFD700, #FFA500);
                padding: 20px;
                color: #000;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }

            .chat-header h3 {
                margin: 0;
                font-size: 16px;
                font-weight: 600;
            }

            .chat-status {
                font-size: 12px;
                opacity: 0.8;
            }

            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                display: flex;
                flex-direction: column;
                gap: 15px;
            }

            .chat-message {
                max-width: 80%;
                padding: 12px 16px;
                border-radius: 12px;
                font-size: 14px;
                line-height: 1.5;
                animation: messageSlide 0.3s ease;
            }

            @keyframes messageSlide {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .chat-message.bot {
                align-self: flex-start;
                background: rgba(255, 215, 0, 0.1);
                border: 1px solid rgba(255, 215, 0, 0.2);
                color: #FFD700;
            }

            .chat-message.user {
                align-self: flex-end;
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: #fff;
            }

            .chat-input-container {
                padding: 15px;
                background: rgba(20, 20, 20, 0.8);
                border-top: 1px solid rgba(255, 215, 0, 0.1);
                display: flex;
                gap: 10px;
            }

            .chat-input {
                flex: 1;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 215, 0, 0.2);
                border-radius: 25px;
                padding: 12px 20px;
                color: #fff;
                font-size: 14px;
                outline: none;
            }

            .chat-input::placeholder {
                color: rgba(255, 255, 255, 0.4);
            }

            .chat-send-btn {
                width: 45px;
                height: 45px;
                border-radius: 50%;
                background: linear-gradient(135deg, #FFD700, #FFA500);
                border: none;
                cursor: pointer;
                font-size: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: transform 0.2s;
            }

            .chat-send-btn:hover {
                transform: scale(1.1);
            }

            .quick-actions {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                padding: 0 20px 15px;
            }

            .quick-action-btn {
                background: rgba(255, 215, 0, 0.1);
                border: 1px solid rgba(255, 215, 0, 0.3);
                color: #FFD700;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 12px;
                cursor: pointer;
                transition: all 0.2s;
            }

            .quick-action-btn:hover {
                background: rgba(255, 215, 0, 0.2);
                transform: translateY(-2px);
            }

            .typing-indicator {
                display: flex;
                gap: 4px;
                padding: 12px 16px;
                background: rgba(255, 215, 0, 0.1);
                border: 1px solid rgba(255, 215, 0, 0.2);
                border-radius: 12px;
                width: fit-content;
            }

            .typing-dot {
                width: 8px;
                height: 8px;
                background: #FFD700;
                border-radius: 50%;
                animation: typingAnimation 1.4s infinite;
            }

            .typing-dot:nth-child(2) { animation-delay: 0.2s; }
            .typing-dot:nth-child(3) { animation-delay: 0.4s; }

            @keyframes typingAnimation {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-10px); }
            }
        `;

        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }

    createChatWidget() {
        const widget = document.createElement('div');
        widget.className = 'eldorado-chatbot';
        widget.innerHTML = `
            <div class="chat-window" id="chat-window">
                <div class="chat-header">
                    <div>
                        <h3>El Dorado Assistant</h3>
                        <div class="chat-status">● Online</div>
                    </div>
                    <button id="chat-close-btn" style="background:none;border:none;color:#000;font-size:24px;cursor:pointer;">&times;</button>
                </div>
                <div class="quick-actions" id="quick-actions">
                    <button class="quick-action-btn" data-action="products">View Products</button>
                    <button class="quick-action-btn" data-action="shipping">Shipping Info</button>
                    <button class="quick-action-btn" data-action="963hz">What is 963Hz?</button>
                    <button class="quick-action-btn" data-action="materials">Materials</button>
                </div>
                <div class="chat-messages" id="chat-messages">
                    <div class="chat-message bot">
                        👋 Welcome to El Dorado! I'm your AI assistant. How can I help you discover the perfect piece today?
                    </div>
                </div>
                <div class="chat-input-container">
                    <input 
                        type="text" 
                        class="chat-input" 
                        id="chat-input" 
                        placeholder="Ask me anything..."
                        autocomplete="off"
                    />
                    <button class="chat-send-btn" id="chat-send">➤</button>
                </div>
            </div>
        `;

        document.body.appendChild(widget);
        this.attachEventListeners();
    }

    attachEventListeners() {
        // Close button
        const closeBtn = document.getElementById('chat-close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.toggleChat());
        }

        // Global trigger listeners (for footer/nav links)
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('trigger-chat') || e.target.closest('.trigger-chat')) {
                e.preventDefault();
                this.toggleChat();
            }
        });

        document.getElementById('chat-send').addEventListener('click', () => {
            this.sendMessage();
        });

        document.getElementById('chat-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Quick action buttons
        document.querySelectorAll('.quick-action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.getAttribute('data-action');
                this.handleQuickAction(action);
            });
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const chatWindow = document.getElementById('chat-window');
        chatWindow.classList.toggle('open', this.isOpen);
    }

    sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();

        if (!message) return;

        this.addMessage(message, 'user');
        input.value = '';

        // Show typing indicator
        this.showTypingIndicator();

        // Simulate AI response (in production, connect to your AI backend)
        setTimeout(() => {
            const response = this.generateResponse(message);
            this.hideTypingIndicator();
            this.addMessage(response, 'bot');
            this.saveConversation();
        }, 1000 + Math.random() * 1000);
    }

    handleQuickAction(action) {
        const actions = {
            'products': 'I want to see your product collection!',
            'shipping': 'What are your shipping options?',
            '963hz': 'Tell me about 963Hz resonance technology',
            'materials': 'What materials do you use?'
        };

        const message = actions[action];
        if (message) {
            this.addMessage(message, 'user');
            this.showTypingIndicator();

            setTimeout(() => {
                const response = this.generateResponse(message);
                this.hideTypingIndicator();
                this.addMessage(response, 'bot');
            }, 1000);
        }
    }

    generateResponse(message) {
        const lowerMessage = message.toLowerCase();

        // Product inquiries
        if (lowerMessage.includes('product') || lowerMessage.includes('collection') || lowerMessage.includes('jewelry')) {
            return "✨ Our Lunar Elegance Collection features 6 premium pieces:\n\n💎 Cruz-Ki — Cross Pendant — $200\n⛓️ Fuego Cadena — Cuban Link Chain — $1,200\n💫 Dumfe — Cuban Link Bracelet — $400\n✨ Chan — Gucci Link Bracelet — $300\n🌙 Oni — Box Chain Bracelet — $200\n⚡ Fan — Chain Link Bracelet — $200\n\nAll crafted in 925 sterling silver with 963Hz resonance. Which piece calls to you?";
        }

        // 963Hz inquiries
        if (lowerMessage.includes('963') || lowerMessage.includes('frequency') || lowerMessage.includes('resonance')) {
            return "963Hz is the 'Frequency of the Gods' 🌟\n\nIt activates the pineal gland and promotes:\n• Spiritual awakening\n• Enhanced clarity\n• Elevated consciousness\n• Positive energy flow\n\nEach El Dorado piece is designed to resonate at this powerful frequency.";
        }

        // Shipping inquiries
        if (lowerMessage.includes('ship') || lowerMessage.includes('delivery') || lowerMessage.includes('how long')) {
            return "🌍 We offer worldwide shipping!\n\n📦 Standard: 5-7 business days ($15)\n✈️ Express: 2-3 business days ($25)\n🎁 Free shipping on orders over $400\n\nAll orders are insured and tracked.";
        }

        // Material inquiries
        if (lowerMessage.includes('material') || lowerMessage.includes('silver') || lowerMessage.includes('quality')) {
            return "✨ Premium 925 Sterling Silver\n\n• 92.5% pure silver content\n• Hypoallergenic & skin-safe\n• Tarnish-resistant coating\n• Lifetime quality guarantee\n• Ethically sourced\n\nEvery piece comes with authentication certificate.";
        }

        // Price inquiries
        if (lowerMessage.includes('price') || lowerMessage.includes('cost') || lowerMessage.includes('how much')) {
            return "💎 Our collection ranges from $200-$1,200\n\nCruz-Ki — Cross Pendant: $200\nFuego Cadena — Cuban Link Chain: $1,200\nDumfe — Cuban Link Bracelet: $400\nChan — Gucci Link Bracelet: $300\nOni — Box Chain Bracelet: $200\nFan — Chain Link Bracelet: $200\n\nAll prices include authentication certificate and premium packaging!";
        }

        // Payment inquiries
        if (lowerMessage.includes('payment') || lowerMessage.includes('pay') || lowerMessage.includes('stripe') || lowerMessage.includes('crypto')) {
            return "💳 We accept multiple payment methods:\n\n• Credit/Debit Cards (Stripe)\n• XRP Cryptocurrency\n• Apple Pay & Google Pay\n\nAll transactions are secure and encrypted. 🔒";
        }

        // Return/refund inquiries
        if (lowerMessage.includes('return') || lowerMessage.includes('refund') || lowerMessage.includes('guarantee')) {
            return "✅ 30-Day Money-Back Guarantee\n\nNot in love with your piece? Return it within 30 days for a full refund - no questions asked.\n\n• Free return shipping\n• Quick refund processing\n• Lifetime warranty on craftsmanship";
        }

        // Contact inquiries
        if (lowerMessage.includes('contact') || lowerMessage.includes('email') || lowerMessage.includes('support')) {
            return "📧 Contact Us:\n\nEmail: tommy@innovlead.ca\nResponse time: Within 4 hours\n\nOr continue chatting with me - I'm here 24/7! 😊";
        }

        // Default response
        return "I'm here to help! I can tell you about:\n\n💎 Our products & prices\n✨ 963Hz resonance technology\n🌍 Shipping & delivery\n💳 Payment options\n📧 Customer support\n\nWhat would you like to know?";
    }

    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}`;
        messageDiv.textContent = text;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        this.conversationHistory.push({ text, sender, timestamp: Date.now() });
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.id = 'typing-indicator';
        indicator.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        messagesContainer.appendChild(indicator);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    saveConversation() {
        try {
            localStorage.setItem('eldorado_chat_history', JSON.stringify(this.conversationHistory));
        } catch (e) {
            console.error('Failed to save conversation:', e);
        }
    }

    loadConversationHistory() {
        try {
            const saved = localStorage.getItem('eldorado_chat_history');
            if (saved) {
                this.conversationHistory = JSON.parse(saved);
                // Optionally restore messages in UI
            }
        } catch (e) {
            console.error('Failed to load conversation:', e);
        }
    }
}

// Initialize chatbot when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.eldoradoChatbot = new ElDoradoChatbot();
    });
} else {
    window.eldoradoChatbot = new ElDoradoChatbot();
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ElDoradoChatbot;
}
