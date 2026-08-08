# idk why this is its own function
def turnOffThreads(thread):
    thread.setFalse()
    return

# this listens for any input to the console to update the thread enabling class to kill all the threads
def running(thread):
    print("Type anything to disable audio stack!")
    while(1):
        i = input()
        if i is not None:
            turnOffThreads(thread)
            break