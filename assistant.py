import speech_recognition as sr
import pyttsx3
import requests
import datetime
import pytz

# Function to speak the output
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to fetch weather details
def get_weather(city):
    api_key = "31895d271571d8b36da9d91f08d14d86"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city} is {weather} with a temperature of {temp} °C."
    else:
        return "Sorry, I couldn't fetch the weather."

# Function to fetch news
def get_news(topic=None):
    api_key_news = "c83dc0a09cf6440d914b14f4eb9a2528"
    url_news = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key_news}" if topic else f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key_news}"
    response = requests.get(url_news)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        headlines = [article['title'] for article in articles[:5]]
        if headlines:
            return headlines
        else:
            return ["No relevant news articles found."]
    else:
        return None

# Function to get current time based on the time zone
def get_time(timezone):
    common_timezones = {
        "indian standard time": "Asia/Kolkata",
        "eastern standard time": "US/Eastern",
        "central standard time": "US/Central",
        "pacific standard time": "US/Pacific",
        "greenwich mean time": "GMT",
    }

    normalized_timezone = timezone.lower().strip()
    tz_name = common_timezones.get(normalized_timezone, normalized_timezone)

    try:
        tz = pytz.timezone(tz_name)
        current_time = datetime.datetime.now(tz).strftime("%I:%M %p")
        return f"The current time in {tz_name} is {current_time}."
    except pytz.UnknownTimeZoneError:
        return f"Invalid time zone '{timezone}'. Please provide a valid time zone, like 'Asia/Kolkata' or 'US/Eastern'."

# Function to set reminders
def set_reminder(task, time):
    return f"Reminder set for {task} at {time}."

# Main voice assistant function
def voice_assistant():
    recognizer = sr.Recognizer()
    print("Assistant: Hello! I'm your personal assistant. How can I help you today?")
    speak("Hello! I'm your personal assistant. How can I help you today?")

    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = recognizer.recognize_google(audio, language="en-US").lower()
                print("You:", text)
            except sr.UnknownValueError:
                print("Assistant: Sorry, I did not understand that.")
                speak("Sorry, I did not understand that.")
                continue
            except sr.RequestError:
                print("Assistant: Sorry, I'm having trouble connecting to the service.")
                speak("Sorry, I'm having trouble connecting to the service.")
                continue

            if "weather" in text:
                print("Assistant: Please specify a city.")
                speak("Please specify a city.")
                try:
                    city_audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    city = recognizer.recognize_google(city_audio, language="en-US").lower()
                    weather_info = get_weather(city)
                    print(f"Assistant: {weather_info}")
                    speak(weather_info)
                except:
                    print("Assistant: I couldn't understand the city name.")
                    speak("I couldn't understand the city name.")

            elif "news" in text:
                print("Assistant: What topic would you like to hear about?")
                speak("What topic would you like to hear about?")
                try:
                    topic_audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    topic = recognizer.recognize_google(topic_audio, language="en-US").lower()
                    headlines = get_news(topic)
                    print(f"Assistant: Here are the top news articles about {topic}:")
                    speak(f"Here are the top news articles about {topic}:")
                    for i, headline in enumerate(headlines, 1):
                        print(f"{i}. {headline}")
                        speak(headline)
                except:
                    print("Assistant: Sorry, I couldn't understand the topic.")
                    speak("Sorry, I couldn't understand the topic.")

            elif "time" in text:
                print("Assistant: Please specify a time zone.")
                speak("Please specify a time zone.")
                try:
                    tz_audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    timezone = recognizer.recognize_google(tz_audio, language="en-US").lower()
                    current_time = get_time(timezone)
                    print(f"Assistant: {current_time}")
                    speak(current_time)
                except:
                    print("Assistant: I couldn't understand the time zone.")
                    speak("I couldn't understand the time zone.")

            elif "reminder" in text:
                print("Assistant: What would you like to set a reminder for?")
                speak("What would you like to set a reminder for?")
                try:
                    task_audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    task = recognizer.recognize_google(task_audio, language="en-US").lower()
                    print("Assistant: At what time?")
                    speak("At what time?")
                    time_audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    time = recognizer.recognize_google(time_audio, language="en-US").lower()
                    reminder = set_reminder(task, time)
                    print(f"Assistant: {reminder}")
                    speak(reminder)
                except:
                    print("Assistant: Sorry, I couldn't set the reminder.")
                    speak("Sorry, I couldn't set the reminder.")

            elif "exit" in text or "quit" in text or "bye" in text:
                print("Assistant: Goodbye!")
                speak("Goodbye!")
                break

            else:
                print("Assistant: I'm not sure how to help with that.")
                speak("I'm not sure how to help with that.")

if __name__ == "__main__":
    voice_assistant()
