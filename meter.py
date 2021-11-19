import minimalmodbus
import os
import time
import logging
import requests
import json


def postUrl(info):
    server = os.environ['SERVER']
    url = os.environ['URL']
    route = server + url
    requests.post(route, json=json.dumps(info))


# logging
LOG_LEVEL = os.environ['LOG_LEVEL']

logging.basicConfig(filename='meter.log', level=LOG_LEVEL)

# Device configuration

# slave address (in decimal)
DEVICE_ADDRESS = 1
# ENABLE/DISABLE communication debug mode
DEVICE_DEBUG = False
# Master PORT name -- Change as needed for your host.
PORT_NAME = os.environ['PORT']

# MODBUS instrument initialization
instrument = minimalmodbus.Instrument(PORT_NAME, DEVICE_ADDRESS, debug=DEVICE_DEBUG)

# MODBUS instrument connection settings
# Change as needed depending on your Hardware requirements
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.mode = minimalmodbus.MODE_RTU
instrument.serial.timeout = 0.2

# Print MODBUS configuration
print("MODBUS Configuration\n")
print("********************\n")
print(instrument)
print("\n********************\n")

# Read Temperature
REGISTER_ADDRESS_TEMP = 0
REGISTER_NUMBER_DECIMALS = 2
ModBus_Command = 3

count = 0
PERIOD = os.environ['PERIOD']

while True:
    # Register number, number of decimals, function code
    try:
        data = instrument.read_registers(REGISTER_ADDRESS_TEMP, 3, 3)
        string = time.strftime("%Y-%m-%d %H:%M:%S - ") + " ".join(map(str, data))
        print(string)
        logging.info(string)

        count += 1
        if count == int(PERIOD):
            info = {
                'voltage': data[0],
                'current': data[1],
                'temperature': data[2]
            }
            postUrl(info)
            count = 0
    except Exception as e:
        print(e)
        logging.debug(e)

    time.sleep(1)
