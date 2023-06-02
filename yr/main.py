#main
import cv2
import os
import numpy as np
import functions as fs
import modules

"""
객체 검출
문제 발생 : 전처리 3.부터 선이 인식 안됨
-> normalization의 standard를 13으로 해줌/ 12까지 선이 먹힘
-> functions의 10(standard)를 10이하에서 13으로 바꿈

객체 인식
문제 발생 : 인식과정 6. recognition_modules 함수에서 pass 오류 발생
-> key만 return해주면 된다고 생각 pass 지움
문제 발생 : 인식과정 6. 전부 완성해서 실행했을 때 list 에러 발생
-> 인식 과정 6. 조표 드럼악보에는 조표가 없으므로 무시하고 넘어감
문제 발생 : 인식과정 7.을 하며 이전에 했던 recognize_key 함수를 사용해야하나 에러가 발생함
->recognition_modules의 recognize_key 함수에서 조표 관련 삭제
-> modules에서 recognition함수 수정(주석으로 표기되어있음)/return에서 key(조표)삭제-> main에서도 삭제

image_0 = image
image_1 = masked_image
image_2 = removed_image
image_3 = normalized_image
image_4 = object_image
image_5 = analyzed_image
"""

#이미지 불러오기
image=cv2.imread("C:/music-sheet-algorithm/yr/image/drum_sheet(1).jpg", cv2.IMREAD_ANYCOLOR)

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
recognized_image, beats, pitches = modules.recognition(analyzed_image, staves, objects)
#조표 버전= recognized_image, key, beats, pitches = modules.recognition(analyzed_image, staves, objects)  

#이미지 띄우기
cv2.imshow('image', recognized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()