import cv2
import mediapipe as mp
import serial
import time

# Initialize serial communication with Arduino
arduino = serial.Serial('COM5', 9600)  # Change 'COM5' to your Arduino's port
time.sleep(2)  # Wait for the serial connection to initialize

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Function to send commands to Arduino
def send_command(command):
    arduino.write(command.encode())
    time.sleep(0.1)  # Short delay to prevent command flooding-------------------------------------------------------------------------------------------
def calculate_distance(landmark1, landmark2):
    return ((landmark1.x - landmark2.x) ** 2 + (landmark1.y - landmark2.y) ** 2) ** 0.5

# Start video capture
cap = cv2.VideoCapture(0)  # Change the index if you have multiple cameras

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip for a mirror view
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extract landmark coordinates
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]


            # Calculate distance between thumb and index finger tips
            thumb_index_distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
            thumb_middle_distance = calculate_distance(thumb_tip, middle_tip)
            index_middle_distance = calculate_distance(index_tip, middle_tip)
            thumb_ring_distance = calculate_distance(thumb_tip, ring_tip)


            if thumb_index_distance < 0.05:
                cv2.putText(frame, 'Forward', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                send_command('F')
            elif thumb_middle_distance < 0.05:
                cv2.putText(frame, 'Backward', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                send_command('B')
            elif index_middle_distance < 0.05:
                cv2.putText(frame, 'Left', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                send_command('L')
            elif thumb_ring_distance < 0.05:
                cv2.putText(frame, 'Right', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                send_command('R')
            else:
                cv2.putText(frame, 'Stop', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                send_command('S')

    cv2.imshow('Gesture Controlled Car', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
