#!/bin/bash

# Jhopan VPN Bot - Installation Script
# For Linux/macOS

echo "🚀 Installing Jhopan VPN Bot..."
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✓ Virtual environment created"
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 Next steps:"
echo "1. Copy .env.example to .env"
echo "   cp .env.example .env"
echo ""
echo "2. Edit .env and add your bot token"
echo "   nano .env"
echo ""
echo "3. Run the bot:"
echo "   source venv/bin/activate"
echo "   python bot.py"
echo ""
echo "🎉 Happy tunneling!"
