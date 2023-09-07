import cv2
import os
import functions as fs
import modules
import glob
import DrumNote_CNN

# 이미지 불러오기
resource_path = os.getcwd() + "/drum_sheet/"

# resource_path 내의 모든 jpg 파일 가져오기
image_files = glob.glob(resource_path + "*.jpg")

# 각 이미지에 대한 처리
for image_file in image_files:

    origin_image = cv2.imread(image_file)
    origin_image = cv2.resize(origin_image, (2480,3509))
    # 1. 보표 영역 추출 및 그 외 노이즈 제거
    image_1 = modules.remove_noise(origin_image)
    # 2. 오선 제거
    image_2, staves = modules.remove_staves(image_1)
    # 3. 악보 이미지 정규화
    image_3, staves, new_h, new_w = modules.normalization(image_2, staves, 15)
    
    resized_color_origin_img = cv2.resize(origin_image, (new_w, new_h))

    # 이미지 파일의 이름을 폴더로 만들기
    image_filename = os.path.basename(image_file)
    image_folder_name = os.path.splitext(image_filename)[0]

    # 폴더 경로 생성
    staff_image = os.path.join(resource_path, image_folder_name)

    # 폴더가 존재하지 않으면 생성
    if not os.path.exists(staff_image):
        os.makedirs(staff_image, exist_ok=True)

        # 보표 추출
        modules.extract_staff_from_images(resized_color_origin_img, staff_image)
        # 객체(음표) 추출
        modules.obj_detection_cnn(staff_image)
    else:
        print(f"Folder '{image_folder_name}' already exists. Skipping processing for this image.")

# 예측 및 txt파일 결과 출력
DrumNote_CNN.run_drum_note_cnn()