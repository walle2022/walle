#!/usr/bin/env python3
#Implementation of WALL-E's eye movements on startup to replicate the ones from the movie

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

##################### GPIO pin description and setup #######################

    # Pin 32 = Left Eye  (Purple wire)
    # Pin 33 = Right Eye (Green wire)

GPIO.setup(32, GPIO.OUT)        # Purple Wire
GPIO.setup(33, GPIO.OUT)        # Green Wire
left = GPIO.PWM(32,34)
right = GPIO.PWM(33,34)
left.start(0)
right.start(0)

#############################################################################

######################### helper functions ##################################
def leftEye():
    # moves Left Eye
    print("LEFT Eye called")
    left.ChangeDutyCycle(5)
    left.ChangeFrequency(28)
    time.sleep(1)
    left.ChangeFrequency(34)
    time.sleep(1)
    left.ChangeFrequency(28)
    time.sleep(0.3)
    left.ChangeFrequency(34)
    time.sleep(0.5)
    left.ChangeDutyCycle(0)

def rightEye():
    # moves Right Eye
    print("RIGHT Eye called")
    right.ChangeDutyCycle(5)
    right.ChangeFrequency(45)
    time.sleep(1)
    right.ChangeFrequency(34)
    time.sleep(1)
    right.ChangeFrequency(45)
    time.sleep(0.3)
    right.ChangeFrequency(34)
    time.sleep(0.5)
    right.ChangeDutyCycle(0)

def bothEyes():
    # moves Both Eyes
    print("BOTH Eyes called")
    right.ChangeDutyCycle(5)
    right.ChangeFrequency(45)
    left.ChangeDutyCycle(5)
    left.ChangeFrequency(28)
    time.sleep(1)
    right.ChangeFrequency(34)
    right.ChangeDutyCycle(0)
    left.ChangeFrequency(34)
    left.ChangeDutyCycle(0)
    time.sleep(1)
    right.ChangeDutyCycle(5)
    right.ChangeFrequency(45)
    left.ChangeDutyCycle(5)
    left.ChangeFrequency(28)
    time.sleep(0.3)
    right.ChangeFrequency(34)
    right.ChangeDutyCycle(0)
    left.ChangeFrequency(34)
    left.ChangeDutyCycle(0)
    time.sleep(0.5)

#############################################################################
    
while True:
    rightEye()
    leftEye()
    bothEyes()
GPIO.cleanup()
