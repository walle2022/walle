#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import board 
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import datetime
from datetime import date
import adafruit_vl53l0x
import adafruit_tca9548a
import neopixel_spi as neopixel
import os
import speech_recognition as sr
import sys
import pyttsx3
import wolframalpha
import wikipedia
from adafruit_servokit import ServoKit
import adafruit_motor.servo
import adafruit_pca9685

r = sr.Recognizer()
m = sr.Microphone()
r.energy_threshold = 50

GPIO.cleanup()

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', 'english+m1')
engine.setProperty('volume', .5) 

#Initialize and set up motors
GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.OUT)        # Purple Wire
GPIO.setup(36, GPIO.OUT)        # Green Wire
GPIO.setup(37, GPIO.OUT)        # Purple Wire
GPIO.setup(38, GPIO.OUT)        # Green Wire

# Initialize I2C bus and sensor for ToF sensors. Pin 27(SDA) and 28(SCL)
i2c = busio.I2C(board.SCL, board.SDA)
tca = adafruit_tca9548a.TCA9548A(i2c, address = 0x71)
vl530 = adafruit_vl53l0x.VL53L0X(tca[0]) #edge detection
#vl531 = adafruit_vl53l0x.VL53L0X(tca[3]) #object detection

#Initialize I2C for PWM Servos
i2c1 = busio.I2C(board.SCL_1, board.SDA_1)
kit = ServoKit(channels=16, i2c=i2c1)
leftArm = kit.servo[6]
rightArm = kit.servo[7]
#leftEye = kit.servo[8]
#rightEye = kit.servo[9]

#Initialize NeoPixels
NUM_PIXELS = 24
PIXEL_ORDER = neopixel.GRB
happy = 0xf2a900
sad = 0x0047ab
love = 0x9f2b68
snack = 0xcc5500
destruction = [0x8b0000, 0xf2a900, 0x71b2c9, 0xd7a3ab]
dancey = 0xf2a900
time_date = 0x71b2c9
startup = 0x00ff00
run = 0xffffff
blank = 0x000000

spi = board.SPI()
pixels = neopixel.NeoPixel_SPI(
    spi, NUM_PIXELS, pixel_order=PIXEL_ORDER, auto_write=False
)

pixels.brightness = 0.1

def SpeakText(command): 
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', 'english+m1')
    engine.say(command)
    engine.runAndWait()
    flag_s = False 

flag_s = False 

def search(query):
    global flag_s 
    try:
        app_id = '46QGX6-4H8RAEWTGT'
        client = wolframalpha.Client(app_id)
        print(flag_s) 
        print('before')
        if flag_s == True:
            print('its true')
            res = client.query('')
        else:
            print('else')
            res = client.query(query)
            answer = next(res.results).text
            print(answer)
            flag_s = True
            SpeakText('Your answer is ' + answer)

    except:
        query = query.split(' ')
        query = ' '.join(query[0:])
        if flag_s == True: 
            query = ''
        else: 
            print('else')
            SpeakText('playing ' + query)
            print(query)
            print(wikipedia.summary(query, sentences = 1)) 
            flag_s = True 
            SpeakText(wikipedia.summary(query, sentences = 1))


def leftEye():
    # moves Left Eye
    print("LEFT Eye called")
    global leftEye
    leftEye.angle = 155
    time.sleep(1)
    leftEye.angle = 120
    time.sleep(1)
    leftEye.angle = 155
    time.sleep(0.3)
    leftEye.angle = 120
    time.sleep(0.3)
    

def rightEye():
    # moves Right Eye
    print("RIGHT Eye called")
    global rightEye
    rightEye.angle = 1
    time.sleep(1)
    rightEye.angle = 45
    time.sleep(1)
    rightEye.angle = 1
    time.sleep(0.3)
    rightEye .angle = 45
    time.sleep(0.3)

def bothEyes():
    # moves Both Eyes
    print("BOTH Eyes called")
    global rightEye
    global leftEye
    rightEye.angle = 1
    leftEye.angle = 155
    time.sleep(1)
    rightEye.angle = 45
    leftEye.angle = 120
    time.sleep(1)
    rightEye.angle = 1
    leftEye.angle = 155
    time.sleep(0.3)
    rightEye.angle = 45
    leftEye.angle = 120
    time.sleep(0.3)

