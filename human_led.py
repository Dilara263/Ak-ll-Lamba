#Bu kod, bir kamera kullanarak goruntude insan tespiti yapar ve bir LED yardimiyla fiziki bir cikti verir. Eger goruntude en az bir kisi tespit edilirse, LED yanar. Kisi tespiti sona erdiginde LED kapanir.

import RPi.GPIO as GPIO
import cv2

# GPIO ayarlari
LED_PIN = 17  # GPIO17 pini (Pin 11)

GPIO.setmode(GPIO.BCM)      # BCM pin numaralama modunu kullan
GPIO.setup(LED_PIN, GPIO.OUT)  # LED pinini cikis olarak ayarla

# HOG insan tespiti icin hazirlik
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Kamera ac
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera acilamadi.")
    exit()

print("Kamera baslatildi. Cikmak icin 'q' ya bas.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Kareyi kuculturuz performans icin
    frame = cv2.resize(frame, (320, 240))

    # Insanlari tespit et
    (rects, weights) = hog.detectMultiScale(
        frame,
        winStride=(8, 8),
        padding=(8, 8),
        scale=1.05
    )

    # Insan bulunduysa LED yak
    if len(rects) > 0:
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED ac
        print(f"{len(rects)} kisi tespit edildi! LED acildi.")
    else:
        GPIO.output(LED_PIN, GPIO.LOW)   # LED kapat

    # Tespit edilen insanlari kare icine al
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Sonucu goster
    cv2.imshow("Insan Tespiti (HOG)", frame)

    # 'q' ya basinca cik
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynaklari temizle
GPIO.output(LED_PIN, GPIO.LOW)
GPIO.cleanup()

cap.release()
cv2.destroyAllWindows()
