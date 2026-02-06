"""
InnovLead Education Bot - Main Entry Point
Telegram bot for AI & Privacy education
"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from config import get_settings
from bot.handlers import (
    start_handler,
    learn_handler,
    privacy_handler,
    progress_handler,
    help_handler,
    fallback_handler
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

settings = get_settings()


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates"""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Start the bot"""
    try:
        # Create application
        application = Application.builder().token(settings.telegram_bot_token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_handler.start_command))
        application.add_handler(CommandHandler("aprender", learn_handler.learn_command))
        application.add_handler(CommandHandler("privacidad", privacy_handler.privacy_command))
        application.add_handler(CommandHandler("progreso", progress_handler.progress_command))
        application.add_handler(CommandHandler("ayuda", help_handler.help_command))
        
        # Add message handler for general conversations (AI tutor)
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            fallback_handler.handle_message
        ))
        
        # Add callback query handlers for inline keyboards
        application.add_handler(learn_handler.get_callback_handler())
        application.add_handler(privacy_handler.get_callback_handler())
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        # Start bot
        logger.info("InnovLead Education Bot starting...")
        logger.info(f"Environment: {settings.environment}")
        logger.info(f"AI Provider: {settings.ai_provider}")
        logger.info(f"Database: {settings.database_url}")
        
        print("\n" + "="*70)
        print("InnovLead Universal AI Education Bot")
        print("="*70)
        print(f"[OK] Bot is running in {settings.bot_mode} mode")
        print(f"[OK] AI Tutor: {'Enabled' if settings.enable_ai_tutor else 'Disabled'}")
        print(f"[OK] Organization: {settings.org_name}")
        print(f"[OK] Environment: {settings.environment}")
        print("\n[TIP] Press Ctrl+C to stop the bot")
        print("="*70 + "\n")
        
        # Run bot
        if settings.bot_mode == 'polling':
            application.run_polling(allowed_updates=Update.ALL_TYPES)
        else:
            # Webhook mode (for production)
            application.run_webhook(
                listen="0.0.0.0",
                port=settings.webhook_port,
                url_path=settings.telegram_bot_token,
                webhook_url=f"{settings.webhook_url}/{settings.telegram_bot_token}"
            )
    
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("\nBot stopped. Thank you for supporting InnovLead Foundation!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n[ERROR] Error starting bot: {e}")
        print("[TIP] Make sure your .env file is configured correctly")


if __name__ == '__main__':
    main()
