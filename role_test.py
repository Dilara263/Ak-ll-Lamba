#Bu kod, Raspberry Pi uzerinden bir role modulu ile bagli olan LED lambayi kontrol etmek icin kullanilir. Role, harici yukleri (ornegin ampul, LED, motor) kontrol etmek icin bir anahtar gorevi gorur. Bu kodda 2 saniye araliklarla lamba yanip soner.

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

RELAY_PIN = 17
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, False)
#GPIO.LOW
try:
    while True:
        GPIO.setup(RELAY_PIN, True)  # Röleyi aktif et (LED yanar)
        time.sleep(2)
        GPIO.setup(RELAY_PIN, False)   # Röleyi pasif et (LED söner)
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
#ilk başta GPIO.setup yazan yerde GPIO.output yazıyordu. Bu durumda röle ışığı açıp kapatmıyordu. sonrasında bunu setup ile değiştirdikten sonra röle ile led doğru çalışmaya başladı.
