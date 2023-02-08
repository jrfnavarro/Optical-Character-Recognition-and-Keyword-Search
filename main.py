import os
from PIL import Image
import pytesseract
from tqdm import tqdm
import cv2

def analyze_images(dir_path, keywords):
    for filename in tqdm(os.listdir(dir_path)):
        if not filename.startswith("detected_"):
            try:
                image = cv2.imread(os.path.join(dir_path, filename))
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gray = cv2.medianBlur(gray, 3)
                gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                with Image.fromarray(gray) as im:
                    text = pytesseract.image_to_string(im)
                    for keyword in keywords:
                        if keyword.lower() in text.lower():
                            os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, "detected_" + filename))
                            print(f"{filename} has been detected")
                            break
            except:
                pass

while True:
    dir_path = input("Enter the path of the directory: ")
    if os.path.isdir(dir_path):
        break
    print("Invalid path. Please enter a valid path.")

keywords = input("Enter keywords to search for, separated by commas: ").split(',')
keywords = [keyword.strip() for keyword in keywords]

for i in range(2):
    analyze_images(dir_path, keywords)
print("Process is done")
