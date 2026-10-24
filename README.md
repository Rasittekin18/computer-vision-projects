# 👁️ Computer Vision & OpenCV Project Hub

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Google-orange?logo=google&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-yellow?logo=yolo&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-purple)
![Maintained](https://img.shields.io/badge/Status-Active-brightgreen)

<br/>

**A comprehensive, production-oriented monorepo showcasing 12 real-world Computer Vision, Deep Learning, and OpenCV applications.**  
Developed by **[Raşit Tekin](https://github.com/Rasittekin18)**.

[Proje Listesi](#-projeler-ve-modüller) • [Kurulum & Çalıştırma](#-kurulum-ve-genel-kullanım) • [Teknolojiler](#-kullanılan-teknolojiler) • [İletişim](#-yazar)

</div>

---

## 📌 Genel Bakış (Overview)

Bu repo; sürücü güvenliğinden akıllı otopark sistemlerine, MediaPipe tabanlı biyometrik ve iskelet takibinden YOLOv8 nesne tespitine kadar **12 farklı bilgisayarlı görü ve görüntü işleme projesini** tek bir düzenli çatı altında bir araya getirir.

Her proje kendi alt dizininde bağımsız çalışabilir halde korunmuştur; kendi kaynak kodlarını, veri setlerini/örneklerini ve özel dokümantasyonunu içerir.

---

## 📂 Projeler ve Modüller

| # | Proje Adı | Açıklama | Anahtar Teknolojiler | Klasör Linki |
| :-: | :--- | :--- | :--- | :-: |
| 01 | **Driver Drowsiness Detection** | Sürücünün göz kırpma ve kapanma oranını (EAR) analiz ederek yorgunluk/uyuklama anında sesli ve görsel alarm üreten gerçek zamanlı güvenlik sistemi. | OpenCV, MediaPipe / Dlib, SciPy | [`/driver-drowsiness-detection`](./driver-drowsiness-detection) |
| 02 | **Road Lane Tracking System** | Otonom sürüş için kamera görüntüsünden yol şerit çizgilerini tespit eden ve takip eden görüntü işleme boru hattı. | OpenCV, Canny Edge, Hough Transform | [`/road-lane-tracking-system`](./road-lane-tracking-system) |
| 03 | **Parking Space Detection** | Otopark kamera akışlarında park alanlarının doluluk/boşluk durumunu piksel yoğunluğu ve eşikleme ile gerçek zamanlı tespit eden akıllı sistem. | OpenCV, Adaptive Thresholding, NumPy | [`/parking-space-detection`](./parking-space-detection) |
| 04 | **3D Face Landmark Detection** | Yüz üzerinde 468 adet üç boyutlu referans noktasını yüksek FPS ile tespit eden yüz geometrisi analizi. | MediaPipe Face Mesh, OpenCV | [`/3d-face-landmark-detection`](./3d-face-landmark-detection) |
| 05 | **Facial Detection** | Yüz sınır kutusu tespiti ve yüz özelliklerinin gerçek zamanlı video akışında izlenmesi. | OpenCV Haar Cascades / MediaPipe | [`/facial-detection`](./facial-detection) |
| 06 | **Human Pose Tracking System** | İnsan vücudundaki eklem noktalarını ve duruş pozisyonunu 33 anahtar nokta üzerinden izleyen iskelet takip sistemi. | MediaPipe Pose, OpenCV | [`/human-pose-tracking-system`](./human-pose-tracking-system) |
| 07 | **AI Personal Workout Trainer** | Egzersiz hareketlerini (ör. biceps curl, squat) kamera karşısında analiz eden, açı hesaplayarak tekrar (rep) sayan yapay zeka antrenörü. | MediaPipe Pose, Trigonometri, OpenCV | [`/ai-personal-workout-trainer`](./ai-personal-workout-trainer) |
| 08 | **Hand Gesture Tracking** | El üzerindeki 21 eklem noktasını eşzamanlı izleyen ve el hareketlerini tanıyan hassas etkileşim modülü. | MediaPipe Hands, OpenCV | [`/hand-gesture-tracking`](./hand-gesture-tracking) |
| 09 | **Finger Counting System** | Kameraya gösterilen parmak sayısını el geometrisi ve kontur analiziyle hatasız sayan bilgisayarlı görü uygulaması. | OpenCV, Convexity Defects, Math | [`/finger-counting-computer-vision`](./finger-counting-computer-vision) |
| 10 | **Bottle Detector** | Konveyör veya masa üstündeki şişeleri tespit eden ve boyut/konum analizleri yapan YOLOv8 nesne tanıma modeli. | YOLOv8 (Ultralytics), OpenCV | [`/BottleDetector`](./BottleDetector) |
| 11 | **7 - Image Processing with OpenCV** | Filtreleme, morfolojik işlemler, kenar bulma ve renk uzayları üzerine kapsamlı modüler eğitim serisi. | OpenCV, NumPy, Matplotlib | [`/7-Image_Processing_with_OpenCV`](./7-Image_Processing_with_OpenCV) |
| 12 | **OpenCV Image Processing** | Geometrik dönüşümler, eşikleme ve özellik çıkarımı üzerine pratik kod kütüphanesi. | OpenCV, Python | [`/OpenCV_Image_Processing`](./OpenCV_Image_Processing) |

---

## 🚀 Kurulum ve Genel Kullanım

Herhangi bir alt projeyi çalıştırmak için öncelikle repoyu klonlayıp bir Python sanal ortamı oluşturun:

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/Rasittekin18/computer-vision-projects.git
cd computer-vision-projects
```

### 2. Sanal Ortam Oluşturun (Tavsiye Edilen)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Genel Bağımlılıkları Yükleyin
```bash
pip install opencv-python mediapipe ultralytics numpy matplotlib scipy
```

### 4. İstediğiniz Projeyi Çalıştırın
Her proje bağımsız bir klasör içindedir. İlgili klasöre girip ana Python dosyasını çalıştırmanız yeterlidir:

```bash
# Örnek 1: Sürücü yorgunluk tespiti
cd driver-drowsiness-detection
python driver-drowsiness-detection.py

# Örnek 2: AI Antrenör / Tekrar Sayacı
cd ../ai-personal-workout-trainer
python main.py

# Örnek 3: Otopark Doluluk Tespiti
cd ../parking-space-detection
python main.py
```
*(Detaylı proje-özel ayarlar için her alt klasördeki kendi `README.md` dosyasına başvurabilirsiniz).*

---

## 🛠️ Kullanılan Teknolojiler

- **Programlama Dili:** Python 3.8+
- **Görüntü İşleme & Çizim:** OpenCV (cv2)
- **Biyometrik / İskelet Takibi:** Google MediaPipe (Hands, Pose, Face Mesh)
- **Derin Öğrenme / Nesne Tespiti:** Ultralytics YOLOv8, PyTorch
- **Sayısal Hesaplama & Matematik:** NumPy, SciPy

---

## 👨‍💻 Yazar

**Raşit Tekin**  
*Electronics Engineer \| AI & Data Science*  
- GitHub: [@Rasittekin18](https://github.com/Rasittekin18)  
- E-posta: [rasittekin18@gmail.com](mailto:rasittekin18@gmail.com)  
- Konum: İstanbul, Türkiye

---

## 📄 Lisans

Bu projedeki tüm çalışmalar **MIT Lisansı** altında sunulmaktadır.
