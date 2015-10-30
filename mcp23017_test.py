#!/usr/bin/python
from Adafruit.Adafruit_MCP230xx.Adafruit_MCP230xx import Adafruit_MCP230XX
from time import sleep

mcp = Adafruit_MCP230XX(address = 0x21, num_gpios = 16) # MCP23017

# Set pins 0, 1 and 2 to output (you can set pins 0..15 this way)
mcp.config(0, mcp.OUTPUT)

# Read input pin and display the results
print "Pin 3 = %d" % (mcp.input(3) >> 3)

# Python speed test on output 0 toggling at max speed
print "Starting blinky on pin 0 (CTRL+C to quit)"
while (True):
  mcp.output(0, 1)  # Pin 0 High
  sleep(1);
  mcp.output(0, 0)  # Pin 0 Low
  sleep(1);
