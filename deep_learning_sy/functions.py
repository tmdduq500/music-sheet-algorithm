#functions
import cv2
import numpy as np

# 이진화
def threshold(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return image

# 가중치 설정
def weighted(value):
    standard = 13
    return int(value * (standard / 13))

# 닫힘 연산
def closing(image):
    kernel = np.ones((weighted(5), weighted(5)), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return image

# 텍스트 표시
def put_text(image, text, loc):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, str(text), loc, font, 0.6, (255, 0, 0), 2)

# 객체 y좌표 반환
def get_center(y, h):
    return (y + y + h) / 2