import cv2
import os

def count_white_pixels(image_path):
    image = cv2.imread(image_path)
    # 이미지를 그레이스케일로 변환
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 흰색 픽셀 수를 계산 (흰색 픽셀의 값은 255)
    white_pixels = cv2.countNonZero(gray_image)
    return white_pixels

def visualize_white_pixels(image_folder):
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # 이미지 파일 필터링
            image_path = os.path.join(image_folder, filename)
            white_pixel_count = count_white_pixels(image_path)

            # 이미지를 읽어온 다음 흰색 픽셀 수를 터미널에 출력합니다.
            print(f"{filename}: {white_pixel_count}개의 흰색 픽셀")

            # 이미지를 출력합니다.
            image = cv2.imread(image_path)
            cv2.imshow(filename, image)
            cv2.waitKey(0)  # 키 입력 대기
            cv2.destroyAllWindows()  # 창 닫기
            
if __name__ == "__main__":
    image_folder = r"D:\re-music-sheet-algoritm\sy\obj_img"  # 실제 이미지 폴더 경로로 대체해주세요
    visualize_white_pixels(image_folder)
