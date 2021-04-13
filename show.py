import os
import random

# Reference: https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
# For the given path, get the List of all files in the directory tree
def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

all_samples = getListOfFiles("./data/")
samples = []
for i in all_samples:
    if i[len(i)-4:] == ".png":
        samples.append(i)

samples_show = random.sample(samples, 100)

for i in samples_show:
    print("<img src=\"", i, "\" width=\"100\">", sep="")
