#!/usr/bin/env python3
"""
Check Bot Configuration
Validate .env file and show current settings
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger("config_check")


def main():
    """Check configuration"""
    
    print("=" * 60)
    print("🔍 Jhopan VPN Bot - Configuration Check")
    print("=" * 60)
    print()
    
    # Check .env file
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    
    if not os.path.exists(env_file):
        print("❌ .env file not found!")
        print(f"   Expected location: {env_file}")
        print()
        print("💡 Run: cp .env.example .env")
        return False
    
    print(f"✅ .env file found: {env_file}")
    print()
    
    # Validate config
    try:
        Config.validate()
        print("✅ Configuration is valid!")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    print()
    print("📋 Current Configuration:")
    print("-" * 60)
    
    # Bot settings
    print("\n🤖 Bot Settings:")
    print(f"  Token: {'***' + Config.TELEGRAM_BOT_TOKEN[-10:] if Config.TELEGRAM_BOT_TOKEN else 'NOT SET'}")
    
    # Worker settings
    print("\n🌐 Worker Settings:")
    print(f"  Domain: {Config.WORKER_DOMAIN}")
    print(f"  API URL: {Config.get_api_url()}")
    
    if Config.WORKER_DOMAINS:
        print(f"  Load Balancing: {len(Config.WORKER_DOMAINS)} domains")
        for i, domain in enumerate(Config.WORKER_DOMAINS, 1):
            print(f"    {i}. {domain}")
    
    # Admin settings
    print("\n👑 Admin Settings:")
    print(f"  Admin-Only Mode: {'✅ Enabled' if Config.ADMIN_ONLY else '❌ Disabled'}")
    print(f"  Admin IDs: {Config.ADMIN_IDS if Config.ADMIN_IDS else 'None'}")
    
    # Default settings
    print("\n⚙️ Default Settings:")
    print(f"  Country: {Config.DEFAULT_COUNTRY}")
    print(f"  Protocol: {Config.DEFAULT_PROTOCOL}")
    print(f"  Port: {Config.DEFAULT_PORT}")
    print(f"  Format: {Config.DEFAULT_FORMAT}")
    print(f"  Limit: {Config.DEFAULT_LIMIT}")
    
    # API settings
    print("\n🔧 API Settings:")
    print(f"  Timeout: {Config.API_TIMEOUT}s")
    print(f"  Max Retries: {Config.MAX_RETRIES}")
    print(f"  Cache Duration: {Config.CACHE_DURATION}s")
    
    # Logging
    print("\n📝 Logging:")
    print(f"  Log Level: {Config.LOG_LEVEL}")
    
    print()
    print("=" * 60)
    print("✅ Configuration check complete!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
