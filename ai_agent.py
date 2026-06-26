import speech_recognition as sr
import pyttsx3
import os
from google import genai
client = genai.Client()

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("User:", text)
        return text
    except:
        return None
def ask_ai(prompt):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={'system_instruction': "You are an AI hiring assistant."}
        )
        return response.text
    except Exception as e:
        return f"Error connecting to Gemini: {str(e)}"

speak("AI Agent started")

while True:
    text = listen()₹

    if text is None:
        speak("Sorry, I didn't hear you")
        continue

    if "exit" in text.lower():
        speak("Goodbye")
        break

    reply = ask_ai(text)
    speak(reply)



