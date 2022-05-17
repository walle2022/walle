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
import time
from adafruit_servokit import ServoKit
import adafruit_motor.servo
import adafruit_pca9685

GPIO.cleanup()

i2c = busio.I2C(board.SCL, board.SDA)
kit = ServoKit(channels=16, i2c=i2c)
left = kit.servo[6]
right = kit.servo[7]

#Initialize and set up motors
GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.OUT)        # MoB Purple Wire
GPIO.setup(36, GPIO.OUT)        # MoB Green Wire
GPIO.setup(37, GPIO.OUT)        # MoA Green Wire
GPIO.setup(38, GPIO.OUT)        # MoA Purple Wire

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
count = 0
while count<3:
    turnLeft()
    left.angle = 35
    right.angle = 50
    time.sleep(0.4)
    turnRight()
    left.angle = 1
    right.angle = 20
    time.sleep(0.4)
    reverseLeft()
    left.angle = 35
    right.angle = 50
    time.sleep(0.4)
    reverseRight()
    left.angle = 1
    right.angle = 20
    time.sleep(0.4)
    STOPPED()
    left.angle = None
    right.angle = None
    count+=1
