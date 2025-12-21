"""
Configuration module
Load and validate environment variables
"""

import os
from dotenv import load_dotenv
from typing import List

# Load .env file
load_dotenv()


class Config:
    """Bot configuration from environment variables"""
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # Cloudflare Worker
    WORKER_DOMAIN: str = os.getenv("WORKER_DOMAIN", "jhopan.my.id")
    WORKER_DOMAINS: List[str] = [
        domain.strip() 
        for domain in os.getenv("WORKER_DOMAINS", "").split(",") 
        if domain.strip()
    ]
    
    # Admin settings
    ADMIN_IDS: List[int] = [
        int(id.strip()) 
        for id in os.getenv("ADMIN_IDS", "").split(",") 
        if id.strip().isdigit()
    ]
    ADMIN_ONLY: bool = os.getenv("ADMIN_ONLY", "false").lower() == "true"
    
    # Default settings
    DEFAULT_COUNTRY: str = os.getenv("DEFAULT_COUNTRY", "ID")
    DEFAULT_PROTOCOL: str = os.getenv("DEFAULT_PROTOCOL", "vless")
    DEFAULT_PORT: str = os.getenv("DEFAULT_PORT", "443")
    DEFAULT_FORMAT: str = os.getenv("DEFAULT_FORMAT", "raw")
    DEFAULT_LIMIT: int = int(os.getenv("DEFAULT_LIMIT", "10"))
    
    # API settings
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    CACHE_DURATION: int = int(os.getenv("CACHE_DURATION", "300"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def get_api_url(cls) -> str:
        """Get API base URL"""
        domain = cls.WORKER_DOMAINS[0] if cls.WORKER_DOMAINS else cls.WORKER_DOMAIN
        return f"https://{domain}/api/v1/sub"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required in .env file")
        
        if cls.ADMIN_ONLY and not cls.ADMIN_IDS:
            raise ValueError("ADMIN_IDS required when ADMIN_ONLY is true")
        
        return True


# Validate on import
Config.validate()
