# This is CartoonAI A personal Assistant with OpenAI
import datetime
import os
import webbrowser
import pyttsx3
import requests
import speech_recognition as sr
import openai
import json
from config import OpenAIapikey, weatherAPIkey, NewsApikey


# Function For getting temperature from weather API
def temperature(query):
    city = query.split()[-1]
    url = f"http://api.weatherapi.com/v1/current.json?key={weatherAPIkey}&q={city}"
    try:
        r = requests.get(url)
        weather_dict = json.loads(r.text)
        curr_temp = weather_dict["current"]["temp_c"]
        say(f"The current temperature of {city} is {curr_temp}")
        print(f"The current temperature of {city} is {curr_temp}")

    except Exception as e:
        say("Some error Occurred...")
        print("Some error Occurred...", e)


# Function declaration for OPENAI
def ai(prompt):
    openai.api_key = OpenAIapikey
    text = f"OpenAI response For : {prompt} \n\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="prompt",
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        print(response["choices"][0]["text"])
        text += response["choices"][0]["text"]
        if not os.path.exists("OpenAI_Files"):
            os.mkdir("OpenAI_Files")
        with open(f"OpenAI_Files/{''.join(prompt.split('openai')[1:]) }.txt", "w") as f:
            f.write(text)

    except Exception as e:
        print("Some error Occurred", e)


# Say Function for Speech of Cartoon
def say(text):
    engine = pyttsx3.init()
    engine.say(f"{text}")
    print(f"{text}")
    engine.runAndWait()
    engine.stop()


# Function for taking Command from Microphone
def takeCommand():
    r = sr.Recognizer()
    # device_index = 30
    with sr.Microphone() as source:

        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said : {query}")
            return query
        except Exception as e:
            print("Error : ", e)
            return f"Some error Occurred, please say it again"


chatStr = ""


def chat(query):
    global chatStr
    openai.api_key = OpenAIapikey
    chatStr = f"You : {query} \n Cartoon : "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="prompt",
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        say(response["choices"][0]["text"])
        chatStr += f"{response['choices'][0]['text']}\n "
        with open("Chat.txt", "a") as f:
            f.write(chatStr)
        return response["choices"][0]["text"]
    except Exception as e:
        say("Some error Occurred")
        return e


if __name__ == '__main__':
    text = 'Hello..! I am Cartoon AI'
    say(text)
    text = "Say something"
    say(text)
    while True:
        query = takeCommand()
        x = query.split()[1]
        # print(x)
        # say(query)

        # For opening website
        if f"Open {x}".lower() in query.lower():

            say(f"Opening {x}")
            webbrowser.open(f"https://{x}.com")

        # To open Music from Path
        elif "open music" in query:
            '''Add Music path Here'''
            musicpath = ""
            os.system(f"open {musicpath}")

        # For the date and time
        elif "the time" in query:
            curr_time = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {curr_time}")

        # For using OPENAI
        elif "Using openai".lower() in query.lower():
            ai(prompt=query)

        # For weather Update
        elif "current temperature of".lower() in query.lower():
            temperature(query)

        # To exit CARTOON AI
        elif "Cartoon Quit".lower() in query.lower():
            exit()

        # To RESET the CHAT to BLANK
        elif "reset chat".lower() in query.lower():
            chatStr = ""

        # For the TALKBACK functionality
        else:
            print("Talking...")
            chat(query)


# todo: integrating yfinance api
# todo: integrating News api
