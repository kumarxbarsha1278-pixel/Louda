#!/bin/bash

echo "🚀 ARK POWER SYSTEM STARTING..."
echo "📦 Installing Python libraries..."
pip install flask telebot requests psutil --quiet
echo "⚙️ Compiling ARK.c binary..."
gcc ARK.c -o ARK -lpthread -O3
chmod +x ARK
echo "🧹 Cleaning old sessions..."
pkill -f api.py
pkill -f ARK.py
echo "🌐 Starting Flask API on port 8080..."
nohup python3 api.py > api_logs.txt 2>&1 &
sleep 2
echo "🤖 Starting Telegram Bot..."
nohup python3 ARK.py > bot_logs.txt 2>&1 &
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SYSTEM IS NOW LIVE!"
echo "📡 API Status: Running"
echo "🤖 Bot Status: Running"
echo "📝 Logs saved in: api_logs.txt and bot_logs.txt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
