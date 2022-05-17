#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import board 
import busio
import adafruit_vl53l0x
import adafruit_tca9548a
import neopixel_spi as neopixel
import os
import speech_recognition as sr
import sys
import pyttsx3
import wolframalpha
import wikipedia

GPIO.cleanup()

#Initialize and set up motors
GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.OUT)        # Purple Wire
GPIO.setup(36, GPIO.OUT)        # Green Wire
GPIO.setup(37, GPIO.OUT)        # Purple Wire
GPIO.setup(38, GPIO.OUT)        # Green Wire

# Initialize I2C bus and sensor. Pin 3(SDA) and 5(SCL)
i2c = busio.I2C(board.SCL, board.SDA)
tca = adafruit_tca9548a.TCA9548A(i2c,address = 0x71 )
vl530 = adafruit_vl53l0x.VL53L0X(tca[0]) #edge detection
vl531 = adafruit_vl53l0x.VL53L0X(tca[1]) #object detection

def STOPPED():
    #both motors are stopped
    print("STOPPED function called")
    GPIO.output(35, False)
    GPIO.output(36, False)
    GPIO.output(37, False)
    GPIO.output(38, False)

def turnLeft():
    #RIGHT motor moves clockwise
    #left motor is stopped
    print("turnLeft function called")
    GPIO.output(35, False)
    GPIO.output(36, True)
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

def detection():
    while(vl530.range < 350 and vl531.range > 200):
        forward()
    STOPPED()
    time.sleep(2)
    while(vl531.range <= 200): #object Detection
        turnLeft()
        time.sleep(3)
        turnRight()
        time.sleep(2)
        forward()
    STOPPED()
    while(vl530.range >= 350): #edge detection
        reverse()
        time.sleep(2)
        turnLeft()
        time.sleep(0.4)
        forward()
        time.sleep(5)
    STOPPED()

detection()
print("Range 1: {0}mm".format(vl530.range))
