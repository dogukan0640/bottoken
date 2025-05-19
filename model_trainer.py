import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

CSV_FILE = "predictions.csv"
MODEL_FILE = "model.pkl"

FEATURES = [
    "ob", "fvg", "eqh", "ema_trend",
    "volume_spike", "atr_value",
    "funding_rate", "open_interest"
]

TARGET = "actual"

def train_model():
    if not os.path.exists(CSV_FILE):
        print("Veri dosyası bulunamadı.")
        return None

    df = pd.read_csv(CSV_FILE)
    df = df.dropna(subset=[TARGET])  # sadece etiketli verilerle eğitim yapılır

    if df.empty:
        print("Eğitim için yeterli veri yok.")
        return None

    X = df[FEATURES]
    y = df[TARGET].astype(int)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, MODEL_FILE)
    joblib.dump(model, MODEL_FILE)
print(f"✅ Model kaydedildi: {MODEL_FILE}")

import os
print("📁 Klasördeki dosyalar:", os.listdir())


if __name__ == "__main__":
    train_model()
