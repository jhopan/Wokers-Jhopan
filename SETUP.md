# 🚀 Setup Guide - Jhopan VPN

Panduan lengkap setup Jhopan VPN dari awal sampai jalan!

---

## 📋 Yang Dibutuhkan

1. **Akun Cloudflare** (gratis) → [cloudflare.com](https://dash.cloudflare.com/sign-up)
2. **Domain gratis** (pilih salah satu):
   - Freenom (.tk, .ml, .ga, .cf, .gq) - **TUTUP PERMANENT**
   - [eu.org](https://nic.eu.org) - Gratis, approval 1-2 minggu
   - [freedns.afraid.org](https://freedns.afraid.org) - Instant
   - [duckdns.org](https://www.duckdns.org) - Instant, subdomain
   - [no-ip.com](https://www.noip.com) - Free dynamic DNS
3. **Akun Telegram** → Untuk bot
4. **PC/VPS** → Untuk jalankan bot (PC Windows/Linux atau VPS)

---

## 🌐 STEP 1: Siapkan Domain Gratis

### Option A: DuckDNS (Paling Mudah - Instant)

1. **Buka** [duckdns.org](https://www.duckdns.org)
2. **Login** dengan Google/GitHub
3. **Buat subdomain**:
   ```
   Subdomain: jhopan
   Hasil: jhopan.duckdns.org
   ```
4. **Copy token** untuk nanti

### Option B: eu.org (Professional - Approval 1-2 minggu)

1. **Buka** [nic.eu.org](https://nic.eu.org/arf/en/contact/create/)
2. **Register** akun baru
3. **Login** dan pilih "Register a domain"
4. **Isi form**:
   ```
   Domain name: jhopan
   Hasil: jhopan.eu.org
   ```
5. **Nameservers** → Isi dengan Cloudflare NS (step 2)
6. **Submit** dan tunggu email approval (1-2 minggu)

### Option C: FreeDNS (Instant - Banyak Pilihan)

1. **Buka** [freedns.afraid.org](https://freedns.afraid.org)
2. **Register** akun gratis
3. **Subdomain** → Add subdomain:
   ```
   Subdomain: jhopan
   Domain: pilih dari list (contoh: mooo.com)
   Hasil: jhopan.mooo.com
   ```
4. **Destination** → Isi IP Cloudflare nanti (step 2)

### Option D: No-IP (Dynamic DNS)

1. **Buka** [noip.com](https://www.noip.com/sign-up)
2. **Register** akun free
3. **Create hostname**:
   ```
   Hostname: jhopan
   Domain: pilih dari list
   Hasil: jhopan.ddns.net
   ```

**💡 Rekomendasi:** DuckDNS (instant) atau eu.org (professional)

---

## ☁️ STEP 2: Setup Cloudflare Workers

### 2.1 Buat Akun Cloudflare

1. **Daftar** di [Cloudflare Dashboard](https://dash.cloudflare.com/sign-up)
2. **Verifikasi** email
3. **Login** ke dashboard

### 2.2 Deploy Worker

Ada 2 cara:

#### Cara A: Via Wrangler CLI (Recommended)

```bash
# Install Node.js dulu (nodejs.org)

# Install Wrangler
npm install -g wrangler

# Login ke Cloudflare
wrangler login

# Deploy worker
wrangler deploy
```

**Hasil:**
```
Deployed jhopan to jhopan.workers.dev
```

#### Cara B: Via Dashboard (Manual)

1. **Buka** [Cloudflare Workers Dashboard](https://dash.cloudflare.com/?to=/:account/workers)
2. **Create Application** → Create Worker
3. **Copy code** dari `_worker.js`
4. **Paste** ke editor
5. **Deploy**

**Nama worker:** `jhopan`  
**URL:** `https://jhopan.workers.dev`

### 2.3 Setup Custom Domain (Opsional tapi Recommended)

Jika pakai domain sendiri (eu.org, mooo.com, dll):

1. **Add domain ke Cloudflare**:
   - Dashboard → Add site
   - Masukkan domain: `jhopan.eu.org`
   - Plan: Free
   - Cloudflare akan kasih nameservers

2. **Update nameservers**:
   - Copy NS dari Cloudflare:
     ```
     cary.ns.cloudflare.com
     shea.ns.cloudflare.com
     ```
   - Update di registrar domain (eu.org/freedns/dll)

3. **Tunggu DNS propagation** (15 menit - 48 jam)

4. **Add custom domain ke Worker**:
   - Workers → jhopan → Settings → Triggers
   - Add Custom Domain
   - Masukkan: `vpn.jhopan.eu.org` atau `jhopan.mooo.com`
   - Save

**Hasil:** Worker bisa diakses via custom domain!

---

## 🌍 STEP 3: Konfigurasi Domain di Code

### 3.1 Update SUB_PAGE_URL

**Fungsi:** Halaman web untuk ambil config manual

Buka `_worker.js` line 18:

```javascript
// Jika pakai Workers domain:
const SUB_PAGE_URL = "https://jhopan.workers.dev";

// Jika pakai custom domain:
const SUB_PAGE_URL = "https://jhopan.mooo.com";
// atau
const SUB_PAGE_URL = "https://vpn.jhopan.eu.org";
```

**Penjelasan:**
- Ini adalah URL halaman web yang akan dibuka user untuk copy config
- Ketika user akses `https://jhopan.workers.dev/sub` → redirect ke SUB_PAGE_URL
- Bisa pakai GitHub Pages atau domain custom

### 3.2 Setup GitHub Pages (Untuk SUB_PAGE_URL)

1. **Buat file `index.html`** di repo:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Jhopan VPN Config</title>
</head>
<body>
    <h1>🚀 Jhopan VPN</h1>
    <p>Get your VPN configuration via Telegram Bot!</p>
    <a href="https://t.me/YOUR_BOT_USERNAME">@YourBotUsername</a>
</body>
</html>
```

2. **Enable GitHub Pages**:
   - Repo Settings → Pages
   - Source: Deploy from main branch
   - Folder: / (root)
   - Save

3. **URL akan jadi:**
```
https://jhopan.github.io/Wokers-Jhopan
```

4. **Update _worker.js**:
```javascript
const SUB_PAGE_URL = "https://jhopan.github.io/Wokers-Jhopan";
```

5. **Deploy ulang worker**:
```bash
wrangler deploy
```

### 3.3 Verifikasi Proxy Lists

File sudah tersedia:
- ✅ `kvProxyList.json` - 51 negara, 316+ proxy
- ✅ `proxyList.txt` - Backup list

URLs sudah benar:
```javascript
const KV_PRX_URL = "https://raw.githubusercontent.com/jhopan/Wokers-Jhopan/refs/heads/main/kvProxyList.json";
const PRX_BANK_URL = "https://raw.githubusercontent.com/jhopan/Wokers-Jhopan/refs/heads/main/proxyList.txt";
```

**✅ Sudah auto dari GitHub repo!**

---

## 🤖 STEP 4: Setup Telegram Bot

### 4.1 Buat Bot di Telegram

1. **Buka Telegram** dan cari `@BotFather`
2. **Ketik** `/newbot`
3. **Nama bot**: `Jhopan VPN Bot`
4. **Username**: `jhopan_vpn_bot` (harus unique dan akhiran `_bot`)
5. **Copy token**: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz...`

### 4.2 Install Dependencies (PC/VPS)

**Windows:**
```bash
cd telegram-bot
pip install -r requirements.txt
```

**Linux/VPS:**
```bash
cd telegram-bot
pip3 install -r requirements.txt
```

### 4.3 Konfigurasi Bot

**Cara A: Via Setup Script**
```bash
python setup.py
```

Isi:
```
1. Telegram Bot Token: 1234567890:ABC...
2. Worker Domain: jhopan.workers.dev
   (atau custom: jhopan.mooo.com)
```

**Cara B: Manual Edit**

Buat file `.env`:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHI...
WORKER_DOMAIN=jhopan.workers.dev
```

Atau edit langsung `telegram-bot.py` line 18:
```python
TELEGRAM_BOT_TOKEN = "YOUR_TOKEN_HERE"
WORKER_DOMAIN = "jhopan.workers.dev"  # atau custom domain
```

### 4.4 Test Worker API

```bash
python test_worker.py jhopan.workers.dev
```

Output yang diharapkan:
```
✅ Worker Alive
✅ API Endpoint
✅ Country List
✅ Config Generation
```

### 4.5 Jalankan Bot

```bash
python telegram-bot.py
```

Output:
```
Bot started successfully!
Bot username: @jhopan_vpn_bot
Press Ctrl+C to stop
```

---

## ✅ STEP 5: Test End-to-End

### 5.1 Test di Telegram

1. **Buka bot** di Telegram: `@jhopan_vpn_bot`
2. **Ketik** `/start`
3. **Lihat menu**:
   ```
   🚀 Ambil Config VPN
   ⚙️ Pengaturan
   📊 Status Server
   ❓ Bantuan
   ```
4. **Tap** 🚀 Ambil Config VPN
5. **Pilih negara**: 🇮🇩 Indonesia
6. **Pilih protokol**: VLESS
7. **Copy config** yang muncul

### 5.2 Test Config di V2Ray/Clash

**V2RayN (Windows):**
1. Copy config
2. Paste di V2RayN → Add server from clipboard
3. Connect

**Clash (Android/iOS):**
1. Copy config URL
2. Import ke Clash
3. Connect

---

## 🔧 Konfigurasi Lanjutan

### Custom Domain di Worker

**Jika ingin pakai domain sendiri penuh:**

1. **Domain** → DNS Settings
2. **Add A Record**:
   ```
   Type: A
   Name: vpn (atau @)
   Content: 192.0.2.1 (dummy, akan di-proxy Cloudflare)
   Proxy: ON (orange cloud)
   ```

3. **Worker Routes**:
   - Workers → jhopan → Triggers
   - Add route: `vpn.jhopan.eu.org/*`
   - Select worker: jhopan

4. **Update bot**:
   ```python
   WORKER_DOMAIN = "vpn.jhopan.eu.org"
   ```

### Multiple Workers (Load Balance)

Deploy ke beberapa subdomain:

```bash
# Worker 1
wrangler deploy --name jhopan1
# Hasil: jhopan1.workers.dev

# Worker 2
wrangler deploy --name jhopan2
# Hasil: jhopan2.workers.dev

# Worker 3
wrangler deploy --name jhopan3
# Hasil: jhopan3.workers.dev
```

Update bot untuk random select:
```python
import random

workers = [
    "jhopan1.workers.dev",
    "jhopan2.workers.dev",
    "jhopan3.workers.dev"
]

WORKER_DOMAIN = random.choice(workers)
```

---

## 🔒 Security Best Practices

### 1. Environment Variables

Jangan hardcode token di code:
```python
# ❌ JANGAN:
TELEGRAM_BOT_TOKEN = "123456:ABC..."

# ✅ PAKAI:
import os
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
```

### 2. Rate Limiting

Tambahkan di worker untuk anti-spam:
```javascript
// Di _worker.js, tambahkan rate limit
const RATE_LIMIT = 100; // request per menit
```

### 3. HTTPS Only

Pastikan semua domain pakai HTTPS (auto dari Cloudflare)

### 4. Bot Commands Whitelist

Batasi user yang bisa pakai bot:
```python
ALLOWED_USERS = [123456789, 987654321]  # User IDs

if update.effective_user.id not in ALLOWED_USERS:
    return
```

---

## 🐛 Troubleshooting

### Bot tidak respon

**Cek:**
1. Token benar? Test: `curl https://api.telegram.org/bot<TOKEN>/getMe`
2. Bot jalan? Lihat terminal ada error?
3. Internet PC/VPS lancar?

**Fix:**
```bash
# Restart bot
Ctrl+C
python telegram-bot.py
```

### Worker error 500

**Cek:**
1. Deploy sukses? `wrangler deploy`
2. Code error? Lihat logs: `wrangler tail`
3. Proxy list error? Test URL:
   ```
   https://raw.githubusercontent.com/jhopan/Wokers-Jhopan/main/kvProxyList.json
   ```

**Fix:**
```bash
# Deploy ulang
wrangler deploy --force
```

### Config tidak work di V2Ray

**Cek:**
1. Format config benar?
2. Server proxy masih hidup? (Proxy bisa mati kapan saja)
3. Coba negara lain

**Fix:**
- Ganti server: Pilih negara lain di bot
- Update proxy list: Edit `kvProxyList.json`

### Domain tidak resolve

**Cek:**
```bash
# Test DNS
nslookup jhopan.mooo.com

# Test ping
ping jhopan.workers.dev
```

**Fix:**
- Tunggu DNS propagation (up to 48 jam)
- Clear DNS cache:
  ```bash
  # Windows
  ipconfig /flushdns
  
  # Linux
  sudo systemd-resolve --flush-caches
  ```

---

## 📊 Monitoring

### Worker Analytics

1. **Dashboard** → Workers → jhopan → Metrics
2. Lihat:
   - Request count
   - Success rate
   - Error rate
   - Bandwidth

### Bot Logs

```bash
# Jalankan dengan logging
python telegram-bot.py > bot.log 2>&1

# Lihat logs
tail -f bot.log
```

---

## 🚀 Production Deployment (VPS)

### Run Bot as Service (Linux)

1. **Buat systemd service**:
```bash
sudo nano /etc/systemd/system/jhopan-bot.service
```

2. **Isi**:
```ini
[Unit]
Description=Jhopan VPN Telegram Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/home/youruser/Wokers-Jhopan/telegram-bot
ExecStart=/usr/bin/python3 telegram-bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. **Enable & start**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable jhopan-bot
sudo systemctl start jhopan-bot
```

4. **Check status**:
```bash
sudo systemctl status jhopan-bot
```

### Auto-restart on Failure

Service sudah include `Restart=always`, jadi bot auto restart jika crash.

---

## 🎯 Ringkasan URL

| Komponen | URL | Fungsi |
|----------|-----|--------|
| **Worker** | `jhopan.workers.dev` | VPN tunneling endpoint |
| **Custom Domain** | `jhopan.mooo.com` | Alternative worker URL |
| **Sub Page** | `jhopan.github.io/Wokers-Jhopan` | Web interface |
| **API** | `jhopan.workers.dev/api/v1/sub` | Bot fetch config |
| **Proxy KV** | `github.com/.../kvProxyList.json` | Country proxy list |
| **Proxy Bank** | `github.com/.../proxyList.txt` | Full proxy list |
| **Telegram Bot** | `@jhopan_vpn_bot` | User interface |

---

## 📝 Checklist Setup

- [ ] Akun Cloudflare dibuat
- [ ] Domain gratis didapat (DuckDNS/eu.org/FreeDNS)
- [ ] Worker di-deploy: `wrangler deploy`
- [ ] Custom domain setup (opsional)
- [ ] SUB_PAGE_URL dikonfigurasi di `_worker.js`
- [ ] GitHub Pages enabled
- [ ] Bot Telegram dibuat via @BotFather
- [ ] Token bot dicopy
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Bot dikonfigurasi: `.env` atau `setup.py`
- [ ] Worker API ditest: `python test_worker.py`
- [ ] Bot dijalankan: `python telegram-bot.py`
- [ ] Test end-to-end via Telegram
- [ ] Config ditest di V2Ray/Clash
- [ ] Production deployment (VPS opsional)

---

## 🎉 Selesai!

Bot dan Worker sudah jalan! User bisa:

1. Buka bot: `@jhopan_vpn_bot`
2. Tap menu: 🚀 Ambil Config VPN
3. Pilih negara: 51 negara tersedia
4. Copy config
5. Pakai di V2Ray/Clash
6. Internet bebas! 🌍

**Butuh bantuan?** Cek troubleshooting di atas atau buka issue di GitHub!

---

**Made with ❤️ by Jhopan**  
**Original:** [FoolVPN-ID/Nautica](https://github.com/FoolVPN-ID/Nautica)
