import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hand and Face Detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_face_detection = mp.solutions.face_detection

# Initialize video capture
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# Define a function to classify gestures based on landmarks
def classify_gesture(landmarks, image_height, image_width, face_bbox=None):
    # Get landmark positions (normalized x, y, z)
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    thumb_base = landmarks[2]

    # Convert normalized coordinates to image space
    thumb_tip_x, thumb_tip_y = int(thumb_tip.x * image_width), int(thumb_tip.y * image_height)
    index_tip_x, index_tip_y = int(index_tip.x * image_width), int(index_tip.y * image_height)
    thumb_base_y = int(thumb_base.y * image_height)

    # Gesture: Thumbs Up
    if thumb_tip_y < thumb_base_y and index_tip_y > thumb_base_y:
        return "Gesture: Thumbs up"

    # Gesture: Hi (Waving Hand)
    if thumb_tip.y < landmarks[3].y and index_tip.y < landmarks[6].y:
        return "Gesture: Hi"

    # Gesture: Danger (Closed fist)
    if all([landmarks[finger].y > landmarks[finger - 2].y for finger in [4, 8, 12, 16, 20]]):
        return "Gesture: Danger"

    # Gesture: Help (Open hand)
    if all([landmarks[finger].y < landmarks[finger - 2].y for finger in [8, 12, 16, 20]]):
        return "Gesture: Help"

    # Gesture: Fist
    if all([landmarks[finger].y > landmarks[finger - 2].y for finger in [8, 12, 16, 20]]):
        return "Gesture: Yes"

    # Gesture: Peace (V-sign)
    if (landmarks[8].y < landmarks[6].y and  # Index finger extended
        landmarks[12].y < landmarks[10].y and  # Middle finger extended
        landmarks[16].y > landmarks[14].y and  # Ring finger curled
        landmarks[20].y > landmarks[18].y):  # Pinky curled
        return "Gesture: Peace (V-sign)"

    # Gesture: Okay
    if (abs(index_tip.x - thumb_tip.x) < 0.05 and
        landmarks[12].y < landmarks[10].y and
        landmarks[16].y < landmarks[14].y and
        landmarks[20].y < landmarks[18].y):
        return "Gesture: Okay"

    # Gesture: Pointing to Face (I)
    if face_bbox:
        face_x1, face_y1, face_x2, face_y2 = face_bbox
        if face_x1 <= index_tip_x <= face_x2 and face_y1 <= index_tip_y <= face_y2:
            return "Gesture: I"

    # Gesture: Pointing
    if (landmarks[8].y < landmarks[6].y and
        landmarks[12].y > landmarks[10].y and
        landmarks[16].y > landmarks[14].y and
        landmarks[20].y > landmarks[18].y):
        return "Gesture: Pointing"

    return "Unknown Gesture"

# Initialize MediaPipe Hands and Face Detection
with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands, \
        mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:

    # OpenCV window for full-screen mode
    cv2.namedWindow("Hand Gesture Recognition with Face Detection", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Hand Gesture Recognition with Face Detection", cv2.WND_PROP_FULLSCREEN, 1)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Get frame dimensions
        frame_height, frame_width, _ = frame.shape

        # Convert the BGR image to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame for hand landmarks and face detection
        hand_results = hands.process(frame_rgb)
        face_results = face_detection.process(frame_rgb)

        # Get face bounding box
        face_bbox = None
        if face_results.detections:
            for detection in face_results.detections:
                bboxC = detection.location_data.relative_bounding_box
                face_x1 = int(bboxC.xmin * frame_width)
                face_y1 = int(bboxC.ymin * frame_height)
                face_x2 = face_x1 + int(bboxC.width * frame_width)
                face_y2 = face_y1 + int(bboxC.height * frame_height)
                face_bbox = (face_x1, face_y1, face_x2, face_y2)

                # Draw face bounding box
                #cv2.rectangle(frame, (face_x1, face_y1), (face_x2, face_y2), (135, 132, 134), 2)

        # Draw hand landmarks and classify gestures
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract landmarks and classify gesture
                landmarks = hand_landmarks.landmark
                gesture = classify_gesture(landmarks, frame_height, frame_width, face_bbox)

                # Display gesture on the frame
                cv2.putText(frame, gesture, (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

        # Show the frame
        cv2.imshow('Hand Gesture Recognition with Face Detection', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
