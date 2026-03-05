import requests
import os

def send_telegram_summary(jobs):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not jobs:
        return

    message = "🇰🇪 *New Jobs Found (Hourly Update)*\n\n"
    for i, job in enumerate(jobs, 1):
        message += f"{i}. [{job['title']}]({job['url']})\n🏢 {job['company']}\n\n"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    requests.post(url, data=payload)