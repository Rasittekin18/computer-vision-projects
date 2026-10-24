# 🖐️ Real-Time Hand Gesture & Landmark Tracking with OpenCV & MediaPipe

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Solutions-orange.svg)](https://developers.google.com/mediapipe)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end computer vision application that performs **real-time hand detection and 21-point landmark tracking** using Google's **MediaPipe** framework and **OpenCV**. 

The system captures video input from a webcam or video file, detects hand regions using a Palm Detection model, locates 21 key structural hand joint landmarks in 3D, converts them into pixel coordinates, and tracks them seamlessly with real-time FPS overlay.

---

## 📌 Features

- **Real-Time Hand Detection & Tracking:** Leverages MediaPipe's lightweight two-stage pipeline (Palm Detector + Hand Landmark Model).
- **21 Landmark Coordinates Mapping:** Identifies 3D coordinates ($x, y, z$) for all major hand joints (wrist, knuckles, finger tips) and maps them to 2Pixel $(x, y)$ frame locations.
- **Specific Landmark Highlighting:** Demonstrates how to target and extract specific joints by landmark ID (e.g., Thumb Tip `ID 4`, Pinky Tip `ID 20`).
- **Live Performance Metrics:** Calculates and visually renders real-time **FPS (Frames Per Second)** directly onto the video feed.
- **Multi-Hand Support:** Easily configurable to track single or multiple hands simultaneously.
- **Flexible Video Source:** Supports live webcam streams, pre-recorded video files, and static image analysis.

---

## 🛠️ Tech Stack & Prerequisites

* **Language:** Python 3.8+
* **Core Libraries:**
  * `opencv-python` (Computer Vision & Video Processing)
  * `mediapipe` (Hand Landmark & Joint Detection)
  * `time` (Performance & FPS calculations)

---

## 🧠 How It Works

The tracking mechanism operates in two main phases:

1. **Palm Detection (Detector):** Detects the hand region / bounding box within the video frame.
2. **Hand Landmark Model:** Predicts 21 3D hand joint coordinates relative to the detected hand region.

```
+------------------+     +--------------------+     +------------------------+
|  Input Video     | --> |  Palm Detector     | --> |  21 Hand Landmarks     |
|  (RGB Conversion)|     |  (Bounding Box)    |     |  (X, Y, Z Coordinates) |
+------------------+     +--------------------+     +------------------------+
                                                                |
                                                                v
                                                    +------------------------+
                                                    |  Pixel Translation &   |
                                                    |  UI Render (OpenCV)    |
                                                    +------------------------+
```

### 🖐️ Hand Landmark Map (21 Joints)

| Landmark ID | Description | Landmark ID | Description |
| :---: | :--- | :---: | :--- |
| **0** | Wrist (Bilek) | **11** | Middle Finger PIP |
| **1** | Thumb CMC | **12** | Middle Finger Tip |
| **2** | Thumb MCP | **13** | Ring Finger MCP |
| **3** | Thumb IP | **14** | Ring Finger PIP |
| **4** | **Thumb Tip (Başparmak Ucu)** | **15** | Ring Finger DIP |
| **5** | Index Finger MCP | **16** | Ring Finger Tip |
| **6** | Index Finger PIP | **17** | Pinky MCP |
| **7** | Index Finger DIP | **18** | Pinky PIP |
| **8** | Index Finger Tip | **19** | Pinky DIP |
| **9** | Middle Finger MCP | **20** | **Pinky Tip (Serçe Parmak Ucu)** |
| **10** | Middle Finger DIP | | |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/hand-gesture-tracking.git
cd hand-gesture-tracking
```

### 2. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install opencv-python mediapipe
```

### 3. Run the Tracking Application
Execute the Python script:
```bash
python hand_tracking.py
```
*Press `Ctrl+C` or close the display window to terminate the application.*

---

## 💻 Code Structure & Explanation

```python
import cv2
import time
import mediapipe as mp

# Initialize camera feed
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands solution
mpHand = mp.solutions.hands
hands = mpHand.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mpDraw = mp.solutions.drawing_utils
```

### Key Logic:
1. **BGR to RGB Conversion:** MediaPipe requires RGB images, whereas OpenCV reads in BGR.
2. **Process Frame:** `hands.process(imgRGB)` extracts hand landmarks.
3. **Coordinate Normalization:** Normalized landmark values ($x \in [0, 1], y \in [0, 1]$) are scaled by image height $h$ and width $w$ to obtain pixel coordinates `cx, cy`:
   ```python
   h, w, c = img.shape
   cx, cy = int(lm.x * w), int(lm.y * h)
   ```
4. **Drawing Connection Lines & Joints:** `mpDraw.draw_landmarks(...)` renders skeletal connections.

---

## 🔮 Potential Future Extensions

- 🖱️ **Virtual Mouse Control:** Controlling screen cursor using index finger coordinates.
- 🔊 **Gesture-based Volume Control:** Adjusting system audio based on the distance between thumb tip and index tip.
- 🤟 **Sign Language Recognition:** Classifying hand poses into alphabet letters or action commands.

---



