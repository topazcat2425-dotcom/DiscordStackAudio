from threading import Thread
import PlaysToMic.PlaysToMic as PlaysToMic
import AudioRecorder.AudioRecorder as AudioRecorder
import FileDeleter.FileDeleter as fileDeleter

# EDIT THIS TO INCREASE THE MAXIMUM FILES YOU HAVE TO FILL
MAX_HEIGHT_OF_STACK = 10

if __name__ == '__main__':
    thread1 = Thread(target = PlaysToMic.doTheStack, args=(MAX_HEIGHT_OF_STACK,))
    thread2 = Thread(target = AudioRecorder.startRecording, args=(MAX_HEIGHT_OF_STACK,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    fileDeleter.deleteAllFiles("AudioStuff\\wavs")
