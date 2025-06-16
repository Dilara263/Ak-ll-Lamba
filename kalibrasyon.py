import cv2
import numpy as np
import glob

# Chessboard boyutu
CHESSBOARD_SIZE = (9, 6)  # iç köşe sayısı

# 3D nokta vektörü oluştur (0,0,0), (1,0,0), ..., (8,5,0)
objp = np.zeros((CHESSBOARD_SIZE[0]*CHESSBOARD_SIZE[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0], 0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)

objpoints = []  # gerçek dünya koordinatları
imgpoints = []  # görüntü koordinatları

cap = cv2.VideoCapture(0)

print("Satranç tahtası görüntülerini farklı açılardan göster. 's' ile kaydet, 'q' ile bitir.")

saved = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret_corners, corners = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE, None)

    if ret_corners:
        cv2.drawChessboardCorners(frame, CHESSBOARD_SIZE, corners, ret_corners)

    cv2.imshow("Kalibrasyon Goruntusu", frame)
    key = cv2.waitKey(1)

    if key == ord('s') and ret_corners:
        objpoints.append(objp)
        imgpoints.append(corners)
        saved += 1
        print(f"[INFO] Kaydedilen poz: {saved}")

    elif key == ord('q') or saved >= 15:
        break

cap.release()
cv2.destroyAllWindows()

if saved < 10:
    print("Yeterli görüntü alınamadı!")
    exit()

# Kalibrasyonu yap
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("\n--- Kamera Kalibrasyon Sonuçları ---")
print("Kamera Matrisi (cameraMatrix):\n", mtx)
print("Distorsiyon Katsayıları (distCoeffs):\n", dist)
