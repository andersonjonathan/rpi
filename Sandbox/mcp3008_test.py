__author__ = 'jonathan'
import time
import os
import RPi.GPIO as GPIO
from Adafruit.Adafruit_MCP3008.mcp3008 import readadc
GPIO.setmode(GPIO.BCM)
DEBUG = 1

SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
# 10k trim pot connected to adc #0
potentiometer_adc = 0;
last_read = 0
tolerance = 5
# this keeps track of the last potentiometer value
# to keep from being jittery we'll only change
# volume when the pot has moved more than 5 'counts'
while True:
    # we'll assume that the pot didn't move
    trim_pot_changed = False
    # read the analog pin
    trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
    # how much has it changed since the last read?
    pot_adjust = abs(trim_pot - last_read)
    if DEBUG:
        print "trim_pot:", trim_pot
        print "pot_adjust:", pot_adjust
        print "last_read", last_read
    if ( pot_adjust > tolerance ):
        trim_pot_changed = True
    if DEBUG:
        print "trim_pot_changed", trim_pot_changed
    if ( trim_pot_changed ):
        set_volume = trim_pot / 10.24
        set_volume = round(set_volume)
        set_volume = int(set_volume)
        # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
        # round out decimal value
        # cast volume as integer
        print 'Volume = {volume}%' .format(volume = set_volume)
        set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
        #os.system(set_vol_cmd) # set volume
        if DEBUG:
            print "set_volume", set_volume
            print "tri_pot_changed", set_volume
        # save the potentiometer reading for the next loop
        last_read = trim_pot
    # hang out and do nothing for a half second
    time.sleep(0.5)