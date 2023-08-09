#functions
import cv2

#이미지 그레이스케일 -> 이진화/ 이진화된 이미지 return 
def threshold(image):
    image =cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return image