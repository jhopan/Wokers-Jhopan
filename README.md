# Jhopan VPN - Free VPN Configuration Generator

![Cloudflare Workers](https://img.shields.io/badge/Cloudflare-Workers-F38020?logo=cloudflare)
![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-222222?logo=github)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

Sistem VPN gratis berbasis Cloudflare Workers dengan generator konfigurasi untuk VLESS, Trojan, dan Shadowsocks. Mendukung 51 negara dengan 316+ proxy server.

## Fitur Utama

- **51 Negara** - Indonesia, Singapore, US, Japan, Korea, dll
- **3 Protokol** - VLESS, Trojan, Shadowsocks
- **4 Format** - Raw Links, Clash YAML, Base64, Sing-Box JSON
- **Auto Sorting** - Server terurut berdasarkan ping
- **Telegram Bot** - Interface menu untuk ambil config
- **Web Generator** - https://jhopan.github.io/Wokers-Jhopan
- **100% Gratis** - Tanpa subscription

---

## Struktur Project

```
Jhopan-VPN/
 _worker.js              # Main Cloudflare Worker (843 lines)
 index.html              # Web Generator Interface
 wrangler.toml           # Cloudflare Worker Config
 kvProxyList.json        # Proxy list 51 negara
 proxyList.txt           # Proxy bank (IP,Port,Country,Org)
 rawProxyList.txt        # Raw proxy data
 telegram-bot/           # Telegram Bot
    telegram-bot.py     # Main bot script
    setup.py            # Setup wizard
    requirements.txt    # Python dependencies
    .env.example        # Environment template
 helper/                 # Helper scripts
     proxyip.ts          # Proxy list generator
```

---

## Quick Start

### 1 Deploy Cloudflare Worker

#### **Opsi A: Via Dashboard (Recommended)**

1. Login ke https://dash.cloudflare.com
2. **Workers & Pages** **Create Application** **Create Worker**
3. **Edit Code**
4. **Hapus semua** code default
5. **Copy semua** dari `_worker.js` (843 baris)
6. **Paste** **Save and Deploy**

#### **Opsi B: Via Wrangler CLI**

```bash
# Install Wrangler
npm install -g wrangler

# Login
wrangler login

# Deploy
wrangler deploy
```

### 2 Setup Custom Domain (Opsional tapi Recommended)

1. Dashboard **Workers** Pilih worker kamu
2. **Settings** **Triggers** **Custom Domains**
3. **Add Custom Domain** Masukkan domain (contoh: `vpn.yourdomain.com`)
4. Tunggu 1-2 menit untuk DNS propagation

### 3 Setup GitHub Pages (Web Generator)

1. Fork/Clone repository ini
2. Push `index.html` ke GitHub
3. **Settings** **Pages**
4. **Source**: Deploy from branch `main` folder `/ (root)`
5. **Save** Tunggu 2-3 menit
6. Akses di `https://username.github.io/repository-name`

### 4️⃣ Setup Telegram Bot (Opsional)

#### **Linux/macOS:**

```bash
cd telegram-bot

# Run automatic installer
chmod +x install.sh
./install.sh

# Setup .env file
cp .env.example .env
nano .env  # Edit dan tambahkan BOT_TOKEN

# Run bot
./run.sh
```

#### **Windows:**

```cmd
cd telegram-bot

# Run automatic installer
install.bat

# Setup .env file
copy .env.example .env
notepad .env  # Edit dan tambahkan BOT_TOKEN

# Run bot
run.bat
```

#### **Manual Installation:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup .env
cp .env.example .env
# Edit .env and add your bot token

# Run bot
python bot.py
```

#### **Setup Admin-Only Mode:**

Edit file `.env`:

```env
# Admin-only mode: hanya admin yang bisa pakai bot
ADMIN_ONLY=true

# Telegram User ID admin (gunakan /myid untuk cek ID)
ADMIN_IDS=123456789,987654321
```

---

## Konfigurasi & Customization

### Mengubah URL & Domain

**File: `_worker.js`**

```javascript
// Line 18-20: Update URL sesuai domain kamu
const SUB_PAGE_URL = "https://username.github.io/repository-name";
const KV_PRX_URL =
  "https://raw.githubusercontent.com/username/repository/main/kvProxyList.json";
const PRX_BANK_URL =
  "https://raw.githubusercontent.com/username/repository/main/proxyList.txt";
```

**File: `index.html`**

```javascript
// Line 436: Update default worker domain
const workerDomain = urlParams.get("host") || "your-domain.com";
```

**File: `telegram-bot/bot.py`**

```python
# Edit .env file
WORKER_DOMAIN=your-domain.com
```

### Disable Website (Hanya Telegram)

Jika kamu ingin **non-aktifkan website** dan hanya pakai Telegram bot dengan admin-only:

**1. Disable GitHub Pages:**

- Repo Settings → Pages → Source: **None**
- Website akan mati, hanya API worker yang jalan

**2. Enable Admin-Only di Telegram Bot:**

Edit `telegram-bot/.env`:

```env
# Hanya admin yang bisa akses bot
ADMIN_ONLY=true

# ID Telegram admin (cek dengan /myid di bot)
ADMIN_IDS=123456789,987654321
```

**3. Optional - Password Protect Worker:**

Edit `_worker.js`, tambahkan di awal function:

```javascript
// Line ~100, di function handleRequest
async function handleRequest(request) {
  const url = new URL(request.url);

  // Password protection
  const authToken = url.searchParams.get("token");
  const SECRET_TOKEN = "your-secret-token-here"; // Ganti ini

  if (authToken !== SECRET_TOKEN) {
    return new Response("Unauthorized", { status: 401 });
  }

  // ... rest of code
}
```

Lalu update bot untuk include token:

```python
# telegram-bot/bot.py - Line ~40
API_BASE_URL = f"https://{WORKER_DOMAIN}/api/v1/sub?token=your-secret-token-here"
```

**Result:** Website mati ✅ | Telegram bot admin-only ✅ | API protected ✅
WORKER_DOMAIN = "your-domain.com"

```

---

##  API Documentation

### Endpoint: `/api/v1/sub`

**Base URL:** `https://your-domain.com/api/v1/sub`

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cc` | string | all | Country code (ID,SG,US,JP,dll) |
| `vpn` | string | all | Protocol (vless,trojan,ss) |
| `port` | string | 443,80 | Port (443,80) |
| `limit` | number | 10 | Jumlah config (1-50) |
| `format` | string | raw | Format output (raw,clash,v2ray,sfa) |

### Contoh Request

**Raw Links (Indonesia, VLESS, TLS):**
```

https://your-domain.com/api/v1/sub?cc=ID&vpn=vless&port=443&limit=10&format=raw

```

**Clash YAML (Singapore, All Protocols):**
```

https://your-domain.com/api/v1/sub?cc=SG&vpn=vless,trojan,ss&port=443&limit=20&format=clash

```

---

##  Penggunaan

### Via Web Generator

1. Buka https://your-domain.com/sub
2. Pilih **Country** (Indonesia, Singapore, dll)
3. Pilih **Protocol** (VLESS, Trojan, Shadowsocks)
4. Pilih **Security** (TLS atau NTLS)
5. Klik **Show Available Servers**
6. **Pilih server** dengan ping terendah
7. **Ganti format** (Raw/Clash/Base64/Sing-Box)
8. **Copy** atau **Download** config

### Via Telegram Bot

1. Start bot: `/start`
2. Klik: ** Ambil Config VPN**
3. Pilih negara: ** Indonesia**
4. Pilih protocol: ** VLESS**
5. Pilih format: ** Clash**
6. Pilih port: ** 443 (TLS)**
7. Terima config dalam format Clash YAML

---

##  Daftar Negara

| Code | Country | Code | Country |
|------|---------|------|---------|
| ID |  Indonesia | SG |  Singapore |
| US |  United States | JP |  Japan |
| KR |  South Korea | HK |  Hong Kong |
| DE |  Germany | FR |  France |
| GB |  United Kingdom | NL |  Netherlands |

**Total:** 51 negara dengan 316+ server

---

##  Aplikasi Client

### Android
- **V2RayNG** - Format: Raw Links, Base64
- **Clash for Android** - Format: Clash YAML
- **SagerNet** - Format: Sing-Box JSON

### Windows
- **v2rayN** - Format: Raw Links, Base64
- **Clash for Windows** - Format: Clash YAML

---

##  Troubleshooting

### Worker menunjukkan "Example Domain"
**Solusi:** Code worker belum di-deploy. Copy `_worker.js` ke dashboard dan deploy.

### API error 404
**Solusi:** Pastikan custom domain sudah di-setup di **Triggers  Custom Domains**.

### Telegram bot tidak respon
**Solusi:**
1. Cek TOKEN bot benar
2. Cek `WORKER_DOMAIN` sudah sesuai
3. Install dependencies: `pip install -r requirements.txt`

---

##  Limits & Quota

### Cloudflare Workers Free Plan
- **100,000 requests/day**
- **10ms CPU time per request**
- **Unlimited custom domains**

---

##  License

MIT License

---

**Made with  by Jhopan**

** Happy Tunneling!**
```
