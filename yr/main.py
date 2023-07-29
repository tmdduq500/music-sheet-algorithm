#main
import cv2
import os
import numpy as np
import functions as fs
import modules

"""
image_0 = image
image_1 = masked_image
image_2 = removed_image
image_3 = normalized_image
image_4 = object_image
image_5 = analyzed_image
image_6 = recognized_image
"""

#이미지 불러오기
image=cv2.imread("C:/music-sheet-algoritm/yr/music_sheet_jpg/4.jpg", cv2.IMREAD_ANYCOLOR)

#전처리 1. 보표 영역 추출 및 그 외 노이즈 제거-modules-fs
masked_image = modules.remove_noise(image)

#전처리 2. 오선 제거
removed_image, staves = modules.remove_staves(masked_image)

#전처리 3. 악보 이미지 정규화
normalized_image, staves = modules.normalization(removed_image, staves, 13)

#객체 검출 4. 객체 검출 과정
obj_image, objects = modules.object_detection(normalized_image, staves)

#객체 분석 5. 객체 분석 과정
analyzed_image, objects = modules.object_analysis(obj_image, objects)

#객체 인식 6. 인식 과정
recognized_image, key, beats, pitches = modules.recognition(analyzed_image, staves, objects)
#조표 버전= recognized_image, key, beats, pitches = modules.recognition(analyzed_image, staves, objects)  

#이미지 띄우기
cv2.imshow('image', recognized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()