# Virtual_Mouse
A real-time computer vision system that enables touchless control of the mouse and keyboard using hand gestures detected through a webcam.  Built using OpenCV, MediaPipe, and PyAutoGUI, this project transforms 21-point hand landmark detection into system-level cursor movement, scrolling, clicking, and game controls.

✨ Features
🖱️ Mouse Mode

Cursor movement using index finger tracking
Gesture-based left click
Scroll up & down using thumb gestures
Smooth cursor motion with interpolation
Frame reduction mapping for precision

🎮 Game Mode

Accelerate (All fingers closed)
Brake (All fingers open)
Boost (Thumb gesture)
Gesture-based mode switching (2-second hold detection)
Real-time key press simulation

🧠 Technical Overview
1️⃣ Hand Landmark Detection

Uses MediaPipe Hands
Extracts 21 3D hand landmarks
Tracks fingertip indices: 8, 12, 16, 20
Thumb orientation detection using landmark comparison

2️⃣ Gesture Recognition Logic

Rule-based finger state detection (fingers_up() function)
Boolean landmark comparison (no ML classifier)
Time-based debounce logic to prevent accidental triggers
Gesture priority control to avoid conflicts

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

Sensitive to lighting conditions
Single-hand tracking only
Rule-based gesture detection (not ML-trained)
Performance depends on camera quality

🔮 Future Improvements

Machine learning-based gesture classification
Multi-hand support
Drag & drop gesture
Custom gesture configuration
GUI-based control panel

📜 License

This project is open-source and available under the MIT License.
