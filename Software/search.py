#!/usr/bin/env python3
#This is the implementation of the search feature that uses both Wikipedia and WolframAlpha in order to compute both simple and 
#complex math questions as well as searching wikipedia for general knowledge

import speech_recognition as sr
import time
import sys
import wolframalpha
import wikipedia
import pyttsx3

engine = pyttsx3.init()

def SpeakText(command):
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

r = sr.Recognizer()
r.energy_threshold = 300
m = sr.Microphone()

with m as audio:
    while True:
        try:
            print('Say something')
            r.adjust_for_ambient_noise(audio)
            a = r.listen(audio)
            print("Converting")
            speech = r.recognize_google(a)
            print(speech)
            r.energy_threshold = 60
            search(speech)
            r.energy_threshold = 3500
        except:
            print('error')
