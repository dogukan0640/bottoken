import csv
import os
from datetime import datetime

CSV_FILE = "predictions.csv"

FIELDNAMES = [
    "datetime", "symbol", "pattern",
    "ob", "fvg", "eqh", "ema_trend",
    "volume_spike", "atr_value",
    "funding_rate", "open_interest", 
    "prediction", "actual"
]

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

def log_prediction(
    symbol, pattern, ob, fvg, eqh, ema_trend,
    volume_spike, atr_value, funding_rate, open_interest,
    prediction, actual=None
):
    init_csv()
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow({
            "datetime": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "pattern": pattern,
            "ob": ob,
            "fvg": fvg,
            "eqh": eqh,
            "ema_trend": ema_trend,
            "volume_spike": volume_spike,
            "atr_value": atr_value,
            "funding_rate": funding_rate,
            "open_interest": open_interest,
            "prediction": prediction,
            "actual": actual
        })
