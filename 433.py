import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sender = 22
T = 0.0005
GPIO.setup(sender, GPIO.OUT)


def one():
    GPIO.output(sender, 1)
    time.sleep(T)
    GPIO.output(sender, 0)
    time.sleep(T)


def zero():
    GPIO.output(sender, 1)
    time.sleep(T)
    GPIO.output(sender, 0)
    time.sleep(5*T)


def sync():
    GPIO.output(sender, 1)
    time.sleep(T)
    GPIO.output(sender, 0)
    time.sleep(10*T)


def pause():
    GPIO.output(sender, 1)
    time.sleep(T)
    GPIO.output(sender, 0)
    time.sleep(40*T)
# S1010 10101 001
# 10011 01010 011
# 01010 01100 110
# 10011 01001 011
# 01010 10101 010P
i = 0
GPIO.output(sender, 0)
time.sleep(0.002)
while i < 5:
    # S1010 10101 001
    sync()
    one()
    zero()
    one()
    zero()

    one()
    zero()
    one()
    zero()
    one()

    zero()
    zero()
    one()

    # 10011 01010 011
    one()
    zero()
    zero()
    one()
    one()

    zero()
    one()
    zero()
    one()
    zero()

    zero()
    one()
    one()

    # 01010 01100 110
    zero()
    one()
    zero()
    one()
    zero()

    zero()
    one()
    one()
    zero()
    zero()

    one()
    one()
    zero()

    # 10011 01001 011
    one()
    zero()
    zero()
    one()
    one()

    zero()
    one()
    zero()
    zero()
    one()

    zero()
    one()
    one()

    # 01010 10101 010P
    zero()
    one()
    zero()
    one()
    zero()

    one()
    zero()
    one()
    zero()
    one()

    zero()
    one()
    zero()
    pause()
    i += 1
GPIO.cleanup()
