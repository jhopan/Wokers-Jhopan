"""
Command Handlers
/start, /config, /help, /status, /myid
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.config import Config
from app.utils import check_access, admin_only
from app.utils.api import fetch_config

logger = logging.getLogger(__name__)


class CommandHandlers:
    """Command handlers for the bot"""
    
    def __init__(self):
        self.user_data = {}
    
    def get_user_data(self, user_id: int) -> dict:
        """Get or initialize user data"""
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "country": Config.DEFAULT_COUNTRY,
                "protocol": Config.DEFAULT_PROTOCOL,
                "port": Config.DEFAULT_PORT,
                "format": Config.DEFAULT_FORMAT,
                "limit": Config.DEFAULT_LIMIT
            }
        return self.user_data[user_id]
    
    @check_access
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler: /start - Show main menu"""
        user = update.effective_user
        user_id = user.id
        is_admin = user_id in Config.ADMIN_IDS
        admin_badge = " 👑" if is_admin else ""
        
        keyboard = [
            [InlineKeyboardButton("🚀 Ambil Config VPN", callback_data="menu_config")],
            [
                InlineKeyboardButton("⚙️ Pengaturan", callback_data="menu_settings"),
                InlineKeyboardButton("📊 Status", callback_data="menu_status")
            ],
            [InlineKeyboardButton("❓ Bantuan", callback_data="menu_help")]
        ]
        
        if is_admin:
            keyboard.append([InlineKeyboardButton("👑 Admin Panel", callback_data="menu_admin")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""
👋 <b>Halo {user.first_name}{admin_badge}!</b>

Selamat datang di <b>Jhopan VPN Bot</b> 🚀

🌍 <b>51 Negara</b> | 316+ Server
🔐 <b>3 Protokol</b>: VLESS, Trojan, Shadowsocks
📋 <b>4 Format</b>: Raw, Clash, Sing-Box, v2rayN

Pilih menu di bawah untuk memulai:
"""
        
        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    
    @check_access
    async def cmd_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler: /config - Quick access to config menu"""
        from .callbacks import CallbackHandlers
        callback_handler = CallbackHandlers(self.user_data)
        await callback_handler.show_country_menu(update, context)
    
    @check_access
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler: /help - Show help message"""
        help_text = """
📚 <b>Bantuan Jhopan VPN Bot</b>

<b>Command:</b>
/start - Menu utama
/config - Ambil config VPN
/help - Bantuan
/status - Status server
/myid - Lihat User ID kamu

<b>Cara Pakai:</b>
1️⃣ Pilih negara server
2️⃣ Pilih protokol (VLESS/Trojan/SS)
3️⃣ Pilih format output
4️⃣ Pilih port (TLS/Non-TLS)
5️⃣ Salin config dan import ke app

<b>Aplikasi Client:</b>
• Android: V2RayNG, Clash for Android
• iOS: Shadowrocket, Stash
• Windows: v2rayN, Clash for Windows
• macOS: V2RayX, ClashX

<b>Support:</b>
GitHub: github.com/jhopan/Wokers-Jhopan
"""
        await update.message.reply_text(help_text, parse_mode="HTML")
    
    @check_access
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler: /status - Show bot & API status"""
        try:
            # Test API
            test_config = fetch_config({
                "cc": "ID",
                "vpn": "vless",
                "port": "443",
                "limit": "1",
                "format": "raw"
            })
            
            api_status = "✅ Online" if test_config else "❌ Offline"
        except Exception as e:
            api_status = f"❌ Error: {str(e)[:50]}"
        
        status_text = f"""
📊 <b>Status Jhopan VPN</b>

🤖 <b>Bot:</b> ✅ Running
🌐 <b>API:</b> {api_status}
🔗 <b>Domain:</b> {Config.WORKER_DOMAIN}

👥 <b>Mode:</b> {"🔒 Admin Only" if Config.ADMIN_ONLY else "🌍 Public"}
👑 <b>Admins:</b> {len(Config.ADMIN_IDS)} user(s)

📈 <b>Stats:</b>
• Active users: {len(self.user_data)}
• Countries: 51
• Servers: 316+
"""
        await update.message.reply_text(status_text, parse_mode="HTML")
    
    @check_access
    async def cmd_myid(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler: /myid - Show user ID"""
        user = update.effective_user
        user_id = user.id
        is_admin = user_id in Config.ADMIN_IDS
        
        message = f"""
👤 <b>Info User</b>

<b>User ID:</b> <code>{user_id}</code>
<b>Username:</b> @{user.username or 'N/A'}
<b>Name:</b> {user.first_name} {user.last_name or ''}
<b>Role:</b> {"👑 Admin" if is_admin else "👤 User"}

💡 <i>Copy User ID di atas untuk registrasi admin</i>
"""
        await update.message.reply_text(message, parse_mode="HTML")
