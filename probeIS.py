# using modules and layout from adafruit official website for MCP3008 

import busio
import digitalio
import time
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from ISStreamer.Streamer import Streamer

# SPI bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# chip select
cs = digitalio.DigitalInOut(board.D5)

# mcp object
mcp = MCP.MCP3008(spi, cs)

# analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

# create bucket in initial state
streamer = Streamer(
    bucket_name="Probe",
    bucket_key="94GXJX4HG8XG",
    access_key="ist_BmX3KMqVGoOAZNOYI6EwRStbB1I0DMKF"
        )

# function for getting readings
def getTemp():

    # create variables to store averages
    totalADC = 0
    totalVolt = 0

    # loop through and gather an average reading over the course of a second
    for count in range(10):
        totalADC += chan.value
        totalVolt += chan.voltage
        time.sleep(.1)
        val = totalADC / 10
    return val

# functon for converting reading into temperature in Fahrenheit
def convertToF(val):
    
    # split between hot and cold converters (calibrated these functions based on resistance and temperature)
    if(val > 24300):
        # colder conversion
        temp = 162 - (0.00236 * val) - ((0.00000000835) * val * val)
    else:
        # hotter conversion
        temp = 245 - (0.01 * val) + ((0.000000171) * val * val)
    return round(temp, 2)

# function for sending data to initial state
def sendData(temp):
    streamer.log("Probe", temp)
    streamer.flush()
    streamer.close()




