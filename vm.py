import cv2
import mediapipe as mp
import pyautogui
import time
import atexit

pyautogui.FAILSAFE = False

# Constants
CAMERA_WIDTH = 960
CAMERA_HEIGHT = 540
FRAME_REDUCTION = 150
SMOOTHENING = 6
CURSOR_SPEED = 1.3
ACTION_DELAY = 0.6
HAND_CONFIDENCE_THRESHOLD = 0.5
MODE_TOGGLE_TIME = 2.0
SCROLL_DEBOUNCE = 0.2
CURSOR_DEADZONE = 5

# Initialize camera and hand detection
cap = cv2.VideoCapture(0)
cap.set(3, CAMERA_WIDTH)
cap.set(4, CAMERA_HEIGHT)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=HAND_CONFIDENCE_THRESHOLD,
    min_tracking_confidence=HAND_CONFIDENCE_THRESHOLD
)
draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()

# State variables
prev_x, prev_y = 0, 0
last_action = 0
last_scroll = 0
mode_timer = 0
game_mode = False
active_keys = set()

# FPS tracking
fps_time = time.time()
fps_count = 0

def fingers_up(lm):
    """Detect which fingers are raised"""
    tips = [8, 12, 16, 20]
    return [lm[t].y < lm[t-2].y for t in tips]

def cleanup():
    """Release resources properly"""
    for key in active_keys:
        pyautogui.keyUp(key)
    hands.close()
    cap.release()
    cv2.destroyAllWindows()

# Register cleanup on exit
atexit.register(cleanup)

while True:
    success, img = cap.read()
    if not success:
        print("⚠️ Camera read failed! Retrying...")
        continue

    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture_name = "None"

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        handedness = result.multi_handedness[0]
        confidence = handedness.classification[0].score
        
        # Only process if confidence is above threshold
        if confidence > HAND_CONFIDENCE_THRESHOLD:
            lm = hand.landmark
            fingers = fingers_up(lm)
            now = time.time()

            # MODE TOGGLE
            if fingers[0] and not fingers[1] and not fingers[2] and fingers[3]:
                gesture_name = "Mode Toggle"
                if mode_timer == 0:
                    mode_timer = now
                elif now - mode_timer > MODE_TOGGLE_TIME:
                    game_mode = not game_mode
                    mode_timer = 0
                    # Release all keys when switching modes
                    for key in active_keys:
                        pyautogui.keyUp(key)
                    active_keys.clear()
                    time.sleep(1)
            else:
                mode_timer = 0

            if game_mode:
                cv2.putText(img,"GAME MODE",(20,50),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                if fingers == [False, False, False, False]:
                    gesture_name = "Accelerate"
                    if 'right' not in active_keys:
                        pyautogui.keyDown('right')
                        active_keys.add('right')
                else:
                    if 'right' in active_keys:
                        pyautogui.keyUp('right')
                        active_keys.discard('right')

                if fingers == [True, True, True, True]:
                    gesture_name = "Brake"
                    if 'left' not in active_keys:
                        pyautogui.keyDown('left')
                        active_keys.add('left')
                else:
                    if 'left' in active_keys:
                        pyautogui.keyUp('left')
                        active_keys.discard('left')

                if fingers[0] and fingers[1] and not fingers[2]:
                    gesture_name = "Neutral"
                    for key in ['right', 'left']:
                        if key in active_keys:
                            pyautogui.keyUp(key)
                            active_keys.discard(key)

                if lm[4].y < lm[3].y and not fingers[0]:
                    gesture_name = "Boost"
                    if 'up' not in active_keys:
                        pyautogui.keyDown('up')
                        active_keys.add('up')
                else:
                    if 'up' in active_keys:
                        pyautogui.keyUp('up')
                        active_keys.discard('up')

            else:
                cv2.putText(img,"MOUSE MODE",(20,50),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

                x = int(lm[8].x*w)
                y = int(lm[8].y*h)

                # LEFT CLICK (debounced)
                if fingers[0] and fingers[1] and not fingers[2] and now-last_action > ACTION_DELAY:
                    gesture_name = "Left Click"
                    pyautogui.click()
                    last_action = now

                # Move cursor with deadzone
                elif fingers[0] and not fingers[1]:
                    gesture_name = "Move Cursor"

                    mapped_x = (x-FRAME_REDUCTION)*screen_w/(w-2*FRAME_REDUCTION)
                    mapped_y = (y-FRAME_REDUCTION)*screen_h/(h-2*FRAME_REDUCTION)

                    mapped_x = max(0,min(screen_w,mapped_x))
                    mapped_y = max(0,min(screen_h,mapped_y))

                    mapped_x *= CURSOR_SPEED
                    mapped_y *= CURSOR_SPEED

                    # Apply smoothing
                    curr_x = prev_x + (mapped_x-prev_x)/SMOOTHENING
                    curr_y = prev_y + (mapped_y-prev_y)/SMOOTHENING

                    # Deadzone filter to reduce jitter
                    if abs(curr_x - prev_x) > CURSOR_DEADZONE or abs(curr_y - prev_y) > CURSOR_DEADZONE:
                        pyautogui.moveTo(curr_x,curr_y)
                        prev_x, prev_y = curr_x, curr_y

                # Scroll Up (debounced)
                elif lm[4].y < lm[3].y and not fingers[0] and now - last_scroll > SCROLL_DEBOUNCE:
                    gesture_name = "Scroll Up"
                    pyautogui.scroll(30)
                    last_scroll = now

                # Scroll Down (debounced)
                elif lm[4].y > lm[3].y and not fingers[0] and now - last_scroll > SCROLL_DEBOUNCE:
                    gesture_name = "Scroll Down"
                    pyautogui.scroll(-30)
                    last_scroll = now

            # Draw hand landmarks
            draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

    # Display gesture name
    cv2.putText(img, f"Gesture: {gesture_name}", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
    
    # FPS counter
    fps_count += 1
    if time.time() - fps_time > 1:
        fps = fps_count / (time.time() - fps_time)
        fps_time = time.time()
        fps_count = 0
        cv2.putText(img, f"FPS: {fps:.1f}", (20, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 0), 2)

    cv2.imshow("Gesture Control", img)

    if cv2.waitKey(1) == 27:  # ESC key to exit
        break

cleanup()