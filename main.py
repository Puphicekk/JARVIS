# JARVIS 2.0
import pywhatkit
import os
import struct
from pydub import AudioSegment
from pydub.playback import play
import config
from fuzzywuzzy import fuzz
import datetime
from num2words import num2words
import keyboard
import webbrowser
import random
import pvporcupine
import pyaudio
# from config import porcupine_key
import tkinter
import customtkinter
from PIL import ImageTk, Image
import vosk
import sys
import sounddevice as sd
import queue
import json
import torch
import time
import os
from tts import va_speak

model = vosk.Model("model_small")
samplerate = 16000
device = 1

q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def va_listen(callback):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(json.loads(rec.Result())["text"])
                return
            #else:
            #    print(rec.PartialResult())
#фронт 1
customtkinter.set_appearance_mode('dark')#light
customtkinter.set_default_color_theme('green')#цвет объектов
app = customtkinter.CTk()
app.title('JARVIS')
app.iconbitmap('favicon.ico')
app.geometry('600x440')
app.resizable(False, False)
imgb = ImageTk.PhotoImage(Image.open('black_vers.png'))

lb = customtkinter.CTkLabel(master=app, image=imgb)
lb.pack()

frame = customtkinter.CTkFrame(master=lb, width=300, height=300, corner_radius=15, bg_color='black')
frame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

l2 = customtkinter.CTkLabel(master=frame, text='Settings', font=('Century Gothic', 30))
l2.place(x=100, y=30)

def entry_button():
    api = entry_pico.get()
    return api

def combobox_button():
    name = entry_name.get()

    return name

entry_pico = customtkinter.CTkEntry(master=frame, width=200, placeholder_text='API KEY PICOVOICE')
entry_pico.place(x=35, y=80)



names = ['jarvis', 'alexa', 'bumblebee', 'picovoice']
entry_name = customtkinter.CTkComboBox(master=frame, values=names, width=200)
entry_name.place(x=35, y=120)

switch_var_1 = customtkinter.StringVar(value='on')
switch_var_2 = customtkinter.StringVar(value='on')
def swithc_event():
    if switch_var_1.get() == 'on':
        customtkinter.set_appearance_mode('dark')
    if switch_var_1.get() == 'off':
        customtkinter.set_appearance_mode('System')

def switch_event2():
    global audio_stream, pa, porcupine
    if switch_var_2.get() == 'on':
        audio_stream = pa.open(rate=porcupine.sample_rate,
                               channels=1,
                               format=pyaudio.paInt16,
                               input=True,
                               frames_per_buffer=porcupine.frame_length)

    if switch_var_2.get() == 'off':
        audio_stream.close()


switch_1 = customtkinter.CTkSwitch(master=frame, text='theme', command=swithc_event, variable=switch_var_1, onvalue='on', offvalue='off')
switch_1.place(x=35, y=160)
switch_2 = customtkinter.CTkSwitch(master=frame, text='listen', command=switch_event2, variable=switch_var_2, onvalue='on', offvalue='off')
switch_2.place(x=35, y=200)



#бэкенд


def va_respond(voice: str):
    cmd = recognize_cmd(filter_cmd(voice))
    if 'найди как' in voice or 'заугугли' in voice or 'поищи' in voice or 'поищи как' in voice or 'поищи что' in voice or 'за гугле как' in voice or 'за гугли как' in voice or 'за гугле что' in voice or 'найди видео' in voice:
        execute_cmd('google_query', voice)
    elif cmd['cmd'] not in config.VA_CMD_LIST.keys():
        va_speak('Я не поняла что вы сказали')
    else:
        execute_cmd(cmd['cmd'], voice)


def filter_cmd(raw_voice: str):
    cmd = raw_voice



    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
    if rc['percent'] >= 55:
        print(rc)
        return rc
    else:
        rc = {'cmd': 'passive', 'percent': 0}
        return rc



