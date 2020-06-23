import os

import speech_recognition as sr

from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS as tts

micName = "USB PnP Audio Device: Audio (hw:1,0)"

def capture():
    """Capture audio"""

    rec = sr.Recognizer()

    with sr.Microphone(device_index = 2, chunk_size = 1024) as source:
        print('I\'M LISTENING...')
        audio = rec.listen(source, phrase_time_limit=5)

    try:
        text = rec.recognize_google(audio, language='en-US')
        print("TEXT RECOGNIZED: " + text)
        return text

    except:
        #speak('Sorry, I could not understand what you said.')
        print("Sorry, I could not understand what you said.")
        return 0
    
if __name__ == "__main__":

    # First get name
    print("Try to say something")
    name = capture()

    # Then just keep listening & responding
    while 1:
        #speak('What do you have to say?')
        captured_text = capture()#.lower()
        #print("Captured text " + captured_text)