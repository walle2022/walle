#!/usr/bin/env python3

import time
import board
import neopixel_spi as neopixel

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

while True:
    color = input("Enter emotion:\n")
    if color == "trash":
        for i in range(NUM_PIXELS):
            pixels[i] = trash
        pixels.show()
    elif color=="happy":
        for i in range(NUM_PIXELS):
            pixels[i] = happy
        pixels.show()
    elif color=="sad":
        for i in range(NUM_PIXELS):
            pixels[i] = sad
        pixels.show()
    elif color=="love":
        for i in range(NUM_PIXELS):
            pixels[i] = love
        pixels.show()
    elif color=="snack":
        for i in range(NUM_PIXELS):
            pixels[i] = snack
        pixels.show()
    elif color=="destruction":
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
        break

