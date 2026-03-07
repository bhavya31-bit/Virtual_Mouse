# Virtual_Mouse 🖱️

A real-time computer vision system that enables **touchless control** of the mouse and keyboard using hand gestures detected through a webcam. Built using OpenCV, MediaPipe, and PyAutoGUI, this project transforms 21-point hand landmark detection into system-level cursor movement, scrolling, clicking, and game controls.

**Status:** ⚡ Optimized & Production-Ready (v2.0 with performance improvements)

🚀 Recent Optimizations (v2.0)

**Performance & Stability Improvements:**
- ⚡ **Smart Key Management** - Reduces OS calls by tracking active keys intelligently
- 🎯 **Cursor Deadzone** - Eliminates jitter with 5px movement threshold
- 🔇 **Scroll Debouncing** - Prevents scroll spam with 0.2s debounce intervals
- 📊 **FPS Monitoring** - Real-time performance tracking on display
- 🛡️ **Confidence Filtering** - Only processes high-confidence hand detections (>0.5)
- 🔧 **Configurable Constants** - Easy tuning: SMOOTHENING, CURSOR_SPEED, FRAME_REDUCTION, etc.
- 🧹 **Proper Resource Cleanup** - Automatic cleanup on exit with atexit handler
- 🚨 **Better Error Handling** - Graceful camera failure recovery
- 🎮 **Key Release on Mode Switch** - Prevents stuck keys when toggling modes

**Technical Details:**
```
Cursor Chain: Hand Detection → Confidence Filter → Landmark Extraction 
            → Finger State Detection → Gesture Recognition → Mouse/Keyboard Control
            
Key Improvements:
- Reduced redundant keyDown/keyUp calls via active_keys set
- Smoothing + Deadzone combination for optimal responsiveness
- Hand confidence threshold filters noisy detections
- FPS counter helps identify bottlenecks
```

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
2. MediaPipe detects hand landmarks & validates confidence
3. Finger states are computed using landmark positions
4. Gesture conditions trigger mouse or keyboard events
5. Cursor movement is smoothed & filtered for stability
6. Real-time FPS monitoring ensures performance

**Gesture Recognition Pipeline:**
```
Video Frame → Hand Detection → Landmark Extraction (21 points)
           → Confidence Check (must be > 0.5)
           → Finger State Analysis (8,12,16,20 indices)
           → Gesture Classification (Rule-based)
           → Action Execution (Mouse/Keyboard)
```

🔧 Configuration

All tuning parameters are at the top of `vm.py`:

```python
CAMERA_WIDTH = 960              # Camera resolution width
CAMERA_HEIGHT = 540             # Camera resolution height
FRAME_REDUCTION = 150           # Pixel margin for cursor mapping
SMOOTHENING = 6                 # Cursor smoothing factor (higher = smoother)
CURSOR_SPEED = 1.3              # Cursor movement multiplier
ACTION_DELAY = 0.6              # Debounce for click actions (seconds)
HAND_CONFIDENCE_THRESHOLD = 0.5 # Min confidence for hand detection (0.0-1.0)
MODE_TOGGLE_TIME = 2.0          # Duration to hold for mode switch (seconds)
SCROLL_DEBOUNCE = 0.2           # Min interval between scroll events (seconds)
CURSOR_DEADZONE = 5             # Pixel threshold to filter jitter (pixels)
```

**Tuning Tips:**
- 🐢 Increase `SMOOTHENING` if cursor feels jittery
- 🚀 Decrease `SMOOTHENING` if cursor feels laggy
- ⚡ Increase `CURSOR_SPEED` for faster cursor movement
- 📍 Increase `CURSOR_DEADZONE` if seeing unwanted micro-movements
- 📜 Adjust `SCROLL_DEBOUNCE` for scroll sensitivity
- 🎯 Increase `HAND_CONFIDENCE_THRESHOLD` if getting false hand detections

� Tech Stack
1) Python 3.10 / 3.11
2) OpenCV (`cv2`)
3) MediaPipe (`mediapipe`)
4) PyAutoGUI (`pyautogui`)

📦 Installation & Setup

**Prerequisites:**
- Python 3.10 or 3.11
- Webcam/Camera device
- Windows/macOS/Linux

**Quick Start:**
```bash
# Clone the repository
git clone <repo-url>
cd Virtual_Mouse

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install opencv-python mediapipe pyautogui

# Run the application
python vm.py
```

**How to Use:**
- 🚪 Press `ESC` to exit
- 🔀 Hold 👍👎 (thumb + pinky up) for 2 seconds to toggle modes
- 📊 Watch FPS counter for performance (top-left corner)
- 🎮 Game Mode (Red): Accelerate/Brake with finger gestures
- 🖱️ Mouse Mode (Green): Move cursor, click, scroll

�📈 Applications
1. Touchless Human-Computer Interaction
2. Accessibility Tools
3. Smart Gaming Controls
4. Gesture-Based Interfaces
5. AR/VR Interaction Foundations

⚠️ Limitations
1) Sensitive to lighting conditions (use well-lit environments)
2) Single-hand tracking only (dual-hand support coming soon)
3) Rule-based gesture detection (not ML-trained)
4) Performance depends on camera quality
5) Works best with clear hand visibility

📋 Changelog

**v2.0 (Latest) - Optimization Release**
- ✅ Smart key management reduces OS overhead
- ✅ Cursor deadzone eliminates jitter
- ✅ Scroll debouncing prevents spam
- ✅ Hand confidence filtering improves accuracy
- ✅ Configurable constants for easy tuning
- ✅ Real-time FPS counter for performance monitoring
- ✅ Improved error handling & resource cleanup
- ✅ Tested and verified for production use

**v1.0 - Initial Release**
- Basic mouse control with gestures
- Game mode with keyboard controls
- Real-time hand detection

🔮 Future Improvements

1) Machine learning-based gesture classification
2) Multi-hand support for complex gestures
3) Drag & drop gesture implementation
4) Custom gesture configuration UI
5) GUI-based control panel with visual settings
6) Gesture recording & playback
7) Hand pose classification (open/closed/pointing)
8) Performance optimization for lower-end hardware
🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Camera not detected | Check camera permissions, try different USB port |
| Jittery cursor movement | Increase `SMOOTHENING` value (e.g., 8-10) |
| Cursor moves too fast | Decrease `CURSOR_SPEED` (e.g., 0.8-1.0) |
| Gestures not recognized | Improve lighting, ensure hand is clearly visible |
| Scroll not working | Adjust `SCROLL_DEBOUNCE` to lower value (0.1-0.15) |
| Low FPS (<20) | Close other applications, reduce camera resolution |
| Hand detection fails | Increase `HAND_CONFIDENCE_THRESHOLD` to 0.3-0.4 |
| Stuck key presses | Press ESC and restart, this is handled automatically in v2.0 |

💡 Best Practices

1. **Lighting** - Use natural or LED lighting, avoid backlighting
2. **Distance** - Keep hand 30-60cm from camera for best detection
3. **Background** - Use contrasting backgrounds (not white walls)
4. **Speed** - Move hand gestures slowly and deliberately
5. **Calibration** - Test gestures in your environment first
6. **Performance** - Monitor FPS counter, close other resource-heavy apps
7. **Accessibility** - Great for accessibility needs, test with varied hand positions

📞 Support & Contributing

Found a bug or have suggestions? 
- Create an issue on GitHub
- Test the latest v2.0 optimized version
- Share your feedback and use cases!

**Contributors Welcome:** Fork the repository and submit pull requests!
📜 License

This project is open-source and available under the MIT License.