def execute_cmd(cmd: str, voice):
    controller = webbrowser.get()
    if cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказывать анекдоты ..."
        text += "и открывать браузер"
        pass
    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        va_speak('сейчас'+num2words(now))

    elif cmd == 'joke':
        jokes = ['Как смеются программисты? ... ехе ехе ехе',
                 'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «м+ожно присоединиться?»',
                 'Программист это машина для преобразования кофе в код']

        ch = random.randint(0,2)
        va_speak(jokes[ch])

    elif cmd == 'open_browser':
        webbrowser.open('https://www.google.com/')

    elif cmd == 'open_yandex':
        webbrowser.open('https://yandex.ru/')

    elif cmd == 'open_steam':
        try:
            os.startfile(f'W:\Mikha\JARVIS_2.0/apps/Steam.lnk')
        except:
            va_speak('У вас не установлено это приложение')

    elif cmd == 'open_discord':
        try:
            os.startfile(f'W:\Mikha\JARVIS_2.0/apps/Discord.lnk')
        except:
            va_speak('У вас не установлено это приложение')

    elif cmd == 'open_music':
        try:
            os.startfile(f'W:\Mikha\JARVIS_2.0/apps/Яндекс Музыка.lnk')
        except:
            va_speak('У вас не установлено это приложение')

    elif cmd == 'open_bin':
        try:
            os.startfile(f'W:\Mikha\JARVIS_2.0/apps/Корзина - Ярлык.lnk')
        except:
            va_speak('У вас не установлено это приложение')

    elif cmd == 'open_wallpaper':
        try:
            os.startfile(f'W:\Mikha\JARVIS_2.0/apps/Wallpaper Engine.url')

        except:
            va_speak('У вас не установлено это приложение')

    elif cmd == 'open_youtube':
        webbrowser.open('https://www.youtube.com')

    elif cmd == 'google_query':
        text_to_search = voice
        to_search = text_to_search.split('гугле')[-1]
        to_search1 = to_search.split('как')[-1]
        to_search1.split('найди')
        to_search1.split('поищи')
        webbrowser.open(f'https://www.google.com/search?q={to_search1}')

    elif cmd == 'search_youtube':
        text_to_search = voice
        to_search = text_to_search.split('ютуб')[-1]
        pywhatkit.playonyt(f"{to_search}")

    elif cmd == 'next_video':
        keyboard.send('shift + N')

    elif cmd == 'previous_video':
        keyboard.send('shift + P')

    elif cmd == 'skip_back':
        keyboard.send('left')

    elif cmd == 'skip_forward':
        keyboard.send('right')

    elif cmd == 'subtitles_video':
        keyboard.send('c')

    elif cmd == 'sound_video_on':
        keyboard.send('f10')

    elif cmd == 'sound_video_off':
        keyboard.send('f8')

    elif cmd == 'full_screen_video':
        keyboard.send('f')

    elif cmd == 'end_video':
        keyboard.send('end')

    elif cmd == 'start_video':
        keyboard.send('0')

    elif cmd == 'pause':
        keyboard.send('space')

    elif cmd == 'pause':
        keyboard.send('space')

# controller = webbrowser.get()
# porcupine = pvporcupine.create(access_key=porcupine_key, keywords=['jarvis'])
#
# pa = pyaudio.PyAudio()
# audio_stream = pa.open(
#                   rate=porcupine.sample_rate,
#                   channels=1,
#                   format=pyaudio.paInt16,
#                   input=True,
#                   frames_per_buffer=porcupine.frame_length)


# начать прослушивание команд

#WT/TvQbJ7ARpkQ36Pk6Qtp3KNY5JiFDkpfM4dJ9i8vFtmyp2OVUlKA==
def start():
    try:
        controller = webbrowser.get()
        porcupine_key = entry_button()
        porcupine = pvporcupine.create(access_key=str(porcupine_key), keywords=[str(combobox_button())])
        print('подключ')
        va_speak('Здравствуйте, буду рада вам помочь')
        # pa = pyaudio.PyAudio()
        # audio_stream = pa.open(
        #     rate=porcupine.sample_rate,
        #     channels=1,
        #     format=pyaudio.paInt16,
        #     input=True,
        #     frames_per_buffer=porcupine.frame_length)
        while True:
            if switch_var_2.get() == 'on':
                pa = pyaudio.PyAudio()
                audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0:
                    print('слушаю')
                    print(va_listen(va_respond))
            elif switch_var_2.get() == 'off':
                pa = pyaudio.PyAudio()
                audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)
                audio_stream.close()
            app.update()

        app.mainloop()

    except:
        va_speak('Вы не ввели все данные')
        print('отказ')


save_button = customtkinter.CTkButton(master=frame, text='Save', command=start)
save_button.place(x=35, y=240)

print('JARVIS_2.0 начал свою работу')
app.mainloop()



