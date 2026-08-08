from threading import Thread
from ThreadEnable import ThreadEnable
import PlaysToMic.PlaysToMic as PlaysToMic
import AudioRecorder.AudioRecorder as AudioRecorder
import FileDeleter.FileDeleter as fileDeleter
import ThreadEnabler.ThreadEnabler as ThreadEnabler


MAX_HEIGHT_OF_STACK = 15

if __name__ == '__main__':
    boolean = ThreadEnable()

    thread1 = Thread(target = PlaysToMic.doTheStack, args=(boolean,))
    thread2 = Thread(target = AudioRecorder.startRecording, args=(boolean,))
    thread3 = Thread(target = ThreadEnabler.running, args=(boolean,))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    if not boolean.readBool():
        fileDeleter.deleteAllFiles("AudioStuff\\wavs")
