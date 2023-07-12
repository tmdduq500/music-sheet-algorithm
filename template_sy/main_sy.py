#main
import cv2
import os
import numpy as np
import functions as fs
import modules

#이미지 불러오기
image=cv2.imread(r"D:\re-music-sheet-algoritm\sy\music_sheet_jpg\1.jpg", cv2.IMREAD_ANYCOLOR)


# 1. 보표 영역 추출 및 그 외 노이즈 제거
masked_image = modules.remove_noise(image)

# 2. 오선 제거
removed_image, staves = modules.remove_staves(masked_image)

# 3. 악보 이미지 정규화
normalized_image, staves = modules.normalization(removed_image, staves, 13)

# 4. 객체 검출 과정
obj_detection_image, objects = modules.object_detection(normalized_image, staves)

#이미지 띄우기
cv2.imshow('image', obj_detection_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
