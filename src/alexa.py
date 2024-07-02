import datetime
import speech_recognition as sr
import pyttsx3
import pywhatkit
import urllib.request
import json
import wikipedia
import openai

name='alexa'
key= 'AIzaSyC6mJjI0G4RVJ0KHWS-HopjiGEzObYpF_0'
openai.api_key= ''

listener = sr.Recognizer()
engine= pyttsx3.init()

voices= engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

for voice in voices:
    print(voice)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    rec=""
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            rec= listener.recognize_google(voice)
            rec=rec.lower()
            if name in rec:
                rec = rec.replace(name,'')
                print(rec)
    except:
        pass
    return rec

def search_chatgpt(query):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def run():
    rec = listen()
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        talk('Reproduciendo' + music)
        pywhatkit.playonyt(music)
    elif 'cuantos suscriptores tiene' in rec:
        name_subs=rec.replace('cuantos suscriptores tiene', '')
        data=urllib.request.urlopen('https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername='+ name_subs)
        subs=json.loads(data)["items"][0]["statistics"]["subscriberCount"]
        talk(name_subs+ "tiene{:,d}".format(int(subs))+ "suscriptores!")
    elif 'hora' in rec:
        hora= datetime.datetime().now().strftime('%I:%M %p')
        talk("Son las "+hora)
    elif 'busca' in rec:
        order = rec.replace('busca', '')
        info = wikipedia.summary(order,1)
        talk(info)
    elif 'busca en chat' in rec:
        order=rec.replace('busca en chat','')
        info=search_chatgpt(order)
        talk(info)
    else:
        talk("Vuelve a intentarlo")

while(True):
    run()