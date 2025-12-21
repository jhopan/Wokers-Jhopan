"""
Jhopan VPN Telegram Bot
Bot untuk mengambil konfigurasi VPN dari Jhopan Cloudflare Workers

Requirements:
- python-telegram-bot
- requests

Install: pip install python-telegram-bot requests
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import requests
from typing import Optional

# ============== CONFIGURATION ==============
# Ganti dengan token bot Telegram kamu dari @BotFather
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Domain Cloudflare Workers (sudah pakai custom domain)
WORKER_DOMAIN = "jhopan.my.id"

# URL API Jhopan
API_BASE_URL = f"https://{WORKER_DOMAIN}/api/v1/sub"

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


class JhopanBot:
    """Bot Telegram untuk Jhopan VPN"""
    
    def __init__(self):
        self.user_settings = {}  # Store user preferences
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk command /start - Tampilkan menu utama"""
        user = update.effective_user
        
        # Main menu keyboard
        keyboard = [
            [InlineKeyboardButton("🚀 Ambil Config VPN", callback_data="main_get_config")],
            [
                InlineKeyboardButton("⚙️ Pengaturan", callback_data="main_settings"),
                InlineKeyboardButton("📊 Status Server", callback_data="main_stats")
            ],
            [InlineKeyboardButton("❓ Bantuan", callback_data="main_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_message = f"""
👋 <b>Halo {user.first_name}!</b>

Selamat datang di <b>Jhopan VPN Bot</b> 🚀

<b>📋 Protokol Tersedia:</b>
• VLESS (Cepat & Ringan)
• Trojan (Aman & Stealthy)
• Shadowsocks (Populer)

<b>🌍 Server Global:</b>
Indonesia, Singapore, US, Japan, Korea, dll

<b>💎 100% GRATIS!</b>

Pilih menu di bawah untuk memulai:
"""
        
        if update.message:
            await update.message.reply_html(welcome_message, reply_markup=reply_markup)
        else:
            await update.callback_query.message.edit_text(welcome_message, reply_markup=reply_markup, parse_mode="HTML")
    
    async def show_country_menu(self, query):
        """Tampilkan menu pilihan negara"""
        keyboard = []
        row = []
        for idx, (name, code) in enumerate(COUNTRIES.items()):
            row.append(InlineKeyboardButton(name, callback_data=f"country_{code}"))
🚀 Ambil Config VPN - Pilih negara, protocol, format

<b>2️⃣ Pengaturan:</b>
⚙️ Pengaturan - Lihat pengaturan saat ini
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="back_to_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🌍 <b>Pilih Negara Server:</b>\n\nPilih lokasi server yang kamu inginkan:",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    
    async def show_settings(self, query, user_id):
        """Tampilkan pengaturan user"""
        settings = self.user_settings.get(user_id, {})
        
        settings_text = f"""
⚙️ <b>Pengaturan Saat Ini</b>

📍 Negara: {settings.get('country', 'Belum diatur')}
⚡ Protocol: {settings.get('protocol', 'Belum diatur')}
🔌 Port: {settings.get('port', 'Belum diatur')}
📦 Format: {settings.get('format', 'Belum diatur')}

<i>Pengaturan ini akan digunakan saat kamu ambil config</i>
"""
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(settings_text, reply_markup=reply_markup, parse_mode="HTML")
    
    async def show_stats(self, query):
        """Tampilkan statistik server"""
        try:
            response = requests.get(f"https://{WORKER_DOMAIN}/api/v1/myip", timeout=10)
            data = response.json()
            
            stats_text = f"""
📊 <b>Status Server</b>

🌐 <b>Domain:</b> {WORKER_DOMAIN}
📍 <b>Lokasi:</b> {data.get('colo', 'Unknown')}
⚡ <b>Status:</b> ✅ Online
⏱️ <b>Response:</b> {response.elapsed.total_seconds() * 1000:.0f}ms

<b>📋 Protocol:</b>
• VLESS ⚡
• Trojan 🔒
• Shadowsocks 🥷

<b>🌍 Server:</b>
ID, SG, US, JP, KR, DE, GB, FR, dll

<b>💰 Biaya:</b>
100% GRATIS!
"""
        except:
            stats_text = """
📊 <b>Status Server</b>

❌ Tidak dapat mengambil data server
Silakan coba lagi nanti
"""
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(stats_text, reply_markup=reply_markup, parse_mode="HTML")
    
    async def show_help(self, query):
        """Tampilkan bantuan"""
        help_text = """
<b>📖 Panduan Penggunaan</b>

<b>1️⃣ Dapatkan Konfigurasi:</b>
/get - Pilih negara, protocol, format

<b>2️⃣ Atur Preferensi:</b>
/settings - Atur default country, protocol, dll

<b>3️⃣ Format Output:</b>
• <b>Raw/Text</b> - Link mentah (untuk import manual)
• <b>Clash</b> - Format Clash for Windows
• <b>Sing-Box</b> - Format Sing-Box
• <b>v2rayN</b> - Base64 untuk v2rayN

<b>4️⃣ Cara Import:</b>

<i>Untuk Clash:</i>
1. Copy config yang diberikan bot
2. Buka Clash for Windows
3. Profiles > Import from clipboard

<i>Untuk v2rayN:</i>
1. Copy link yang diberikan bot
2. Buka v2rayN
3. Import > Import from clipboard

<i>Untuk Shadowrocket (iOS):</i>
1. Copy link mentah (raw)
2. Buka Shadowrocket
3. Tap + > Import from clipboard

<b>⚙️ Pengaturan VPN:</b>
• Security: <code>none</code>
• Transport: <code>ws</code> (WebSocket)
• TLS: Port 443 = ON, Port 80 = OFF
• Path: Auto (berisi proxy IP)

<b>🔧 Troubleshooting:</b>
• Tidak bisa browsing? Gunakan DoH: <code>https://8.8.8.8/dns-query</code>
• Connection timeout? Coba port lain (443/80)
• Slow speed? Pilih negara terdekat

<b>💡 Tips:</b>
• Gunakan UUID v4 variant 2
• Port 443 lebih stabil (TLS)
• Filter by country untuk speed optimal

<b>📊 Batasan:</b>
• Max 100 config per request
• WebSocket max 15 menit (auto-reconnect)
• Free tier: 100k requests/day

<i>🆘 Butuh bantuan? Hubungi admin</i>
"""
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        Redirect ke menu"""
        keyboard = [[InlineKeyboardButton("🚀 Mulai Ambil Config", callback_data="main_get_config")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_html(
            "Klik tombol di bawah untuk memulai:",
            reply_markup=reply_markupage.reply_html(help_text)
    
    async def get_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk command /get - Mulai proses get config"""
        keyboard = []
        row = []
        for idx, (name, code) in enumerate(COUNTRIES.items()):
            row.append(InlineKeyboardButton(name, callback_data=f"country_{code}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🌍 <b>Pilih Negara:</b>",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk button callback"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = update.effective_user.id
        
        # Initialize user settings if not exists
        if user_id not in self.user_settings:
            self.user_settings[user_id] = {}
        
        # Handle main menu
        if data == "main_get_config":
            await self.show_country_menu(query)
            return
        elif data == "main_settings":
            await self.show_settings(query, user_id)
            return
        elif data == "main_stats":
            await self.show_stats(query)
            return
        elif data == "main_help":
            await self.show_help(query)
            return
        elif data == "back_to_main":
            await self.start(update, context)
            return
        
        # Handle country selection
        if data.startswith("country_"):
            country = data.replace("country_", "")
            self.user_settings[user_id]["country"] = country
            
            # Show protocol selection
            keyboard = []
            row = []
            for idx, (name, proto) in enumerate(PROTOCOLS.items()):
                row.append(InlineKeyboardButton(name, callback_data=f"protocol_{proto}"))
                if len(row) == 2:
                    keyboard.append(row)
                    row = []
            if row:
                keyboard.append(row)
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "⚡ <b>Pilih Protocol:</b>",
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
        
        # Handle protocol selection
        elif data.startswith("protocol_"):
            protocol = data.replace("protocol_", "")
            self.user_settings[user_id]["protocol"] = protocol
            
            # Show port selection
            keyboard = []
            for name, port in PORTS.items():
                keyboard.append([InlineKeyboardButton(name, callback_data=f"port_{port}")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "🔌 <b>Pilih Port:</b>",
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
        
        # Handle port selection
        elif data.startswith("port_"):
            port = data.replace("port_", "")
            self.user_settings[user_id]["port"] = port
            
            # Show format selection
            keyboard = []
            for name, fmt in FORMATS.items():
                keyboard.append([InlineKeyboardButton(name, callback_data=f"format_{fmt}")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "📦 <b>Pilih Format Output:</b>",
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
        
        # Handle format selection - Final step, fetch config
        elif data.startswith("format_"):
            fmt = data.replace("format_", "")
            self.user_settings[user_id]["format"] = fmt
            
            await query.edit_message_text("⏳ <b>Mengambil konfigurasi...</b>", parse_mode="HTML")
            
            # Fetch configuration
            config = await self.fetch_config(user_id)
            
            if config:
                await self.send_config(query, config, fmt, user_id)
            else:
                await query.edit_message_text(
                    "❌ <b>Gagal mengambil konfigurasi!</b>\n\n"
                    "Silakan coba lagi atau hubungi admin.",
                    parse_mode="HTML"
                )
    
    async def fetch_config(self, user_id: int) -> Optional[str]:
        """Fetch configuration from Nautica API"""
        settings = self.user_settings.get(user_id, {})
        
        # Build API parameters
        params = {
            "limit": 10,  # Default 10 configs
            "format": settings.get("format", "raw"),
        }
        
        # Add country filter if not ALL
        country = settings.get("country", "ALL")
        if country != "ALL":
            params["cc"] = country
        
        # Add protocol filter
        protocol = settings.get("protocol", "vless,trojan,ss")
        params["vpn"] = protocol
        
        # Add port filter
        port = settings.get("port", "443,80")
        params["port"] = port
        
        # Add domain
        params["domain"] = WORKER_DOMAIN
        
        try:
            logger.info(f"Fetching config with params: {params}")
            response = requests.get(API_BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching config: {e}")
            return None
    
    async def send_config(self, query, config: str, fmt: str, user_id: int):
        """Send configuration to user"""
        # Add back button
        keyboard = [[InlineKeyboardButton("🔙 Menu Utama", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(summary, parse_mode="HTML")
        
        # Send back to main button as separate message
        await query.message.reply_html(
            "Gunakan tombol di bawah untuk kembali:",
            reply_markup=reply_markup
        )

<i>Mengirim konfigurasi...</i>
"""
        await query.edit_message_text(summary, parse_mode="HTML")
        
        # Send config based on format
        if fmt == "raw":
            # Split by newline and send as text
            configs = config.strip().split("\n")
            message = f"<b>📝 Konfigurasi Raw ({len(configs)} links):</b>\n\n"
            message += "<code>" + config[:4000] + "</code>"  # Telegram limit 4096 chars
            
            await query.message.reply_html(message)
            
            # If too long, send as file
            if len(config) > 4000:
                with open(f"config_{user_id}.txt", "w") as f:
                    f.write(config)
                await query.message.reply_document(
                    document=open(f"config_{user_id}.txt", "rb"),
                    filename="nautica_config.txt",
                    caption="📄 <b>Full configuration file</b>",
                    parse_mode="HTML"
                )
        
        elif fmt in ["clash", "sfa"]:
            # Send as YAML/JSON file
            filename = f"nautica_{fmt}.{'yaml' if fmt == 'clash' else 'json'}"
            with open(f"config_{user_id}_{fmt}", "w") as f:
                f.write(config)
            
            await query.message.reply_document(
                document=open(f"config_{user_id}_{fmt}", "rb"),
                filename=filename with menu button
        keyboard = [
            [InlineKeyboardButton("🔄 Ambil Config Lagi", callback_data="main_get_config")],
            [InlineKeyboardButton("🏠 Menu Utama", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        instructions = """
<b>📱 Cara Import:</b>

<b>Clash for Windows:</b>
• Profiles > Import > From File/Clipboard

<b>v2rayN:</b>
• Servers > Import > From Clipboard

<b>Shadowrocket (iOS):</b>
• + > Import from Clipboard

<b>v2rayNG (Android):</b>
• + > Import from Clipboard

<b>⚙️ Pengaturan Penting:</b>
• Security: <code>none</code>
• Transport: <code>ws</code>
• Jika tidak bisa browsing, set DoH: <code>https://8.8.8.8/dns-query</code>

<i>Selamat menggunakan VPN gratis! 🚀</i>
"""
        await query.message.reply_html(instructions, reply_markup=reply_markup
<b>v2rayNG (Android):</b>
• + > Import from Clipboard

<b>⚙️ Pengaturan Penting:</b>
• Security: <code>none</code>
• Transport: <code>ws</code>
• Jika tidak bisa browsing, set DoH: <code>https://8.8.8.8/dns-query</code>

<b>🔄 Get New Config:</b>
/get - Ambil konfigurasi baru

<i>Enjoy your free VPN! 🚀</i>
"""
        await query.message.reply_html(instructions)
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk command /stats"""
        try:
            # Fetch myip to get server info
            response = requests.get(f"https://{WORKER_DOMAIN}/api/v1/myip", timeout=10)
            data = response.json()
            
            stats_message = f"""
📊 <b>Server Statistics</b>

🌐 <b>Worker Domain:</b>
<code>{WORKER_DOMAIN}</code>

🔗 <b>API Endpoint:</b>
<code>{API_BASE_URL}</code>

📍 <b>Server Location:</b>
Colo: {data.get('colo', 'Unknown')}

✅ <b>Status:</b> Online
⚡ <b>Response Time:</b> {response.elapsed.total_seconds() * 1000:.0f}ms

<b>📋 Available Protocols:</b>
• VLESS ⚡
• Trojan 🔒
• Shadowsocks 🥷

<b>🌍 Available Countries:</b>
• ID, SG, US, JP, KR, DE, GB, FR, etc.

<b>💡 Limits (Free Tier):</b>
• 100,000 requests/day
• 10ms CPU time/request
• WebSocket max 15 min

<i>Last updated: {data.get('timestamp', 'Unknown')}</i>
"""
            await update.message.reply_html(stats_message)
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            await update.message.reply_html(
                "❌ <b>Gagal mendapatkan statistik server</b>\n\n"
                "Server mungkin sedang down atau maintenance."
            )
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk command /settings"""
        user_id = update.effective_user.id
        settings = self.user_settings.get(user_id, {})
        
        current_settings = f"""
⚙️ <b>Pengaturan Saat Ini</b>

📍 <b>Default Country:</b> {settings.get('country', 'Not Set')}
⚡ <b>Default Protocol:</b> {settings.get('protocol', 'Not Set')}
🔌 <b>Default Port:</b> {settings.get('port', 'Not Set')}
📦 <b>Default Format:</b> {settings.get('format', 'Not Set')}

<i>Pengaturan akan digunakan sebagai default untuk request berikutnya.</i>

Gunakan /get untuk mengubah pengaturan.
"""
        await update.message.reply_html(current_settings)
    
    def run(self):
        """Run the bot"""
        # Create application
        app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("get", self.get_config))
        app.add_handler(CommandHandler("stats", self.stats_command))
        app.add_handler(CommandHandler("settings", self.settings_command))
        app.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Start bot
        logger.info("🤖 Bot started!")
        print("=" * 50)
        print("🤖 Nautica VPN Bot is running...")
        print("=" * 50)
        app.run_polling()


if __name__ == "__main__":
    bot = NauticaBot()
    bot.run()
JhopanJhopan