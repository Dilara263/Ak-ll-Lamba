#Bu kodda bir HC-SR04 ultrasonik mesafe sensoru kullanilarak cisimle olan mesafe olculur. Cisim yaklastikca bir LED’in parlakligi PWM (Pulse Width Modulation) kullanilarak artirilir. Uzaklastikca LED’in parlakligi azalir. Bu sayede mesafeye duyali isik sistemi olusturulur.

import RPi.GPIO as GPIO
import time

# GPIO ayarlari
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 23     # TRIG pini
ECHO = 24     # ECHO pini
LED = 18      # PWM ile bagli LED pini

# Pin modlari ayarlaniyor
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

# PWM LED baslatiliyor (1000 Hz frekans)
pwm_led = GPIO.PWM(LED, 1000)
pwm_led.start(0)

print("Mesafe sensoru baslatildi...")

try:
    while True:
        # Sensor tetikleme islemi
        GPIO.output(TRIG, False)
        time.sleep(0.05)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # ECHO sinyali bekleniyor
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        # Zaman farki hesaplanip mesafeye cevriliyor
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # cm cinsinden mesafe
        distance = round(distance, 2)

        if 2 < distance < 100:  
            # Mesafe icerisindeyse parlaklik ayarla (yaklasinca artar)
            brightness = max(0, min(100, 100 - (distance)))  
            pwm_led.ChangeDutyCycle(brightness)
            print(f"Mesafe: {distance} cm - Parlaklik: {int(brightness)}%")
        else:
            # Menzil disinda ise LED kapat
            pwm_led.ChangeDutyCycle(0)
            print("Menzil disinda!")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program sonlandiriliyor...")
    pwm_led.stop()
    GPIO.cleanup()
