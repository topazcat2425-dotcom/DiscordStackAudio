# Source - https://stackoverflow.com/a/61674334
# Posted by PyPylia, modified by community. See post 'Timeline' for change history
# Retrieved 2026-07-12, License - CC BY-SA 4.0

from pygame import mixer #Playing sound   pip install pygame
from numpy import random
import time
import glob
import soundfile as sf
import os

USED_FILES = []

# this reads files
def readFiles():
    txtfiles = []
    for file in glob.glob("AudioStuff\\wavs\\*.wav"):
        txtfiles.append(file.split('\\')[len(file.split('\\')) - 1])
    return(txtfiles)

# gets the top of the stack, theoretically
def getTopFile():
    top = "-1"

    for file in readFiles():

        if (( int(file.removesuffix(".wav")) > int(top.removesuffix(".wav"))) and file not in USED_FILES):
            top = file

    print(top)
    return(top, getLength(top))

# gets the duration of the file
def getLength(file):
    
    fileTime = 0
    if (file != "-1.wav"):
        f = sf.SoundFile(f"AudioStuff\\wavs\\{file}")
        # print('samples = {}'.format(f.frames))
        # print('sample rate = {}'.format(f.samplerate))
        # print('seconds = {}'.format(f.frames / f.samplerate))

        fileTime = float(format(f.frames / f.samplerate))

    baseTime = 5
    if (fileTime > baseTime):
        baseTime = fileTime + 1

    print(baseTime)
    return(baseTime)

# plays the file through the VB virtual audio cable
def playFile(file, duration):
    # duration = getLength(f"AudioStuff\\wavs\\{file}")
    mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)') #Initialize it with the correct device
    mixer.music.load(f"AudioStuff\\wavs\\{file}") #Load the mp3
    mixer.music.play() #Play it

    
    time.sleep(duration)
    mixer.music.unload()
    mixer.music.stop()
    print("playing?")

# sleeps for a random amount of time... isn't used :I
def randomWait(bottomLimit, topLimit):
    x = random.randint(bottomLimit, topLimit)
    print("random chosen is:")
    print(x)
    time.sleep(x)

def doTheStack(threadChecker):


    # HERE TO CHANGE THE TIME BEFORE IT STARTS UNSTACKING!!
    timeBeforeStack = 10


    print("-------------------------------------")
    print(f"You have {timeBeforeStack} seconds to fill the stack before it starts removing")
    print(f"You can turn off the program by typing anything into the console ctrl+c will NOT work")
    print("-------------------------------------")

    time.sleep(timeBeforeStack)
    count = 1
    while (threadChecker.readBool()):
        file, duration = getTopFile()

        # kill the loop here
        if not threadChecker.readBool():
            break
        elif (file != "-1.wav"):
            print(f"playing audio file {file}")
            playFile(file, duration)
        
            USED_FILES.append(file)
            count += 1
        else:
            time.sleep(1)
        
        
    
    time.sleep(5)
