#!/usr/bin/env python3

import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import os
import datetime
import time
import adafruit_tca9548a

# Define the Reset Pin
#oled_reset = digitalio.DigitalInOut(board.D4)

# Change these to the right size for your display!
WIDTH = 128
HEIGHT = 32  # Change to 64 if needed
BORDER = 5

# Use for I2C.
i2c = busio.I2C(board.SCL, board.SDA)
#tca = adafruit_tca9548a.TCA9548A(i2c)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)
#, reset=oled_reset)

#spi = busio.SPI(board.SCK, MOSI=board.MOSI)
#reset_pin = digitalio.DigitalInOut(board.D4) # any pin!
#cs_pin = digitalio.DigitalInOut(board.D5)    # any pin!
#dc_pin = digitalio.DigitalInOut(board.D6)    # any pin!

#oled = adafruit_ssd1306.SSD1306_SPI(128, 32, spi, dc_pin, reset_pin, cs_pin)

# Use for SPI
#spi = board.SPI()
#oled_cs = board.D5
#oled_dc = board.D6
#display_bus = displayio.FourWire(spi, command=oled_dc, chip_select=oled_cs,reset=oled_reset, baudrate= 1000000)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
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
#text = "Hello World!"
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
print('oled')
oled.image(image)
oled.show()

