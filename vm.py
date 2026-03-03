import cv2
import mediapipe as mp
import pyautogui
import time

pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)
cap.set(3, 960)
cap.set(4, 540)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()

frame_reduction = 150
smoothening = 6
cursor_speed = 1.3

prev_x, prev_y = 0, 0
last_action = 0
action_delay = 0.6

game_mode = False
mode_timer = 0

def fingers_up(lm):
    tips = [8, 12, 16, 20]
    return [lm[t].y < lm[t-2].y for t in tips]

while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture_name = "None"

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            lm = hand.landmark
            fingers = fingers_up(lm)
            now = time.time()

            # MODE TOGGLE
            if fingers[0] and not fingers[1] and not fingers[2] and fingers[3]:
                gesture_name = "Mode Toggle"
                if mode_timer == 0:
                    mode_timer = now
                elif now - mode_timer > 2:
                    game_mode = not game_mode
                    mode_timer = 0
                    time.sleep(1)
            else:
                mode_timer = 0

            if game_mode:
                cv2.putText(img,"GAME MODE",(20,50),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                if fingers == [False, False, False, False]:
                    gesture_name = "Accelerate"
                    pyautogui.keyDown('right')
                else:
                    pyautogui.keyUp('right')

                if fingers == [True, True, True, True]:
                    gesture_name = "Brake"
                    pyautogui.keyDown('left')
                else:
                    pyautogui.keyUp('left')

                if fingers[0] and fingers[1] and not fingers[2]:
                    gesture_name = "Neutral"
                    pyautogui.keyUp('right')
                    pyautogui.keyUp('left')

                if lm[4].y < lm[3].y and not fingers[0]:
                    gesture_name = "Boost"
                    pyautogui.keyDown('up')
                else:
                    pyautogui.keyUp('up')

            else:
                cv2.putText(img,"MOUSE MODE",(20,50),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

                x = int(lm[8].x*w)
                y = int(lm[8].y*h)

                # ✅ LEFT CLICK FIRST (IMPORTANT FIX)
                if fingers[0] and fingers[1] and not fingers[2] and now-last_action > action_delay:
                    gesture_name = "Left Click"
                    pyautogui.click()
                    last_action = now

                # Move cursor
                elif fingers[0] and not fingers[1]:
                    gesture_name = "Move Cursor"

                    mapped_x = (x-frame_reduction)*screen_w/(w-2*frame_reduction)
                    mapped_y = (y-frame_reduction)*screen_h/(h-2*frame_reduction)

                    mapped_x = max(0,min(screen_w,mapped_x))
                    mapped_y = max(0,min(screen_h,mapped_y))

                    mapped_x *= cursor_speed
                    mapped_y *= cursor_speed

                    curr_x = prev_x + (mapped_x-prev_x)/smoothening
                    curr_y = prev_y + (mapped_y-prev_y)/smoothening

                    pyautogui.moveTo(curr_x,curr_y)
                    prev_x, prev_y = curr_x, curr_y

                # Scroll Up
                elif lm[4].y < lm[3].y and not fingers[0]:
                    gesture_name = "Scroll Up"
                    pyautogui.scroll(30)

                # Scroll Down
                elif lm[4].y > lm[3].y and not fingers[0]:
                    gesture_name = "Scroll Down"
                    pyautogui.scroll(-30)

            draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

    cv2.putText(img, f"Gesture: {gesture_name}", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

    cv2.imshow("Gesture Control", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()