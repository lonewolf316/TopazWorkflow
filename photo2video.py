import os
import cv2
import numpy as np
import glob
from queue import Queue
from threading import Thread
import time 

numThreads = 20 # If program runs out of memory, turn this number down
frameSize = (3840, 2160)

q = Queue(maxsize=0) # Filename queue going into worker
r = Queue(maxsize=0) # Images returning from worker

print("Finding Files")
allFiles = [f for f in os.listdir("testdata") if os.path.isfile(os.path.join("testdata", f))]
lastFrame = len(allFiles)-1

for file in allFiles:
    q.put(file)

time.sleep(1)

def importWorker(q, r):
    while True:
        name = q.get()
        img = cv2.imread("testdata/"+name)
        frameNumber = int(os.path.splitext(name)[0])
        #print("Processed: "+str(frameNumber))
        r.put([frameNumber, img])
        q.task_done()


def exportWorker(r, total):
    currentNum=0
    disorderFrames = []
    out = cv2.VideoWriter('output_video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 60, frameSize)
    while currentNum <= total:
        frame = r.get()
        if frame[0] == currentNum:
            out.write(frame[1])
            print("Appended frame: " + str(frame[0]))
            currentNum+=1
        else:
            disorderFrames.append(frame)
            for frame in disorderFrames:
                if frame[0] == currentNum:
                    out.write(frame[1])
                    print("Appended frame: " + str(frame[0]))
                    currentNum+=1
                
                pass
        r.task_done()
    out.release()    



for i in range(numThreads):
    importWorkerThread = Thread(target=importWorker, args=(q, r))
    importWorkerThread.setDaemon(True)
    importWorkerThread.start()

exportWorkerThread = Thread(target=exportWorker, args=(r, lastFrame))
exportWorkerThread.setDaemon(True)
exportWorkerThread.start()

q.join()
r.join()
