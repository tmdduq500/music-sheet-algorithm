import cv2
import os
import functions as fs
import modules
import glob

# 이미지 불러오기
resource_path = os.getcwd() + "/drum_sheet/"

# resource_path 내의 모든 jpg 파일 가져오기
image_files = glob.glob(resource_path + "*.jpg")

# 각 이미지에 대한 처리
for image_file in image_files:
    image_0 = cv2.imread(image_file)

    # 1. 보표 영역 추출 및 그 외 노이즈 제거
    image_1 = modules.remove_noise(image_0)

    # 2. 오선 제거
    image_2, staves = modules.remove_staves(image_1)

    # 3. 악보 이미지 정규화
    image_3, staves, new_h, new_w = modules.normalization(image_2, staves, 15)
    image_4 = cv2.resize(image_0, (new_w, new_h))

    # 이미지 파일의 이름을 폴더로 만들기
    image_filename = os.path.basename(image_file)
    image_folder_name = os.path.splitext(image_filename)[0]

    # 폴더가 존재하지 않으면 생성
    staff_image = os.path.join(resource_path, image_folder_name)
    os.makedirs(staff_image, exist_ok=True)

    # 이미지에 대한 추가 작업 수행
    modules.extract_symbols_from_images(image_4, staff_image)

    modules.obj_detection(staff_image)
