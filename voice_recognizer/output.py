from gtts import gTTS
import pygame
import io

def speak_online(text):
    # Створюємо аудіо об'єкт у пам'ятіgit remote remove origin
    tts = gTTS(text=text, lang='uk', slow=False)
    audio_data = io.BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)

    # Ініціалізація pygame для відтворення аудіо
    pygame.mixer.init()
    pygame.mixer.music.load(audio_data, 'mp3')
    pygame.mixer.music.play()

    # Очікування завершення відтворення
    while pygame.mixer.music.get_busy():
        pass
