import requests
import os

def send_telegram_summary(jobs):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("❌ ERROR: Secrets are missing in GitHub Settings!")
        return

    message = "🇰🇪 *Bot Test Message*\n\nIf you see this, the connection is live!"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, data=payload)
        # THIS LINE IS THE KEY: It will tell us why it's failing
        print(f"📡 Telegram Response: Status {response.status_code}, Content: {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
