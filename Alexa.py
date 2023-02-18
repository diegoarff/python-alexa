import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
from datetime import datetime

# Utility variables
assitant_name = 'alexa'
keep_listening = True
lang = 'es-MX'

# Languages and topics
languages = {
    'en-US': {
        'SALUDO': ['hello', 'hello, what can i do for you?'],
        'ESTADIA': ['are you there', 'yes, i am. what do you need?'],
        'REPRODUCE': ['play', 'playing'],
        'HORA': ['time', 'the current time is'],
        'MATH': ['what is', 'is'],
        'IDIOMA': ['language', 'done, language changed to '],
        'TERMINA': ['stop', 'ok, goodbye'],
        'WIKI': ['search'],
        'ERROR': ['listen_error', 'an error ocurred parsing your command. please try again.']
    },
    'es-MX': {
        'SALUDO': ['hola', 'hola, que puedo hacer por ti?'],
        'ESTADIA': ['estas ahi', 'si, aqui estoy. que necesitas?'],
        'REPRODUCE': ['reproduce', 'reproduciendo'],
        'HORA': ['hora', 'la hora es'],
        'MATH': ['cuanto es', 'es'],
        'IDIOMA': ['idioma', 'listo, idioma cambiado a '],
        'TERMINA': ['termina', 'hasta luego'],
        'WIKI': ['busca'],
        'ERROR': ['listen_error', 'ocurrio un error obteniendo tu comando. por favor intenta de nuevo'] 
    }
}

# Name recognizer
recognizer = sr.Recognizer()

# Voice configuration
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 200) # Velocidad de habla
engine.setProperty('volume', 1)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def set_voice_type(lang):
    if lang == 'es-MX':
        engine.setProperty('voice', voices[0].id)
    elif lang == 'en-US':
        engine.setProperty('voice', voices[1].id)
    
def get_user_command():
    # Activate microphone
    with sr.Microphone() as source:
        print('Listening...')
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        command = "" # set command with empty value to avoid error returning
        
        try:
            command = recognizer.recognize_google(audio, language=lang).lower()
        except:
            command = 'listen_error'
            
    return command

def run_alexa():
    global lang
    set_voice_type(lang)

    command = get_user_command()
    topics = languages.get(lang)
    
    if assitant_name in command:
        command = command.replace(assitant_name, '')
        command = command.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
        print(command)
        
        # Define topics
        if topics.get('ESTADIA')[0] in command:
            speak(topics.get('ESTADIA')[1])
            
        elif topics.get('SALUDO')[0] in command:
            speak(topics.get('SALUDO')[1])
            
        elif topics.get('REPRODUCE')[0] in command:
            song = command.replace(topics.get('REPRODUCE')[0], '')
            speak(f"{topics.get('REPRODUCE')[1]} {song}")
            pywhatkit.playonyt(song)
            
        elif topics.get('HORA')[0] in command:
            time = datetime.now().strftime('%I:%M %p')
            speak(f"{topics.get('HORA')[1]} {time}")
            
        elif topics.get('WIKI')[0] in command:

            topic = command.replace(topics.get('WIKI')[0], '')
            
            if lang == 'es-MX':
                wikipedia.set_lang('es')
            elif lang == 'en-US':
                wikipedia.set_lang('en')
            
            info = wikipedia.summary(topic, 1)
            speak(info)
                
        elif topics.get('MATH')[0] in command:
            prompt = command.replace(topics.get('MATH')[0], '')
            result = eval(prompt)
            speak(f"{prompt} {topics.get('MATH')[1]} {result}")
        
        
        elif topics.get('IDIOMA')[0] in command:
            if lang == 'es-MX':
                lang = 'en-US'
            elif lang == 'en-US':
                lang = 'es-MX'
            speak(topics.get('IDIOMA')[1] + lang)
            
        elif topics.get('TERMINA')[0] in command:
            speak(topics.get('TERMINA')[1])
            return False
        
        else:
            speak(topics.get('ERROR')[1])
        
    return True
        
while keep_listening:
    keep_listening = run_alexa()
    
    

