import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sender = 22

GPIO.setup(sender, GPIO.OUT)
i = 0
while i < 100:
    GPIO.output(sender, 1)
    time.sleep(0.001)
    GPIO.output(sender, 0)
    time.sleep(0.001)
    i += 1
GPIO.cleanup()
