#This will be implemented on a Raspberry Pi
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
from bs4 import BeautifulSoup
import pyglet
import time
import threading
from urllib.request import urlopen
import re
import sys
from playsound import playsound

user = "Bryan"

#Text to speech class utilized in order to get around the hang time that it has by default
class TTS():
    # Setting up text-to-speech voice and speaking rate
    engine = None
    voices = None
    rate = None

    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty("voices")
        self.rate = self.engine.getProperty("rate")
        self.engine.setProperty("voice", self.voices[1].id)
        self.engine.setProperty("rate", 200)
    # Converts text to speech and reads aloud the text put into the function
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

###########################################
#Greets user based on the time of the day
def greeting():
    tts = TTS()
    hour = int(datetime.datetime.now().hour)

    if hour > 0 and hour < 12:
        tts.speak("Good Morning" + user)
    elif hour >= 12 and hour < 18:
        tts.speak("Good Afternoon" + user)
    else:
        tts.speak("Good Evening" + user)

    tts.speak("How may I help you today?")
    del(tts)

#If I want to send emails use this function
def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("myemail@gmail.com", "password")
    server.sendmail("email@gmail.com")
    server.close

#Searches youtube and opens the first result
#WIP
def searchYT(text):
    search_keyword = text.replace(" ", "+")
    html = urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    link = "https://www.youtube.com/watch?v=" + video_ids[0]

    webbrowser.open_new(link)

def searchGoogle(text):
    search_keyword = text.replace(" ","+")
    webbrowser.open("https://www.google.com/search?q=" + search_keyword)

#Setting up pyglet window to display and play T-MO gif
def displayGIF(local_dir):
    tmo_gif = os.path.join(local_dir,"images\\T-MO.gif")
    ani = pyglet.image.load_animation(tmo_gif)
    aniSprite = pyglet.sprite.Sprite(ani)

    w = aniSprite.width
    h = aniSprite.height

    window = pyglet.window.Window(width=w, height=h)

    r,g,b,alpha = 0.5, 0.5, 0.8, 0.5

    pyglet.gl.glClearColor(r,g,b,alpha)

    @window.event
    def on_draw():
        window.clear()
        aniSprite.draw()

    pyglet.app.run()

def startBryBot(query):

    text_speech = TTS()

    #Where the audio portion begins

    if "wikipedia" in query.lower():
        # playsound(wario_fine)
        text_speech.speak("Searching Wikipedia...")
        query = query.lower().replace("wikipedia","")
        results = wikipedia.summary(query, sentences = 3)
        text_speech.speak(results)

    elif "youtube" in query.lower():
        text_speech.speak("On it")
        query = query.lower().replace("youtube","")
        searchYT(query)

    elif "google" in query.lower():
        text_speech.speak("I got you, homie")
        query = query.lower().replace("google","")
        searchGoogle(query)

    elif "play music" in query.lower():
        song_dir= "C:\\Users\\bryan\\Music".encode("utf-8")
        songs = os.listdir(song_dir)
        os.startfile(os.path.join(song_dir,songs[1]))

    elif "epic" in query.lower():
        text_speech.speak("Hell Yeah!")
        webbrowser.open("https://www.youtube.com/watch?v=dGJlZw4FYgE")

    elif "the time" in query.lower():
        time = datetime.datetime.now().strftime("%H:%M:%S")
        text_speech.speak(f"{user}, the time is {time}")

    elif "send email" in query.lower():
        try:
            speak("Who should I send it to")
            to = command()
            speak("What do you want to send")
            content = command()
            sendEmail(to, content)
            speak("The email has been sent!")

        except Exception as e:
            print(e)

    elif "play games" in query.lower():
        os.system("emulationstation")
        sys.exit(0)

    elif "tell me a joke" in query.lower():
        text_speech.speak("Yo momma")

    elif "song" in query.lower():
        text_speech.speak("")

    elif "thank you" in query.lower():
        text_speech.speak("You're welcome" + user)
    elif "close windows" in query.lower():
        os.system("taskkill /im chrome.exe /f")

    elif "turn off" in query.lower():
        text_speech.speak("Goodbye" + user)
        os.system("shutdown /s /t 1")

    del(text_speech)


#Continuous speech recognition using sphinx and google api
def command():
    query = None
    #Adjust threshold for speech so it does not recognize background noise
    r = sr.Recognizer()
    r.energy_threshold = 400
    r.dynamic_energy_threshold = False
    # Words that sphinx should listen closely for. 0-1 is the sensitivity
    # of the wake word.
    keywords = [("senna", 1), ("hey senna", 1), ]

    source = sr.Microphone()

    def callback(recognizer, audio):  # this is called from the background thread
        print("Hi")
        try:
            speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords)
            print(f"user said: {speech_as_text}")

            # Look for your "Ok Google" keyword in speech_as_text
            if "google" in speech_as_text or "hey google":
                greeting()
                recognize_main()

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")


    def recognize_main():
        print("Recognizing Main...")
        audio_data = r.listen(source)

        # interpret the user's words however you normally interpret them
        try:
            query = r.recognize_google(audio_data)
            print(f"user said: {query}")
            startBryBot(query)

        except:
            print("Oops! Didn't catch that")


    def start_recognizer():
        print("Listening...")
        r.listen_in_background(source, callback)
        time.sleep(1000000)

    start_recognizer()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    playsound(os.path.join(local_dir,"sounds\\pokemon-red_blue_yellow-item-found-sound-effect.mp3"))
    #Use threading to execute both functions
    x = threading.Thread(target=displayGIF, args=(local_dir,),daemon=True)
    y = threading.Thread(target=command, args=())

    x.start()
    y.start()
