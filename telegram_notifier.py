import requests

TELEGRAM_TOKEN = "7744478523:AAEtRJar6uF7m0cxKfQh7r7TltXYxWwtmm0"
TELEGRAM_CHAT_ID = "1009868232"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print("Telegram hata:", response.text)
    except Exception as e:
        print("Telegram bağlantı hatası:", e)