def eyeMovement():
    leftEye = kit.servo[8]
    rightEye = kit.servo[9]
    rightEye.angle = 1
    time.sleep(1)
    rightEye.angle = 45
    time.sleep(1)
    rightEye.angle = 1
    time.sleep(0.3)
    rightEye .angle = 45
    time.sleep(0.3)
    leftEye.angle = 155
    time.sleep(1)
    leftEye.angle = 120
    time.sleep(1)
    leftEye.angle = 155
    time.sleep(0.3)
    leftEye.angle = 120
    time.sleep(0.3)
    rightEye.angle = 1
    leftEye.angle = 155
    time.sleep(1)
    rightEye.angle = 45
    leftEye.angle = 120
    time.sleep(1)
    rightEye.angle = 1
    leftEye.angle = 155
    time.sleep(0.3)
    rightEye.angle = 45
    leftEye.angle = 120
    time.sleep(0.3)
    leftEye.angle = None
    rightEye.angle = None

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
    elif color == 'dance':
        for i in range(NUM_PIXELS):
            pixels[i] = dancey
        pixels.show()
    elif color == 'date':
        for i in range(NUM_PIXELS):
            pixels[i] = time_date
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
    elif word == 'date':
        today = date.today()
        d2 = today.strftime("%B %d, %Y")
        myText = "Today is " + str(d2)
        engine.say(myText)
        engine.runAndWait()
    elif word == 'snack':
        myText = 'Okay. Opening the snack box. Nom Nom.'
        engine.say(myText)
        engine.runAndWait()
    elif word == 'hello':
        myText = 'Hi friend. My name is Wall-E.'
        engine.say(myText)
        engine.runAndWait()
    elif word == 'stop':
        myText = 'Stopping the engine'
        engine.say(myText)
        engine.runAndWait()
    elif word == 'forward':
        myText = 'Ok. Moving forward'
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
        leftArm.angle = 35
        rightArm.angle = 50
        time.sleep(1)
        leftArm.angle = 1
        rightArm.angle = 20
        time.sleep(1)
        leftArm.angle = 35
        rightArm.angle = 50
        time.sleep(1)
        rightArm.angle = 20
        leftArm.angle = 1
        time.sleep(1)
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
    while(vl530.range < 350): # and vl531.range > 200):
        forward()
    STOPPED()
    time.sleep(2)
    '''
    while(vl531.range <= 200): #object Detection
        colors('destruction')
        turnLeft()
        time.sleep(3)
        turnRight()
        time.sleep(2)
        forward()
    STOPPED()
    '''
    while(vl530.range >= 350): #edge detection
        colors('destruction')
        reverse()
        time.sleep(6)
        turnLeft()
        time.sleep(0.4)
        forward()
        time.sleep(1)
    STOPPED()

def volume(new_vol):
    vol = float(new_vol)
    vol = vol/10
    engine.setProperty("volume", vol)
    engine.say("Ok. Volume set to " + str(new_vol))
    engine.runAndWait()

def oled(num):
    # Change these to the right size for your display!
    WIDTH = 128
    HEIGHT = 32  # Change to 64 if needed
    BORDER = 5
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
    # Clear display.
    oled.fill(0)
    oled.show()
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    if num == 1:
        image = Image.new("1", (oled.width, oled.height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
    # Draw a white background
        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
    # Draw a smaller inner rectangle
        draw.rectangle(
            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
            outline=0,
            fill=0,
        )   
    # Load default font.
        font = ImageFont.load_default()
    # Draw Some Text
        text = datetime.datetime.now()
        text = text.strftime("%m/%d/%Y %H:%M")
        (font_width, font_height) = font.getsize(text)
        draw.text(
            (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
            text,
            font=font,
            fill=255,
        )
    # Display image
        oled.image(image)
        oled.show()
    else:
        image = Image.new("1", (oled.width, oled.height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
    # Draw a white background
        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
    # Draw a smaller inner rectangle
        draw.rectangle(
            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
            outline=0,
            fill=0,
        )
    # Load default font.
        font = ImageFont.load_default()
    # Draw Some Text
        text = 'converting'
        (font_width, font_height) = font.getsize(text)
        draw.text(
            (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
            text,
            font=font,
            fill=255,
        )
    # Display image
        oled.image(image)
        oled.show()


def dance():
    colors("dance")
    count = 0
    while count<3:
        turnLeft()
        leftArm.angle = 35
        rightArm.angle = 50
        time.sleep(0.4)
        turnRight()
        leftArm.angle = 1
        rightArm.angle = 20
        time.sleep(0.4)
        reverseLeft()
        leftArm.angle = 35
        rightArm.angle = 50
        time.sleep(0.4)
        reverseRight()
        leftArm.angle = 1
        rightArm.angle = 20
        time.sleep(0.4)
        STOPPED()
        leftArm.angle = None
        rightArm.angle = None
        count+=1

#with m as audio:
print("Starting Up")
colors('startUp')
#commands('startup')
eyeMovement()
dance()
commands('date')
    #commands('greet')
vol_flag = False 
in_flag = False 
with m as audio:
    while True:
        oled(1)
        try:
            print('Say something')
            colors('command')
            r.adjust_for_ambient_noise(audio)
            a = r.listen(audio)
            print("converting")
            oled(0)
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
                elif ((word == 'date' or word == 'day') and flag == True):
                    flag = False
                    colors('date')
                    commands('date')
                elif (word  == 'sleep' and flag == True):
                    flag = False
                    colors(word)
                    commands(word)
                    time.sleep(2)
                    pixels.brightness = 0
                elif (word == 'dance' and flag == True):
                    flag = False
                    dance()
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
                    turnLeft()
                    time.sleep(4)
                    reverseRight()
                    time.sleep(4)
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
                    #forward()
                    detection()
                    time.sleep(2)
                    STOPPED()
                elif (word == 'search' and flag == True):
                    flag = False
                    commands(word)
                    time.sleep(3)
                    colors(word)
                    r.adjust_for_ambient_noise(audio)
                    a = r.listen(audio)
                    print("converting")
                    oled(0)
                    speech = r.recognize_google(a)
                    search(speech)
                else:
                    flag = False
        except sr.UnknownValueError as e:
            continue
