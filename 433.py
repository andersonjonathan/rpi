import RPi.GPIO as GPIO
import time

# S 1010 1010 1001 1001 1010 1001 1010 1001 1001 1010 0110 1001 0110 1010 1010 1010 P
# S HH   HH   HH   HH   HH   HH   HH   HH   HH   HH   HH   HH   HH   GO   CC   EE   P
#
# Bitcoding
# The data part on the physical link is coded so that every logical bit is sent as two physical bits, where the second one is the inverse of the first one.
# '0' => '01'
# '1' => '10'
# Example: For the logical datastream 0111, is sent over the air as 01101010.
#
# Packetformat
# Every packet consists of a sync bit followed by 26 + 2 + 4 (total 32 logical data part bits) and is ended by a pause bit.
#
# S HHHH HHHH HHHH HHHH HHHH HHHH HHGO CCEE P
#
# S = Sync bit.
# H = The first 26 bits are transmitter unique codes, and it is this code that the reciever "learns" to recognize.
# G = Group code. Set to 0 for on, 1 for off.
# O = On/Off bit. Set to 0 for on, 1 for off.
# C = Channel bits. Proove/Anslut = 00, Nexa = 11.
# E = Unit bits. Device to be turned on or off.
# Proove/Anslut Unit #1 = 00, #2 = 01, #3 = 10.
# Nexa Unit #1 = 11, #2 = 10, #3 = 01.
# P = Pause bit.
#
# '1' bit:
#  _____
# |     |
# |     |
# |     |_____
#
# |-----|-----|
#    T     T
#
# '0' bit:
#  _____
# |     |
# |     |
# |     |_________________________
#
# |-----|-------------------------|
#    T               5T
#
# 'SYNC' bit:
#  _____
# |     |
# |     |
# |     |__________________________________________________
#
# |-----|--------------------------------------------------|
#    T                         10T
#
# 'PAUSE' bit:
#  _____
# |     |
# |     |
# |     |_______________________ . . . ____
#
# |-----|----------------------- . . . ----|
#    T                40T
#
# T = 250 us
# (5T = 1250 us)
# (10T = 2500 us)
# (40T = 10 ms)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sender = 22
T = 0.00025
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


def unique_transmitter_code():
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
    zero()


def group(on):
    if on:
        one()
        zero()
    else:
        zero()
        one()


def on_off(on):
    if not on:
        one()
        zero()
    else:
        zero()
        one()


def chanel():
    one()
    zero()
    one()
    zero()


def unit(nr):
    if nr == 1:
        one()
        zero()
        one()
        zero()
    if nr == 2:
        one()
        zero()
        zero()
        one()
    if nr == 3:
        zero()
        one()
        one()
        zero()
    if nr == 4:
        zero()
        one()
        zero()
        one()


def send_code(group_on, on, unit_nr):
    i = 0
    GPIO.output(sender, 0)
    time.sleep(0.002)
    
    while i < 10:
        sync()
        unique_transmitter_code()
        group(group_on)
        on_off(on)
        chanel()
        unit(unit_nr)
        pause()
        i += 1

# GPIO.cleanup()
