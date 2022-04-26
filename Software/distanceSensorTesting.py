#!/usr/bin/env python3
#This code is configured to work on pins 3(SDA) and 5(SCL) on the Jetson Nano and not configured to work on the I2C Bus 

import board
import busio
import time
import adafruit_vl53l0x

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

print(type(vl53.range))
# Main loop will read the range and print it every second.
while True:
    print("Range: {0}mm".format(vl53.range))
    time.sleep(0.1)
