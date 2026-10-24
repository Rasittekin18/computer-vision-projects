# 👁️ Real-Time Eye Blink Counter & Driver Drowsiness Detection System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![cvzone](https://img.shields.io/badge/cvzone-1.5%2B-orange.svg)](https://pypi.org/project/cvzone/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Solutions-blue.svg)](https://developers.google.com/mediapipe)

A real-time **Computer Vision Eye Blink Counter & Driver Drowsiness Detection System** developed using **OpenCV**, **cvzone**, and Google's **MediaPipe Face Mesh** engine.

Micro-sleep and driver fatigue are leading causes of automotive accidents worldwide. This system addresses driver safety by continuously tracking 3D eye landmarks, computing dynamic Eye Aspect Ratios (ratio of vertical eye opening to horizontal eye width), plotting live telemetry data via `cvzone.PlotModule.LivePlot`, and identifying prolonged eye closures or rapid blink frequency anomalies.

---

## 📌 Features

- **High-Precision Eye Landmark Tracking:** Extracts specific 3D facial mesh keypoints (`idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]`) isolating the target eye structure.
- **Euclidean Eye Aspect Ratio (EAR) Computation:** Calculates vertical distance ($L_{	ext{vertical}}$ between upper and lower eyelids) versus horizontal distance ($L_{	ext{horizontal}}$ between left and right eye corners) using `detector.findDistance()`.
- **Moving Average Smoothing:** Uses a rolling 3-frame buffer (`ratioList`) to smooth ratio fluctuations and mitigate single-frame detection noise.
- **Debounced Blink State Machine:** Implements a lockout counter (`counter > 10`) to prevent duplicate counts during a single eye blink event.
- **Live Visual Telemetry & HUD Overlay (`LivePlot` & `cvzone.stackImages`):** Renders real-time ratio wave charts alongside the video stream in a side-by-side dashboard layout.

---

## 🛠️ Tech Stack & Prerequisites

* **Language:** Python 3.8+
* **Core Libraries:**
  * `opencv-python` (Video Input Decoding & Rendering)
  * `cvzone` (Higher-level wrapper for MediaPipe FaceMeshDetector, LivePlot, text rendering, image stacking)
  * `mediapipe` (Underlying Face Mesh Engine)

---

## 🧠 Image Processing & Detection Pipeline

```
 +--------------------------+
 |  Input Video / Webcam    |
 +--------------------------+
              |
              v
 +--------------------------+
 | MediaPipe FaceMesh       | --> Detects 468 3D facial mesh landmarks
 +--------------------------+
              |
              v
 +--------------------------+
 | Eye Landmark Extraction  | --> Extracts Up/Down (159, 23) & Left/Right (130, 243)
 +--------------------------+
              |
              v
 +--------------------------+
 | Ratio Calculation        | --> Ratio = (Vertical Distance / Horizontal Distance) * 100
 | & 3-Frame Rolling Avg    |
 +--------------------------+
              |
              v
 +------------------------------------------------------------+
 | State Machine Evaluation & Thresholding                    |
 | - If ratioAvg < 35 & counter == 0 --> Blink + 1, Green HUD |
 | - Debounce lockout (counter > 10)                          |
 +------------------------------------------------------------+
              |
              v
 +------------------------------------------------------------+
 | Dashboard Rendering (Stacked Image + LivePlot Telemetry)   |
 +------------------------------------------------------------+
```

---

## 📐 Mathematical Model & Ratio Equation

### 1. Eye Aspect Ratio (EAR) Percentage
Given Euclidean vertical landmark distance $L_v = d(P_{159}, P_{23})$ and horizontal landmark distance $L_h = d(P_{130}, P_{243})$:

$$	ext{Ratio} = \left( rac{L_v}{L_h} 
ight) 	imes 100$$

### 2. Moving Average Filtering
To eliminate high-frequency noise artifacts:

$$	ext{Ratio}_{	ext{avg}} = rac{1}{N} \sum_{i=1}^{N} 	ext{Ratio}_i \quad 	ext{where } N \le 3$$

When $	ext{Ratio}_{	ext{avg}} < 35$, an eye closure / blink event is registered.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/eye-blink-drowsiness-detection.git
cd eye-blink-drowsiness-detection
```

### 2. Install Dependencies
```bash
pip install opencv-python cvzone mediapipe
```

### 3. Run the Blink Detector
Place your test video files (`video1.mp4`, `video2.mp4`) in the project directory, then execute:
```bash
python sleep_detection.py
```

---

## 💻 Code Architecture & Structure

```python
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

# Video Input
cap = cv2.VideoCapture("video2.mp4")

# Initialize FaceMesh Detector & Real-time Telemetry Plotter
detector = FaceMeshDetector()
plotY = LivePlot(540, 360, [10, 60])

# Specific Eye Landmark IDs
idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
color = (0, 0, 255)
ratioList = []
counter = 0
blickCounter = 0

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break
        
    img, faces = detector.findFaceMesh(img, draw=False)
    
    if faces:
        face = faces[0]
        
        # Highlight eye landmark points
        for id in idList:
            cv2.circle(img, face[id], 5, color, cv2.FILLED)
        
        # Key coordinate points for ratio calculation
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        
        lengthVer, _ = detector.findDistance(leftUp, leftDown)
        lengthHor, _ = detector.findDistance(leftLeft, leftRight)
        
        cv2.line(img, leftUp, leftDown, (0, 255, 0), 3)
        cv2.line(img, leftLeft, leftRight, (0, 255, 0), 3)
        
        # Calculate aspect ratio
        ratio = int((lengthVer / lengthHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)       
        
        ratioAvg = sum(ratioList) / len(ratioList)
        
        # Blink Detection Threshold & State Machine
        if ratioAvg < 35 and counter == 0:
            blickCounter += 1
            color = (0, 255, 0)
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10: # Lockout threshold (10 frames)
                counter = 0
                color = (0, 0, 255)
        
        # UI Overlay
        cvzone.putTextRect(img, f'Blink Count: {blickCounter}', (50, 100), colorR=color)
        imgPlot = plotY.update(ratioAvg, color)
        
        # Stack Video Feed & Telemetry Chart Side-by-Side
        imgResized = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([imgResized, imgPlot], 2, 1)
        
        cv2.imshow("Driver Drowsiness & Blink Detection", imgStack)
        
    if cv2.waitKey(25) & 0xFF == 27: # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 🎯 Hyperparameter Tuning & Threshold Guidelines

- **Ratio Threshold (`ratioAvg < 35`):**
  - Adjust based on camera proximity and individual eye structure.
  - For subtle sleepiness detection where eyes stay half-closed, increase threshold to `38-40`[cite: 26].
- **Debounce Window (`counter > 10`):**
  - Controls frame lockout during a single blink event[cite: 26, 27].
  - Increasing the frame lockout prevents double counting slow blinks, while lowering it captures rapid multi-blinks[cite: 26, 27].
- **Rolling Average Window (`len(ratioList) > 3`):**
  - Controls smoothing sensitivity. A window of 3-4 frames prevents single-frame noise glitches without introducing lag[cite: 26, 27].

---

