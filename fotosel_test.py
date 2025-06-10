#Bu kodda bir LDR (Light Dependent Resistor) ve kondansator kullanilarak odasindaki isik miktari olculur. LDR'nin uzerinden gecen zaman olcumuyle, ortam isiginin ne kadar parlak ya da karanlik oldugu belirlenir. Bu degerlere gore LED parlakligi PWM (Pulse Width Modulation) ile ayarlanir. Yani ortam karardikca LED daha cok yanar.



import RPi.GPIO as GPIO
import time
from gpiozero import PWMLED

# Pin ayarlari
ldr_pin = 5  # LDR ve kondansatorun bagli oldugu GPIO pini
led = PWMLED(17)  # PWM ile LED bagli olan GPIO pini (GPIO17)

# GPIO ayari
GPIO.setmode(GPIO.BCM)

def rc_time(pin):
    count = 0

    # Kondansatoru bosalt
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
    time.sleep(0.1)

    # Pini girise ayarla ve sarj suresini olc
    GPIO.setup(pin, GPIO.IN)

    # Kondansator sarj olana kadar say
    while GPIO.input(pin) == GPIO.LOW:
        count += 1
        if count > 10000:
            break  # guvenlik siniri

    return count

try:
    while True:
        light_level = rc_time(ldr_pin)
        # Degeri normalize et (karanlik = daha yuksek sayi)
        brightness = min(1.0, max(0.0, (light_level_
