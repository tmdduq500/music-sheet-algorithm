#main
import cv2
import os
import numpy as np
import functions_sy as fs
import modules_sy

#이미지 불러오기
image=cv2.imread(r"D:\music-sheet-algoritm\template_sy\music_sheet_jpg\1.jpg", cv2.IMREAD_ANYCOLOR)

# 1. 보표 영역 추출 및 그 외 노이즈 제거
masked_image = modules_sy.remove_noise(image)

# 2. 오선 제거
removed_image, staves = modules_sy.remove_staves(masked_image)

# 3. 악보 이미지 정규화
normalized_image, staves = modules_sy.normalization(removed_image, staves, 13)

# 4. 객체 검출 과정
obj_detection_image, objects = modules_sy.object_detection(normalized_image, staves)

template_folder_path = r"D:\music-sheet-algoritm\template_sy\note_head"
template_images = [os.path.join(template_folder_path, filename) for filename in os.listdir(template_folder_path)]

# Perform template matching and draw rectangles on the original image
image_with_rectangles = modules_sy.template_matching(obj_detection_image.copy(), template_images)

#이미지 띄우기
cv2.imshow('image', image_with_rectangles)
cv2.waitKey(0)
cv2.destroyAllWindows()
