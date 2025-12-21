#!/usr/bin/env python3
"""
Jhopan VPN Bot - Main Entry Point
Clean modular structure with app/, handlers/, utils/

Run: python main.py
"""

import sys
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from app.config import Config
from app.utils.logger import setup_logger
from app.handlers.commands import CommandHandlers
from app.handlers.callbacks import CallbackHandlers

# Setup logger
logger = setup_logger("jhopan_bot")


def main():
    """Main function - Initialize and run bot"""
    
    logger.info("=" * 60)
    logger.info("🚀 Starting Jhopan VPN Bot v2.0")
    logger.info("=" * 60)
    
    # Validate config
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        logger.error("Please check your .env file")
        sys.exit(1)
    
    # Log configuration
    logger.info(f"🌐 Worker Domain: {Config.WORKER_DOMAIN}")
    logger.info(f"🔗 API URL: {Config.get_api_url()}")
    
    if Config.ADMIN_ONLY:
        logger.info(f"🔒 Running in ADMIN ONLY mode")
        logger.info(f"👑 Allowed admins: {Config.ADMIN_IDS}")
    else:
        logger.info("🌍 Running in PUBLIC mode")
    
    # Initialize handlers
    cmd_handlers = CommandHandlers()
    callback_handlers = CallbackHandlers(cmd_handlers.user_data)
    
    # Build application
    logger.info("📦 Building Telegram application...")
    app = ApplicationBuilder().token(Config.TELEGRAM_BOT_TOKEN).build()
    
    # Register command handlers
    logger.info("📝 Registering command handlers...")
    app.add_handler(CommandHandler("start", cmd_handlers.cmd_start))
    app.add_handler(CommandHandler("config", cmd_handlers.cmd_config))
    app.add_handler(CommandHandler("help", cmd_handlers.cmd_help))
    app.add_handler(CommandHandler("status", cmd_handlers.cmd_status))
    app.add_handler(CommandHandler("myid", cmd_handlers.cmd_myid))
    
    # Register callback handlers
    logger.info("📝 Registering callback handlers...")
    app.add_handler(CallbackQueryHandler(callback_handlers.handle_menu, pattern="^menu_"))
    app.add_handler(CallbackQueryHandler(callback_handlers.handle_menu, pattern="^back_"))
    app.add_handler(CallbackQueryHandler(callback_handlers.handle_country, pattern="^country_"))
    app.add_handler(CallbackQueryHandler(callback_handlers.handle_protocol, pattern="^protocol_"))
    app.add_handler(CallbackQueryHandler(callback_handlers.handle_format, pattern="^format_"))
    app.add_handler(CallbackQueryHandler(callback_handlers.handle_port, pattern="^port_"))
    
    # Start bot
    logger.info("=" * 60)
    logger.info("✅ Bot started successfully!")
    logger.info("🎯 Press Ctrl+C to stop")
    logger.info("=" * 60)
    
    # Run polling
    app.run_polling()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n👋 Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
