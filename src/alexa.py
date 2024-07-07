import datetime
import speech_recognition as sr
import pyttsx3
import pywhatkit
import urllib.request
import json
import wikipedia
import openai

name='alexa'
key= '' # indicar api de youtube
openai.api_key= '' # indicar api de openai

listener = sr.Recognizer()
engine= pyttsx3.init()

voices= engine.getProperty('voices')
for voice in voices:
    print(voice) # muestra las voces del sistema disponibles

engine.setProperty('voice',voices[0].id) # el motor de voz se debe establecer por default
def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    rec=""
    try:
        with sr.Microphone() as source:
            print("Ajustando el ruido ambiental, por favor espera...")
            listener.adjust_for_ambient_noise(source, duration=1)
            talk(f"hola, soy {name}")
            print("Escuchando...")
            voice = listener.listen(source, timeout=5)
            rec = listener.recognize_google(voice, language='es-ES')
            print("Reconocido: " + rec)
            rec=rec.lower()
            if name in rec:
                rec = rec.replace(name,'')
                print(rec)
    except sr.UnknownValueError:
        print("No entendí el audio")
    except sr.RequestError as e:
        print("Error de servicio; {0}".format(e))
    except Exception as e:
        print(f"Error: {e}")
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
    elif 'dime la hora' in rec:
        hora= datetime.datetime.now().strftime('%I:%M %p')
        print("Son las "+hora)
        talk("Son las "+hora)
    elif 'busca' in rec:
        order = rec.replace('busca', '')
        info = wikipedia.summary(order,1)
        talk(info)
        print(info)
    elif 'busca en chat' in rec:
        order=rec.replace('busca en chat','')
        info=search_chatgpt(order)
        talk(info)
        print(info)
    else:
        talk("Vuelve a intentarlo")

while(True):
    run()
