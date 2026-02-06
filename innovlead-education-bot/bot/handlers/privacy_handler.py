"""
/privacidad command handler - Quick PIPEDA tips
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from datetime import datetime
import random

from config import get_settings
from database import SessionLocal, User, PIPEDATip, Interaction

settings = get_settings()


async def privacy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /privacidad command - show PIPEDA tips"""
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
            command='/privacidad',
            timestamp=datetime.utcnow()
        )
        db.add(interaction)
        db.commit()
        
        # Get tips by category
        categories = db.query(PIPEDATip.category).distinct().all()
        
        # Create category selection keyboard
        keyboard = []
        category_map = {
            'consent': '✍️ Consent',
            'individual_rights': '⚖️ Your Rights',
            'data_breach': '🚨 Data Breaches'
        }
        
        for (category,) in categories:
            display_name = category_map.get(category, category.title())
            keyboard.append([InlineKeyboardButton(
                display_name,
                callback_data=f"privacy_cat_{category}"
            )])
        
        # Add random tip button
        keyboard.append([InlineKeyboardButton(
            "🎲 Random Tip",
            callback_data="privacy_random"
        )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = """🔒 **PIPEDA Privacy Tips**

Quick reference guide to your privacy rights in Canada!

**What is PIPEDA?**
Canada's Personal Information Protection and Electronic Documents Act - your privacy protection law.

**Select a category to learn more:**

---

💡 **Want the full course?**
Use /aprender and choose "Privacy in Canada (PIPEDA)" module for comprehensive education.

📞 **Need Help?**
Privacy Commissioner of Canada: 1-800-282-1376
Website: www.priv.gc.ca"""
        
        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    finally:
        db.close()


async def show_privacy_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show tips for a specific category"""
    query = update.callback_query
    await query.answer()
    
    category = query.data.split('_')[-1]
    db = SessionLocal()
    
    try:
        # Get all tips for this category
        tips = db.query(PIPEDATip).filter(
            PIPEDATip.category == category
        ).all()
        
        if not tips:
            await query.edit_message_text("No tips found for this category.")
            return
        
        # Create tip selection keyboard
        keyboard = []
        for tip in tips:
            keyboard.append([InlineKeyboardButton(
                tip.title,
                callback_data=f"privacy_tip_{tip.id}"
            )])
        
        # Add back button
        keyboard.append([InlineKeyboardButton(
            "⬅️ Back to Categories",
            callback_data="privacy_back"
        )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        category_names = {
            'consent': '✍️ Consent',
            'individual_rights': '⚖️ Your Rights',
            'data_breach': '🚨 Data Breaches'
        }
        
        message = f"""**{category_names.get(category, category.title())} Tips**

Select a tip to learn more:"""
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    finally:
        db.close()


async def show_privacy_tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show a specific privacy tip"""
    query = update.callback_query
    await query.answer()
    
    tip_id = int(query.data.split('_')[-1])
    db = SessionLocal()
    
    try:
        tip = db.query(PIPEDATip).filter(PIPEDATip.id == tip_id).first()
        
        if not tip:
            await query.edit_message_text("Tip not found.")
            return
        
        keyboard = [
            [InlineKeyboardButton("🎲 Another Tip", callback_data="privacy_random")],
            [InlineKeyboardButton("⬅️ Back to Categories", callback_data="privacy_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""**{tip.title}**

{tip.content}

---
🎯 **Target Audience:** {tip.target_audience.title()}
📚 **Category:** {tip.category.replace('_', ' ').title()}

💡 **Want to learn more?** Use /aprender for the full PIPEDA course!"""
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    finally:
        db.close()


async def show_random_tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show a random privacy tip"""
    query = update.callback_query
    await query.answer("🎲 Here's a random tip!")
    
    db = SessionLocal()
    
    try:
        # Get random tip
        tips = db.query(PIPEDATip).all()
        if tips:
            tip = random.choice(tips)
            
            keyboard = [
                [InlineKeyboardButton("🎲 Another Tip", callback_data="privacy_random")],
                [InlineKeyboardButton("⬅️ Back to Categories", callback_data="privacy_back")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            message = f"""**🎲 Random Privacy Tip**

**{tip.title}**

{tip.content}

---
🎯 **Target Audience:** {tip.target_audience.title()}
📚 **Category:** {tip.category.replace('_', ' ').title()}"""
            
            await query.edit_message_text(
                message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    finally:
        db.close()


async def back_to_privacy_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back to category selection"""
    query = update.callback_query
    await query.answer()
    
    # Simulate privacy_command but with callback
    db = SessionLocal()
    
    try:
        categories = db.query(PIPEDATip.category).distinct().all()
        
        keyboard = []
        category_map = {
            'consent': '✍️ Consent',
            'individual_rights': '⚖️ Your Rights',
            'data_breach': '🚨 Data Breaches'
        }
        
        for (category,) in categories:
            display_name = category_map.get(category, category.title())
            keyboard.append([InlineKeyboardButton(
                display_name,
                callback_data=f"privacy_cat_{category}"
            )])
        
        keyboard.append([InlineKeyboardButton(
            "🎲 Random Tip",
            callback_data="privacy_random"
        )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = """🔒 **PIPEDA Privacy Tips**

Select a category to learn more about your privacy rights in Canada:"""
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    finally:
        db.close()


def get_callback_handler():
    """Return callback query handler for privacy commands"""
    return CallbackQueryHandler(handle_privacy_callback)


async def handle_privacy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Route privacy callbacks to appropriate handlers"""
    query = update.callback_query
    data = query.data
    
    if data.startswith('privacy_cat_'):
        await show_privacy_category(update, context)
    elif data.startswith('privacy_tip_'):
        await show_privacy_tip(update, context)
    elif data == 'privacy_random':
        await show_random_tip(update, context)
    elif data == 'privacy_back':
        await back_to_privacy_categories(update, context)
