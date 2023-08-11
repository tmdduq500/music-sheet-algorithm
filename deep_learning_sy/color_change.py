import os
import cv2

# 입력 폴더 경로 설정
input_folder = r'D:\music-sheet-algoritm\easy_staff_img'

# 출력 폴더 경로 설정
output_folder = r'D:\music-sheet-algoritm\easy_staff_color'

# 입력 폴더 내 모든 이미지 파일 불러오기
image_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.png') or f.lower().endswith('.jpg')]

# 각 이미지 파일에 대해 작업 수행
for image_file in image_files:
    input_path = os.path.join(input_folder, image_file)
    
    # 이미지 불러오기
    binary_sheet = cv2.imread(input_path, cv2.IMREAD_ANYCOLOR)
    
    # 색상 반전
    colored_sheet = cv2.bitwise_not(binary_sheet)
    
    # 출력 파일 경로 설정
    output_path = os.path.join(output_folder, image_file)
    
    # 이미지 저장
    cv2.imwrite(output_path, colored_sheet)
