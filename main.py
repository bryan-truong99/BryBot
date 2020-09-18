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

# Listens to microphone and converts command to string
def command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio)
            print(f"user said: {query}")

        except Exception as e:
            speak("Can you repeat that?")
            command()

    return query

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

def startJarvis():
    speak("Initializing Jarvis...")
    greeting()
    query = command()

    if "wikipedia" in query.lower():
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

if __name__ == "__main__":
    startJarvis()
