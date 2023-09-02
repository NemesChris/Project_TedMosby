import cv2
import mediapipe as mp
import pyautogui
import pygetwindow
import time

# from ini file
selected_webcam = 1
max_number_of_hands = 1
increase_volume_distance = 65
decrease_volume_distance = 15

# inner variables
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
pTime = 0
mutatoX = 0
huvelykX = 0
kozepsoX = 0
mutatoY = 0
huvelykY = 0
kozepsoY = 0

screenX, screenY = pyautogui.size()
cv2font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255, 0, 0)
fontThickness = 2

def get_video_capture_devices():
    index = 0
    arr = []
    names = []
    while True:
        cap = cv2.VideoCapture(index)
        try:
            arr.append(index)
            names.append(cap.getBackendName())
        except Exception as exc:
            print(exc)
            break
        cap.release()
        index += 1
    return arr, names

print('')
print('')
print('PROGRAM STARTING...')
print('')

arr, names = get_video_capture_devices()
print('DEVICES AND NAMES:')
for i in arr[:-1]:
    print(f'{i} - {names[i]}')
print('')

cap = cv2.VideoCapture(selected_webcam)
webcam = cap
print('SELECTED CAM:')
print(selected_webcam)
print('')

windows = pygetwindow.getAllWindows()
print("FOUND WINDOWS:")
available_windows = []
for window in windows:
    if 'Mozilla Firefox' in str(window.title):
        available_windows.append(window)
        print(window)
        print('')
print('')

print("CAMERA OPENED?")
print(webcam.isOpened())
print('')

with mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5,
    max_num_hands=max_number_of_hands,
) as hands:
    while webcam.isOpened():
        ret, frame = webcam.read()

        invert_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(invert_image, 1)
        height, width, _ = image.shape

        # calculate FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(
            image,
            f'FPS:{int(fps)}',
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        line_setup = mp_drawing.DrawingSpec(
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
                mp_drawing.draw_landmarks(
                    image,
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
                            center=(x, y),
                            radius=8,
                            color=(240, 0, 0),
                            thickness=8,
                        )
                        mutatoX = x
                        mutatoY = y
                    # Hüvelykujj
                    if id == 4:
                        cv2.circle(
                            img=image,
                            center=(x, y),
                            radius=8,
                            color=(0, 0, 240),
                            thickness=8,
                        )
                        huvelykX = x
                        huvelykY = y
                    # Kozepsoujj
                    if id == 12:
                        cv2.circle(
                            img=image,
                            center=(x, y),
                            radius=8,
                            color=(0, 0, 240),
                            thickness=8,
                        )
                        kozepsoX = x
                        kozepsoY = y

            middle_distance = ((huvelykY-kozepsoY)**2)**(0.5)//4

            # vonal a középső gombhoz
            cv2.line(
                image,
                (kozepsoX, kozepsoY),
                (huvelykX, huvelykY),
                color=(0, 250, 250),
                thickness=5,
            )

            # középsőujjtávolság kiírása
            org = (kozepsoX+20, kozepsoY)
            if middle_distance:
                # középsőujj távolság
                cv2.putText(
                    image,
                    str(middle_distance),
                    org,
                    cv2font,
                    fontScale,
                    fontColor,
                    fontThickness,
                    cv2.LINE_AA,
                )

                volume_distance = (
                    (huvelykX-mutatoX)**2 + (huvelykY-mutatoY)**2
                )**(0.5)//4
                if volume_distance:
                    # HANGERŐ ÁLLÍTÁSA
                    if middle_distance > 30:
                        # vonal a hangerőcsík mutatására ZÖLD - változtatható
                        cv2.line(
                            image,
                            (mutatoX, mutatoY),
                            (huvelykX, huvelykY),
                            color=(0, 250, 0),
                            thickness=5,
                        )
                        org = (mutatoX+20, mutatoY)
                        # hangerőtávolság
                        cv2.putText(
                            image,
                            str(volume_distance),
                            org,
                            cv2font,
                            fontScale,
                            fontColor,
                            fontThickness,
                            cv2.LINE_AA,
                        )
                        # hangerőszabályzás
                        if volume_distance > increase_volume_distance:
                            pyautogui.press("volumeup")
                        if volume_distance < decrease_volume_distance:
                            pyautogui.press("volumedown")
                    else:
                        # EGÉR VEZÉRLÉSE
                        # vonal a hangerőcsík mutatására KÉK - nem fog változni
                        cv2.line(
                            image,
                            (mutatoX, mutatoY),
                            (huvelykX, huvelykY),
                            color=(0, 0, 250),
                            thickness=5,
                        )
                        org = (mutatoX+20, mutatoY)
                        # hangerőtávolság
                        cv2.putText(
                            image,
                            str(volume_distance),
                            org,
                            cv2font,
                            fontScale,
                            fontColor,
                            fontThickness,
                            cv2.LINE_AA,
                        )

        cv2.imshow("Hand tracking", image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    webcam.release()
    cv2.destroyAllWindows()





#pyautogui.moveTo(sreenX/2, screenY/2, 2)   # moves mouse to X of 100, Y of 200 over 2 seconds

# pyautogui.doubleClick()  # perform a left-button double click

# pyautogui.click(button='right', clicks=3, interval=0.25)  ## triple-click the right mouse button with a quarter second pause in between clicks