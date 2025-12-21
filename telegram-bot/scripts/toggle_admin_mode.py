#!/usr/bin/env python3
"""
Enable/Disable Admin-Only Mode
Toggle ADMIN_ONLY setting in .env file
"""

import sys
import os


def main():
    """Toggle admin-only mode"""
    
    print("=" * 60)
    print("🔒 Jhopan VPN Bot - Admin-Only Mode Toggle")
    print("=" * 60)
    print()
    
    # Get .env file path
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    
    if not os.path.exists(env_file):
        print("❌ .env file not found!")
        print(f"   Expected: {env_file}")
        print()
        print("💡 Run: cp .env.example .env")
        return False
    
    # Read .env file
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Find ADMIN_ONLY line
    admin_only_idx = None
    current_value = "false"
    
    for i, line in enumerate(lines):
        if line.startswith("ADMIN_ONLY="):
            admin_only_idx = i
            current_value = line.split("=", 1)[1].strip().lower()
            break
    
    if admin_only_idx is None:
        print("❌ ADMIN_ONLY not found in .env file!")
        return False
    
    # Show current status
    is_enabled = current_value == "true"
    print(f"Current status: {'🔒 ENABLED' if is_enabled else '🌍 DISABLED'}")
    print()
    
    # Ask for action
    print("What do you want to do?")
    print("1. Enable admin-only mode (only admins can use bot)")
    print("2. Disable admin-only mode (everyone can use bot)")
    print("3. Cancel")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        new_value = "true"
        action = "enabled"
    elif choice == "2":
        new_value = "false"
        action = "disabled"
    elif choice == "3":
        print("Cancelled.")
        return True
    else:
        print("❌ Invalid choice!")
        return False
    
    # Update .env
    lines[admin_only_idx] = f"ADMIN_ONLY={new_value}\n"
    
    with open(env_file, 'w') as f:
        f.writelines(lines)
    
    print()
    print(f"✅ Admin-only mode {action}!")
    print()
    
    if new_value == "true":
        print("🔒 Bot is now in ADMIN-ONLY mode")
        print("   Only users in ADMIN_IDS can access the bot")
    else:
        print("🌍 Bot is now in PUBLIC mode")
        print("   Everyone can use the bot")
    
    print()
    print("💡 Restart the bot to apply changes")
    print()
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
