#This will be implemented on a Raspberry Pi
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import pyglet
import time
import threading
from urllib.request import urlopen
import re
import sys
from playsound import playsound
import google.generativeai as genai

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

        for i, voice in enumerate(self.voices):
            print(f"Voice {i}:")
            print(f" - ID: {voice.id}")
            print(f" - Name: {voice.name}")
            print(f" - Languages: {voice.languages}")
            print(f" - Gender: {voice.gender}")
            print(f" - Age: {voice.age}")
            print()


        self.rate = self.engine.getProperty("rate")
        self.engine.setProperty("voice", self.voices[1].id)
        self.engine.setProperty("rate", 200)

    # Converts text to speech and reads aloud the text put into the function
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

class Brybot():

    def __init__(self):
        self.tts = TTS()

        genai.configure(api_key=os.environ["API_KEY"])
        self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")

    #Greets user based on the time of the day
    def greeting(self):
        hour = int(datetime.datetime.now().hour)

        if 0 < hour < 12:
            self.tts.speak("Good Morning" + user)
        elif 12 <= hour < 18:
            self.tts.speak("Good Afternoon" + user)
        else:
            self.tts.speak("Good Evening" + user)

        self.tts.speak("How may I help you today?")

    #Searches youtube and opens the first result
    #WIP
    def search_yt(self, text):
        search_keyword = text.replace(" ", "+")
        html = urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        link = "https://www.youtube.com/watch?v=" + video_ids[0]

        webbrowser.open_new(link)

    #Setting up pyglet window to display and play T-MO gif
    def display_gif(self, local_dir):
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

    def gemini_response(self, query):
        response = self.gemini_model.generate_content(query)

        return response.text

    def start_bry_bot(self, query):
        lower_query = query.lower()

        if "youtube" in lower_query:
            self.tts.speak("On it")
            query = query.lower().replace("youtube","")
            self.search_yt(query)

        elif "play music" in lower_query:
            song_dir= "C:\\Users\\bryan\\Music".encode("utf-8")
            songs = os.listdir(song_dir)
            os.startfile(os.path.join(song_dir,songs[1]))

        elif "epic" in lower_query:
            self.tts.speak("Hell Yeah!")
            webbrowser.open("https://www.youtube.com/watch?v=dGJlZw4FYgE")

        elif "the time" in lower_query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.tts.speak(f"{user}, the time is {current_time}")

        elif "play games" in lower_query:
            os.system("emulationstation")
            sys.exit(0)

        elif "thank you" in lower_query:
            self.tts.speak("You're welcome" + user)

        elif "close windows" in query.lower():
            os.system("taskkill /im chrome.exe /f")

        elif "turn off" in lower_query:
            self.tts.speak("Goodbye" + user)
            os.system("shutdown /s /t 1")

        else:
            self.tts.speak(self.gemini_response(lower_query))


#Continuous speech recognition using sphinx and google api
def command(brybot):
    query = None
    #Adjust threshold for speech so it does not recognize background noise
    r = sr.Recognizer()
    r.energy_threshold = 400
    r.dynamic_energy_threshold = False
    # Words that sphinx should listen closely for. 0-1 is the sensitivity
    # of the wake word.
    keywords = [("bob", 1), ("hey bob", 1), ]

    source = sr.Microphone()

    def callback(recognizer, audio):  # this is called from the background thread
        try:
            speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords)
            print(f"user said: {speech_as_text}")

            # Look for your "Ok Google" keyword in speech_as_text
            if "bob" in speech_as_text or "hey bob":
                brybot.greeting()
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
            brybot.startbryBot(query)

        except:
            print("Oops! Didn't catch that")


    def start_recognizer():
        print("Listening...")
        r.listen_in_background(source, callback)
        time.sleep(1000000)

    start_recognizer()

if __name__ == "__main__":
    # local_dir = os.path.dirname(__file__)
    # playsound(os.path.join(local_dir,"sounds\\pokemon-red_blue_yellow-item-found-sound-effect.mp3"))
    # #Use threading to execute both functions
    # x = threading.Thread(target=displayGIF, args=(local_dir,),daemon=True)
    # y = threading.Thread(target=command, args=())
    #
    # x.start()
    # y.start()
    brybot = Brybot()
    command(brybot)