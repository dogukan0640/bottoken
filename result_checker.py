import pandas as pd
import requests
from datetime import datetime, timedelta

CSV_FILE = "predictions.csv"

def get_future_price(symbol, from_time, hours_forward=6):
    """Belirtilen saat sonrası fiyatı getirir"""
    end_time = int((from_time + timedelta(hours=hours_forward)).timestamp() * 1000)
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&endTime={end_time}&limit=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0][4])  # close fiyatı
    return None

def update_predictions():
    df = pd.read_csv(CSV_FILE)
    updated = False

    for i, row in df.iterrows():
        if pd.isna(row["actual"]):
            symbol = row["symbol"]
            pred = int(row["prediction"])
            try:
                time_obj = datetime.fromisoformat(row["datetime"])
            except:
                continue

            past_price = float(row.get("atr_value", 1.0))  # geçici olarak 'atr_value' yerinde kullanılacak
            future_price = get_future_price(symbol, time_obj)

            if future_price:
                # Basit kontrol: Yükselir dediyse gerçekten artmış mı
                if (pred == 1 and future_price > past_price) or (pred == 0 and future_price < past_price):
                    df.at[i, "actual"] = 1
                else:
                    df.at[i, "actual"] = 0
                updated = True

    if updated:
        df.to_csv(CSV_FILE, index=False)
        print("Tahmin sonuçları güncellendi.")
    else:
        print("Güncellenecek tahmin bulunamadı.")

if __name__ == "__main__":
    update_predictions()
