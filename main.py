
# --- TEST main.py FOR TELEGRAM BOT ON RENDER ---
import os
import signal
import sys
import requests
from telebot import TeleBot

# ✅ Load token from environment
TOKEN = os.getenv("Telegram_token")
if not TOKEN:
    raise RuntimeError("Telegram_token environment variable is missing!")

print("Your bot is now running ✅")

bot = TeleBot(TOKEN)

# ✅ Graceful shutdown handler
def shutdown_handler(signum, frame):
    print("Received shutdown signal. Cleaning up...")
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
        print("Webhook deleted successfully.")
    except Exception as e:
        print(f"Error deleting webhook: {e}")
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

# ✅ Clear webhook before polling
try:
    requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
    print("Webhook cleared before polling.")
except Exception as e:
    print(f"Error clearing webhook: {e}")

# ✅ Simple command handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Your bot is now running ✅")

# ✅ Start polling
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Polling error: {e}. Restarting in 5s...")
        import time
        time.sleep(5)
