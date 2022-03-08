# Scans Directory for sequentially numbered files to ensure one large sequence exists

import os

def sortContinuous(L):
    first = last = L[0]
    for n in L[1:]:
        if n - 1 == last:
            last = n
        else: 
            yield first, last
            first = last = n
    yield first, last 

dirPath = str(input("Path to scan: "))
fileType = str(input("Filetype to scan: "))

if not fileType.startswith("."):
    fileType = "." + fileType

print("Searching for " + fileType + " files in " + dirPath)
allFiles = [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f))]

matchingFiles = []
for file in allFiles:
    ext = os.path.splitext(file)
    if ext[1] == fileType:
        matchingFiles.append(ext[0])

intFiles = []
strFiles = []
for file in matchingFiles:
    try:
        file = int(file)
        intFiles.append(file)
    except:
        strFiles.append(file)

intFiles.sort()

if len(intFiles) > 0:
    continuousLists = list(sortContinuous(intFiles))


print("Currently Present Files:")
if len(continuousLists)>0:
    for entry in continuousLists:
        if entry[0] != entry[1]:
            print(str(entry[0]) + " through " + str(entry[1]))
        else:
            print(entry[0])

if len(strFiles) > 0:
    print("Non Numerical Files:")
    for entry in strFiles:
        print(entry)

input("Press any key to continue")