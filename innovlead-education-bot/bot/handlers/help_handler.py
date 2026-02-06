"""
/ayuda command handler - Help & support
"""
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from config import get_settings
from database import SessionLocal, User, Interaction

settings = get_settings()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ayuda command - show help information"""
    user = update.effective_user
    db = SessionLocal()
    
    try:
        db_user = db.query(User).filter(User.telegram_id == user.id).first()
        
        if db_user:
            # Update last active
            db_user.last_active = datetime.utcnow()
            
            # Log interaction
            interaction = Interaction(
                user_id=db_user.id,
                interaction_type='command',
                command='/ayuda',
                timestamp=datetime.utcnow()
            )
            db.add(interaction)
            db.commit()
        
        help_message = f"""❓ **InnovLead Education Bot - Help Guide**

**Available Commands:**

🚀 **/start** - Welcome message & registration
📚 **/aprender** - Access educational modules
🔒 **/privacidad** - Quick PIPEDA privacy tips
📊 **/progreso** - View your learning progress
❓ **/ayuda** - Show this help message

---

**About InnovLead Foundation:**

We're a Canadian nonprofit (in registration as Registered Charity) democratizing AI and privacy education for vulnerable communities and NGOs.

**Leadership:**
• **Tommy Fernandez** - Executive Director
• **William Melendez** - Technical Chair

**Mission:**
Provide free, accessible AI and privacy education to empower communities without resources.

---

**Educational Modules:**

🤖 **AI Ethics & Responsible AI** (5 lessons)
Learn about ethical AI, bias recognition, and responsible use of generative AI tools.

🔒 **Privacy in Canada (PIPEDA)** (6 lessons)
Understand your privacy rights, data protection, and PIPEDA compliance.

⚡ **Social Automation Tools** (4 lessons)
Master low-code automation platforms like n8n for nonprofit productivity.

---

**How to Use This Bot:**

1️⃣ Use **/aprender** to select a module
2️⃣ Read through lessons at your own pace
3️⃣ Mark lessons complete as you finish
4️⃣ Use **/progreso** to track your achievements
5️⃣ Ask me questions anytime!

---

**Privacy & Data:**

We collect minimal data (Telegram ID, username, lesson progress) solely for:
✅ Educational tracking
✅ CRA charity impact reporting
✅ Improving our services

We DON'T:
❌ Share data with third parties
❌ Sell your information
❌ Use data for commercial purposes

All data handling complies with PIPEDA (Canada's privacy law).

---

**Need Support?**

📧 Email: {settings.org_email}
🌐 Website: {settings.org_website}
💬 Community: {settings.org_telegram_community}

**For Privacy Issues:**
Privacy Commissioner of Canada
📞 1-800-282-1376
🌐 www.priv.gc.ca

---

**Important Legal Notice:**

🚨 This bot is for **educational purposes only**. InnovLead Foundation is a nonprofit and does NOT offer commercial consulting services.

For professional AI/privacy consulting, please seek qualified service providers.

---

**Contributing:**

Want to help? We're open source!
• Report bugs
• Suggest features
• Contribute content
• Spread the word

Contact us at {settings.org_email}

---

💡 **Pro Tip:** You can ask me questions about AI, privacy, or automation anytime! I'm your AI tutor, here to help you learn.

🌟 **Let's democratize AI education together!**"""
        
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    finally:
        db.close()
