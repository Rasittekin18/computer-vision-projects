# 🎭 Real-Time Face Mesh & 468-Point Facial Landmark Tracking

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Solutions-orange.svg)](https://developers.google.com/mediapipe)

An advanced real-time **Computer Vision Facial Topology & Mesh Tracking System** developed using **OpenCV** and Google's **MediaPipe Face Mesh** framework.

Going beyond basic face detection bounding boxes, this system estimates 3D facial surface geometry by tracking **468 3D facial landmarks** in real time. It enables precise tracking of fine-grained facial contours, micro-expressions, eye blinks, eyebrow movements, lip motion, and mouth openings under dynamic conditions.

---

## 📌 Features

- **468 3D Facial Landmark Tracking:** Detects high-density $X, Y, Z$ facial coordinates across region-of-interest (ROI) features (eyes, eyebrows, nose bridge, lips, face oval).
- **Sub-Pixel Mesh Tesselation:** Draws full facial mesh wireframes using `FACEMESH_TESSELATION` or feature outlines using `FACEMESH_CONTOURS`.
- **Customizable Drawing Specifications:** Adjusts landmark line thickness and circle point radii using `mpDraw.DrawingSpec`.
- **Micro-Expression & Feature Foundation:** Serves as the core geometric foundation for downstream tasks:
  - 😄 **Emotion Recognition & Smile Analysis:** Tracking relative distances between mouth corners and upper/lower lip keypoints.
  - 🗣️ **Lip Reading & Speech Detection:** Measuring dynamic vertical openings between lips.
  - 😴 **Drowsiness & Blink Detection (EAR):** Evaluating Eye Aspect Ratio (EAR) by tracking top and bottom eyelid landmarks.
- **Configurable Face Tracking:** Supports tracking single or multiple faces in the frame (`max_num_faces`).

---

## 🛠️ Tech Stack & Prerequisites

* **Language:** Python 3.8+
* **Core Libraries:**
  * `opencv-python` (Video Frame Decoding & Window Rendering)
  * `mediapipe` (MediaPipe Face Mesh Engine & Landmark Estimator)
  * `time` (Timestamping & Real-time FPS Calculation)

---

## 🧠 How The Pipeline Works

1. **Face Region Cropping & Orientation:** Detects candidate face regions and normalizes bounding orientation.
2. **Facial Feature Extraction:** Predicts 468 3D landmark locations across face mesh surfaces.
3. **Pixel Coordinate Scaling:** Scales normalized landmark coordinates ($x \in [0.0, 1.0], y \in [0.0, 1.0]$) into exact frame pixel locations ($cx, cy$):
   $$cx = 	ext{int}(x 	imes 	ext{Width})$$
   $$cy = 	ext{int}(y 	imes 	ext{Height})$$
4. **Mesh Rendering:** Overlays wireframe tessellations and calculates live performance FPS metrics.

```
+-------------------+     +-------------------------+     +--------------------------+
|  Input Video Stream| --> |  Face ROI Detection     | --> |  468 3D Facial Landmarks |
|  (RGB Conversion) |     |  & Feature Extraction   |     |  (X, Y, Z Coordinates)   |
+-------------------+     +-------------------------+     +--------------------------+
                                                                       |
                                                                       v
                                                           +--------------------------+
                                                           | Pixel Mapping &          |
                                                           | Mesh Tesselation Render  |
                                                           +--------------------------+
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/face-mesh-tracking-system.git
cd face-mesh-tracking-system
```

### 2. Install Dependencies
```bash
pip install opencv-python mediapipe
```

### 3. Run the Face Mesh Application
Place your sample test videos (`video1.mp4`, `video2.mp4`, `video3.mp4`) in the project directory and run:
```bash
python face_mesh.py
```

---

## 💻 Code Structure & Explanation

```python
import cv2
import time
import mediapipe as mp

# Video Input
cap = cv2.VideoCapture("video3.mp4")

# Initialize MediaPipe Face Mesh
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
mpDraw = mp.solutions.drawing_utils

# Custom Drawing Specifications (Thickness = 1, Circle Radius = 1)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

pTime = 0
while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    # Convert BGR image to RGB for MediaPipe processing
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        # Draw Mesh Wireframe Tesselation
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(
                img, 
                faceLms, 
                mpFaceMesh.FACEMESH_TESSELATION, 
                drawSpec, 
                drawSpec
            )

        # Extract 468 landmark coordinates (ID, cx, cy)
        for id, lm in enumerate(faceLms.landmark):
            h, w, _ = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            # print([id, cx, cy])

    # Calculate and display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime
    
    cv2.putText(img, f"FPS: {int(fps)}", (10, 65), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.imshow("Real-Time Face Mesh Tracking", img)
    
    if cv2.waitKey(50) & 0xFF == 27: # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 💡 Practical Applications & Downstream Projects

Using the extracted 468 landmark IDs (`id, cx, cy`), you can build intelligent vision algorithms:

1. **😊 Smile / Emotion Recognition:** Measure the euclidean distance between mouth corner landmarks (e.g., left and right lip edges) relative to lip opening height[cite: 16].
2. **😴 Drowsiness / Eye Blink Counter:** Compute the Eye Aspect Ratio (EAR) by monitoring vertical vs. horizontal distance ratios of upper and lower eyelid landmarks[cite: 16].
3. **🗣️ Active Speaker Detection:** Detect dynamic vertical displacement between upper and lower inner lip landmarks to verify if a person is talking[cite: 16].

---

