import requests
import pandas as pd
import time
import joblib
import os
from pattern_detector import detect_patterns
from telegram_notifier import send_telegram_message
from data_logger import log_prediction
from model_trainer import train_model

def get_usdt_symbols():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    symbols = []
    if response.status_code == 200:
        data = response.json()
        for s in data['symbols']:
            if s['quoteAsset'] == 'USDT' and s['status'] == 'TRADING':
                symbols.append(s['symbol'])
    return symbols

def get_binance_ohlcv(symbol="BTCUSDT", interval="1h", limit=200):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data, columns=[
                'time', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
            ])
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            df = df[['time', 'open', 'high', 'low', 'close', 'volume']]
            df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
            return df
    except Exception as e:
        print(f"{symbol} hata:", e)
    return None

def mock_features(df):
    # Geçici olarak rasgele değerler üretilir (gerçek sistemde analizle doldurulacak)
    return {
        "ob": 1,
        "fvg": 0,
        "eqh": 1,
        "ema_trend": 1,
        "volume_spike": 0,
        "atr_value": 1.2,
        "funding_rate": -0.01,
        "open_interest": 1000000
    }

def calculate_confidence_score(features):
    score = 0
    score += 10 if features['ob'] else 0
    score += 10 if features['fvg'] else 0
    score += 5 if features['eqh'] else 0
    score += 10 if features['ema_trend'] else 0
    score += 5 if features['volume_spike'] else 0
    score += 5 if features['funding_rate'] < 0 else 0
    score += 5 if features['open_interest'] > 1000000 else 0
    return min(score, 100)


    model_file = "model.pkl"
    if not os.path.exists(model_file):
        print("Model bulunamadı, yeniden eğitiliyor...")
        model = train_model()
    else:
        model = joblib.load(model_file)
    df = pd.DataFrame([features])
    pred = model.predict(df)[0]
    return pred

if __name__ == "__main__":
    symbols = get_usdt_symbols()
    print(f"Toplam {len(symbols)} USDT paritesi bulundu.")

    for i, symbol in enumerate(symbols[:5]):
        print(f"[{i+1}] {symbol} verisi alınıyor...")
        df = get_binance_ohlcv(symbol)
        if df is not None:
            patterns = detect_patterns(df)
            if patterns:
                print(f"{symbol} için bulunan formasyonlar:")
                for time_point, pattern in patterns:
                    features = mock_features(df)  # geçici mock analiz
                    prediction = predict_with_model(features)
                    score = calculate_confidence_score(features)
                    if score < 60:
                        continue
                    log_prediction(symbol, pattern, **features, prediction=prediction)
                    
                    entry_price = float(df["close"].iloc[-1])
                    sl_price = entry_price * 0.99 if prediction == 1 else entry_price * 1.01
                    tp_price = entry_price * 1.02 if prediction == 1 else entry_price * 0.98

                    message = f"📈 <b>{symbol}</b> - <b>{pattern}</b>\n"
                    message += f"🤖 AI Tahmini: {'YÜKSELİR' if prediction == 1 else 'DÜŞER'}\n"
                    message += f"🎯 Giriş: {entry_price:.4f}\n"
                    message += f"✅ TP: {tp_price:.4f}\n"
                    message += f"🛑 SL: {sl_price:.4f}\n"
                    message += f"📊 Güven Skoru: {score}/100"

                    send_telegram_message(message)

                    print(f" - {time_point} ➜ {pattern} ➜ Tahmin: {'YÜKSELİR' if prediction == 1 else 'DÜŞER'}")
            else:
                print(f"{symbol} için formasyon bulunamadı.")
        else:
            print(f"{symbol} verisi alınamadı.")
        time.sleep(0.5)
