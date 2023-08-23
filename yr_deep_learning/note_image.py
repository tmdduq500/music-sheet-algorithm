from PIL import Image
import os
import random

# 입력 및 출력 폴더 경로 설정
input_folder = r'C:\music-sheet-algoritm\yr_deep_learning\easy_staff_color'
output_folder = r'C:\music-sheet-algoritm\yr_deep_learning\notes'

# 입력 폴더 내의 모든 이미지 파일을 가져옴
image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg')]

for image_file in image_files:
    image_path = os.path.join(input_folder, image_file)
    image = Image.open(image_path)

    # 음표 객체 검출 및 잘라내기 작업
    # 여기에 실제 이미지 처리 코드를 추가해야 함

    # 임의의 위치와 크기로 음표 객체의 좌표 정보 생성 (예시)
    x = random.randint(0, image.width - 50)  # 임의의 x 좌표
    y = random.randint(0, image.height - 50)  # 임의의 y 좌표
    width = 50  # 임의의 너비
    height = 50  # 임의의 높이
    
    # 검출된 음표 객체의 좌표 정보를 사용하여 잘라내기
    note_bbox = (x, y, x + width, y + height)
    note_image = image.crop(note_bbox)

    # 잘라낸 이미지를 저장할 경로 설정
    output_path = os.path.join(output_folder, image_file)
    note_image.save(output_path)

    print(f"Processed {image_file} and saved to {output_path}")

print("All images processed and saved.")