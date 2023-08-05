import cv2
import os
import numpy as np
import functions as fs
import modules
import glob

def get_image_files_from_folder(folder_path, file_extension="jpg"):
    pattern = f"{folder_path}/*.{file_extension}"
    image_files = glob.glob(pattern)
    return image_files

# 이미지를 불러올 폴더 경로 설정
image_folder_path = r"D:\re-music-sheet-algoritm\sy\music_sheet_jpg"

# 폴더 내의 이미지 파일들 가져오기
image_files = get_image_files_from_folder(image_folder_path)

# 이미지를 저장할 폴더 경로 설정
save_folder_path = r"D:\re-music-sheet-algoritm\sy\object_images"

# 저장 폴더가 없으면 생성
if not os.path.exists(save_folder_path):
    os.makedirs(save_folder_path)

for image_file in image_files:
    
    # 이미지 불러오기
    image = cv2.imread(image_file, cv2.IMREAD_ANYCOLOR)

    # 1. 보표 영역 추출 및 그 외 노이즈 제거
    masked_image = modules.remove_noise(image)

    # 2. 오선 제거
    removed_image, staves = modules.remove_staves(masked_image)

    # # 3. 악보 이미지 정규화
    # normalized_image, staves = modules.normalization(removed_image, staves, 13)

    # 4. 객체 검출 과정
    obj_detection_image, objects = modules.object_detection(removed_image, staves)

    # 객체 이미지 저장
    for i, obj_info in enumerate(objects):
        line_number, (x, y, w, h, area) = obj_info

        # 객체 부분 이미지 잘라내기
        object_image = obj_detection_image[y:y+h, x:x+w]

        # 이미지 저장 경로 설정 (현재 이미지 파일명과 객체 번호를 활용)
        image_name = os.path.splitext(os.path.basename(image_file))[0]  # 이미지 파일명 (확장자 제외)
        save_path = os.path.join(save_folder_path, f"{image_name}_object_{i+1}.png")

        # 이미지 저장
        cv2.imwrite(save_path, object_image)