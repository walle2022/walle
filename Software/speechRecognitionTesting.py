#!/usr/bin/env python3

import speech_recognition as sr
import time
import sys

r = sr.Recognizer()
r.energy_threshold = 300
m =sr.Microphone()

with m as audio:
    while True:
        print('Say something')
        r.adjust_for_ambient_noise(audio)
        a = r.listen(audio)
        print("converting")
        sys.stdout.write(r.recognize_google(a))
