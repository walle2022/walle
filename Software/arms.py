#!/usr/bin/env python3

import time
from adafruit_servokit import ServoKit
import adafruit_motor.servo
import board
import busio
import adafruit_pca9685

i2c = busio.I2C(board.SCL_1, board.SDA_1)
kit = ServoKit(channels=16, i2c=i2c)
left = kit.servo[6]
right = kit.servo[7]
print('setting up')
right.angle = 20
time.sleep(1)
left.angle = 1
time.sleep(1)
#left.angle = None
count = 0

while count<3: 
    left.angle = 35
    right.angle = 50
    time.sleep(1)
    left.angle = 1
    right.angle = 20
    time.sleep(1)
    left.angle = 35
    right.angle = 50
    time.sleep(1)
    right.angle = 20
    left.angle = 1
    time.sleep(1)
    count+=1
left.angle = None
right.angle = None
