try:
    import RPi.GPIO as GPIO
except ImportError:
    import RPiMock.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def set_state(gpio, action):
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, action)
