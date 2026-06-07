#!/bin/bash

# Ensure required Python libraries are installed
echo "Checking dependencies..."
pip install -q python-telegram-bot httpx

# Check if config.json exists before running
if [ ! -f "config.json" ]; then
    echo "❌ Error: config.json file is missing!"
    echo "Please create a config.json file with your tokens before running this script."
    exit 1
fi

echo "🚀 Starting your Telegram Bot..."
python bot.py