#!/bin/bash

# Jhopan VPN Bot - Run Script
# Automatically activate venv and run bot

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./install.sh first"
    exit 1
fi

# Activate venv
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "✅ .env created! Please edit it and add your bot token:"
    echo "   nano .env"
    echo ""
    echo "Then run ./run.sh again"
    exit 1
fi

# Run bot
echo "🚀 Starting Jhopan VPN Bot..."
python bot.py
