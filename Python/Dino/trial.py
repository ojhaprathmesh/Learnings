from PIL import ImageGrab  # ImageOps
import time
xShift = 70
yShift = 0

time.sleep(5)
image = ImageGrab.grab().convert('RGB')
# image = ImageOps.invert(image)
data = image.load()
for i in range(700-xShift, 770-xShift):
    for j in range(250-yShift, 290-yShift):
        data[i, j] = 83

image.show()