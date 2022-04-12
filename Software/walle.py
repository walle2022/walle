#!/usr/bin/env python3

import Jetson.GPIO as GPIO
import time
import board
import busio
import adafruit_vl53l0x

GPIO.setmode(GPIO.BOARD)
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)
channel = 13
GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
try: 
    while True:
        if(vl53.range < 150):
            GPIO.output(channel, GPIO.LOW)
        else:
            GPIO.output(channel, GPIO.HIGH)
            time.sleep(0.25)
finally:
    GPIO.cleanup()


