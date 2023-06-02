import os
from pdf2image import convert_from_path
from PIL import Image
import time

def pdf_to_jpg(input_path, output_path):
    # PDF를 이미지로 변환
    images = convert_from_path(input_path, poppler_path=r"C:\poppler-23.05.0\Library\bin")

    for i, image in enumerate(images):
        # 현재 시간을 기반으로 고유한 파일명 생성
        timestamp = str(int(time.time() * 1000))
        image_path = os.path.join(output_path, f"{timestamp}_page_{i+1}.jpg")

        # 이미지 저장
        image.save(image_path, "JPEG")

        print(f"저장 완료: {image_path}")

def convert_pdfs_to_jpgs(input_folder, output_folder):
    # 입력 폴더 내의 모든 파일 검색
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            # PDF 파일 경로 설정
            pdf_path = os.path.join(input_folder, filename)

            # 디렉토리 생성
            os.makedirs(output_folder, exist_ok=True)

            # PDF를 JPG로 변환
            pdf_to_jpg(pdf_path, output_folder)

# 입력 폴더와 출력 폴더 경로 설정
input_folder = r"image"
output_folder = r"image"

# 폴더 내의 PDF 파일들을 JPG로 변환
convert_pdfs_to_jpgs(input_folder, output_folder)


"""pdf-> jpg 변환 하기(파일 1개 변환할 때)"""
# file_name = 'sample'
# file_path = 'D:\\music-sheet-algorithm\\sy\\' + file_name + '.pdf'
# pop_path = 'C:\\poppler-23.05.0\\Library\\bin'

# pages = convert_from_path(file_path, poppler_path=pop_path)

# for i, page in enumerate(pages):
#     page.save(file_name + str(i) + '.jpg', 'JPEG')
