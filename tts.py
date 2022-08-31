import time
from gtts import gTTS #google text to speech will turn a string into a audio file (in this use mp3)
import os
from pathlib import Path #so the way to the mp3 can be a relative path and not an actual path that only works on my pc
from mutagen.mp3 import MP3 #has a way to read mp3 file metadata
vlcActive = True #import vlc but user might not have the actual vlc app installed, so catch if they haven't
try:
    import vlc
except:
    print("cant use the vlc module, module is missing or vlc may not be installed on the machine")
    vlcActive = False

def duration(path): #function takes a (path to a) mp3 file and returns the length of it in seconds
    audio = MP3(path)
    length = audio.info.length
    return(length)

def TTS(text): #turn string into audio and play it
    global vlcActive
    if vlcActive: #only when the vlc module is imported correctly
        language = "en"
        speech = gTTS(text = text, lang = language, slow = False) #turns text into audio
        script_path = Path(__file__).parent #gets the path of the script
        #print(script_path)
        mp3_path = (script_path / "text.mp3").resolve() #get the full path of the mp3 file
        #print(mp3_path)
        speech.save(mp3_path) #save the audio as text.mp3
        audio = vlc.MediaPlayer(mp3_path) #create vlc instance
        audio.play() #play the vlc instance
        time.sleep(duration(mp3_path)) #wait for the duration of the mp3
        audio.stop() #stop the vlc instance
    else:
        print("vlc module not active")

if __name__ == "__main__":
    testList = ["test1","test2","test3"]
    for x in testList:
        TTS(x)
