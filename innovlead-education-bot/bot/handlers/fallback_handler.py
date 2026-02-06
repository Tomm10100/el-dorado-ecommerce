"""
Fallback message handler - AI Tutor for general questions
"""
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from config import get_settings
from database import SessionLocal, User, Interaction
from ai import get_ai_tutor

settings = get_settings()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle general text messages - AI Tutor responses"""
    user = update.effective_user
    message_text = update.message.text
    
    db = SessionLocal()
    
    try:
        db_user = db.query(User).filter(User.telegram_id == user.id).first()
        
        if not db_user:
            await update.message.reply_text(
                "👋 Welcome! Please use /start to register first, then I can help you learn! 🚀"
            )
            return
        
        # Update last active
        db_user.last_active = datetime.utcnow()
        
        # Handle consent
        if not db_user.consent_data_processing:
            if "i consent" in message_text.lower() or "consent" in message_text.lower():
                db_user.consent_data_processing = True
                db.commit()
                
                await update.message.reply_text(
                    """✅ **Thank you for your consent!**

You're all set to begin your learning journey.

🎓 Use /aprender to start with your first module!
💡 Or ask me any question about AI, privacy, or automation.

Let's learn together! 🚀""",
                    parse_mode='Markdown'
                )
                return
            else:
                await update.message.reply_text(
                    """📚 **Almost there!**

Please type "I consent" to agree to minimal data collection for educational tracking, or use /ayuda to learn more about our privacy practices.

Your privacy is important to us! 🔒""",
                    parse_mode='Markdown'
                )
                return
        
        # Check if AI tutor is enabled
        if not settings.enable_ai_tutor:
            await update.message.reply_text(
                "🤖 AI Tutor is currently disabled. Please use the available commands:\n\n" +
                "/aprender - Learning modules\n" +
                "/privacidad - Privacy tips\n" +
                "/progreso - Your progress\n" +
                "/ayuda - Help"
            )
            return
        
        # Get AI tutor response
        try:
            ai_tutor = get_ai_tutor()
            if ai_tutor is None:
                await update.message.reply_text(
                    "🤖 AI Tutor is not available right now. Please use /aprender to access modules or /ayuda for help."
                )
                return
            
            # Show typing indicator
            await update.message.chat.send_action("typing")
            
            # Get response from AI
            response = ai_tutor.ask(message_text)
            
            # Log interaction
            interaction = Interaction(
                user_id=db_user.id,
                interaction_type='ai_query',
                message_text=message_text[:500],  # Limit length
                ai_response_length=len(response),
                timestamp=datetime.utcnow()
            )
            db.add(interaction)
            db.commit()
            
            # Send response
            await update.message.reply_text(response, parse_mode='Markdown')
        
        except Exception as e:
            error_message = f"""😔 I'm having trouble responding right now.

**What you can do:**
• Try rephrasing your question
• Use /aprender for structured lessons
• Use /privacidad for quick privacy tips
• Contact us: {settings.org_email}

I apologize for the inconvenience!"""
            
            await update.message.reply_text(error_message, parse_mode='Markdown')
            
            # Log error
            print(f"AI Tutor error: {e}")
    
    finally:
        db.close()
