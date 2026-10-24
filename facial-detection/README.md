# 👤 Real-Time Face Detection & Bounding Box Localization

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Solutions-orange.svg)](https://developers.google.com/mediapipe)

A lightweight, real-time **Computer Vision Face Detection System** built using **OpenCV** and Google's **MediaPipe Face Detection** model. 

The application detects faces across video streams, camera feeds, or static images, calculates relative spatial bounding boxes, scales relative normalized coordinates ($x_{\min}, y_{\min}, w, h$) into pixel dimensions, and visualizes tracking boundaries under varying real-world conditions (including masked faces, partial occlusion, and side-profile rotations).

---

## 📌 Features

- **BlazeFace Model Integration:** Uses MediaPipe's lightweight, ultra-fast BlazeFace detector optimized for real-time mobile and edge processing.
- **Robust Multi-Face Detection:** Tracks single or multiple faces in the same frame simultaneously.
- **Occlusion & Mask Handling:** Successfully detects human faces even with physical obstacles such as face masks, glasses, or hair coverage.
- **Normalized-to-Pixel Coordinate Calculation:** Converts normalized float bounding boxes ($[0.0, 1.0]$) into exact pixel values ($X, Y, 	ext{Width}, 	ext{Height}$) using image dimensions ($W, H$).
- **Customizable Confidence Tuning:** Demonstrates tuning `min_detection_confidence` (e.g., `0.20` to `0.50`) to balance false positives vs. side-profile detection sensitivity.

---

## 🛠️ Tech Stack & Prerequisites

* **Language:** Python 3.8+
* **Core Libraries:**
  * `opencv-python` (Video Decoding, Image Conversions & Bounding Box Visualization)
  * `mediapipe` (BlazeFace Detection Pipeline)

---

## 🧠 How The Bounding Box Logic Works

MediaPipe returns relative bounding box values (`relative_bounding_box`) normalized between $0.0$ and $1.0$:

* $x_{\min}$: Normalized top-left $X$ position
* $y_{\min}$: Normalized top-left $Y$ position
* $w_{	ext{rel}}$: Relative width of face
* $h_{	ext{rel}}$: Relative height of face

### Pixel Scaling Equations:
Given frame height $H$ and frame width $W$:

$$	ext{X}_{	ext{pixel}} = 	ext{int}(x_{\min} 	imes W)$$
$$	ext{Y}_{	ext{pixel}} = 	ext{int}(y_{\min} 	imes H)$$
$$	ext{Width}_{	ext{pixel}} = 	ext{int}(w_{	ext{rel}} 	imes W)$$
$$	ext{Height}_{	ext{pixel}} = 	ext{int}(h_{	ext{rel}} 	imes H)$$

```
 (0,0) ----------------------------------> W
   |   (X_pixel, Y_pixel)
   |       +-------------------+
   |       |                   |
   |       |    Face Region    |  Height_pixel
   |       |                   |
   |       +-------------------+
   |            Width_pixel
   v
   H
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/face-detection-system.git
cd face-detection-system
```

### 2. Install Dependencies
```bash
pip install opencv-python mediapipe
```

### 3. Run the Detection Application
Place your sample videos (`video1.mp4`, `video2.mp4`, `video3.mp4`) in the project root directory, then run:
```bash
python face_detection.py
```

---

## 💻 Code Structure & Explanation

```python
import cv2
import mediapipe as mp

# Load input video stream
cap = cv2.VideoCapture("video3.mp4")

# Initialize MediaPipe Face Detection with custom confidence threshold
mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection(min_detection_confidence=0.20)
mpDraw = mp.solutions.drawing_utils

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    # Convert BGR image to RGB for MediaPipe processing
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)

    if results.detections:
        for id, detection in enumerate(results.detections):
            # Extract normalized relative bounding box coordinates
            bboxC = detection.location_data.relative_bounding_box
            h, w, _ = img.shape
            
            # Map normalized coordinates to pixel space
            bbox = (
                int(bboxC.xmin * w),
                int(bboxC.ymin * h),
                int(bboxC.width * w),
                int(bboxC.height * h)
            )
            
            # Render bounding box on original image frame
            cv2.rectangle(img, bbox, (0, 255, 255), 2)

    cv2.imshow("Real-Time Face Detection", img)
    if cv2.waitKey(10) & 0xFF == 27: # Press ESC to stop
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 🎯 Hyperparameter Tuning & Threshold Experiments

As explained in the project walkthrough, adjusting `min_detection_confidence` balances detection persistence and precision:

- **Low Threshold (`0.20`):** Increases sensitivity to detect obscured faces (e.g., side profiles, partial occlusion by hair, low lighting).
- **Default Threshold (`0.50`):** Standard balance between stability and recall.
- **High Threshold (`0.80`):** Reduces false positives but may lose tracking when faces rotate away from the camera.

---


