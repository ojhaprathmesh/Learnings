import cv2
import mediapipe as mp
import numpy as np
import pyttsx3

# Function to calculate angle (replace with desired formula)
def calculate_angle(p1, p2, p3):
    a = np.linalg.norm(p2 - p1)
    b = np.linalg.norm(p3 - p2)
    c = np.linalg.norm(p1 - p3)
    # Ensure correct calculation for obtuse angles
    angle = np.degrees(np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)))
    if angle > 180:
        angle = 360 - angle
    return angle

# Initialize PoseNet model
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Video input setup
cap = cv2.VideoCapture(0)

# Changing the dimensions
original_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
original_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
original_aspect_ratio = original_width / original_height

new_width = 10000  # Adjust desired width
new_height = new_width / original_aspect_ratio

cap.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)

engine = pyttsx3.init()

previous_form = None

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        ret, frame = cap.read()

        # Laterally invert the frame
        frame = cv2.flip(frame, 1)  # Flip code 1 for horizontal inversion

        # Pre-process frame for PoseNet
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img.flags.writeable = False

        # Margin of error
        moe = 7.5

        # Run PoseNet inference on GPU
        results = pose.process(img)

        # Re-enable writing to the image
        img.flags.writeable = True

        # Extract keypoint data
        if results.pose_landmarks:
            keypoints = [(int(kp.x * img.shape[1]), int(kp.y * img.shape[0]))
                         for kp in results.pose_landmarks.landmark]

            # Calculate angles for left arm
            shoulder_left = np.array(keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER])
            elbow_left = np.array(keypoints[mp_pose.PoseLandmark.LEFT_ELBOW])
            wrist_left = np.array(keypoints[mp_pose.PoseLandmark.LEFT_WRIST])

            # Calculate angles for right arm
            shoulder_right = np.array(keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER])
            elbow_right = np.array(keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW])
            wrist_right = np.array(keypoints[mp_pose.PoseLandmark.RIGHT_WRIST])

            # Draw lines for shoulders and arms
            cv2.line(img, shoulder_left, elbow_left, (255, 0, 0), 2)
            cv2.line(img, elbow_left, wrist_left, (255, 0, 0), 2)
            cv2.line(img, shoulder_right, elbow_right, (255, 0, 0), 2)
            cv2.line(img, elbow_right, wrist_right, (255, 0, 0), 2)

            # Shoulder press detection
            form = None
            if elbow_left[1] > shoulder_left[1] and elbow_right[1] > shoulder_right[1]:
                form = "Correct Form"
            elif elbow_left[1] <= shoulder_left[1] and elbow_right[1] <= shoulder_right[1]:
                form = "Incorrect Form"
            else:
                form = "Partial Form"

            # Speak the shoulder press form
            if form != previous_form:
                previous_form = form
                engine.say(form)
                engine.runAndWait()

            # Display text indicating shoulder press form
            cv2.putText(img, f"Shoulder Press Form: {form}", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Visualization
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Display frame with keypoints, angles, and alignment status (optional)
            cv2.imshow("Pose Estimation", img)

        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Pose Estimation', cv2.WND_PROP_VISIBLE) == False:
            break

cap.release()
cv2.destroyAllWindows()
