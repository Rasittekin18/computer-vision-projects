from ultralytics import YOLO
import cv2

def main():
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Hata: Kamera açılamadı!")
        return

    # Belirli dikdörtgen alanın koordinatları (örnek: ekranın merkezi)
    rx1, ry1, rx2, ry2 = 100, 80, 580, 450  # Alanın sol üst (x, y) ve sağ alt (x, y) koordinatları

    # Piksel başına düşen mm değeri
    px_to_mm = 0.896

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Hata: Frame okunamadı!")
            break

        results = model(frame, verbose=False)

        # Algılanan kutuların işlenmesi
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = box.conf[0]
                xyxy = box.xyxy[0].cpu().numpy().astype(int)
                x1, y1, x2, y2 = xyxy

                label = model.model.names[cls_id] if hasattr(model.model, "names") else str(cls_id)

                if label.lower() == 'bottle':
                    # Algılanan şişenin belirlenen dikdörtgen alan içinde olup olmadığını kontrol et
                    if x1 >= rx1 and y1 >= ry1 and x2 <= rx2 and y2 <= ry2:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        width_px = x2 - x1
                        height_px = y2 - y1

                        # mm cinsine dönüştürme
                        width_mm = width_px / px_to_mm
                        height_mm = height_px / px_to_mm

                        text = f"Bottle: {conf:.2f} | {width_mm:.1f}mm x {height_mm:.1f}mm"
                        cv2.putText(frame, text, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Dikdörtgen alanı görselleştirme
        cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (0, 0, 255), 2)

        cv2.imshow("YOLOv8 Şişe Tespiti", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
