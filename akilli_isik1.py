import RPi.GPIO as GPIO
import time
import cv2

# --- Pin ayarlari ---
LDR_PIN = 5         # Fotosel (LDR)
TRIG = 23           # HC-SR04 TRIG
ECHO = 24           # HC-SR04 ECHO
LED_PIN = 17        # LED cikisi

# --- GPIO ayarlari ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)  # Baslangicta LED kapali

# --- Kamera ayarlari ---
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera acilamadi.")
    exit()

# --- LDR okuma fonksiyonu ---
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

# --- HC-SR04 mesafe fonksiyonu ---
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

# --- Ana dongu ---
print("Sistem basladi. Cikmak icin Ctrl+C ya da 'q'.")

son_gorulme_zamani = time.time()

try:
    while True:
        # 1. Ortam isigi kontrolu
        isik = oku_isik(LDR_PIN)
        print(f"[FOTOSEL] Ortam isik seviyesi: {isik}")
        if isik > 200:
            print("[SISTEM] Ortam karanlik, sistem aktif.")

            # 2. Mesafe kontrolu
            mesafe = oku_mesafe()
            print(f"[HC-SR04] Olculen mesafe: {mesafe} cm")

            if mesafe < 60:
                print("[GIRIS] Iceriye biri girdi! LED yakildi.")
                GPIO.output(LED_PIN, GPIO.HIGH)
                son_gorulme_zamani = time.time()

            # 3. Kamera ile insan tespiti
            ret, frame = cap.read()
            if not ret:
                print("[KAMERA] Goruntu alinamadi.")
                continue

            frame = cv2.resize(frame, (320, 240))
            dikdortgenler, _ = hog.detectMultiScale(frame, winStride=(8, 8), padding=(8, 8), scale=1.05)

            if len(dikdortgenler) > 0:
                print(f"[KAMERA] Kamerada {len(dikdortgenler)} kisi algilandi.")
                son_gorulme_zamani = time.time()
            else:
                print("[KAMERA] Kamerada kimse algilanamadi.")
                if time.time() - son_gorulme_zamani > 15:
                    print("[CIKIS] Odada kimse yok, LED kapatildi.")
                    GPIO.output(LED_PIN, GPIO.LOW)

            for (x, y, w, h) in dikdortgenler:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow("Kamera Goruntusu - Insan Tespiti", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("[FOTOSEL] Ortam aydinlik, sistem pasif. LED kapali.")
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(1)

except KeyboardInterrupt:
    print("\n[SONLANDIRMA] Program durduruldu.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()
