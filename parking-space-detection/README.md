# 🅿️ Real-Time Automated Parking Space Counter (Computer Vision)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.20%2B-013243.svg)](https://numpy.org/)

An intelligent, real-time **Automated Parking Space Detection and Counter System** built using **OpenCV**, **NumPy**, and Python's **Pickle** module. 

The application enables users to interactively define custom parking slot regions on an overhead camera view, saves pixel coordinates persistently, applies morphological image processing pipelines (Adaptive Thresholding, Gaussian Blur, Median Blur, Dilation), counts active non-zero pixels inside each cropped parking slot ROI, and dynamically updates available (`FREE`) vs. occupied parking slot counts.

---

## 📌 Features

- **Interactive Parking Space Picker (`ParkingSpacePicker.py`):**
  - **Left Mouse Click (`EVENT_LBUTTONDOWN`):** Adds a new fixed-size parking slot ROI coordinate ($27 	imes 15$ pixels) to the grid.
  - **Right Mouse Click (`EVENT_RBUTTONDOWN`):** Removes an existing parking slot coordinate if clicked within its bounding box bounds.
  - **Data Persistence:** Serializes and loads position arrays (`posList`) to/from a binary `CarParkPos` file using `pickle`.
- **Image Processing Pipeline (`ParkingSpaceCounter.py`):**
  - Converts video frames to grayscale.
  - Applies **Gaussian Blur** to reduce high-frequency noise.
  - Uses **Adaptive Gaussian Thresholding** (`THRESH_BINARY_INV`) to isolate car edges/reflections as white pixels against dark backgrounds.
  - Applies **Median Blur** to eliminate salt-and-pepper pixel noise (such as moving pedestrians).
  - Uses **Dilation** (`cv2.dilate`) to thicken vehicle structural edges and bridge interior gaps.
- **Dynamic Occupancy Logic:**
  - Crops each predefined slot position ($X, Y 	o X+W, Y+H$).
  - Counts non-zero white pixels (`cv2.countNonZero`).
  - **Occupied Slot (Red Box):** Non-zero pixel count $\ge 150$.
  - **Free Slot (Green Box):** Non-zero pixel count $< 150$.
- **Real-Time Visual Overlay:** Displays live pixel counts per slot alongside total available capacity (e.g., `Free: 9/22`).

---

## 🛠️ Tech Stack & Prerequisites

* **Language:** Python 3.8+
* **Core Libraries:**
  * `opencv-python` (Image/Video Processing, Thresholding, Interactive GUI Callbacks)
  * `numpy` (Kernel Array Definitions for Morphological Operations)
  * `pickle` (Python Object Serialization for Position Persistence)

---

## 🧠 Image Processing & Detection Pipeline

```
 +-------------------------+
 | Input Video Frame (BGR) |
 +-------------------------+
              |
              v
 +-------------------------+
 | Grayscale Conversion    |
 +-------------------------+
              |
              v
 +-------------------------+
 | Gaussian Blur (3x3)     | --> Suppresses image noise
 +-------------------------+
              |
              v
 +-------------------------+
 | Adaptive Thresholding   | --> Binary Inverted (Cars/Edges -> White Pixels)
 +-------------------------+
              |
              v
 +-------------------------+
 | Median Blur (5x5)       | --> Eliminates speckle noise/pedestrians
 +-------------------------+
              |
              v
 +-------------------------+
 | Dilation (3x3 Kernel)   | --> Thickens structural car white pixels
 +-------------------------+
              |
              v
 +------------------------------------------------------------+
 | ROI Cropping & Non-Zero Pixel Counting                     |
 | - If count < 150  --> GREEN Box  (Space Counter + 1)       |
 | - If count >= 150 --> RED Box    (Occupied)                |
 +------------------------------------------------------------+
```

---

## 📁 Repository File Structure

```
.
├── ParkingSpacePicker.py   # Interactive ROI selection script with mouse callbacks
├── ParkingSpaceCounter.py  # Main execution script running image processing pipeline
├── CarParkPos              # Binary pickle file storing array of (X, Y) slot positions
├── first_frame.png         # Static image template used for picking slot coordinates
└── video.mp4               # Target overhead parking camera video stream
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/parking-space-counter.git
cd parking-space-counter
```

### 2. Install Dependencies
```bash
pip install opencv-python numpy
```

### 3. Step 1: Define Parking Slots
Run the interactive picker script to select parking spots on `first_frame.png`:
```bash
python ParkingSpacePicker.py
```
* **Left Click:** Add a parking slot rectangle.
* **Right Click:** Remove a parking slot rectangle.
* Close the window when finished. Coordinates will automatically save to `CarParkPos`.

### 4. Step 2: Run the Parking Space Counter
Run the main video processing pipeline script:
```bash
python ParkingSpaceCounter.py
```

---

## 💻 Code Structure & Explanation

### 1. Interactive Picker (`ParkingSpacePicker.py`)
```python
import cv2
import pickle

width, height = 27, 15

try:
    with open("CarParkPos", "rb") as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                break
                
    with open("CarParkPos", "wb") as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread("first_frame.png")
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 0), 2)
        
    cv2.imshow("Parking Space Picker", img)
    cv2.setMouseCallback("Parking Space Picker", mouseClick)
    if cv2.waitKey(1) & 0xFF == 27:
        break
```

### 2. Space Counter & Processor (`ParkingSpaceCounter.py`)
```python
import cv2
import pickle
import numpy as np

width, height = 27, 15
cap = cv2.VideoCapture("video.mp4")

with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)

def checkParkSpace(imgg, img):
    spaceCounter = 0
    for pos in posList:
        x, y = pos
        img_crop = imgg[y:y + height, x:x + width]
        count = cv2.countNonZero(img_crop)
        
        if count < 150:
            color = (0, 255, 0) # Green = Free
            spaceCounter += 1
        else:
            color = (0, 0, 255) # Red = Occupied
            
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 2)
        cv2.putText(img, str(count), (x, y + height - 2), 
                    cv2.FONT_HERSHEY_PLAIN, 1, color, 1)
        
    cv2.putText(img, f"Free: {spaceCounter}/{len(posList)}", (15, 24), 
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 4)

while cap.isOpened():
    success, img = cap.read()
    if not success:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Loop video stream
        continue
        
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(
        imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 25, 16
    )
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    imgDilate = cv2.dilate(imgMedian, np.ones((3, 3)), iterations=1)
    
    checkParkSpace(imgDilate, img)
    
    cv2.imshow("Automated Parking Space Counter", img)
    if cv2.waitKey(10) & 0xFF == 27:
        break
```

---

