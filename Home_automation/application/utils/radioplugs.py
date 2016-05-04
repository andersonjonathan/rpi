try:
    import RPi.GPIO as GPIO
except ImportError:
    import RPiMock.GPIO as GPIO

import time


def transmit(payload, sender):
    """
    :param sender: GPIO port to send on
    :param payload: Shall be a list of tuples (bit, time)
    :return:
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(sender, GPIO.OUT)
    i = 0
    while i < 10:
        for p in payload:
            GPIO.output(sender, p[0])
            time.sleep(p[1])
        i += 1
