"""
Decorators for access control
"""

from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from app.config import Config
import logging

logger = logging.getLogger(__name__)


def admin_only(func):
    """Decorator - Only admins can access this function"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in Config.ADMIN_IDS:
            await update.effective_message.reply_text(
                "⛔ <b>Admin Only</b>\n\n"
                "This feature is only available for administrators.",
                parse_mode="HTML"
            )
            logger.warning(f"Non-admin user {user_id} tried to access admin function: {func.__name__}")
            return
        
        return await func(update, context)
    return wrapper


def check_access(func):
    """Decorator - Check if user has access (admin-only mode check)"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id
        
        # Log access
        logger.info(f"User {user_id} ({user.username or user.first_name}) accessing {func.__name__}")
        
        # Check admin-only mode
        if Config.ADMIN_ONLY and user_id not in Config.ADMIN_IDS:
            message = (
                "⛔ <b>Access Denied</b>\n\n"
                "Bot ini dalam mode <b>Admin Only</b>.\n"
                f"User ID kamu: <code>{user_id}</code>\n\n"
                "Hubungi admin untuk mendapatkan akses."
            )
            
            if update.callback_query:
                await update.callback_query.answer(
                    "⛔ Access Denied - Admin Only",
                    show_alert=True
                )
                await update.callback_query.message.reply_text(message, parse_mode="HTML")
            else:
                await update.message.reply_text(message, parse_mode="HTML")
            
            logger.warning(f"Access denied for user {user_id} (Admin-only mode enabled)")
            return
        
        return await func(update, context)
    return wrapper
