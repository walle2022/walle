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
        
