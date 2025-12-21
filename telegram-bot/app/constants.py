"""
Constants - Countries, Protocols, Formats, Ports
"""

# Country codes with emoji flags
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

# VPN Protocols
PROTOCOLS = {
    "⚡ VLESS": "vless",
    "🔒 Trojan": "trojan",
    "🥷 Shadowsocks": "ss",
    "🌐 All Protocols": "vless,trojan,ss"
}

# Output formats
FORMATS = {
    "📝 Raw/Text": "raw",
    "⚔️ Clash": "clash",
    "📦 Sing-Box (SFA)": "sfa",
    "🎯 v2rayN": "v2ray"
}

# Ports
PORTS = {
    "🔐 443 (TLS)": "443",
    "🌐 80 (Non-TLS)": "80",
    "🔄 Both": "443,80"
}

# Protocol descriptions
PROTOCOL_INFO = {
    "vless": {
        "name": "VLESS",
        "emoji": "⚡",
        "description": "Modern, fast, low latency",
        "recommended": True
    },
    "trojan": {
        "name": "Trojan",
        "emoji": "🔒",
        "description": "Stealthy, bypass censorship",
        "recommended": True
    },
    "ss": {
        "name": "Shadowsocks",
        "emoji": "🥷",
        "description": "Popular, widely supported",
        "recommended": False
    }
}

# Format descriptions
FORMAT_INFO = {
    "raw": {
        "name": "Raw/Text",
        "emoji": "📝",
        "description": "Universal link format",
        "clients": ["All clients"]
    },
    "clash": {
        "name": "Clash",
        "emoji": "⚔️",
        "description": "Clash YAML config",
        "clients": ["Clash for Windows", "Clash for Android"]
    },
    "sfa": {
        "name": "Sing-Box",
        "emoji": "📦",
        "description": "Sing-Box JSON config",
        "clients": ["SagerNet", "SFA"]
    },
    "v2ray": {
        "name": "v2rayN",
        "emoji": "🎯",
        "description": "Base64 subscription",
        "clients": ["v2rayN", "V2RayNG"]
    }
}
