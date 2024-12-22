import pyttsx3
import random
import time

game_over = False
numList = []

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
newRate = 100
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', newRate)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def welcome():
    speak("Welcome To Tambola")
    time.sleep(5)

def numGenerator():
    for a in range(1,91):
        numList.append(a)

def gameLoop():
    numGenerator()
    random.shuffle(numList)
    x = 0
    while x < 89:
        x += 1
        number = int(numList[x])
        speak(number)
        time.sleep(8)

welcome()
gameLoop()
