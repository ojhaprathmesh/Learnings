import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. Reading the image
image_path = 'Assignment-1/MRI-Brain.jpg'
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Read as grayscale for histogram simplicity

# 2. Displaying the image
cv2.imshow('Original Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 3. Know the dimension of the image
print(f"Image shape (height, width): {img.shape}")

# 4. Know the pixel intensities inside a ROI and at specific locations
# Example: pixel at (50, 50)
pixel_value = img[50, 50]
print(f"Pixel value at (50, 50): {pixel_value}")

# ROI: region from (30, 30) to (80, 80)
roi = img[30:80, 30:80]
print(f"ROI shape: {roi.shape}")
print(f"ROI pixel values:\n{roi}")

# 5. Cropping the image
cropped_img = img[30:130, 30:130]  # Crop a 100x100 region
cv2.imshow('Cropped Image', cropped_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 6. Changing the size of the image
resized_img = cv2.resize(img, (200, 200))  # Resize to 200x200
cv2.imshow('Resized Image', resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 7. Display histogram
plt.figure()
plt.title('Grayscale Histogram')
plt.xlabel('Pixel value')
plt.ylabel('Frequency')
plt.hist(img.ravel(), bins=256, range=[0,256])
plt.show()
