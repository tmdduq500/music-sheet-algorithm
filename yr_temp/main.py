import cv2
import os
import numpy as np
import functions as fs
import modules

#이미지 불러오기
image=cv2.imread("C:/music-sheet-algoritm/yr_re/music_sheet_jpg/4_re.jpg", cv2.IMREAD_ANYCOLOR)

# 전처리 1. 보표 영역 추출 및 그 외 노이즈 제거
masked_image = modules.remove_noise(image)

#이미지 띄우기
cv2.imshow('image', masked_image)
cv2.waitKey(0)
cv2.destroyAllWindows()