import cv2

# Open the default camera (webcam)
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if frame is read correctly
    if not ret:
        print("Error capturing frame")
        break

    # Display the resulting frame
    cv2.imshow('Camera', frame)

    # Exit loop if 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
