#!/usr/bin/env python3
"""
Add Admin User
Add user ID to admin list in .env file
"""

import sys
import os


def main():
    """Add admin user to .env"""
    
    print("=" * 60)
    print("👑 Jhopan VPN Bot - Add Admin User")
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
    
    # Get user ID
    print("Enter Telegram User ID to add as admin:")
    print("(You can get this by using /myid command in bot)")
    print()
    
    user_id = input("User ID: ").strip()
    
    if not user_id.isdigit():
        print("❌ Invalid User ID! Must be a number.")
        return False
    
    # Read .env file
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Find ADMIN_IDS line
    admin_line_idx = None
    current_admins = []
    
    for i, line in enumerate(lines):
        if line.startswith("ADMIN_IDS="):
            admin_line_idx = i
            # Parse current admins
            admin_str = line.split("=", 1)[1].strip()
            if admin_str:
                current_admins = [id.strip() for id in admin_str.split(",") if id.strip()]
            break
    
    if admin_line_idx is None:
        print("❌ ADMIN_IDS not found in .env file!")
        return False
    
    # Check if already admin
    if user_id in current_admins:
        print(f"⚠️  User {user_id} is already an admin!")
        return True
    
    # Add new admin
    current_admins.append(user_id)
    new_admin_line = f"ADMIN_IDS={','.join(current_admins)}\n"
    
    lines[admin_line_idx] = new_admin_line
    
    # Write back to .env
    with open(env_file, 'w') as f:
        f.writelines(lines)
    
    print()
    print("✅ Admin added successfully!")
    print()
    print(f"📋 Current admins: {', '.join(current_admins)}")
    print()
    print("💡 Restart the bot to apply changes")
    print()
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
