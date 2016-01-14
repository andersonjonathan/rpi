try:
    import RPi.GPIO as GPIO
except ImportError:
    import RPiMock.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
sender = 22
GPIO.setup(sender, GPIO.OUT)


def transmit(payload):
    """
    :param payload: Shall be a list of tuples (bit, time)
    :return:
    """
    i = 0
    while i < 10:
        for p in payload:
            GPIO.output(sender, p[0])
            time.sleep(p[1])
        i += 1
