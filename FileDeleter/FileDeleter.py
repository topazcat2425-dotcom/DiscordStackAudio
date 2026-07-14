import os

# deletes a single file
def deleteFile(file):
    os.remove(file) 

# deletes ALL the files in a folder
def deleteAllFiles(folder):
    dirList = os.listdir(folder)
    for i in dirList:
        deleteFile(f"{folder}\\{i}")