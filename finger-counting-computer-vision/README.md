# 🖐️ Real-Time Computer Vision Finger Counter 

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Solutions-orange.svg)](https://developers.google.com/mediapipe)

A real-time Computer Vision and Hand Gesture Recognition system built using **OpenCV** and Google's **MediaPipe** framework. 

The application detects hands from a webcam feed, tracks 21 anatomical hand landmarks, applies spatial coordinate geometry to determine whether each finger (thumb, index, middle, ring, pinky) is open or closed, and renders the live finger count directly on the video output.

---

## 📌 Features

- **Geometric Joint Comparison:** Determines finger state (extended/flexed) by comparing relative spatial positions of finger tips against lower knuckle joints.
- **Dedicated Thumb Orientation Logic:** Accounts for thumb anatomy by using horizontal ($X$-axis) spatial relation rather than vertical ($Y$-axis) height.
- **Dynamic On-Screen Display:** Highlights hand skeletons and displays the calculated finger count in real-time.
- **Robust Pipeline:** Operates seamlessly across webcams with normalized image dimensions ($640 	imes 480$).
- **Zero Heavy Training Needed:** High-precision gesture classification built on pure heuristic rules and geometric tracking without complex heavy neural network training.

---

## 🛠️ Tech Stack & Prerequisites

* **Language:** Python 3.8+
* **Core Libraries:**
  * `opencv-python` (Camera Stream Capture, Image Processing, UI Overlay)
  * `mediapipe` (Hand Landmark Engine & Joint Estimation)

---

## 🧠 How The Algorithm Works

Finger state detection relies on tracking specific **Landmark IDs** defined in the MediaPipe Hands architecture.

### 📐 Structural Logic

1. **4 Main Fingers (Index, Middle, Ring, Pinky):**
   - A finger is considered **OPEN (1)** if the $Y$-coordinate of its **tip** is lower than the $Y$-coordinate of its **second knuckle joint** (PIP joint) in pixel space (since pixel $Y$ grows downwards):
     $$	ext{Tip}_{Y} < 	ext{Joint}_{Y} \implies 	ext{Extended (1)}$$
   - Landmark pairs evaluated:
     - **Index:** Tip `8` vs Joint `6`
     - **Middle:** Tip `12` vs Joint `10`
     - **Ring:** Tip `16` vs Joint `14`
     - **Pinky:** Tip `20` vs Joint `18`

2. **Thumb Logic:**
   - Because thumb movement occurs primarily along the horizontal axis, the thumb's status is calculated along the $X$-axis relative to its adjacent joint (IP joint `3` / CMC `2`):
     $$	ext{ThumbTip}_{X} < 	ext{ThumbJoint}_{X} \implies 	ext{Extended (1)}$$ *(Right Hand orientation)*

```
 +------------------------+
 |  Input Frame (RGB)     |
 +------------------------+
             |
             v
 +------------------------+
 | MediaPipe Landmark Ext. | --> Extracts 21 Landmark Coordinates [ID, X, Y]
 +------------------------+
             |
             v
 +------------------------+
 | Spatial Logic Checks   |
 | - Thumb (X-axis)       | --> Appends [1, 0, 1, 1, 0] to Finger List
 | - 4 Fingers (Y-axis)   |
 +------------------------+
             |
             v
 +------------------------+
 | Count & Render Overlay | --> Displays Total Open Count on Screen
 +------------------------+
```

---

## 🖐️ MediaPipe Hand Landmarks Mapping

| Tip Landmark ID | Finger Name | Reference Joint ID | Condition |
| :---: | :--- | :---: | :--- |
| **4** | **Thumb (Başparmak)** | **3 / 2** | `lmList[4][1] < lmList[3][1]` ($X$-axis) |
| **8** | **Index Finger (İşaret)** | **6** | `lmList[8][2] < lmList[6][2]` ($Y$-axis) |
| **12** | **Middle Finger (Orta)** | **10** | `lmList[12][2] < lmList[10][2]` ($Y$-axis) |
| **16** | **Ring Finger (Yüzük)** | **14** | `lmList[16][2] < lmList[14][2]` ($Y$-axis) |
| **20** | **Pinky Finger (Serçe)** | **18** | `lmList[20][2] < lmList[18][2]` ($Y$-axis) |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/finger-counting-computer-vision.git
cd finger-counting-computer-vision
```

### 2. Install Dependencies
```bash
pip install opencv-python mediapipe
```

### 3. Run the Application
```bash
python finger_counter.py
```

---

## 💻 Code Summary

```python
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

mpHand = mp.solutions.hands
hands = mpHand.Hands()
mpDraw = mp.solutions.drawing_utils 

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    lmList = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
       
    if len(lmList) != 0:
        fingers = []
        
        # Thumb (X-axis evaluation)
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # 4 Fingers (Y-axis evaluation)
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
    
        totalF = fingers.count(1)
        cv2.putText(img, str(totalF), (30, 125), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 8)
        
    cv2.imshow("Finger Counter", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```


