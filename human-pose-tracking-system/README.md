# 🕺 Real-Time Human Pose Tracking & Estimation System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Solutions-orange.svg)](https://developers.google.com/mediapipe)

A real-time Computer Vision application that performs full-body **Human Pose Estimation and 33-Keypoint Body Landmark Tracking** using **OpenCV** and Google's **MediaPipe Pose** framework.

The system processes pre-recorded video files or live camera feeds, locates 33 skeletal body joints (eyes, ears, shoulders, elbows, wrists, hips, knees, ankles) in 3D coordinate space ($x, y, z$), maps them to 2D frame pixels, renders skeletal connection wireframes, and calculates real-time FPS performance.

---

## 📌 Features

- **33 Keypoint Body Landmark Detection:** Detects full-body structural joints ranging from facial landmarks to fingers, toes, and hips.
- **Bi-directional Tracking:** Supports live webcam streams as well as file-based video analysis across sports, athletics, and human activity monitoring.
- **Joint-Specific Extraction & Highlight:** Demonstrates targeting specific joints by landmark ID (e.g., Left Elbow `ID 13`, Right Elbow `ID 14`) for motion analysis.
- **Real-Time Performance Metrics:** Integrates dynamic FPS calculation overlays on high-definition video frames.
- **Action & Movement Analysis Foundation:** Serves as a baseline engine for classifying sports actions (running, jump rope, basketball shooting, goalkeeper jump/saves) based on spatial joint angles and movement kinematics.

---

## 🛠️ Tech Stack & Prerequisites

* **Language:** Python 3.8+
* **Core Libraries:**
  * `opencv-python` (Video Frame Extraction, Visual Rendering, Window Controls)
  * `mediapipe` (MediaPipe Pose Solution & Kinematic Joint Estimator)
  * `time` (Timestamping & Frame Rate Computation)

---

## 🧠 How It Works

The Pose Estimation architecture consists of two main processing blocks:

1. **Full-Body Detector:** Detects person bounding boxes / full-body ROI within each image frame.
2. **Pose Landmark Model:** Predicts 33 3D skeletal landmark positions ($x, y, z$, plus visibility scores) relative to the ROI.

```
+------------------+     +-----------------------+     +------------------------+
|  Video / Camera  | --> |  Full-Body Detector   | --> |  33 Body Landmarks     |
|  (RGB Conversion)|     |  (Region of Interest) |     |  (3D Coordinates X,Y,Z)|
+------------------+     +-----------------------+     +------------------------+
                                                                   |
                                                                   v
                                                       +------------------------+
                                                       |  Pixel Translation &   |
                                                       |  Skeletal Overlay      |
                                                       +------------------------+
```

---

## 🧍 MediaPipe 33 Landmark Map Reference

```
 0 - nose                11 - left_shoulder      23 - left_hip
 1 - left_eye_inner      12 - right_shoulder     24 - right_hip
 2 - left_eye            13 - left_elbow         25 - left_knee
 3 - left_eye_outer      14 - right_elbow        26 - right_knee
 4 - right_eye_inner     15 - left_wrist         27 - left_ankle
 5 - right_eye           16 - right_wrist        28 - right_ankle
 6 - right_eye_outer     17 - left_pinky         29 - left_heel
 7 - left_ear            18 - right_pinky        30 - right_heel
 8 - right_ear           19 - left_index         31 - left_foot_index
 9 - mouth_left          20 - right_index        32 - right_foot_index
10 - mouth_right         21 - left_thumb
                         22 - right_thumb
```

### Key Joint Indices:
- **Face / Head:** `0 - 10`
- **Arms & Shoulders:** `11 (Left Shoulder)`, `12 (Right Shoulder)`, `13 (Left Elbow)`, `14 (Right Elbow)`, `15 (Left Wrist)`, `16 (Right Wrist)`
- **Torso & Legs:** `23 (Left Hip)`, `24 (Right Hip)`, `25 (Left Knee)`, `26 (Right Knee)`, `27 (Left Ankle)`, `28 (Right Ankle)`

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/human-pose-tracking-system.git
cd human-pose-tracking-system
```

### 2. Install Dependencies
```bash
pip install opencv-python mediapipe
```

### 3. Prepare Input Media & Run Script
Place your test videos (`video1.mp4`, `video5.mp4`, etc.) in the project directory, then run:
```bash
python pose_tracking.py
```
*(To use a live webcam instead, edit `cap = cv2.VideoCapture(0)` in `pose_tracking.py`)*

---

## 💻 Code Structure & Explanation

```python
import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Pose Solution
mpPose = mp.solutions.pose
pose = mpPose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture("video5.mp4")
pTime = 0

while True:
    success, img = cap.read()
    if not success:
        break
        
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    
    if results.pose_landmarks:
        # Draw full skeletal connection tree
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        
        # Extract pixel coordinates for each landmark
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, _ = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            
            # Example: Highlight left elbow (ID 13)
            if id == 13:
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
    
    # Calculate live FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime    
    
    cv2.putText(img, f"FPS: {int(fps)}", (10, 65), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.imshow("Human Pose Tracking", img)
    if cv2.waitKey(25) & 0xFF == 27: # ESC to exit
        break
```

---

## 🏃 Real-World Applications & Sports Analytics Insights

The extracted 33 landmarks enable rule-based gesture classification and deep biometric analysis:

1. **🏃 Running Analytics:**
   - Evaluates knee angle flexion ($\sim 90^\circ$ bends) and alternating foot stride distances ($|X_{	ext{LeftAnkle}} - X_{	ext{RightAnkle}}|$) to classify sprinting/running states.
2. **⚽ Goalkeeper Action Detection:**
   - Monitors asymmetric leg flexion coupled with lateral body displacement trajectories to detect diving saves.
3. **🏀 Basketball Shooting / Dribbling:**
   - Tracks elbow extension above head height (`Y_Elbow < Y_Head`) and repeating wrist elevation patterns.
4. **🧘 Jump Rope Tracking:**
   - Detects symmetric multi-arm angle oscillations ($	heta_{	ext{Elbow}}$) synchronized with vertical jump displacement along the $Y$-axis.


