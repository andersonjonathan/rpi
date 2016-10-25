#!/usr/bin/python
from Adafruit.Adafruit_MCP230xx.Adafruit_MCP230xx import Adafruit_MCP230XX
from time import sleep

mcp = Adafruit_MCP230XX(address = 0x21, num_gpios = 16) # MCP23017

# Set pins 0, 1 and 2 to output (you can set pins 0..15 this way)
d1 = 8
d2 = 9
d3 = 10
d4 = 11
d5 = 12
d6 = 13
d7 = 7
d8 = 6
d9 = 5
d10 = 4
d11 = 3
d12 = 2
mcp.config(d1, mcp.OUTPUT)
mcp.config(d2, mcp.OUTPUT)
mcp.config(d3, mcp.OUTPUT)
mcp.config(d4, mcp.OUTPUT)
mcp.config(d5, mcp.OUTPUT)
mcp.config(d6, mcp.OUTPUT)
mcp.config(d7, mcp.OUTPUT)
mcp.config(d8, mcp.OUTPUT)
mcp.config(d9, mcp.OUTPUT)
mcp.config(d10, mcp.OUTPUT)
mcp.config(d11, mcp.OUTPUT)
mcp.config(d12, mcp.OUTPUT)

mcp.output(d7, 1)  # Segment 1
mcp.output(d10, 0)  # Segment 2
mcp.output(d11, 0)  # Segment 3
mcp.output(d6, 0)  # Segment 4
while (True):
    mcp.output(d1, 1)
    mcp.output(d2, 1)
    mcp.output(d4, 1)
    mcp.output(d5, 1)
    mcp.output(d9, 1)
    mcp.output(d8, 1)
    mcp.output(d12, 1)

    sleep(1)
    mcp.output(d1, 0)
    mcp.output(d2, 0)
    mcp.output(d4, 0)
    mcp.output(d5, 0)
    mcp.output(d9, 0)
    mcp.output(d8, 0)
    mcp.output(d12, 0)
    sleep(1)
