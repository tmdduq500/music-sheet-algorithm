#main
import cv2
import os
import numpy as np
import functions_sy as fs
import modules_sy as modules_sy

#이미지 불러오기
image=cv2.imread(r"D:\music-sheet-algoritm\sy\asd\1.1.JPG", cv2.IMREAD_ANYCOLOR)

#전처리 1. 보표 영역 추출 및 그 외 노이즈 제거
masked_image = modules_sy.remove_noise(image)

#전처리 2. 오선 제거
removed_image, staves = modules_sy.remove_staves(masked_image)

# #전처리 3. 악보 이미지 정규화
# normalized_image, staves = modules_sy.normalization(removed_image, staves, 13)

# 4. 객체 검출 
obj_detection_image, objects = modules_sy.object_detection(removed_image, staves)

# # 5. 객체 분석 
# obj_analysis_image, objects = modules_sy.object_analysis(obj_detection_image, objects)

# # 6. 객체 인식 
# obj_recognition_image, key, beats, pitches = modules_sy.recognition(obj_analysis_image, staves, objects)


#이미지 띄우기
cv2.imshow('image', obj_detection_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
