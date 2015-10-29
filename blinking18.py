import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 23
button = 18

GPIO.setup(led, GPIO.OUT)
GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)

while True:
    if not GPIO.input(button):
        print("button pressed")
        break

i = 0
while i < 10:
    GPIO.output(led, 1)
    time.sleep(1)
    GPIO.output(led, 0)
    time.sleep(1)
    i += 1
GPIO.cleanup()
