import cv2
import numpy as np

# joining images
img = cv2.imread("Lenna_(test_image).png")
cv2.imshow("Orjinal", img)
cv2.waitKey(0)   # burası çok önemli!
cv2.destroyAllWindows()

# Veri çeşitlendirme işlemlerinde kullanılır.
hor = np.hstack((img, img))
cv2.imshow("Horizontal Image", hor)
cv2.waitKey(0)   # burası çok önemli!
cv2.destroyAllWindows()


ver = np.vstack((img, img))
cv2.imshow("Vertical Image", ver)
cv2.waitKey(0)   # burası çok önemli!
cv2.destroyAllWindows()
