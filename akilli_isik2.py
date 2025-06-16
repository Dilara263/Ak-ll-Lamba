#USB kamera için OpenCV kullanılarak satranç tahtası (chessboard) görüntülerinden kamera kalibrasyonu yapmak amacıyla hazırlanmıştır.
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

# --- Pin Ayarları ---
LDR_PIN = 5
TRIG = 23
ECHO = 24
LED_PIN = 17

# --- GPIO Ayarları ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# --- KAMERA Kalibrasyon Parametreleri ---
# Bu değerleri sen kendi kalibrasyon çıktınla değiştirmelisin
camera_matrix = np.array([[800.2, 0, 320.5],
                          [0, 800.1, 240.7],
                          [0, 0, 1]], dtype=np.float32)

dist_coeffs = np.array([0.05, -0.12, 0.001, 0.002, 0.0], dtype=np.float32)

# --- Kamera Ayarları (HOG + SVM) ---
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[HATA] Kamera açılamadı.")
    exit()

# --- LDR Okuma Fonksiyonu ---
def oku_isik(pin):
    sayac = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(pin, GPIO.IN)
    while GPIO.input(pin) == GPIO.LOW:
        sayac += 1
        if sayac > 10000:
            break
    return sayac

# --- HC-SR04 Mesafe Fonksiyonu ---
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
    mesafe = round(sure * 17150, 2)
    return mesafe

# --- Ana Döngü ---
print("Sistem başlatıldı. Çıkmak için Ctrl+C ya da 'q'.")

son_gorulme_zamani = time.time()

try:
    while True:
        # 1. Ortam ışık kontrolü
        isik = oku_isik(LDR_PIN)
        print(f"[FOTOSEL] Işık seviyesi: {isik}")

        if isik > 200:
            print("[SİSTEM] Ortam karanlık, sistem aktif.")

            # 2. Mesafe kontrolü
            mesafe = oku_mesafe()
            print(f"[HC-SR04] Ölçülen mesafe: {mesafe} cm")

            if mesafe < 60:
                print("[GİRİŞ] Biri algılandı! LED yakıldı.")
                GPIO.output(LED_PIN, GPIO.HIGH)
                son_gorulme_zamani = time.time()

            # 3. Kamera ile insan tespiti
            ret, frame = cap.read()
            if not ret:
                print("[KAMERA] Görüntü alınamadı.")
                continue

            # Görüntüyü düzelt (undistort)
            frame = cv2.undistort(frame, camera_matrix, dist_coeffs)

            # Görüntüyü yeniden boyutlandır
            frame = cv2.resize(frame, (320, 240))

            # İnsan tespiti
            dikdortgenler, _ = hog.detectMultiScale(frame, winStride=(8, 8), padding=(8, 8), scale=1.05)

            if len(dikdortgenler) > 0:
                print(f"[KAMERA] {len(dikdortgenler)} kişi algılandı.")
                son_gorulme_zamani = time.time()
            else:
                print("[KAMERA] Kimse algılanmadı.")
                if time.time() - son_gorulme_zamani > 15:
                    print("[ÇIKIŞ] Oda boş, LED kapatıldı.")
                    GPIO.output(LED_PIN, GPIO.LOW)

            # Dikdörtgenleri çiz
            for (x, y, w, h) in dikdortgenler:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow("Kalibrasyonlu Kamera Görüntüsü", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
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
