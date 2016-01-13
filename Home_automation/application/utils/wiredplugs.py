import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def turn_on(gpio):
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, 0)


def turn_off(gpio):
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, 1)