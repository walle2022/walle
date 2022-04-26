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
import wolframalpha
import wikipedia

r = sr.Recognizer()
m = sr.Microphone()
r.energy_threshold = 50

GPIO.cleanup()

engine = pyttsx3.init()
#voices = engine.getProperty('voices')
engine.setProperty('rate', 150)
engine.setProperty('voice', 'english+m1')
engine.setProperty('volume', .5) 

#Initialize and set up motors
GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.OUT)        # Purple Wire
GPIO.setup(36, GPIO.OUT)        # Green Wire
GPIO.setup(37, GPIO.OUT)        # Purple Wire
GPIO.setup(38, GPIO.OUT)        # Green Wire

# Initialize I2C bus and sensor. Pin 3(SDA) and 5(SCL)
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

#Initialize NeoPixels
NUM_PIXELS = 24
PIXEL_ORDER = neopixel.GRB
happy = 0xf2a900
sad = 0x0047ab
love = 0x9f2b68
snack = 0xcc5500
destruction = [0x8b0000, 0xf2a900, 0x71b2c9, 0xd7a3ab]
startup = 0x00ff00
run = 0xffffff
blank = 0x000000

spi = board.SPI()

pixels = neopixel.NeoPixel_SPI(
    spi, NUM_PIXELS, pixel_order=PIXEL_ORDER, auto_write=False
)

pixels.brightness = 0.1

#Initialize Servos For Eyes
# Pin 32 = Left Eye  (Purple wire)
# Pin 33 = Right Eye (Green wire)

GPIO.setup(32, GPIO.OUT)        # Purple Wire
GPIO.setup(33, GPIO.OUT)        # Green Wire
left = GPIO.PWM(32,34)
right = GPIO.PWM(33,34)
left.start(0)
right.start(0)

def SpeakText(command): 
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', 'english+m1')
    engine.say(command)
    engine.runAndWait()

def search(query):
    try:
        app_id = '46QGX6-4H8RAEWTGT'
        client = wolframalpha.Client(app_id)
        res = client.query(query)
        answer = next(res.results).text
        print(answer)
        SpeakText('Your answer is ' + answer)

    except:
        query = query.split(' ')
        query = ' '.join(query[0:])

        SpeakText('I am searching for ' + query)
        print(wikipedia.summary(query, sentences = 3))
        SpeakText(wikipedia.summary(query, sentences = 3))

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


def colors(color):
    if color == "startUp":
        for i in range(NUM_PIXELS):
            pixels[i] = startup
        pixels.show()
    elif color == "command":
        for i in range(2):
            for i in range(NUM_PIXELS):
                pixels[i] = run
                pixels.show()
                pixels[i] = blank
                pixels.show()
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
    elif color=='forward':
        for i in range(NUM_PIXELS):
            pixels[i] = run
        pixels.show()
    elif color == 'search':
        for j in range(3):
            for i in range(NUM_PIXELS):
                pixels[i] = sad
            pixels.show()
            time.sleep(0.1)
            for k in range(NUM_PIXELS):
                pixels[k] = 0x000000
            pixels.show()
            time.sleep(0.1)
            #pixels.brightness += 0.3
        for m in range(NUM_PIXELS):
            pixels[m] = sad
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
        myText = 'Hi friend. My name is Wall-E. Whats your name?'
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
    elif word == 'startup': 
        myText = 'Starting Up' 
        engine.say(myText)
        engine.runAndWait()
    elif word == 'greet': 
        myText = 'Hello, my name is Wall-E.'
        engine.say(myText)
        engine.runAndWait()
    elif word == 'search':
        myText = 'Ok. What would you like me to search?'
        engine.say(myText)
        engine.runAndWait()
    elif word == 'volume':
        myText = 'Ok. Please give me a number between 1 and 10.'
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

def volume(new_vol):
    vol = float(new_vol)
    vol = vol/10
    engine.setProperty("volume", vol)
    engine.say("Ok. Volume set to " + str(new_vol))
    engine.runAndWait()

with m as audio:
    print("Starting Up")
    colors('startUp')
    commands('startup')
    rightEye()
    leftEye()
    bothEyes()
    commands('greet')
    vol_flag = False 
    in_flag = False 
    while True:
        try:
            print('Say something')
            colors('command')
            r.adjust_for_ambient_noise(audio)
            a = r.listen(audio)
            print("converting")
            print(r.recognize_google(a))
            colors('run')
            if (vol_flag == True): 
                a = ''
                line = '' 
                vol_flag = False 
                in_flag = True
            else: 
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
                elif (word == 'volume' and flag == True):
                    flag = False
                    commands(word)
                    vol_flag = True
                elif((word == '1' or word == '2' or word == '3' or word == '4' or word == '5' or word == '6' or word == '7' or word == '8' or word == '9' or word == '10')  and in_flag == True):
                    in_flag = False
                    volume(word)
                elif (word  == 'hello' and flag == True):
                    flag = False
                    colors(word)
                    commands(word)
                    #face_detect()
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
                    colors(word)
                    forward()
                    time.sleep(2)
                    STOPPED()
                elif (word == 'search' and flag == True):
                    flag = False
                    #commands(word)
                    #time.sleep(3)
                    colors(word)
                    r.adjust_for_ambient_noise(audio)
                    a = r.listen(audio)
                    print("converting")
                    speech = r.recognize_google(a)
                    search(speech)
                else:
                    flag = False
        except sr.UnknownValueError as e:
            continue
