#!/usr/bin/env python3

import board
import busio
import time
import adafruit_vl53l0x
import adafruit_tca9548a

# Create I2C bus as normal
i2c = busio.I2C(board.SCL, board.SDA)

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c, address= 0x71)

# For each sensor, create it using the TCA9548A channel instead of the I2C object
vl531 = adafruit_vl53l0x.VL53L0X(tca[1])

while True:
    print("Range 1: {0}mm".format(vl531.range))
    if(vl531.range <= 200):
        print('Object Detected!')
    time.sleep(0.1)

