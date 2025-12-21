"""
Jhopan VPN Telegram Bot
Bot untuk mengambil konfigurasi VPN dari Jhopan Cloudflare Workers

Features:
- Admin-only mode (opsional)
- Menu-based interface
- Support multiple protocols & formats
- Clean handler structure

Install:
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate    # Windows
pip install -r requirements.txt
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============== CONFIGURATION ==============
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
WORKER_DOMAIN = os.getenv("WORKER_DOMAIN", "jhopan.my.id")
API_BASE_URL = f"https://{WORKER_DOMAIN}/api/v1/sub"

# Admin settings
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
ADMIN_ONLY = os.getenv("ADMIN_ONLY", "false").lower() == "true"

# Default settings
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "ID")
DEFAULT_PROTOCOL = os.getenv("DEFAULT_PROTOCOL", "vless")
DEFAULT_PORT = os.getenv("DEFAULT_PORT", "443")
DEFAULT_FORMAT = os.getenv("DEFAULT_FORMAT", "raw")
DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", "10"))

# API settings
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# ============================================

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Data untuk menu
COUNTRIES = {
    "🇮🇩 Indonesia": "ID",
    "🇸🇬 Singapore": "SG",
    "🇺🇸 United States": "US",
    "🇯🇵 Japan": "JP",
    "🇰🇷 Korea": "KR",
    "🇩🇪 Germany": "DE",
    "🇬🇧 United Kingdom": "GB",
    "🇫🇷 France": "FR",
    "🇭🇰 Hong Kong": "HK",
    "🇳🇱 Netherlands": "NL",
    "🇨🇦 Canada": "CA",
    "🇦🇺 Australia": "AU",
    "🇧🇷 Brazil": "BR",
    "🇮🇳 India": "IN",
    "🇲🇾 Malaysia": "MY",
    "🇹🇭 Thailand": "TH",
    "🇻🇳 Vietnam": "VN",
    "🇹🇷 Turkey": "TR",
    "🌍 All Countries": "ALL"
}

PROTOCOLS = {
    "⚡ VLESS": "vless",
    "🔒 Trojan": "trojan",
    "🥷 Shadowsocks": "ss",
    "🌐 All Protocols": "vless,trojan,ss"
}

FORMATS = {
    "📝 Raw/Text": "raw",
    "⚔️ Clash": "clash",
    "📦 Sing-Box (SFA)": "sfa",
    "🎯 v2rayN": "v2ray"
}

PORTS = {
    "🔐 443 (TLS)": "443",
    "🌐 80 (Non-TLS)": "80",
    "🔄 Both": "443,80"
}


# ============== DECORATORS ==============

def admin_only(func):
    """Decorator untuk command/callback yang hanya bisa diakses admin"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if ADMIN_ONLY and user_id not in ADMIN_IDS:
            await update.effective_message.reply_text(
                "⛔ <b>Access Denied</b>\n\n"
                "Bot ini hanya bisa digunakan oleh admin.\n"
                "Hubungi @jhopan untuk akses.",
                parse_mode="HTML"
            )
            return
        
        return await func(update, context)
    return wrapper


