from PIL import Image
import os

# 입력 및 출력 폴더 경로 설정
input_folder = r'C:\music-sheet-algorithm\yr_deep_learning\easy_staff_color'
output_folder = r'C:\music-sheet-algorithm\yr_deep_learning\notes'

# 입력 폴더 내의 모든 이미지 파일을 가져옴
image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg')]

for image_file in image_files:
    image_path = os.path.join(input_folder, image_file)
    image = Image.open(image_path)

    # 이미지 처리 작업을 위한 코드 추가
    # 예시: 이미지를 그레이스케일로 변환하여 음표 객체 검출
    gray_image = image.convert("L")  # 그레이스케일 변환
    # 이미지 처리 및 음표 객체 검출 작업을 추가해야 함

    # 검출된 음표 객체의 좌표 정보를 사용하여 잘라내기
    # 예시: 임의의 좌표와 크기로 잘라냄
    note_bbox = (x, y, x + width, y + height)
    note_image = image.crop(note_bbox)

    # 잘라낸 이미지를 저장할 경로 설정
    output_path = os.path.join(output_folder, image_file)
    note_image.save(output_path)

    print(f"Processed {image_file} and saved to {output_path}")

print("All images processed and saved.")