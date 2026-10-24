import cv2
import time

# video ismi
video_name = "MOT17-04-DPM.mp4"

cap = cv2.VideoCapture(video_name)
# capture video--> videoyu boş da olsa yükler,video olmasa dahi yükler.
# Hata olduğunu belli etmek için kontrol yapıcaz.
# Video yüklenmemiş olur , ileriki adımlarda fark edemezsin.
print("Genişlik: ", cap.get(3))
print("Yükseklik: ", cap.get(4))

# Bunu yapmak önemlidir.
if cap.isOpened() == False:
    print("Error")

while True: # okuma işleminden herhangi bir şey return edilmeyinceye kadar işlem gerçekleşir.
    ret, frame = cap.read()
# frame : video içinde bulunan her bir resim karesi
# return de bu işlemin başarılı olup olmadığı
    frame = cv2.resize(frame, (960, 540)) # video gösterilen boyutu değiştirir.
    if ret == True: # burda frame okuyoruz while içinde olunca da tüm video akıyor.

        time.sleep(0.01)  # bunu kullanmazsak video çok hızlı gider.

        cv2.imshow("Video", frame)

    else:
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# buradaki breadk'ler while döngüsünün kırılmasna yarar
# ilk break videoda gerçekten gösterecek bir şey kalmadıysa çalışır
# 2. break ise kendi isteğimizle çıkış yaptığımızda çalışır.
cap.release()  # stop capture --> yakalamayı bırak
cv2.destroyAllWindows()
