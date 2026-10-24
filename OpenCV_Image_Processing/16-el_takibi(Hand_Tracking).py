import cv2
import time
import mediapipe as mp
"""" ilk önce el tespit edilir daha sonra track
edilerek elimizin eklem yerlerinin gösterimi sağlanır.
Frame---Palm detector--Hand bb---Hand landmarks---gesture recognizer
Palm detection : el tespiti 
Hand Landmarks : 21 nokta var 
"""
cap = cv2.VideoCapture(0) # default kamera

mpHand = mp.solutions.hands

hands = mpHand.Hands()
# static_image_mode default olarak false'dur. Yani detection yapılır.True olsa track ederiz.
# max_n = toplamdaki el sayısı
#min_detection_confidence , min_tra_confidence arasındaki oranı ve algoritma hızını etkileyen parametreler
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # hand modülü RGB kullanır

    results = hands.process(imgRGB)
    print(results.multi_hand_landmarks) # el olup olmadığını return eder el yoksa none varsa x,y,z koordinatlarını döner . Elimde bulunan eklemlerin koordinatları çıkmaya başladı.

    if results.multi_hand_landmarks: # result none değilse içine giriyoruz for döngüsünün
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS) # bağlantılar işaretlenip çizilecek
            # buradaki eklemleri spesifik olarak bilmek projeyi dinamik hale getirir.

            for id, lm in enumerate(handLms.landmark): # landmark ile x,y,z şeklinde kullanılabilir halde. id ile eklemin hangi eklem olduğunu id değişken içine atarız.
                # print(id, lm)
                h, w, c = img.shape # 480,640,3 gibi

                cx, cy = int(lm.x * w), int(lm.y * h)
                # mesele serçe parmak görürse sola git gibi uygulamalar olabilir.
                # bilek
                if id == 4:
                    cv2.circle(img, (cx, cy), 9, (255, 0, 0), cv2.FILLED)

    # fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, "FPS: " + str(int(fps)), (10, 75), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 5)

    cv2.imshow("img", img)
    cv2.waitKey(1)















