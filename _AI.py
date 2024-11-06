try:
    import requests
    import pygame
    import speech_recognition as sr
    import os
    import urllib.parse
    from fuzzywuzzy import fuzz
    import pyautogui
    import time
    time.sleep(5)
    pygame.mixer.init()
    api_key = '5f118fd9-9bc2-4ca9-8dcc-3c38d7a4b4e3:1ad71162-f438-439a-befa-6b0dfbfd778e'
    url = 'https://uzbekvoice.ai/api/v1/tts'
    music_list = [
        "C:\\Users\\Victus\\Music\\slowly.mp3",
        "C:\\Users\\Victus\\Music\\Ava_famy.mp3",
        "C:\\Users\\Victus\\Music\\dunyo.mp3",
        "C:\\Users\\Victus\\Music\\dutcan.mp3",
        "C:\\Users\\Victus\\Music\\landushi.mp3",
        "C:\\Users\\Victus\\Music\\Si_ai.mp3",
    ]   
    responses = {
        "salom":"Assalomu alaykum!",
        "ellie": "Ha, eshitaman",
        "CMD ni och": "Tushunarli, kommand prompni ochyapman.",
        "ob-havoni ko'rsat": "Bu ob havo haqida ma'lumot",
        "wifni o'chir": "wifini, o'chiryapman.",
        "telegramni och": "Telegrani ochdim!",
        "ekranni rasmga ol": "Rasmni olish uchun maydonni belgilang.",
        "wifini o'chir": "Ho'p, wifini o'chiryapman.",
        "musiqa qo'y": "Musiqa qo'yyapman.",
        "qo'shiq qo'y": "Musiqa qo'yyapman.",
        "almashtir": "Musiqa qo'yyapman.",
        "ovozini pasaytir": "Ho'p, pasaytirayapman.",
        "ovozini ko'tar": "Ho'p, ko'taryapman",
        "ishchi stolimni tayyorla": "Ho'p, kerakli ilovalaringizni ishga tushiryapman.",
        "Men qaytdim": "Ho'p, kerakli ilovalaringizni ishga tushiryapman.",
        "ha": "Ho'p, kerakli ilovalaringizni ishga tushiryapman.",
        "jimib tur": "Ho'p",
        "o'ch": "Ho'p mayli",
        "ovozini o'chir":"Ho'p,",
        "qoshiqni pauzala":"Ho'p,",
        "qoshiqni qo'y":"Ho'p,"
    }
    def speak(text):
        pygame.mixer.quit()
        pygame.mixer.init()

        data = {
            "text": text,
            "model": "fotima-neutral",
            "blocking": "true"
        }

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            audio_url = result['result']['url']

            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                with open('output.wav', 'wb') as audio_file:
                    audio_file.write(audio_response.content)

                pygame.mixer.music.load('output.wav')
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                try:
                    os.remove('output.wav')
                except PermissionError:
                    print("Faylni o'chirishda xato. Fayl hali ishlatilmoqda.")
            else:
                print("Faylni yuklashda xato:", audio_response.status_code, audio_response.text)
        else:
            print("API chaqiruvi xatosi:", response.status_code, response.text)
    speak("Assalomu alykum ishni boshlaysizmi?")
    def search_google(query):
        query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={query}"
        os.system(f"start chrome {url}")
    def get_best_response(text, responses):
        best_match = None
        highest_score = 0
        for key, response in responses.items():
            score = fuzz.ratio(text, key)
            if score > highest_score:
                highest_score = score
                best_match = response
        return best_match
    recognizer = sr.Recognizer()
    current_song_index = -1 
    while True:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                print("Gapiring:")
                audio = recognizer.listen(mic, phrase_time_limit=10)
                text = recognizer.recognize_google(audio, language='uz-UZ')
                text = text.lower()
                print(f"Siz dedingiz: {text}")

                if "googledan" in text or "qidir" in text:
                    search_query = text.replace("googledan", "").replace("deb", "").replace("qidir", "").strip()
                    if search_query:
                        print(f"Google'da qidiryapman: {search_query}")
                        search_google(search_query)
                        speak(f"Ho'p, hozir qidiryapman, qidirdim natijalaringiz ekranda.")
                    else:
                        speak("Men bilmayman.")
                    continue
                
                response = get_best_response(text, responses)

                if response:
                    speak(response)

                    if response == "Musiqa qo'yyapman.":
                        current_song_index = (current_song_index + 1) % len(music_list)
                        pygame.mixer.music.load(music_list[current_song_index])
                        pygame.mixer.music.play()
                    elif response=="Ho'p,":
                        pyautogui.press("volumemute")
                    elif response == "Ho'p mayli":
                        speak("Salom!")  
                        break
                    elif response == "Ho'p":
                        time.sleep(60)
                        l = "Gapiraveraymi?"
                        speak(l)
                        continue
                    elif response == "Ho'p, kerakli ilovalaringizni ishga tushiryapman.":
                        pyautogui.hotkey("win", "s")
                        pyautogui.write("Telegram")
                        pyautogui.press("enter")
                        time.sleep(2)
                        pyautogui.hotkey("win", "s")
                        pyautogui.write("VS")
                        pyautogui.press("enter")
                        time.sleep(2)
                        os.system("start")
                    elif response == "Ho'p pasaytirayapman.":
                        pyautogui.press('volumeup')
                    elif response == "Ok, ovozni ko'tarayapman.":
                        pyautogui.press('volumedown')
                    elif response == "Telegrani ochdim!":
                        pyautogui.hotkey("win", "s")
                        pyautogui.write("Telegram")
                        pyautogui.press("enter")
                    elif response == "Rasmni olish uchun maydonni belgilang.":
                        pyautogui.press("prtsc")
                    elif response == "Ok, Wifi'ni o'chiraman.":
                        os.system("netsh wlan disconnect")
                    elif response == "Bu ob havo haqida ma'lumot":
                        pyautogui.hotkey("win", "s")
                        pyautogui.write("Weather")
                        pyautogui.press("enter")
                    elif response == "Tushunarli, kommand prompni ochyapman.":
                        os.system("start cmd")
                else:
                    print("Gapira olmayman.")
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            continue
        except sr.RequestError:
            speak("Men tushunmayapman, internet yo'q.")
            continue
        except sr.WaitTimeoutError:
            speak("Men eshitmayapman.")
            continue
except Exception as e:
        print(f"Xato yuz berdi: {e}, dastur qayta ishga tushmoqda...")
             