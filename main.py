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
from playsound import playsound
import pyglet
import time

user = "Bryan"

# Setting up text-to-speech voice and speaking rate
engine = pyttsx3.init()
voices = engine.getProperty("voices")
rate = engine.getProperty("rate")

engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 200)

# Converts text to speech and reads aloud the text put into the function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Greets user based on the time of the day
def greeting():
    hour = int(datetime.datetime.now().hour)

    if hour > 0 and hour < 12:
        speak("Good Morning" + user)
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon" + user)
    else:
        speak("Good Evening" + user)

    speak("How may I help you today?")

def command():
    query = None
    #Adjust threshold for speech so it does not recognize background noise
    r = sr.Recognizer()
    r.energy_threshold = 400
    r.dynamic_energy_threshold = False
    # Words that sphinx should listen closely for. 0-1 is the sensitivity
    # of the wake word.
    keywords = [("google", 1), ("hey google", 1), ]

    source = sr.Microphone()


    def callback(recognizer, audio):  # this is called from the background thread
        print("Hi")
        try:
            speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords)
            print(f"user said: {speech_as_text}")

            # Look for your "Ok Google" keyword in speech_as_text
            if "google" in speech_as_text or "hey google":
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
            startWario(query)

        except:
            print("Oops! Didn't catch that")


    def start_recognizer():
        print("Listening...")
        r.listen_in_background(source, callback)
        time.sleep(1000000)

    start_recognizer()
    

#If I want to send emails use this function
def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("myemail@gmail.com", "password")
    server.sendmail("email@gmail.com")
    server.close

#Searches youtube and opens the first result
def searchYT(text):
    words = text.split()
    url = "http://www.youtube.com/results?search_query=" + "+".join(words)
    search_result = requests.get(url).text
    soup = BeautifulSoup(search_result, "html.parser")
    videos = soup.select(".ytd-video-renderer")
    if not videos:
        raise KeyError("No video found")
    link = "https://www.youtube.com" + videos[0]["href"]

    webbrowser.open_new(link)

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

def startWario(query):

    #Variables for the pathnames of the different sound effects
    wario_greeting = os.path.join(local_dir,"sounds\\WELCOME_TO_WARIO_WORLD(Stereo).wav")
    wario_fine = os.path.join(local_dir,"sounds\\FINE.wav")
    wario_oh_kay = os.path.join(local_dir,"sounds\\Oh-KAY(Stereo).wav")

    #Where the audio portion begins
    #playsound(wario_greeting)
    greeting()

    if "wikipedia" in query.lower():
        playsound(wario_fine)
        speak("Searching Wikipedia...")
        query = query.lower().replace("wikipedia","")
        results = wikipedia.summary(query, sentences = 3)
        speak(results)

    elif "youtube" in query.lower():

        query = query.lower().replace("youtube","")
        searchYT(query)

    elif "open google" in query.lower():
        webbrowser.open("google.com")

    elif "play music" in query.lower():
        song_dir= "C:\\Users\\bryan\\Music".encode("utf-8")
        songs = os.listdir(song_dir)
        os.startfile(os.path.join(song_dir,songs[1]))

    elif "whole lotta red" in query.lower():
        webbrowser.open("https://www.youtube.com/watch?v=jEkmWm08-Ho&list=PLkL41eK4K0zmPE2hRDhahHwmWmHEeedRn")

    elif "epic" in query.lower():
        playsound(wario_oh_kay)
        webbrowser.open("https://www.youtube.com/watch?v=dGJlZw4FYgE")

    elif "the time" in query.lower():
        time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"{user}, the time is {time}")

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

if __name__ == "__main__":
    #Need to use threading
    local_dir = os.path.dirname(__file__)
    #displayGIF(local_dir)
    command()
