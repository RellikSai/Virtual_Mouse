# 🖐️ Virtual Mouse Using Computer Vision (MediaPipe + Python)

Control your computer **entirely with hand gestures** using your webcam.
This project turns your hand into a **virtual mouse**, supporting cursor movement, clicks, drag, scroll, zoom, right-click, and even window closing — all powered by **MediaPipe Hand Landmarker** and **PyAutoGUI**.

---

## ✨ Features

### 🖱️ Cursor Movement
- Move your **index finger** to control the mouse pointer
- Smooth motion using **Exponential Moving Average (EMA)** filtering
- **Active margin** prevents unintended movement near camera edges

---

### 👆 Left Click
- **Gesture:** Pinch **thumb + index finger**
- **Action:** Single left click
- Includes debounce protection to avoid double clicks

---

### ✊ Click & Drag
- **Gesture:** Hold **thumb + index finger** together for ~0.5 seconds
- **Action:** Click and drag
- Drag releases automatically when fingers separate

---

### 👉 Right Click
- **Gesture:** Pinch **thumb + middle finger**
- **Action:** Right click
- Debounced for stability

---

### 🖱️ Scroll & Zoom
- **Gesture:** Pinch **middle finger + pinky**
- **Action:** Scroll vertically
  - Smaller thumb–index distance → scroll down
  - Larger thumb–index distance → scroll up
- Enables zooming in supported applications

---

### ❌ Close Active Window
- **Gesture:** Pinch **thumb + pinky**
- **Action:** `Alt + F4`
- Extra debounce time prevents accidental closure

---

### 📊 Visual HUD
- Displays real-time hand landmarks on the video feed
- Useful for debugging and calibration
- Can be toggled via `SHOW_HUD`

---

## 🧠 How It Works

1. Captures live video using **OpenCV**
2. Detects hand landmarks via **MediaPipe Hand Landmarker**
3. Calculates distances between specific fingers
4. Maps gestures to mouse/keyboard actions using **PyAutoGUI**
5. Smooths cursor movement for a natural experience

---

## 🛠️ Requirements

### Hardware
- Webcam
- Good lighting conditions

### Software
- Python **3.9 – 3.13**
- Supported platforms:
  - Windows
  - macOS
  - Linux (X11 recommended)

---

## 📦 Dependencies

Install required libraries:

```bash
pip install opencv-python numpy pyautogui mediapipe
