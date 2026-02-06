"""
/progreso command handler - View user progress
"""
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from config import get_settings
from database import SessionLocal, User, Module, UserProgress, Interaction

settings = get_settings()


async def progress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /progreso command - show user's learning progress"""
    user = update.effective_user
    db = SessionLocal()
    
    try:
        db_user = db.query(User).filter(User.telegram_id == user.id).first()
        if not db_user:
            await update.message.reply_text("Please use /start first to register! 🚀")
            return
        
        # Update last active
        db_user.last_active = datetime.utcnow()
        
        # Log interaction
        interaction = Interaction(
            user_id=db_user.id,
            interaction_type='command',
            command='/progreso',
            timestamp=datetime.utcnow()
        )
        db.add(interaction)
        db.commit()
        
        # Get all modules
        modules = db.query(Module).filter(Module.is_published == True).order_by(Module.order_index).all()
        
        # Calculate overall progress
        total_lessons = sum(module.total_lessons for module in modules)
        total_completed = db.query(UserProgress).filter(
            UserProgress.user_id == db_user.id,
            UserProgress.status == 'completed'
        ).count()
        
        overall_percentage = int((total_completed / total_lessons * 100)) if total_lessons > 0 else 0
        
        # Build progress message
        progress_bars = []
        for module in modules:
            module_completed = db.query(UserProgress).filter(
                UserProgress.user_id == db_user.id,
                UserProgress.module_id == module.id,
                UserProgress.status == 'completed'
            ).count()
            
            percentage = int((module_completed / module.total_lessons * 100)) if module.total_lessons > 0 else 0
            
            # Create progress bar
            filled = int(percentage / 10)
            bar = "█" * filled + "░" * (10 - filled)
            
            status_emoji = "✅" if module_completed == module.total_lessons else "📚"
            
            progress_bars.append(
                f"{status_emoji} **{module.title}**\n"
                f"[{bar}] {percentage}% ({module_completed}/{module.total_lessons} lessons)\n"
            )
        
        # Overall progress bar
        overall_filled = int(overall_percentage / 10)
        overall_bar = "█" * overall_filled + "░" * (10 - overall_filled)
        
        # Get some stats
        total_interactions = db.query(Interaction).filter(
            Interaction.user_id == db_user.id
        ).count()
        
        days_active = (datetime.utcnow() - db_user.registration_date).days
        
        message = f"""📊 **Your Learning Progress**

**Overall Completion**
[{overall_bar}] {overall_percentage}%
{total_completed} of {total_lessons} lessons completed

---

**Module Progress:**

{"".join(progress_bars)}

---

📈 **Your Stats:**
• Member since: {db_user.registration_date.strftime('%B %d, %Y')}
• Days active: {days_active}
• Total interactions: {total_interactions}
• Completion rate: {overall_percentage}%

{'🏆 **Amazing! You''ve completed all modules!**' if total_completed == total_lessons else '💪 **Keep going! Knowledge is power!**'}

Use /aprender to continue your learning journey! 🚀"""
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    finally:
        db.close()
