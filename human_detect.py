#Bu kodda, OpenCV kutuphanesi ve HOG (Histogram of Oriented Gradients) tabanli siniflandirici kullanilarak kameradan alinan goruntulerde insan tespiti yapilir. Insanlar tespit edildiginde, uzerlerine yesil dikdortgen cizilir.
import cv2

# HOG tanimlayici / insan tespit edici baslatiliyor
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# USB kameradan video yakalama baslatiliyor (0 sistemine gore degisebilir)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera acilamadi.")
    exit()

print("Kamera baslatildi. Cikmak icin 'q' tusuna basin.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Islem hizini arttirmak icin goruntu yeniden boyutlandiriliyor
    frame = cv2.resize(frame, (320, 240))

    # Karedeki insanlar tespit ediliyor
    (rects, weights) = hog.detectMultiScale(
        frame,
        winStride=(8, 8),
        padding=(8, 8),
        scale=1.05
    )

    # Tespit edilen insanlarin uzerine dikdortgen ciziliyor
    for (x, y, w, h) in rects:
        print(f"[DETECTED] Kisi ({x}, {y}) - ({x + w}, {y + h}) araliginda")
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Sonuc ekranda gosteriliyor
    cv2.imshow("Human Detection (HOG)", frame)

    # 'q' tusuna basildiginda dongu sonlandirilir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera serbest birakiliyor ve pencereler kapatiliyor
cap.release()
cv2.destroyAllWindows()
