import cv2
import os
import numpy as np
import functions as fs
import modules

#이미지 불러오기
image=cv2.imread("C:/music-sheet-algoritm/yr_temp/music_sheet_jpg/3.jpg", cv2.IMREAD_ANYCOLOR)

# 전처리 1. 보표 영역 추출 및 그 외 노이즈 제거
masked_image = modules.remove_noise(image)

# 전처리 2. 오선 제거
removed_image, staves = modules.remove_staves(masked_image)

# 전처리 3. 이미지 정규화
image_3, staves = modules.normalization(removed_image, staves, 13)

#이미지 띄우기
cv2.imshow('image', image_3)
cv2.waitKey(0)
cv2.destroyAllWindows()