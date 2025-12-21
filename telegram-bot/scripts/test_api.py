#!/usr/bin/env python3
"""
Test API Connection
Check if Cloudflare Worker API is accessible
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.config import Config
from app.utils.api import fetch_config
from app.utils.logger import setup_logger

logger = setup_logger("test_api")


def main():
    """Test API connection"""
    
    print("=" * 60)
    print("🔍 Jhopan VPN Bot - API Connection Test")
    print("=" * 60)
    print()
    
    api_url = Config.get_api_url()
    print(f"🌐 Testing API: {api_url}")
    print()
    
    # Test parameters
    test_cases = [
        {
            "name": "Indonesia VLESS Raw",
            "params": {
                "cc": "ID",
                "vpn": "vless",
                "port": "443",
                "limit": "1",
                "format": "raw"
            }
        },
        {
            "name": "Singapore Trojan Clash",
            "params": {
                "cc": "SG",
                "vpn": "trojan",
                "port": "443",
                "limit": "1",
                "format": "clash"
            }
        },
        {
            "name": "US All Protocols",
            "params": {
                "cc": "US",
                "vpn": "vless,trojan,ss",
                "port": "443,80",
                "limit": "2",
                "format": "raw"
            }
        }
    ]
    
    success_count = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] Testing: {test['name']}")
        print(f"    Params: {test['params']}")
        
        try:
            config = fetch_config(test['params'])
            
            if config:
                print(f"    ✅ Success! ({len(config)} bytes)")
                success_count += 1
                
                # Show first 100 chars
                preview = config[:100].replace('\n', ' ')
                print(f"    Preview: {preview}...")
            else:
                print(f"    ❌ Failed: No data returned")
                
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
        
        print()
    
    # Summary
    print("=" * 60)
    print(f"📊 Test Results: {success_count}/{len(test_cases)} passed")
    
    if success_count == len(test_cases):
        print("✅ All tests passed! API is working correctly.")
    elif success_count > 0:
        print("⚠️  Some tests failed. Check API configuration.")
    else:
        print("❌ All tests failed! API is not accessible.")
    
    print("=" * 60)
    
    return success_count == len(test_cases)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
