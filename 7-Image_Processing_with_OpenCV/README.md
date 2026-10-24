# Image Processing with OpenCV 📷🖼️

Bu depo, **OpenCV** kütüphanesi ve **Python** kullanılarak gerçekleştirilen temel ve orta-ileri düzey görüntü işleme tekniklerini kapsayan uygulama kodlarını ve örnek projeleri içermektedir.

---

## 📌 İçindekiler
- [Proje Hakkında](#-proje-hakkında)
- [Öğrenilen ve Uygulanan Konular](#-öğrenilen-ve-uygulanan-konular)
- [Gereksinimler ve Kurulum](#-gereksinimler-ve-kurulum)
- [Kullanılan Teknolojiler](#-kullanılan-teknolojiler)
- [İletişim](#-iletişim)

---

## 💡 Proje Hakkında

Bilgisayarlı Görü (Computer Vision) projelerinin temelini oluşturan **OpenCV** kütüphanesi ile görüntü işleme süreçleri; piksellerin veri yapısından başlayıp gürültü temizleme, kenar tespiti ve histogram eşitlemeye kadar uygulamalı olarak incelenmiştir.

---

## 📚 Öğrenilen ve Uygulanan Konular

### 1. Temel İşlemler & I/O
- **Resim/Video Okuma ve Kaydetme:** `cv2.imread`, `cv2.VideoCapture`, `cv2.imwrite` ve `VideoWriter` kullanımı.
- **Boyutlandırma & Kırpma:** `cv2.resize` ve NumPy array slicing işlemleri ile ROI çıkarma.
- **Şekil ve Metin:** Bounding Box çizimleri (`line`, `rectangle`, `circle`) ve metin ekleme (`putText`).
- **Görüntü Birleştirme:** `np.hstack` ve `np.vstack` ile dikey/yatay birleştirme.

### 2. İleri Düzey Manipülasyon & Filtreleme
- **Perspektif Çarpıtma:** `cv2.getPerspectiveTransform` ve `cv2.warpPerspective` ile açı düzeltme.
- **Görüntü Karıştırma:** `cv2.addWeighted` ile ağırlıklı matris toplamı.
- **Eşikleme (Thresholding):** Sabit (`cv2.threshold`) ve Adaptif Eşikleme (`cv2.adaptiveThreshold`).
- **Bulanıklaştırma (Blurring):** Average, Gaussian ve Median Filtreleme.
- **Gürültü Yönetimi:** Gaussian ve Salt-and-Pepper (Tuz ve Karabiber) gürültü simülasyonu ve arındırılması.

### 3. Morfoloji & Gradyanlar
- **Morfolojik Operasyonlar:** Erozyon, Genişleme (Dilation), Açma (Opening), Kapatma (Closing) ve Morfolojik Gradyan.
- **Gradyanlar & Kenar Tespiti:** Sobel ($X$ ve $Y$ yönlü) ve Laplacian filtreleri.

### 4. Histogram & Maskeleme
- **Histogram Analizi:** `cv2.calcHist` ve Matplotlib ile BGR/RGB kanal dağılım analizi.
- **Maskeleme:** `cv2.bitwise_and` ile ilgilenilen alanların (ROI) izole edilmesi.
- **Histogram Eşitleme:** `cv2.equalizeHist` ile kontrast artırma.

---

## 🛠️ Gereksinimler ve Kurulum

```bash
# Repoyu klonlayın
git clone https://github.com/Rasittekin18/7-Image_Processing_with_OpenCV.git
cd 7-Image_Processing_with_OpenCV

# Gerekli kütüphaneleri yükleyin
pip install opencv-python numpy matplotlib
```

---

## 🧰 Kullanılan Teknolojiler

- **Python 3.x**
- **OpenCV (`cv2`)**
- **NumPy**
- **Matplotlib**

---

## ✉️ İletişim

**Raşit Tekin** — [@Rasittekin18](https://github.com/Rasittekin18)
