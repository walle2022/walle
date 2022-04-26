#!/usr/bin/env python3

import pyttsx3
import time
import speech_recognition as sr

engine = pyttsx3.init()
r = sr.Recognizer()
r.energy_threshold = 300
new_vol = input("Enter a volume: ")
new_vol = float(new_vol)
engine.setProperty("volume", new_vol)
engine.say('Hello. My name is Wall-E')
engine.runAndWait()
