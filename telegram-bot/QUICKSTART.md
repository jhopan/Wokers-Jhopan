# 🚀 Quick Start - Jhopan VPN Bot

## 📦 Instalasi di Linux

### Cara Paling Mudah (Automatic Installer):

```bash
# 1. Clone repository
git clone https://github.com/jhopan/Wokers-Jhopan.git
cd Wokers-Jhopan/telegram-bot

# 2. Run installer (otomatis buat venv & install dependencies)
chmod +x install.sh
./install.sh

# 3. Setup bot token
cp .env.example .env
nano .env  # Edit dan masukkan bot token dari @BotFather

# 4. Jalankan bot
./run.sh
```

### Setup Admin-Only Mode:

Edit file `.env`:

```env
# Bot token dari @BotFather
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Domain worker kamu
WORKER_DOMAIN=jhopan.my.id

# Admin-only mode (true = hanya admin, false = public)
ADMIN_ONLY=true

# ID Telegram admin (pisahkan dengan koma jika lebih dari 1)
# Cek ID dengan command /myid di bot
ADMIN_IDS=123456789,987654321
```

---

## 🎯 Cara Dapat User ID

1. Start bot: `/start`
2. Ketik command: `/myid`
3. Bot akan reply dengan User ID kamu
4. Copy ID tersebut ke `.env` di `ADMIN_IDS`

---

## 🔒 Disable Website (Hanya Telegram)

Jika kamu mau **non-aktifkan website** dan hanya pakai bot:

### 1. Disable GitHub Pages:
- Buka repo di GitHub
- Settings → Pages
- Source: **None**
- Save

### 2. Enable Admin-Only di Bot:

```env
ADMIN_ONLY=true
ADMIN_IDS=your_user_id
```

### 3. (Opsional) Password Protect API:

Tambahkan token di API request untuk extra security.

---

## ✅ Perintah Bot

| Command | Fungsi |
|---------|--------|
| `/start` | Menu utama |
| `/config` | Quick access ambil config |
| `/help` | Bantuan & cara pakai |
| `/status` | Status bot & API |
| `/myid` | Cek User ID kamu |

---

## 🐛 Troubleshooting

### Error: externally-managed-environment

**Solusi:** Pakai virtual environment (sudah otomatis di installer)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Bot tidak respon

**Cek:**
1. ✅ Token bot benar di `.env`
2. ✅ Virtual environment aktif: `source venv/bin/activate`
3. ✅ Dependencies installed: `pip list | grep telegram`
4. ✅ Internet connection

### Access Denied di bot

**Solusi:** 
- Cek `ADMIN_ONLY` setting di `.env`
- Pastikan User ID kamu ada di `ADMIN_IDS`
- Gunakan `/myid` untuk cek ID

---

## 📚 File Structure

```
telegram-bot/
├── bot.py              # Main bot (NEW - clean handler)
├── telegram-bot.py     # Old bot (deprecated)
├── install.sh          # Auto installer Linux/Mac
├── install.bat         # Auto installer Windows
├── run.sh              # Run script Linux/Mac
├── run.bat             # Run script Windows
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
└── .env                # Your config (create this)
```

---

## 🎉 Done!

Bot sudah siap digunakan. Jika ada masalah, cek troubleshooting atau buka issue di GitHub.

**Happy Tunneling! 🚀**
