# Virtual_Mouse

A real-time computer vision system that enables touchless control of the mouse and keyboard using hand gestures detected through a webcam.  Built using OpenCV, MediaPipe, and PyAutoGUI, this project transforms 21-point hand landmark detection into system-level cursor movement, scrolling, clicking, and game controls.

✨ Features

🖱️ Mouse Mode
1. Cursor movement using index finger tracking
2. Gesture-based left click
3. Scroll up & down using thumb gestures
4. Smooth cursor motion with interpolation
5. Frame reduction mapping for precision

🎮 Game Mode
1. Accelerate (All fingers closed)
2. Brake (All fingers open)
3. Boost (Thumb gesture)
4. Gesture-based mode switching (2-second hold detection)
5. Real-time key press simulation

🧠 Technical Overview

1️⃣ Hand Landmark Detection
1. Uses MediaPipe Hands
2. Extracts 21 3D hand landmarks
3. Tracks fingertip indices: 8, 12, 16, 20
4. Thumb orientation detection using landmark comparison

2️⃣ Gesture Recognition Logic
1. Rule-based finger state detection (fingers_up() function)
2. Boolean landmark comparison (no ML classifier)
3. Time-based debounce logic to prevent accidental triggers
4. Gesture priority control to avoid conflicts

🛠 Tech Stack
1) Python 3.10 / 3.11
2) OpenCV
3) MediaPipe
4) PyAutoGUI

⚙️ How It Works
1. Webcam captures live video
2. MediaPipe detects hand landmarks
3. Finger states are computed
4. Gesture conditions trigger mouse or keyboard events
5. Cursor movement is smoothed for stability

📈 Applications
1. Touchless Human-Computer Interaction
2. Accessibility Tools
3. Smart Gaming Controls
4. Gesture-Based Interfaces
5. AR/VR Interaction Foundations

⚠️ Limitations
1) Sensitive to lighting conditions
2) Single-hand tracking only
3) Rule-based gesture detection (not ML-trained)
4) Performance depends on camera quality

🔮 Future Improvements

1) Machine learning-based gesture classification
2) Multi-hand support
3) Drag & drop gesture
4) Custom gesture configuration
5) GUI-based control panel

📜 License

This project is open-source and available under the MIT License.
