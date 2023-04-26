import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

webcam = cv2.VideoCapture(0)

x1 = 0
x2 = 0
y1 = 0
y2 = 0

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands:
    while webcam.isOpened():
        ret, frame = webcam.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        height, width, _ = image.shape

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        line_setup =  mp_drawing.DrawingSpec(
                        color=(121, 44, 250),
                        thickness=2,
                        circle_radius=2,
                    )
        bump_setup = mp_drawing.DrawingSpec(
                        color=(121, 22, 76),
                        thickness=2,
                        circle_radius=4,
                    )

        detected_hands = results.multi_hand_landmarks

        if detected_hands:
            for hand in detected_hands:
                mp_drawing.draw_landmarks(image, 
                    hand, 
                    mp_hands.HAND_CONNECTIONS,
                    bump_setup,
                    line_setup,                    
                )
                landmarks = hand.landmark

                for id, landmark in enumerate(landmarks):
                    
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    # Mutatóujj
                    if id == 8:
                        cv2.circle(
                            img=image, 
                            center=(x,y),
                            radius=8,
                            color=(240,0,0),
                            thickness=8,
                        )
                        x1 = x
                        y1 = y
                    # Hüvelykujj
                    if id == 4:
                        cv2.circle(
                            img=image, 
                            center=(x,y),
                            radius=8,
                            color=(0,0,240),
                            thickness=8,
                        )
                        x2 = x
                        y2 = y
                    
            distance = ((x2-x1)**2 + (y2-y1)**2)**(0.5)//4

            cv2.line(image, (x1, y1), (x2, y2), color=(0,250,0),thickness=5)
            if distance > 65:
                pyautogui.press("volumeup")
            if distance < 10:
                pyautogui.press("volumedown")

                    
                    # print(results.multi_hand_landmarks)


        cv2.imshow("Hand tracking", image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    webcam.release()
    cv2.destroyAllWindows()


