import speech_recognition as sr
from output import speak_online
import json
import random
from functions import *


def load_speech():
    with open('speech.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data
''

def speech_commands(text:str):
    data = load_speech()
    result = False
    for phrase in data:
        for input_words in phrase['input']:
            if input_words in text.lower():
                output = random.choice(phrase['output'])
                           
                function_name = phrase.get("function")
                if function_name:
                    func = globals().get(function_name)
                    if func:
                        output_func = func(text)
                        for key in output_func.keys():
                            output = output.replace(f'[{key}]',str(output_func[key]))
                speak_online(output)
                print(output)
                result = True


def main():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Ready")
        speak_online("Привіт владика Анатолій! Чим можу допомогти?")
        while True:            
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            try:
                text = recognizer.recognize_google(audio, language="uk-UA")
                print(f'Ваш запит: {text}')                                
                result = speech_commands(text)
                if result == False:
                    variants = [
                        "Я тебе не розумію",
                        "Вибачте не можу розібрати",
                        "Повторіть будь ласка"
                    ]
                    speak_online(random.choice(variants))
            except sr.UnknownValueError:
                print('Не вдалось розпізнати звук')
            except sr.RequestError:
                print("RequestError")
            except sr.WaitTimeoutError:
                print("WaitTimeoutError")


main()
