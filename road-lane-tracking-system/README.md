# 🛣️ Real-Time Autonomous Road Line & Lane Detection System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.20%2B-013243.svg)](https://numpy.org/)

A real-time **Computer Vision Autonomous Road Line & Lane Detection System** developed using **OpenCV** and **NumPy**.

Lane line identification is a fundamental perception component for **Autonomous Vehicles** and **Advanced Driver Assistance Systems (ADAS)**, allowing vehicles to maintain lane positioning, plan trajectory paths, and detect surrounding lane boundaries. This project implements a full vision pipeline—converting video frames to grayscale, detecting high-gradient intensity changes using **Canny Edge Detection**, cropping triangular Region of Interest (ROI) masks, and extracting vector line equations using the **Probabilistic Hough Line Transform (`cv2.HoughLinesP`)**.

---

## 📌 Features

- **End-to-End Image Processing Pipeline:** Processes video frames sequentially using classic computer vision techniques without heavy deep learning overhead.
- **Grayscale Conversion & Canny Edge Detection:** Isolates sharp intensity gradients representing lane boundaries ($250/120$ thresholds).
- **Triangular ROI Masking (`region_of_interest`):** Masks out non-road background elements (sky, mountains, trees, surrounding vegetation) using bitwise AND operations on a dynamic triangular mask.
- **Probabilistic Hough Line Transform (`HoughLinesP`):** Identifies straight lane line segment vectors based on parametric accumulator thresholds, minimum line length, and maximum allowed line gap.
- **Weighted Overlay Generation (`cv2.addWeighted`):** Blends detected green lane line vectors onto original full-color video streams seamlessly.

---

## 🛠️ Tech Stack & Prerequisites

* **Language:** Python 3.8+
* **Core Libraries:**
  * `opencv-python` (Video Capture, Grayscale, Canny Edge Detection, Hough Transforms, Visual Overlays)
  * `numpy` (Array Manipulation, Coordinate Vertices, Bitwise Masking)

---

## 🧠 Image Processing & Detection Pipeline

```
 +--------------------------+
 |  Input Video Frame (BGR) |
 +--------------------------+
              |
              v
 +--------------------------+
 |  Grayscale Conversion    | --> Eliminates color channels
 +--------------------------+
              |
              v
 +--------------------------+
 | Canny Edge Detection     | --> Detects intensity gradients (250, 120)
 +--------------------------+
              |
              v
 +--------------------------+
 | Region of Interest (ROI) | --> Applies triangular mask [(0, H), (W/2, H/2), (W, H)]
 +--------------------------+
              |
              v
 +--------------------------+
 | Probabilistic Hough      | --> Extracts lines via polar parameter space (r, θ)
 | Line Transform           |
 +--------------------------+
              |
              v
 +--------------------------+
 | Weighted Visual Overlay  | --> Blends thick green lane markers onto original frame
 +--------------------------+
```

---

## 📐 Mathematical Foundations

### 1. Canny Edge Gradient
Identifies pixels where image brightness changes sharply by finding the local maximum of the gradient magnitude:

$$|
abla G| = \sqrt{G_x^2 + G_y^2}$$

### 2. Hough Line Equation (Polar Coordinates)
Lines are represented in polar coordinate space $(r, 	heta)$ to handle vertical slopes without infinite gradients:

$$r = x \cos	heta + y \sin	heta$$

In `cv2.HoughLinesP`:
- `rho = 2`: Distance resolution of the accumulator in pixels.
- `theta = np.pi / 180`: Angle resolution in radians ($1^\circ$).
- `threshold = 200`: Minimum number of intersections in the accumulator to detect a line.
- `minLineLength = 150`: Minimum pixel length of a line segment.
- `maxLineGap = 4`: Maximum allowed gap between points to treat them as a single line.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/road-line-detection.git
cd road-line-detection
```

### 2. Install Dependencies
```bash
pip install opencv-python numpy
```

### 3. Run the Lane Detector
Place your target test videos (`video1.mp4`, `video2.mp4`) in the project directory, then execute:
```bash
python road_line_detection.py
```

---

## 💻 Code Architecture & Structure

```python
import cv2
import numpy as np

def region_of_interest(image, vertices):
    # Construct zero mask matching image shape
    mask = np.zeros_like(image)
    match_mask_color = 255
    
    # Fill ROI polygon and perform bitwise AND
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def drawLines(image, lines):
    image = np.copy(image)
    blank_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(blank_image, (x1, y1), (x2, y2), (0, 255, 0), thickness=10)
        
    # Merge detected lines with original image
    image = cv2.addWeighted(image, 0.8, blank_image, 1, 0.0)
    return image

def process(image):
    height, width = image.shape[0], image.shape[1]
    
    # Triangular ROI vertices: bottom-left, top-center, bottom-right
    region_of_interest_vertices = [(0, height), (width / 2, height / 2), (width, height)]
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    canny_image = cv2.Canny(gray_image, 250, 120)
    cropped_image = region_of_interest(canny_image, np.array([region_of_interest_vertices], np.int32))
    
    lines = cv2.HoughLinesP(
        cropped_image, 
        rho=2, 
        theta=np.pi / 180, 
        threshold=200, 
        lines=np.array([]),
        minLineLength=150, 
        maxLineGap=4
    )
    
    imageWithLine = drawLines(image, lines)
    return imageWithLine

# Main Execution Loop
cap = cv2.VideoCapture("video2.mp4") 
 
while cap.isOpened():
    success, img = cap.read()
    if not success:
        break
        
    img = process(img)
    cv2.imshow("Road Line Detection", img)
    if cv2.waitKey(20) & 0xFF == 27: # Press ESC to exit
        break
     
cap.release()
cv2.destroyAllWindows()
```

---

## 🎯 Parameter Tuning Guidelines & Trade-offs

As discussed in the project walkthrough, line detection requires balancing key parameters:

1. **`minLineLength`:**
   - **Higher values ($\ge 150$):** Filters out small noise artifacts (grass, distant hills, sand dunes) but may fail to capture short curved markings.
   - **Lower values ($\le 50$):** Detects short dashed lines and sharp curves, but increases susceptibility to road surface noise.
2. **`maxLineGap`:**
   - Defines the maximum pixel gap allowed to connect fragmented line segments.
3. **Region of Interest (ROI) Polygon Adjustment:**
   - Adjusting vertices from a single triangular zone to multi-segment trapezoids allows capturing additional lanes or wider highway perspectives.

---

