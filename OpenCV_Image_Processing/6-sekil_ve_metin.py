import cv2
import numpy as np

# shape and text
img = np.zeros((512,512,3),np.uint8) # siyah bir resim oluştur
print(img.shape)
cv2.imshow("Image", img)
cv2.waitKey(0)   # burası çok önemli!
cv2.destroyAllWindows()


# opencv rgb değil bgr sıralamasına sahip
cv2.line(img,(0,0),(512,512), (0,255,0), thickness=3) # start - stop - color - thickness
cv2.imshow("Image", img)
cv2.waitKey(0)   # burası çok önemli!
cv2.destroyAllWindows()



cv2.rectangle(img,(0,0),(256,256), (255,0,0), cv2.FILLED) # (bgr) resim,başlangıç,bitiş,renk
cv2.imshow("Image", img)
cv2.waitKey(0)   # burası çok önemli!
cv2.destroyAllWindows()



cv2.circle(img,(300,300),30, (0,0,255), cv2.FILLED) # center - radius
cv2.imshow("Image", img) # aracı takip ediyopruz merkezine koyduk mesela
cv2.waitKey(0)   # burası çok önemli!
cv2.destroyAllWindows()


# resim,başlangıç noktası,font,kalınlık,renk
cv2.putText(img,"CIRCLE ",(325,305),cv2.FONT_HERSHEY_COMPLEX, 1 ,(255,255,255))
cv2.imshow("Image", img)
cv2.waitKey(0)   # burası çok önemli!
cv2.destroyAllWindows()