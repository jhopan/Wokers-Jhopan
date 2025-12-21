"""
Callback Query Handlers
Handle inline keyboard button callbacks
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.config import Config
from app.constants import COUNTRIES, PROTOCOLS, FORMATS, PORTS
from app.utils import check_access, admin_only
from app.utils.api import fetch_config

logger = logging.getLogger(__name__)


class CallbackHandlers:
    """Callback query handlers"""
    
    def __init__(self, user_data: dict):
        self.user_data = user_data
    
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
    async def handle_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    async def handle_country(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle country selection"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        country_code = query.data.replace("country_", "")
        
        user_data = self.get_user_data(user_id)
        user_data["country"] = country_code
        
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
    async def handle_protocol(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle protocol selection"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        protocol = query.data.replace("protocol_", "")
        
        user_data = self.get_user_data(user_id)
        user_data["protocol"] = protocol
        
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
    async def handle_format(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle format selection"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        format_code = query.data.replace("format_", "")
        
        user_data = self.get_user_data(user_id)
        user_data["format"] = format_code
        
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
    async def handle_port(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle port selection and generate config"""
        query = update.callback_query
        await query.answer("⏳ Generating config...")
        
        user_id = update.effective_user.id
        port = query.data.replace("port_", "")
        
        user_data = self.get_user_data(user_id)
        user_data["port"] = port
        
        await self.generate_config(update, context, user_data)
    
    async def generate_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        """Generate and send VPN config"""
        query = update.callback_query
        
        try:
            # Build API params
            params = {
                "cc": user_data["country"],
                "vpn": user_data["protocol"],
                "port": user_data["port"],
                "limit": str(user_data["limit"]),
                "format": user_data["format"]
            }
            
            # Fetch config from API
            config = fetch_config(params)
            
            if not config:
                raise Exception("Failed to fetch config from API")
            
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
            test_config = fetch_config({
                "cc": "ID",
                "vpn": "vless",
                "port": "443",
                "limit": "1",
                "format": "raw"
            })
            
            api_status = "✅ Online" if test_config else "❌ Offline"
        except Exception:
            api_status = "❌ Offline"
        
        keyboard = [[InlineKeyboardButton("« Kembali", callback_data="back_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""
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
            [InlineKeyboardButton("« Kembali", callback_data="back_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"""
👑 <b>Admin Panel</b>

<b>Bot Info:</b>
🤖 Status: ✅ Running
👥 Total Users: {len(self.user_data)}
🔒 Mode: {"Admin Only" if Config.ADMIN_ONLY else "Public"}

<b>Settings:</b>
🌐 Domain: {Config.WORKER_DOMAIN}
👑 Admins: {len(Config.ADMIN_IDS)}
"""
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
