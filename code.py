import streamlit as st

import pandas as pd
import re
import random
from datetime import datetime
import time
import speech_recognition as sr
import pyttsx3

##audio mode add-on
r = sr.Recognizer()
def recog_audio():
    with sr.Microphone() as source:
        print('Say something')
        audio = r.listen(source)
        #voice_data = r.recognize_google(audio)
        try:
            voice_data = r.recognize_google(audio)
            return voice_data
        except sr.UnknownValueError:
            print("Google SR engine could not understand audio. Say again please")
            #recog_audio()

        except sr.RequestError as e:
            print("web request error")
