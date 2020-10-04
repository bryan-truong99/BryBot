import speech_recognition as sr
import time

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
        return query
    except:
        print("Oops! Didn't catch that")


def start_recognizer():
    print("Listening...")
    r.listen_in_background(source, callback)
    time.sleep(1000000)

start_recognizer()
