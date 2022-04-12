#!/usr/bin/env python3
import os
import speech_recognition as sr
import time
import sys
import board 
import neopixel_spi as neopixel

from gtts import gTTS

r = sr.Recognizer()
m = sr.Microphone()
r.energy_threshold = 300

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
        myOutput=gTTS(text=myText,lang='en',slow=False)
        myOutput.save('talk.mp3')
        os.system('mpg123 talk.mp3')
    elif word == 'snack':
        myText = 'Okay. Opening the snack box. Nom Nom.'
        myOutput=gTTS(text=myText,lang='en',slow=False)
        myOutput.save('talk.mp3')
        os.system('mpg123 talk.mp3')
    elif word == 'hello':
        myText = 'Hi friend. My name is Wall-E'
        myOutput=gTTS(text=myText,lang='en',slow=False)
        myOutput.save('talk.mp3')
        os.system('mpg123 talk.mp3')
    else:
        myText = 'It did not work'
        myOutput=gTTS(text=myText,lang='en',slow=False)
        myOutput.save('talk.mp3')
        os.system('mpg123 talk.mp3')

with m as audio: 
    while True:
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
            elif (word  == 'snack' and flag == True):
                flag = False
                colors(word)
                commands(word)
            else:
                flag = False
                #commands(word)
