"""
/start command handler - Welcome & user registration
"""
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from config import get_settings
from database import SessionLocal, User, Interaction

settings = get_settings()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - welcome message and user registration"""
    user = update.effective_user
    db = SessionLocal()
    
    try:
        # Check if user exists
        db_user = db.query(User).filter(User.telegram_id == user.id).first()
        
        if not db_user:
            # New user - register
            db_user = User(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                language_code=user.language_code or 'en',
                is_active=True,
                consent_data_processing=False  # Will ask for consent
            )
            db.add(db_user)
            db.commit()
            
            # Welcome message for new users
            welcome_message = f"""🎓 **Welcome to InnovLead Foundation!**

Hello {user.first_name}! I'm your AI Education Tutor, here to help you learn about:

🤖 **AI Ethics & Responsible AI**
🔒 **Privacy in Canada (PIPEDA)**
⚡ **Social Automation Tools**

**About InnovLead Foundation:**
We're a Canadian nonprofit dedicated to democratizing AI and privacy education for vulnerable communities and NGOs.

**Leadership:**
• Tommy Fernandez - Executive Director
• William Melendez - Technical Chair

---

📚 **Your Privacy Matters**

Before we begin, I need your consent to process your learning data (progress tracking for our CRA charity reporting).

We collect: Telegram ID, username, lesson progress
We use it for: Educational tracking and nonprofit impact reporting
We DON'T share it with third parties

By continuing, you consent to this minimal data collection under PIPEDA.

Type "I consent" to continue or /ayuda for more information.

---

🚀 **Quick Start Commands:**
/aprender - Start learning modules
/privacidad - Quick PIPEDA tips
/progreso - View your progress
/ayuda - Get help

Let's democratize AI education together! 🌟"""
            
            await update.message.reply_text(welcome_message, parse_mode='Markdown')
        
        else:
            # Returning user
            db_user.last_active = datetime.utcnow()
            db.commit()
            
            welcome_back = f"""👋 **Welcome back, {user.first_name}!**

Great to see you again! Ready to continue your learning journey?

🎯 **Quick Access:**
/aprender - Continue your modules
/progreso - See your achievements
/privacidad - Privacy tips
/ayuda - Need help?

What would you like to explore today? 🚀"""
            
            await update.message.reply_text(welcome_back, parse_mode='Markdown')
        
        # Log interaction
        interaction = Interaction(
            user_id=db_user.id,
            interaction_type='command',
            command='/start',
            timestamp=datetime.utcnow()
        )
        db.add(interaction)
        db.commit()
    
    finally:
        db.close()
