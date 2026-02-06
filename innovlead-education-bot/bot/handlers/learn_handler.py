"""
/aprender command handler - Access educational modules
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from datetime import datetime

from config import get_settings
from database import SessionLocal, User, Module, Lesson, UserProgress, Interaction

settings = get_settings()


async def learn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /aprender command - show available modules"""
    user = update.effective_user
    db = SessionLocal()
    
    try:
        # Get or create user
        db_user = db.query(User).filter(User.telegram_id == user.id).first()
        if not db_user:
            await update.message.reply_text(
                "Please use /start first to register! 🚀"
            )
            return
        
        # Update last active
        db_user.last_active = datetime.utcnow()
        db.commit()
        
        # Get all modules
        modules = db.query(Module).filter(Module.is_published == True).order_by(Module.order_index).all()
        
        # Create module selection keyboard
        keyboard = []
        for module in modules:
            # Get user progress for this module
            completed_lessons = db.query(UserProgress).filter(
                UserProgress.user_id == db_user.id,
                UserProgress.module_id == module.id,
                UserProgress.status == 'completed'
            ).count()
            
            progress_emoji = "✅" if completed_lessons == module.total_lessons else "📚"
            button_text = f"{progress_emoji} {module.title} ({completed_lessons}/{module.total_lessons})"
            
            keyboard.append([InlineKeyboardButton(
                button_text,
                callback_data=f"module_{module.id}"
            )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = """🎓 **Choose Your Learning Path**

Select a module to begin your education journey:

**Module Progress Legend:**
📚 In Progress
✅ Completed

Each module contains interactive lessons designed to empower you with practical knowledge.

*Tap a module below to start learning!*"""
        
        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        # Log interaction
        interaction = Interaction(
            user_id=db_user.id,
            interaction_type='command',
            command='/aprender',
            timestamp=datetime.utcnow()
        )
        db.add(interaction)
        db.commit()
    
    finally:
        db.close()


async def module_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle module selection callback"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    module_id = int(query.data.split('_')[1])
    
    db = SessionLocal()
    
    try:
        db_user = db.query(User).filter(User.telegram_id == user.id).first()
        module = db.query(Module).filter(Module.id == module_id).first()
        
        if not module:
            await query.edit_message_text("Module not found. Please try again.")
            return
        
        # Get all lessons for this module
        lessons = db.query(Lesson).filter(
            Lesson.module_id == module_id
        ).order_by(Lesson.order_index).all()
        
        # Create lesson selection keyboard
        keyboard = []
        for lesson in lessons:
            # Check if user completed this lesson
            progress = db.query(UserProgress).filter(
                UserProgress.user_id == db_user.id,
                UserProgress.lesson_id == lesson.id
            ).first()
            
            status_emoji = "✅" if progress and progress.status == 'completed' else "📖"
            button_text = f"{status_emoji} {lesson.title}"
            
            keyboard.append([InlineKeyboardButton(
                button_text,
                callback_data=f"lesson_{lesson.id}"
            )])
        
        # Add back button
        keyboard.append([InlineKeyboardButton("⬅️ Back to Modules", callback_data="back_to_modules")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""📚 **{module.title}**

{module.description}

⏱️ **Estimated Time:** {module.estimated_duration_minutes} minutes
📝 **Lessons:** {module.total_lessons}

*Select a lesson below to begin:*"""
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    finally:
        db.close()


async def lesson_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle lesson selection callback"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    lesson_id = int(query.data.split('_')[1])
    
    db = SessionLocal()
    
    try:
        db_user = db.query(User).filter(User.telegram_id == user.id).first()
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        
        if not lesson:
            await query.edit_message_text("Lesson not found. Please try again.")
            return
        
        # Record lesson access
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == db_user.id,
            UserProgress.lesson_id == lesson_id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=db_user.id,
                module_id=lesson.module_id,
                lesson_id=lesson_id,
                status='in_progress',
                started_at=datetime.utcnow()
            )
            db.add(progress)
        
        # Log interaction
        interaction = Interaction(
            user_id=db_user.id,
            interaction_type='lesson_access',
            module_id=lesson.module_id,
            lesson_id=lesson_id,
            timestamp=datetime.utcnow()
        )
        db.add(interaction)
        db.commit()
        
        # Create action keyboard
        keyboard = [
            [InlineKeyboardButton("✅ Mark as Complete", callback_data=f"complete_{lesson_id}")],
            [InlineKeyboardButton("⬅️ Back to Lessons", callback_data=f"module_{lesson.module_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send lesson content (split if too long)
        lesson_message = f"**{lesson.title}**\n\n{lesson.content}"
        
        # Telegram has a 4096 character limit
        if len(lesson_message) > 4000:
            # Split into parts
            parts = [lesson_message[i:i+4000] for i in range(0, len(lesson_message), 4000)]
            for part in parts[:-1]:
                await query.message.reply_text(part, parse_mode='Markdown')
            # Last part with keyboard
            await query.edit_message_text(
                parts[-1],
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                lesson_message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    finally:
        db.close()


async def complete_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle lesson completion callback"""
    query = update.callback_query
    await query.answer("🎉 Lesson completed!")
    
    user = update.effective_user
    lesson_id = int(query.data.split('_')[1])
    
    db = SessionLocal()
    
    try:
        db_user = db.query(User).filter(User.telegram_id == user.id).first()
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        
        # Update progress
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == db_user.id,
            UserProgress.lesson_id == lesson_id
        ).first()
        
        if progress:
            progress.status = 'completed'
            progress.completed_at = datetime.utcnow()
            db.commit()
        
        # Check if module is complete
        module = db.query(Module).filter(Module.id == lesson.module_id).first()
        total_completed = db.query(UserProgress).filter(
            UserProgress.user_id == db_user.id,
            UserProgress.module_id == lesson.module_id,
            UserProgress.status == 'completed'
        ).count()
        
        if total_completed == module.total_lessons:
            congrats = f"""🏆 **Congratulations!**

You've completed **{module.title}**!

You're now equipped with valuable knowledge to empower yourself and your community.

Ready for the next module? Use /aprender to continue your journey! 🚀"""
            await query.message.reply_text(congrats, parse_mode='Markdown')
        else:
            await query.message.reply_text(
                f"✅ Lesson marked as complete! Keep up the great work! ({total_completed}/{module.total_lessons})",
                parse_mode='Markdown'
            )
        
        # Return to module view
        await module_selected(update, context)
    
    finally:
        db.close()


async def back_to_modules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle back to modules callback"""
    query = update.callback_query
    await query.answer()
    
    # Simulate the learn_command but with query instead of update.message
    await learn_command_from_callback(query, context)


async def learn_command_from_callback(query, context):
    """Helper function to show modules from callback"""
    user = query.from_user
    db = SessionLocal()
    
    try:
        db_user = db.query(User).filter(User.telegram_id == user.id).first()
        modules = db.query(Module).filter(Module.is_published == True).order_by(Module.order_index).all()
        
        keyboard = []
        for module in modules:
            completed_lessons = db.query(UserProgress).filter(
                UserProgress.user_id == db_user.id,
                UserProgress.module_id == module.id,
                UserProgress.status == 'completed'
            ).count()
            
            progress_emoji = "✅" if completed_lessons == module.total_lessons else "📚"
            button_text = f"{progress_emoji} {module.title} ({completed_lessons}/{module.total_lessons})"
            
            keyboard.append([InlineKeyboardButton(
                button_text,
                callback_data=f"module_{module.id}"
            )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = """🎓 **Choose Your Learning Path**

Select a module to begin your education journey:

**Module Progress Legend:**
📚 In Progress
✅ Completed

*Tap a module below to start learning!*"""
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    finally:
        db.close()


def get_callback_handler():
    """Return callback query handler for learn commands"""
    return CallbackQueryHandler(handle_callback)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Route callbacks to appropriate handlers"""
    query = update.callback_query
    data = query.data
    
    if data.startswith('module_'):
        await module_selected(update, context)
    elif data.startswith('lesson_'):
        await lesson_selected(update, context)
    elif data.startswith('complete_'):
        await complete_lesson(update, context)
    elif data == 'back_to_modules':
        await back_to_modules(update, context)