def check_access(func):
    """Decorator untuk cek akses user"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user = update.effective_user
        
        # Log akses
        logger.info(f"User {user_id} ({user.username or user.first_name}) accessing {func.__name__}")
        
        # Cek admin-only mode
        if ADMIN_ONLY and user_id not in ADMIN_IDS:
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
            return
        
        return await func(update, context)
    return wrapper


# ============== HANDLERS ==============

class JhopanBot:
    """Main bot class with clean handler structure"""
    
    def __init__(self):
        self.user_data = {}  # Store user preferences
    
    def get_user_data(self, user_id):
        """Get or initialize user data"""
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "country": DEFAULT_COUNTRY,
                "protocol": DEFAULT_PROTOCOL,
                "port": DEFAULT_PORT,
                "format": DEFAULT_FORMAT,
                "limit": DEFAULT_LIMIT
            }
        return self.user_data[user_id]
    
    # ===== COMMAND HANDLERS =====
    
    @check_access
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler: /start - Show main menu"""
        user = update.effective_user
        user_id = user.id
        
        # Check if admin
        is_admin = user_id in ADMIN_IDS
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
        await self.show_country_menu(update, context)
    
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
            response = requests.get(
                f"{API_BASE_URL}?cc=ID&vpn=vless&port=443&limit=1&format=raw",
                timeout=5
            )
            
            api_status = "✅ Online" if response.status_code == 200 else "⚠️ Slow"
        except Exception as e:
            api_status = f"❌ Offline ({str(e)})"
        
        status_text = f"""
📊 <b>Status Jhopan VPN</b>

🤖 <b>Bot:</b> ✅ Running
🌐 <b>API:</b> {api_status}
🔗 <b>Domain:</b> {WORKER_DOMAIN}

👥 <b>Mode:</b> {"🔒 Admin Only" if ADMIN_ONLY else "🌍 Public"}
👑 <b>Admins:</b> {len(ADMIN_IDS)} user(s)

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
        is_admin = user_id in ADMIN_IDS
        
        message = f"""
👤 <b>Info User</b>

<b>User ID:</b> <code>{user_id}</code>
<b>Username:</b> @{user.username or 'N/A'}
<b>Name:</b> {user.first_name} {user.last_name or ''}
<b>Role:</b> {"👑 Admin" if is_admin else "👤 User"}

💡 <i>Copy User ID di atas untuk registrasi admin</i>
"""
        await update.message.reply_text(message, parse_mode="HTML")
    
    # ===== CALLBACK HANDLERS =====
    
    @check_access
    async def callback_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle main menu callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "menu_config":
            await self.show_country_menu(update, context)
        elif data == "menu_settings":
            await self.show_settings_menu(update, context)
        elif data == "menu_status":
            await self.show_status(update, context)
        elif data == "menu_help":
            await self.show_help(update, context)
        elif data == "menu_admin":
            await self.show_admin_panel(update, context)
        elif data == "back_main":
            await self.show_main_menu(update, context)
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show main menu"""
        query = update.callback_query
        user = update.effective_user
        user_id = user.id
        is_admin = user_id in ADMIN_IDS
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
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    
    async def show_country_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show country selection menu"""
        keyboard = []
        row = []
        
        for name, code in COUNTRIES.items():
            row.append(InlineKeyboardButton(name, callback_data=f"country_{code}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        
        if row:
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("« Kembali", callback_data="back_main")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = """
🌍 <b>Pilih Negara Server</b>

Pilih negara server yang ingin kamu gunakan:
"""
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                message,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text(
                message,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
    
    @check_access
    async def callback_country(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle country selection"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        country_code = query.data.replace("country_", "")
        
        user_data = self.get_user_data(user_id)
        user_data["country"] = country_code
        
        # Show protocol menu
        await self.show_protocol_menu(update, context, country_code)
    
    async def show_protocol_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, country_code: str):
        """Show protocol selection menu"""
        query = update.callback_query
        
        keyboard = []
        for name, code in PROTOCOLS.items():
            keyboard.append([InlineKeyboardButton(name, callback_data=f"protocol_{code}")])
        
        keyboard.append([InlineKeyboardButton("« Kembali", callback_data="menu_config")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        country_name = [k for k, v in COUNTRIES.items() if v == country_code][0]
        
        message = f"""
🔐 <b>Pilih Protokol</b>

Negara: {country_name}

