#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import board 
import busio
import adafruit_vl53l0x
import neopixel_spi as neopixel
import os
import speech_recognition as sr
import sys
import pyttsx3

r = sr.Recognizer()
m = sr.Microphone()
r.energy_threshold = 300

GPIO.cleanup()

engine = pyttsx3.init()
#voices = engine.getProperty('voices')
engine.setProperty('rate', 150)
engine.setProperty('voice', 'english+m1')

#Initialize and set up motors
GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.OUT)        # Purple Wire
GPIO.setup(36, GPIO.OUT)        # Green Wire
GPIO.setup(37, GPIO.OUT)        # Purple Wire
GPIO.setup(38, GPIO.OUT)        # Green Wire

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

#Initialize NeoPixels
NUM_PIXELS = 12
PIXEL_ORDER = neopixel.GRB
happy = 0xf2a900
sad = 0x0047ab
love = 0x9f2b68
snack = 0xcc5500
destruction = [0x8b0000, 0xf2a900, 0x71b2c9, 0xd7a3ab]
trash = 0x00ff00

spi = board.SPI()

pixels = neopixel.NeoPixel_SPI(
    spi, NUM_PIXELS, pixel_order=PIXEL_ORDER, auto_write=False
)

pixels.brightness = 0.1

def colors(color):
    if color == "trash":
        for i in range(NUM_PIXELS):
            pixels[i] = trash
        pixels.show()
    elif color=="hello": #greeting
        for i in range(NUM_PIXELS):
            pixels[i] = happy
        pixels.show()
    elif color=="sad": #battery low
        for i in range(NUM_PIXELS):
            pixels[i] = sad
        pixels.show()
    elif color=="sleep": #sleep
        for i in range(NUM_PIXELS):
            pixels[i] = love
        pixels.show()
    elif color=="snack":
        for i in range(NUM_PIXELS):
            pixels[i] = snack
        pixels.show()
    elif color=="destruction": #obstacle
        #pixels.brightness = 0.5
        for j in range(3):
            for i in range(NUM_PIXELS):
                pixels[i] = destruction[0]
            pixels.show()
            time.sleep(0.1)
            for k in range(NUM_PIXELS):
                pixels[k] = 0x000000
            pixels.show()
            time.sleep(0.1)
            pixels.brightness += 0.3
        for m in range(NUM_PIXELS):
            pixels[m] = destruction[0]
        pixels.show()
        pixels.brightness = 0.1
    else:
        time.sleep(0.1)

def commands(word):
    if word == 'sleep':
        myText = 'Okay. Going to sleep.'
        engine.say(myText)
        engine.runAndWait()
    elif word == 'snack':
        myText = 'Okay. Opening the snack box. Nom Nom.'
        engine.say(myText)
        engine.runAndWait()
    elif word == 'hello':
        myText = 'Hi friend. My name is Wall-E'
        engine.say(myText)
        engine.runAndWait()
    elif word == 'stop':
        myText = 'Stopping the engine'
        engine.say(myText)
        engine.runAndWait()
    elif word == 'forward':
        myText = 'Vroooooom'
        engine.say(myText)
        engine.runAndWait()
    elif word == 'back':
        myText = 'Vroom backwards'
        engine.say(myText)
        engine.runAndWait()
    else:
        myText = 'It did not work'
        engine.say(myText)
        engine.runAndWait()

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
    while(vl53.range < 200):
        GPIO.output(35, False)
        GPIO.output(36,True)
        GPIO.output(37, False)
        GPIO.output(38,True)
    STOPPED()
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

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=960,
    display_height=540,
    framerate=21,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=True"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def face_detect():
    window_title = "Face Detect"
    face_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
    )
    eye_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_eye.xml"
    )
    video_capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret, frame = video_capture.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    roi_gray = gray[y : y + h, x : x + w]
                    roi_color = frame[y : y + h, x : x + w]
                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    print("I c u face \n")
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(
                            roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2
                        )
                        print("I c u eyes \n")
                # Check to see if the user closed the window
                # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
                # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frame)

                else:
                    break
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


with m as audio:
    while True:
        try:
            print('Say something')
            r.adjust_for_ambient_noise(audio)
            a = r.listen(audio)
            print("converting")
            print(r.recognize_google(a))
            line = r.recognize_google(a).lower()
            flag = False
            print(line.split())
            for word in line.split():
                myText = ''
                print(word)
                if (word == 'walle' or word == 'wally' or word == 'wall-e'):
                    flag = True
                elif (word  == 'sleep' and flag == True):
                    flag = False
                    colors(word)
                    commands(word)
                    time.sleep(2)
                    pixels.brightness = 0
                elif (word  == 'hello' and flag == True):
                    flag = False
                    colors(word)
                    commands(word)
                    face_detect()
                elif (word  == 'snack' and flag == True):
                    flag = False
                    colors(word)
                    commands(word)
                elif (word == 'stop' and flag == True):
                    commands(word)
                    flag = False 
                    STOPPED()
                    colors('destruction')
                elif (word == 'back' and flag == True):
                    flag = False
                    commands(word)
                    reverse()
                    time.sleep(4)
                    STOPPED()
                    colors('sad')
                elif (word == 'forward' and flag == True):
                    flag = False
                    commands(word)
                    forward()
                    time.sleep(2)
                    STOPPED()
                    colors('trash')
                else:
                    flag = False
        except sr.UnknownValueError as e:
            continue
            #STOPPED()
            #colors("destruction")
            #time.sleep(5)
            #reverse()
            #time.sleep(5)
            #turnLeft()
            #time.sleep(5)
        #else:
            #forward()
