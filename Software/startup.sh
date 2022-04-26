#!/bin/sh
#Startup script that will run everytime WALL-E is connected to power and will run automatically without needing a keyboard or hdmi input
sudo modprobe spidev
cd Documents
./walle.py
