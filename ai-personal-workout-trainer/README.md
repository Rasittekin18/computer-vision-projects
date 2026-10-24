# 🏋️ AI Personal Workout Trainer & Repetition Counter

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Solutions-orange.svg)](https://developers.google.com/mediapipe)
[![NumPy](https://img.shields.io/badge/NumPy-1.20%2B-013243.svg)](https://numpy.org/)


An intelligent, real-time **Computer Vision AI Personal Trainer** that automatically tracks human exercise routines, calculates precise body joint angles, monitors movement completeness, and counts repetition sets (e.g., Push-ups, Squats, Jumping Jacks, Biceps Curls) using **OpenCV**, **MediaPipe Pose**, and **NumPy**.

---

## 📌 Features

- **Kinematic Joint Angle Calculation:** Calculates 2D spatial angles between three key body joints using vector trigonometry ($rctan2$).
- **Dynamic Repetition Tracking:** Tracks state transitions (`dir = 0` vs `dir = 1`) to ensure full range of motion (ROM) before incrementing rep counts by full integer increments ($0.5 	o 1.0$).
- **Percentage Interpolation (`np.interp`):** Normalizes raw joint angles (e.g., $65^\circ - 145^\circ$) into $0\% - 100\%$ motion completion scales.
- **Custom Visual Feedback:** Renders dynamic joint overlays, connection vectors, real-time angle degree displays, and big bold repetition counters directly onto video feeds.
- **Multi-Exercise Adaptability:** Easily configurable for various workouts:
  - 🏋️ **Push-ups:** Tracking Arm/Elbow Angle (`11: Shoulder`, `13: Elbow`, `15: Wrist`).
  - 🦵 **Squats / Jumping Drills:** Tracking Leg/Knee Angle (`23: Hip`, `25: Knee`, `27: Ankle`).
  - 💪 **Biceps Curls:** Tracking Arm Flexion.

---

## 🛠️ Tech Stack & Prerequisites

* **Language:** Python 3.8+
* **Core Libraries:**
  * `opencv-python` (Frame Capture & Graphical Drawing)
  * `mediapipe` (MediaPipe Pose Solution & Joint Estimation)
  * `numpy` (Interpolation & Vector Array Operations)
  * `math` (Trigonometric Angle Calculations)

---

## 🧠 Mathematical Angle Calculation & Logic

### 1. Vector Angle Equation ($	heta $)
Given three landmark points $P_1(x_1, y_1)$, $P_2(x_2, y_2)$ (vertex joint), and $P_3(x_3, y_3)$:

$$	heta = 	ext{degrees}\left( rctan2(y_3 - y_2, x_3 - x_2) - rctan2(y_1 - y_2, x_1 - x_2) 
ight)$$

If $	heta < 0$, we normalize it to standard $0^\circ - 360^\circ$ space:

$$	heta = 	heta + 360^\circ$$

```
    P1 (Shoulder / Hip)
                          P2 (Elbow / Knee - Vertex) ------> Angle θ
       /
      /
     /
    P3 (Wrist / Ankle)
```

### 2. Repetition State Machine
To avoid false double-counting, the system uses a **Direction State Machine** (`dir`):

- **Flexion Phase (Down/Bend):** When motion percentage reaches $100\%$ (`per == 100`) and `dir == 0`, `count` increments by `0.5` and `dir` switches to `1`.
- **Extension Phase (Up/Return):** When motion percentage returns to $0\%$ (`per == 0`) and `dir == 1`, `count` increments by another `0.5` and `dir` resets to `0`.
- **Total Completed Reps:** `int(count)` displays full completed repetition cycles.

---

## 🏋️ Landmark Map Reference for Exercises

| Exercise | Point 1 ($P_1$) | Vertex Point ($P_2$) | Point 3 ($P_3$) | Target Angle Range |
| :--- | :---: | :---: | :---: | :---: |
| **Push-ups (Şınav)** | `11` (Left Shoulder) | `13` (Left Elbow) | `15` (Left Wrist) | $185^\circ 	o 245^\circ$ |
| **Squats / Jumping (Çömelme/Zıplama)** | `23` (Left Hip) | `25` (Left Knee) | `27` (Left Ankle) | $65^\circ 	o 145^\circ$ |
| **Biceps Curls (Pazu)** | `11` (Shoulder) | `13` (Elbow) | `15` (Wrist) | $30^\circ 	o 160^\circ$ |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-personal-workout-trainer.git
cd ai-personal-workout-trainer
```

### 2. Install Dependencies
```bash
pip install opencv-python mediapipe numpy
```

### 3. Run the Trainer Application
```bash
python workout_trainer.py
```

---

## 💻 Code Structure & Explanation

```python
import cv2
import numpy as np
import mediapipe as mp
import math

def findAngle(img, p1, p2, p3, lmList, draw=True):
    # Extract coordinates
    x1, y1 = lmList[p1][1:]
    x2, y2 = lmList[p2][1:]
    x3, y3 = lmList[p3][1:]
    
    # Calculate angle in degrees
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360
        
    if draw:
        # Draw skeleton limbs & joint highlights
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.line(img, (x3, y3), (x2, y2), (0, 0, 255), 3)
        cv2.circle(img, (x2, y2), 10, (0, 255, 255), cv2.FILLED)
        cv2.putText(img, str(int(angle)), (x2 - 40, y2 + 40), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
                    
    return angle

# Main Loop Execution
cap = cv2.VideoCapture("video2.mp4")
mpPose = mp.solutions.pose
pose = mpPose.Pose()

count = 0
dir = 0

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break
        
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    
    lmList = []
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, _ = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
            
    if len(lmList) != 0:
        # Evaluate Knee flexion angle for Squat / Jump drill
        angle = findAngle(img, 23, 25, 27, lmList)
        per = np.interp(angle, (65, 145), (0, 100))
        
        # State Machine Evaluation
        if per == 100 and dir == 0:
            count += 0.5
            dir = 1
        if per == 0 and dir == 1:
            count += 0.5
            dir = 0
            
        cv2.putText(img, f"Reps: {int(count)}", (45, 125), 
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
                    
    cv2.imshow("AI Personal Workout Trainer", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
```

---


