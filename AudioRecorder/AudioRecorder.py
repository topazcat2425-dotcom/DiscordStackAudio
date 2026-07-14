# Source - https://stackoverflow.com/a/6743593
# Posted by cryo, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-30, License - CC BY-SA 4.0

from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave

THRESHOLD_PASSIVE = 5000
THRESHOLD_NORMAL = 1500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

# I DID NOT MAKE THIS ONE
def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD_NORMAL

# this checks if the passive sound is silent, speaking *should* return true
def isSilentPassive(sndData):
    return max(sndData) < THRESHOLD_PASSIVE

# I DID NOT MAKE THIS ONE
def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

# I DID NOT MAKE THIS ONE
def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD_NORMAL:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

# I DID NOT MAKE THIS ONE
def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    silence = [0] * int(seconds * RATE)
    r = array('h', silence)
    r.extend(snd_data)
    r.extend(silence)
    return r

def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    # PLUS SOME!


    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)


    num_silent = 0
    snd_started = False

    r = array('h')

    # this loop just checks if the background is silent, will break when you start speaking
    while 1:

        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()

        if not isSilentPassive(snd_data):
            r.extend(snd_data)
            break

    print("we are recording!")

    # this loop isn't mine, but it reads and takes the data until it hears prolonged silence
    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        #                                |
        # time limit for silence, change V that value
        if snd_started and num_silent > 20:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r

# I DID NOT MAKE THIS ONE
def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


# loops until the stack is full by making new audio files
def startRecording(maxHeightOfStack):
    print("We are listening now")
    count = 0
    while(count < maxHeightOfStack):

        record_to_file(f'AudioStuff/wavs/{count}.wav')
        print(f"done - result written to {count}.wav")
        count += 1
    
    print("we're all finished recording fr \n----------------------------------------------")