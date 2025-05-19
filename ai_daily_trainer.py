import time
from result_checker import update_predictions
from model_trainer import train_model

def run_daily_training(cycle_hours=0.01):
    print("🧠 Günlük AI eğitim döngüsü başladı...")
    while True:
        try:
            print("🔁 Yeni döngü: tahmin sonuçları kontrol ediliyor...")
            update_predictions()
            print("🛡️ Model yeniden eğitiliyor...")
            train_model()
            print("✅ Eğitim tamamlandı, model kaydedildi.")
        except Exception as e:
            print(f"❌ HATA: {e}")

        print(f"⏳ {cycle_hours} saat sonra tekrar çalışacak...\n")
        time.sleep(cycle_hours * 3600)


if __name__ == "__main__":
    run_daily_training()
