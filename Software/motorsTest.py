#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

##################### GPIO pin description and setup #######################

    # Pin 35 = Input 1 (Purple wire)
    # Pin 36 = Input 2 (Green wire)
    # Pin 37 = Input 3 (Purple wire)
    # Pin 38 = Input 4 (Green wire)

GPIO.setup(35, GPIO.OUT)        # Purple Wire
GPIO.setup(36, GPIO.OUT)        # Green Wire
GPIO.setup(37, GPIO.OUT)        # Purple Wire
GPIO.setup(38, GPIO.OUT)        # Green Wire

######################## helper function definitions #########################


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

def STOPPED():
    #both motors are stopped
    print("STOPPED function called")
    GPIO.output(35, False)
    GPIO.output(36, False)
    GPIO.output(37, False)
    GPIO.output(38, False)


########################              main           #########################
if __name__ == "__main__":
    
    val = int(input("Enter a number (1,2,3,4,5,6,7,9): "))
    print(type(val))
    while (val != 9):
        if val == 1:
            forward()
        elif val == 2:
            reverse()
        elif val == 3:
            turnLeft()
        elif val == 4:
            turnRight()
        elif val == 5:
            reverseLeft()
        elif val == 6:
            reverseRight()
        elif val == 7:
            STOPPED()
        else:
            print("Invalid input")
        val = int(input("Enter a number (1,2,3,4,5,6,7,9): "))
