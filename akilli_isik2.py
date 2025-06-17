#Bu kodda ek olarak USB kamera için OpenCV kullanılarak satranç tahtası görüntülerinden elde edilen kamera kalibrasyonu ayrıca LDR ve mesafe sensörü için veri filtreleme bulunmakta.
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
from collections import deque

# --- Pin Ayarları ---
LDR_PIN = 5       # LDR için GPIO pini
TRIG = 23         # HC-SR04 TRIG pini
ECHO = 24         # HC-SR04 ECHO pini
LED_PIN = 17      # LED kontrol pini (röleye de bağlanabilir)

# --- GPIO Başlatma ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# --- Kamera Kalibrasyon Parametreleri ---
# Satranç tahtası kalibrasyonu ile elde edilen matris ve distorsiyon katsayıları
camera_matrix = np.array([[800.2, 0, 320.5],
                          [0, 800.1, 240.7],
                          [0, 0, 1]], dtype=np.float32)

dist_coeffs = np.array([0.05, -0.12, 0.001, 0.002, 0.0], dtype=np.float32)

# --- HOG Tabanlı İnsan Tespiti için Hazırlık ---
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Kamera başlatılır
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[HATA] Kamera açılamadı.")
    exit()

# --- Veri Filtreleme İçin Kuyruklar (Moving Average) ---
LDR_history = deque(maxlen=5)      # Son 5 ışık değeri
MESAFE_history = deque(maxlen=3)   # Son 3 mesafe değeri

# --- LDR Okuma Fonksiyonu (Ham) ---
def oku_isik(pin):
    sayac = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)  # Kondansatör boşaltma süresi
    GPIO.setup(pin, GPIO.IN)
    while GPIO.input(pin) == GPIO.LOW:
        sayac += 1
        if sayac > 10000:
            break
    return sayac

# --- LDR Okuma (Filtreli) ---
def oku_isik_filtreli(pin):
    raw = oku_isik(pin)
    LDR_history.append(raw)
    ortalama = sum(LDR_history) / len(LDR_history)
    return round(ortalama, 2)

# --- HC-SR04 Mesafe Ölçüm Fonksiyonu (Ham) ---
def oku_mesafe():
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    baslangic, bitis = 0, 0
    while GPIO.input(ECHO) == 0:
        baslangic = time.time()
    while GPIO.input(ECHO) == 1:
        bitis = time.time()

    sure = bitis - baslangic
    mesafe = round(sure * 17150, 2)  # cm
    return mesafe

# --- HC-SR04 Mesafe (Filtreli) ---
def oku_mesafe_filtreli():
    raw = oku_mesafe()
    MESAFE_history.append(raw)
    ortalama = sum(MESAFE_history) / len(MESAFE_history)
    return round(ortalama, 2)

# --- Ana Döngü ---
print("Sistem başlatıldı. Çıkmak için Ctrl+C ya da 'q'.")

son_gorulme_zamani = time.time()  # Oda en son ne zaman doluydu

try:
    while True:
        # 1. LDR ile ortam ışığı ölçülür
        isik = oku_isik_filtreli(LDR_PIN)
        print(f"[FOTOSEL] (Filtreli) Işık seviyesi: {isik}")

        if isik > 300:  # Karanlıksa sistem aktif
            print("[SİSTEM] Ortam karanlık, sistem aktif.")

            # 2. HC-SR04 ile mesafe ölçülür
            mesafe = oku_mesafe_filtreli()
            print(f"[HC-SR04] (Filtreli) Ölçülen mesafe: {mesafe} cm")

            # Mesafe 60 cm'den küçükse biri geldi demektir
            if mesafe < 60:
                print("[GİRİŞ] Biri algılandı! LED yakıldı.")
                GPIO.output(LED_PIN, GPIO.HIGH)
                son_gorulme_zamani = time.time()

            # 3. Kamera ile insan tespiti yapılır
            ret, frame = cap.read()
            if not ret:
                print("[KAMERA] Görüntü alınamadı.")
                continue

            # Görüntü bozulmaları düzeltilir
            frame = cv2.undistort(frame, camera_matrix, dist_coeffs)
            frame = cv2.resize(frame, (320, 240))  # Performans için küçüldü

            # HOG ile insan tespiti
            dikdortgenler, _ = hog.detectMultiScale(frame, winStride=(8, 8), padding=(8, 8), scale=1.05) #Dengeli ve stabil tespit için ideal değerler verildi

            if len(dikdortgenler) > 0:
                print(f"[KAMERA] {len(dikdortgenler)} kişi algılandı.")
                son_gorulme_zamani = time.time()
            else:
                print("[KAMERA] Kimse algılanmadı.")
                # 15 saniye kimse yoksa LED kapatılır
                if time.time() - son_gorulme_zamani > 15:
                    print("[ÇIKIŞ] Oda boş, LED kapatıldı.")
                    GPIO.output(LED_PIN, GPIO.LOW)

            # Tespit edilen kişileri yeşil dikdörtgenle çiz
            for (x, y, w, h) in dikdortgenler:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Görüntüyü ekranda göster
            cv2.imshow("Kalibrasyonlu Kamera Görüntüsü", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            # Ortam aydınlıksa sistem pasif
            print("[FOTOSEL] Ortam aydınlık, sistem pasif. LED kapalı.")
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(1)

except KeyboardInterrupt:
    print("\n[SONLANDIRMA] Program durduruldu.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()
