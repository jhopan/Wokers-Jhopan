# 📁 Project Structure - Jhopan VPN Bot v2.0

Struktur modular dengan clean architecture.

## 🗂️ Directory Structure

```
telegram-bot/
├── app/                        # Main application package
│   ├── __init__.py            # Package initialization
│   ├── config.py              # Configuration & environment variables
│   ├── constants.py           # Constants (countries, protocols, formats)
│   ├── handlers/              # Request handlers
│   │   ├── __init__.py       
│   │   ├── commands.py        # Command handlers (/start, /help, etc)
│   │   └── callbacks.py       # Callback query handlers (buttons)
│   └── utils/                 # Utility modules
│       ├── __init__.py       
│       ├── decorators.py      # @admin_only, @check_access
│       ├── logger.py          # Logging configuration
│       └── api.py             # Cloudflare Workers API client
│
├── scripts/                    # Utility scripts
│   ├── check_config.py        # Validate .env configuration
│   ├── test_api.py            # Test API connection
│   ├── add_admin.py           # Add admin user to .env
│   └── toggle_admin_mode.py   # Enable/disable admin-only mode
│
├── main.py                     # Main entry point (run this)
├── bot.py                      # New modular bot (same as main.py)
├── telegram-bot.py             # Old monolithic bot (deprecated)
│
├── .env                        # Environment variables (create from .env.example)
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
│
├── install.sh                  # Auto installer (Linux/macOS)
├── install.bat                 # Auto installer (Windows)
├── run.sh                      # Run bot (Linux/macOS)
├── run.bat                     # Run bot (Windows)
│
├── QUICKSTART.md              # Quick start guide
├── STRUCTURE.md               # This file
└── README.md                   # Main documentation
```

---

## 📦 Module Descriptions

### `app/config.py`
- Load environment variables from `.env`
- Validate configuration
- Provide `Config` class with all settings
- **Key Classes:** `Config`

### `app/constants.py`
- Define constants (countries, protocols, formats, ports)
- Protocol & format descriptions
- **Key Variables:** `COUNTRIES`, `PROTOCOLS`, `FORMATS`, `PORTS`

### `app/handlers/commands.py`
- Handle bot commands
- **Commands:** `/start`, `/config`, `/help`, `/status`, `/myid`
- **Key Class:** `CommandHandlers`

### `app/handlers/callbacks.py`
- Handle inline keyboard button clicks
- Menu navigation & config generation
- **Key Class:** `CallbackHandlers`

### `app/utils/decorators.py`
- Access control decorators
- **Decorators:** `@admin_only`, `@check_access`

### `app/utils/api.py`
- API client for Cloudflare Workers
- **Functions:** `fetch_config(params)`

### `app/utils/logger.py`
- Logging configuration
- **Functions:** `setup_logger(name)`

---

## 🚀 How to Run

### Quick Start:

```bash
# Install
./install.sh

# Configure
cp .env.example .env
nano .env  # Add bot token

# Run
./run.sh
```

### Manual:

```bash
# Activate venv
source venv/bin/activate

# Run main bot
python main.py

# OR run modular bot
python bot.py
```

---

## 🔧 Utility Scripts

### Check Configuration:
```bash
python scripts/check_config.py
```
Validates `.env` file and shows current settings.

### Test API:
```bash
python scripts/test_api.py
```
Tests Cloudflare Worker API connectivity.

### Add Admin:
```bash
python scripts/add_admin.py
```
Add user ID to admin list in `.env`.

### Toggle Admin Mode:
```bash
python scripts/toggle_admin_mode.py
```
Enable/disable admin-only mode.

---

## 📝 Code Flow

### 1. User sends `/start`
```
main.py
  → CommandHandlers.cmd_start()
    → Show main menu with InlineKeyboardMarkup
```

### 2. User clicks "🚀 Ambil Config VPN"
```
Callback: "menu_config"
  → CallbackHandlers.handle_menu()
    → CallbackHandlers.show_country_menu()
      → User selects country
        → CallbackHandlers.handle_country()
          → CallbackHandlers.show_protocol_menu()
            → ... (format → port)
              → CallbackHandlers.generate_config()
                → utils/api.fetch_config()
                  → Send config to user
```

### 3. Access Control
```
@check_access decorator
  → Check if ADMIN_ONLY enabled
    → If yes, check if user in ADMIN_IDS
      → Allow/deny access
```

---

## 🎯 Benefits of This Structure

### ✅ Modularity
- Setiap modul punya tanggung jawab jelas
- Easy to maintain & extend

### ✅ Reusability
- Utils & decorators bisa dipakai di mana aja
- Clean code, no duplication

### ✅ Testability
- Setiap modul bisa di-test terpisah
- Scripts untuk testing & validation

### ✅ Scalability
- Gampang tambah handler/feature baru
- Struktur jelas, mudah navigasi

### ✅ Professional
- Industry-standard structure
- Easy untuk collaborate

---

## 🔄 Migration from Old Bot

**Old (telegram-bot.py):**
- Monolithic file (600+ lines)
- All code in one file
- Hard to maintain

**New (main.py + app/):**
- Modular structure
- Separated concerns
- Easy to extend

**To migrate:**
1. Use `main.py` instead of `telegram-bot.py`
2. `.env` file remains the same
3. All features work the same

---

## 📚 Documentation

- **QUICKSTART.md** - Quick installation guide
- **STRUCTURE.md** - This file (project structure)
- **README.md** - Main documentation
- **.env.example** - Environment template

---

## 🎉 Happy Coding!

**Made with ❤️ by Jhopan**
