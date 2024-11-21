import time
import random
import requests
from output import speak_online
import speech_recognition as sr

def get_time(text:str):
    current_time = time.localtime()
    output_time = f"{current_time.tm_hour}:{current_time.tm_min}"
    return {"час":output_time}

def get_rundom_number(text:str):
    return {"число":random.randint(0, 100)}

def get_rundom_flip(text:str):
    variants = ["орел","решка"]
    winner = random.choice(variants)
    if winner == "орел":
        return {"сторона переможець":"орел","сторона переможений":"решка"}
    else:
        return {"сторона переможець":"решка", "сторона переможений":"орел"}
    

def get_dollar_curency(text:str):
    result = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
    result = result.json()
    lst_currency = (str(round(float(result[1]["sale"]), 2))).split(".")
    # return {"курс": str(round(float(result[1]["sale"]), 2))}
    return {"курс_грн": {lst_currency[0]}, "курс_копійка":{lst_currency[1]}}

def game(text:str):
    recognizer = sr.Recognizer()
    correct_number = random.randint(10,100)
    speak_online("Давай зіграємо я загадав число від десяти до 100, твоя задача його відгадати, скажи кінець якщо захочеш закінчити гру")
    with sr.Microphone() as source:
        print("Ready to game")
        while True:
            try:
                print("Скажи число")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = recognizer.recognize_google(audio, language="uk-UA")
                print(f'Ви сказали: {text}')
                if text.isdigit():
                    number_user = int(text)
                    if number_user == correct_number:
                        speak_online("вітаю ти вгадав")
                        break
                    elif number_user < correct_number:
                        speak_online(f"спробуй ще, моє число більше за {number_user}")
                    elif number_user > correct_number:
                        speak_online(f"спробуй ще, моє число менше за {number_user}")
                
                elif "кінець" in text:
                    break
                else:
                    speak_online(f"скажіть тільки число нічого зайвого")
                
            except sr.UnknownValueError:
                print('Не вдалось розпізнати звук')
            except sr.RequestError:
                print("RequestError")
            except sr.WaitTimeoutError:
                print("WaitTimeoutError")
    return {}
