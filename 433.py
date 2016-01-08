import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sender = 22

GPIO.setup(sender, GPIO.OUT)
i = 0
while i < 10:
    GPIO.output(sender, 1)
    time.sleep(0.0005)
    GPIO.output(sender, 0)
    time.sleep(0.0005)
    i += 1
GPIO.cleanup()
