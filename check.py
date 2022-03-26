# Checks every png file in a directory to find any corrupt files that
# would break during the photo2video step
# give option to bulk delete files in order to create new ones
from queue import Queue
from threading import Thread
from numpy import add
from tqdm import tqdm
from PIL import Image
import os

q = Queue(maxsize=0) # Filename queue going into worker
r = Queue(maxsize=0) # Broken images found by workers
d = Queue(maxsize=0) # Counter for done images
numThreads = 1

def fileCheckWorker(q, r, d):
    while True:
        filePath = q.get()
        try:
            testImage = Image.open(filePath)
            testImage.verify()
            testImage.close()
        except:
            r.put(filePath)
        d.put(True)
        q.task_done()

def procWatchdog(r, lastFrame):
    with tqdm(total=lastFrame+1) as progress:
        while True:
            d.get()
            progress.update(1)

readDir = input("Source Directory (Defaults to data):")
if readDir == "":
    readDir = "data"

allFiles = [f for f in os.listdir(readDir) if os.path.isfile(os.path.join(readDir, f))]
print("Found " + str(len(allFiles)) + " image files.")

print("Building Queue")
for file in tqdm(allFiles):
    q.put(os.path.join(readDir,file))

print("Starting processing")
for i in range(numThreads):
    importWorkerThread = Thread(target=fileCheckWorker, args=(q, r, d))
    importWorkerThread.start()

exportWorkerThread = Thread(target=procWatchdog, args=(d, len(allFiles)-1))
exportWorkerThread.start()

q.join()

brokeImages = []
while not r.empty():
    addPath = r.get()
    brokeImages.append(addPath)

print()
print("Found broke images:")
print(brokeImages)
deleteYn = input("Delete these files? y/n ")

if deleteYn == "y":
    print("Deleting")
    for file in tqdm(brokeImages):
        os.remove(file)