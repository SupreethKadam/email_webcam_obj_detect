import os
import glob


def clean_folder():
    print("clean_folder function started.")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("clean_folder function ended.")
