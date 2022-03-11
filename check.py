# Checks every png file in a directory to find any corrupt files that
# would break during the photo2video step

from tqdm import tqdm
from PIL import Image
import os

readDir = input("Source Directory (Defaults to data):")
if readDir == "":
    readDir = "data"

allFiles = [f for f in os.listdir(readDir) if os.path.isfile(os.path.join(readDir, f))]
print("Found " + str(len(allFiles)) + " image files.")

brokeImages = []

for file in tqdm(allFiles):
    try:
        testImage = Image.open(os.path.join(readDir,file))
        testImage.verify()
        testImage.close()
    except:
        brokeImages.append(file)

print("Found broke images:")
print(brokeImages)