import cv2
import os
import numpy as np
import functions_sy as fs
import modules_sy as modules_sy


"""폴더 안의 jpg 전부 실행"""
# for i in os.listdir('D:\\music-sheet-algorithm\\sy\\music_sheet_jpg\\'):
#     path = 'D:\\music-sheet-algorithm\\sy\\music_sheet_jpg\\'+i 
#     image = cv2.imread(path)

#     #전처리 1. 보표 영역 추출 및 그 외 노이즈 제거-modules-fs
#     masked_image = modules.remove_noise(image)

#     #전처리 2. 오선 제거
#     removed_image, staves = modules.remove_staves(masked_image)

#     #전처리 3. 악보 이미지 정규화
#     normalized_image, staves = modules.normalization(removed_image, staves, 11)

#     # 4. 객체 검출 과정
#     # obj_detection_image, objects = modules.object_detection(normalized_image, staves)

#     # 이미지 띄우기
#     cv2.imshow('image', normalized_image)
#     k = cv2.waitKey(0)
#     if k == 27:
#         cv2.destroyAllWindows()