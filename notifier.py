import requests
import os

def send_telegram_summary(jobs):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id or not jobs:
        return

    # Build a nice header
    message = "🇰🇪 *New Job Opportunities Found*\n"
    message += "--------------------------\n\n"
    
    for i, job in enumerate(jobs, 1):
        # Format: 1. Job Title
        #         🏢 Company Name
        message += f"{i}. *{job['title']}*\n🏢 {job['company']}\n🔗 [View Job & Apply]({job['url']})\n\n"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    requests.post(url, data=payload)


def send_telegram_football_predictions(predictions):
    """Send today's football match predictions via Telegram."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id or not predictions:
        return

    message = "⚽ *Today's Football Match Predictions*\n"
    message += "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    for pred in predictions:
        message += f"🏆 {pred['competition']}\n"
        message += f"🆚 *{pred['home_team']}* vs *{pred['away_team']}*\n"
        message += f"⏰ Kick-off: {pred['kickoff']}\n"
        message += f"📊 Prediction: *{pred['prediction']}* ({pred['confidence']}% confidence)\n"
        message += f"💡 _{pred['reasoning']}_\n\n"

    message += "━━━━━━━━━━━━━━━━━━━━━━━━\n"
    message += "_Predictions are based on league standings and home advantage. Bet responsibly._"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    requests.post(url, data=payload)
