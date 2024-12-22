import pyautogui # pip install pyautogui
from PIL import ImageGrab
import time

pause = 3

def hit(key):
    pyautogui.keyDown(key)

def isCollide(imgData):
    for i in range(480, 487):
        for j in range(288, 313):
            if imgData[i, j]==83:
                hit('up')
                return True

    # for x in range(260,270):
    #     for y in range(310,320):
    #         if imgData[x, y]==83:
    #             hit('down')
    #             return True

if __name__ == "__main__":
    print(f'Starting Dino In {pause} Seconds')
    time.sleep(pause)
    hit('up')
    while True:
        image = ImageGrab.grab().convert('L')
        data = image.load()
        isCollide(data)