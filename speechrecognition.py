
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import requests
import smtplib
import time
import spacy


engine = pyttsx3.init()
recognizer = sr.Recognizer()
nlp = spacy.load("en_core_web_sm")

# SPEAK FUNCTION

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# LISTEN FUNCTION

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except:
        speak("Sorry, I did not understand.")
        return ""

# NLP INTENT DETECTION


def get_intent(text):
    doc = nlp(text)
    for token in doc:
        if token.lemma_ in ["time", "date", "weather", "email", "remind", "search"]:
            return token.lemma_
    return "unknown"

# WEATHER FUNCTION


def get_weather(city):
    API_KEY = "YOUR_OPENWEATHER_API_KEY"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    data = requests.get(url).json()

    if data.get("main"):
        temp = data["main"]["temp"] - 273.15
        return f"The temperature in {city} is {round(temp)} degrees Celsius."
    else:
        return "Sorry, I could not find the weather."

# EMAIL FUNCTION

def send_email(to_email, message):
    sender_email = "your_email@gmail.com"
    password = "your_app_password"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, to_email, message)
    server.quit()

    speak("Email sent successfully.")

# REMINDER FUNCTION


def set_reminder(seconds, message):
    speak("Reminder set.")
    time.sleep(seconds)
    speak(message)

# CUSTOM COMMANDS

custom_commands = {
    "open youtube": "https://youtube.com",
    "open google": "https://google.com",
    "open github": "https://github.com"
}


# MAIN ASSISTANT LOOP

def run_assistant():
    speak("Hello! I am your Python voice assistant.")

    while True:
        command = listen()

        if "hello" in command:
            speak("Hello! How can I help you?")

        elif "time" in command:
            time_now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {time_now}")

        elif "date" in command:
            date_today = datetime.date.today()
            speak(f"Today's date is {date_today}")

        elif "search" in command:
            speak("What should I search?")
            query = listen()
            webbrowser.open(f"https://www.google.com/search?q={query}")

        elif "wikipedia" in command:
            topic = command.replace("wikipedia", "")
            result = wikipedia.summary(topic, sentences=2)
            speak(result)

        elif "weather" in command:
            speak("Which city?")
            city = listen()
            weather = get_weather(city)
            speak(weather)

        elif "send email" in command:
            speak("Tell me the message.")
            message = listen()
            send_email("receiver_email@gmail.com", message)

        elif "remind me" in command:
            speak("In how many seconds?")
            seconds = int(listen())
            speak("What should I remind you?")
            reminder = listen()
            set_reminder(seconds, reminder)

        elif command in custom_commands:
            webbrowser.open(custom_commands[command])
            speak(f"Opening {command}")

        elif "exit" in command or "stop" in command:
            speak("Goodbye! Have a great day.")
            break

        else:
            speak("I am not sure how to help with that.")


run_assistant()