<b>Protocol Info:</b>
⚡ <b>VLESS</b> - Modern, cepat, low latency
🔒 <b>Trojan</b> - Stealthy, bypass censorship
🥷 <b>Shadowsocks</b> - Popular, widely supported
"""
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    
    @check_access
    async def callback_protocol(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle protocol selection"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        protocol = query.data.replace("protocol_", "")
        
        user_data = self.get_user_data(user_id)
        user_data["protocol"] = protocol
        
        # Show format menu
        await self.show_format_menu(update, context)
    
    async def show_format_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show format selection menu"""
        query = update.callback_query
        
        keyboard = []
        for name, code in FORMATS.items():
            keyboard.append([InlineKeyboardButton(name, callback_data=f"format_{code}")])
        
        keyboard.append([InlineKeyboardButton("« Kembali", callback_data="menu_config")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = """
📋 <b>Pilih Format Output</b>

<b>Format Info:</b>
📝 <b>Raw/Text</b> - Universal link
⚔️ <b>Clash</b> - Clash for Windows/Android
📦 <b>Sing-Box</b> - SFA/Sing-Box client
🎯 <b>v2rayN</b> - Base64 subscription
"""
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    
    @check_access
    async def callback_format(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle format selection"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        format_code = query.data.replace("format_", "")
        
        user_data = self.get_user_data(user_id)
        user_data["format"] = format_code
        
        # Show port menu
        await self.show_port_menu(update, context)
    
    async def show_port_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show port selection menu"""
        query = update.callback_query
        
        keyboard = []
        for name, code in PORTS.items():
            keyboard.append([InlineKeyboardButton(name, callback_data=f"port_{code}")])
        
        keyboard.append([InlineKeyboardButton("« Kembali", callback_data="menu_config")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = """
🔌 <b>Pilih Port</b>

<b>Port Info:</b>
🔐 <b>443 (TLS)</b> - Encrypted, secure
🌐 <b>80 (Non-TLS)</b> - Fast, no encryption
🔄 <b>Both</b> - Get both options
"""
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    
    @check_access
    async def callback_port(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle port selection and generate config"""
        query = update.callback_query
        await query.answer("⏳ Generating config...")
        
        user_id = update.effective_user.id
        port = query.data.replace("port_", "")
        
        user_data = self.get_user_data(user_id)
        user_data["port"] = port
        
        # Generate config
        await self.generate_config(update, context, user_data)
    
    async def generate_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        """Generate and send VPN config"""
        query = update.callback_query
        
        try:
            # Build API URL
            params = {
                "cc": user_data["country"],
                "vpn": user_data["protocol"],
                "port": user_data["port"],
                "limit": user_data["limit"],
                "format": user_data["format"]
            }
            
            # Call API
            response = requests.get(
                API_BASE_URL,
                params=params,
                timeout=API_TIMEOUT
            )
            
            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")
            
            config = response.text
            
            # Send config
            format_name = [k for k, v in FORMATS.items() if v == user_data["format"]][0]
            country_name = [k for k, v in COUNTRIES.items() if v == user_data["country"]][0]
            protocol_name = [k for k, v in PROTOCOLS.items() if v == user_data["protocol"]][0]
            
            message = f"""
✅ <b>Config Generated!</b>

<b>Settings:</b>
🌍 Country: {country_name}
🔐 Protocol: {protocol_name}
📋 Format: {format_name}
🔌 Port: {user_data["port"]}

<b>Config:</b>
<code>{config}</code>

💡 Copy config di atas dan import ke aplikasi VPN kamu
"""
            
            # Back to main menu button
            keyboard = [[InlineKeyboardButton("🏠 Menu Utama", callback_data="back_main")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                message,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
            
        except Exception as e:
            logger.error(f"Error generating config: {e}")
            
            error_message = f"""
❌ <b>Error</b>

Gagal generate config: {str(e)}

Silakan coba lagi atau hubungi admin.
"""
            
            keyboard = [[InlineKeyboardButton("🔄 Coba Lagi", callback_data="menu_config")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                error_message,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
    
    async def show_settings_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show settings menu"""
        query = update.callback_query
        user_id = update.effective_user.id
        user_data = self.get_user_data(user_id)
        
        keyboard = [
            [InlineKeyboardButton(f"📊 Limit: {user_data['limit']}", callback_data="setting_limit")],
            [InlineKeyboardButton("🔄 Reset Settings", callback_data="setting_reset")],
            [InlineKeyboardButton("« Kembali", callback_data="back_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""
⚙️ <b>Pengaturan</b>

<b>Current Settings:</b>
🌍 Country: {user_data['country']}
🔐 Protocol: {user_data['protocol']}
📋 Format: {user_data['format']}
🔌 Port: {user_data['port']}
📊 Limit: {user_data['limit']}
"""
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    
    async def show_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show bot status"""
        query = update.callback_query
        
        try:
            # Test API
            response = requests.get(
                f"{API_BASE_URL}?cc=ID&vpn=vless&port=443&limit=1&format=raw",
                timeout=5
            )
            
            api_status = "✅ Online" if response.status_code == 200 else "⚠️ Slow"
        except Exception as e:
            api_status = f"❌ Offline"
        
        keyboard = [[InlineKeyboardButton("« Kembali", callback_data="back_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""
📊 <b>Status Jhopan VPN</b>

🤖 <b>Bot:</b> ✅ Running
🌐 <b>API:</b> {api_status}
🔗 <b>Domain:</b> {WORKER_DOMAIN}

👥 <b>Mode:</b> {"🔒 Admin Only" if ADMIN_ONLY else "🌍 Public"}
👑 <b>Admins:</b> {len(ADMIN_IDS)} user(s)

📈 <b>Stats:</b>
• Active users: {len(self.user_data)}
• Countries: 51
• Servers: 316+
"""
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    
    async def show_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help message"""
        query = update.callback_query
        
        keyboard = [[InlineKeyboardButton("« Kembali", callback_data="back_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = """
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
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    
    @admin_only
    async def show_admin_panel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show admin panel"""
        query = update.callback_query
        
        keyboard = [
            [
                InlineKeyboardButton("👥 Users", callback_data="admin_users"),
                InlineKeyboardButton("📊 Stats", callback_data="admin_stats")
            ],
            [InlineKeyboardButton("🔄 Restart Bot", callback_data="admin_restart")],
            [InlineKeyboardButton("« Kembali", callback_data="back_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""
👑 <b>Admin Panel</b>

<b>Bot Info:</b>
🤖 Status: ✅ Running
👥 Total Users: {len(self.user_data)}
🔒 Mode: {"Admin Only" if ADMIN_ONLY else "Public"}

<b>Settings:</b>
🌐 Domain: {WORKER_DOMAIN}
👑 Admins: {len(ADMIN_IDS)}
"""
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )


# ============== MAIN ==============

def main():
    """Run the bot"""
    
    if not TELEGRAM_BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN not found in .env file!")
        logger.error("Please create .env file and add your bot token")
        return
    
    logger.info("🚀 Starting Jhopan VPN Bot...")
    
    if ADMIN_ONLY:
        logger.info(f"🔒 Running in ADMIN ONLY mode")
        logger.info(f"👑 Allowed admins: {ADMIN_IDS}")
    else:
        logger.info("🌍 Running in PUBLIC mode")
    
    # Create bot instance
    bot = JhopanBot()
    
    # Build application
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Register command handlers
    app.add_handler(CommandHandler("start", bot.cmd_start))
    app.add_handler(CommandHandler("config", bot.cmd_config))
    app.add_handler(CommandHandler("help", bot.cmd_help))
    app.add_handler(CommandHandler("status", bot.cmd_status))
    app.add_handler(CommandHandler("myid", bot.cmd_myid))
    
    # Register callback handlers
    app.add_handler(CallbackQueryHandler(bot.callback_menu, pattern="^menu_"))
    app.add_handler(CallbackQueryHandler(bot.callback_menu, pattern="^back_"))
    app.add_handler(CallbackQueryHandler(bot.callback_country, pattern="^country_"))
    app.add_handler(CallbackQueryHandler(bot.callback_protocol, pattern="^protocol_"))
    app.add_handler(CallbackQueryHandler(bot.callback_format, pattern="^format_"))
    app.add_handler(CallbackQueryHandler(bot.callback_port, pattern="^port_"))
    
    # Start bot
    logger.info("✅ Bot started successfully!")
    logger.info(f"🌐 API: {API_BASE_URL}")
    
    app.run_polling()


if __name__ == "__main__":
    main()
