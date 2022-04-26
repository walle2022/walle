#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_vl53l0x
import os
import sys

#Initialize and set up motors
GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.OUT)        # Purple Wire
GPIO.setup(36, GPIO.OUT)        # Green Wire
GPIO.setup(37, GPIO.OUT)        # Purple Wire
GPIO.setup(38, GPIO.OUT)        # Green Wire

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

def STOPPED():
    #both motors are stopped
    print("STOPPED function called")
    GPIO.output(35, False)
    GPIO.output(36, False)
    GPIO.output(37, False)
    GPIO.output(38, False)

def forward():
    #both motors move clockwise
    # forward = TOF sensor placement
    print("Forward function called")
    GPIO.output(35, False)
    GPIO.output(36,True)
    GPIO.output(37, False)
    GPIO.output(38,True)

def reverse():
    #both motors move COUNTERclockwise
    # reverse = opposite of TOF sensor placement
    print("Reverse function called")
    GPIO.output(35, True)
    GPIO.output(36, False)
    GPIO.output(37, True)
    GPIO.output(38, False)

def turnLeft():
    #RIGHT motor moves clockwise
    #left motor is stopped
    print("turnLeft function called")
    GPIO.output(35, False)
    GPIO.output(36, True)
    GPIO.output(37, False)
    GPIO.output(38, False)

def turnRight():
    #LEFT motor moves clockwise
    #right motor is stopped
    print("turnRight function called")
    GPIO.output(35, False)
    GPIO.output(36, False)
    GPIO.output(37, False)
    GPIO.output(38, True)

def reverseLeft():
    #RIGHT motor moves COUNTERclockwise
    #left motor is stopped
    print("reverseLeft function called")
    GPIO.output(35, True)
    GPIO.output(36, False)
    GPIO.output(37, False)
    GPIO.output(38, False)

def reverseRight():
    #LEFT motor moves COUNTERclockwise
    #right motor is stopped
    print("reverseRight function called")
    GPIO.output(35, False)
    GPIO.output(36, False)
    GPIO.output(37, True)
    GPIO.output(38, False)

while True:
    if (vl53.range < 200):
        forward()
   else:
       STOPPED()
       reverse()
       time.sleep(3)
       STOPPED()
       turnRight()
       time.sleep(2)
