# modules.py
import cv2
import numpy as np
import functions as fs
import modules
import glob
import os

def remove_noise(image):
    image = fs.threshold(image)  # 이미지 이진화
    mask = np.zeros(image.shape, np.uint8)  # 보표 영역만 추출하기 위해 마스크 생성

    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(image)  # 레이블링
    for i in range(1, cnt):
        x, y, w, h, area = stats[i]
        if w > image.shape[1] * 0.5:  # 보표 영역에만
            cv2.rectangle(mask, (x, y, w, h), (255, 0, 0), -1)  # 사각형 그리기

    masked_image = cv2.bitwise_and(image, mask)  # 보표 영역 추출

    return masked_image

def remove_staves(image):
    height, width = image.shape
    staves = []  # 오선의 좌표, 높이들이 저장될 리스트

    for row in range(height):
        pixels = 0
        for col in range(width):
            pixels += (image[row][col] == 255)  # 한 행에 존재하는 흰색 픽셀의 개수를 셈
        if pixels >= width * 0.5:  # 이미지 넓이의 50% 이상이라면
            if len(staves) == 0 or abs(staves[-1][0] + staves[-1][1] - row) >= 1:  # 첫 오선이거나 이전에 검출된 오선과 다른 오선
                staves.append([row, 1])  # 오선 추가 [오선의 y 좌표][오선 높이]
            else:  # 이전에 검출된 오선과 같은 오선
                staves[-1][1] += 1  # 높이 업데이트
                
    for staff in range(len(staves)):
        top_pixel = staves[staff][0]  # 오선의 최상단 y 좌표
        bot_pixel = staves[staff][0] + staves[staff][1] - 1  # 오선의 최하단 y 좌표 (오선의 최상단 y 좌표 + 오선 높이)
        for col in range(width):
            if staff == len(staves) - 1:  # 마지막 오선에 도달했을 때
                if image[top_pixel - 1][col] == 0:  # 이미지를 넘어갔을 때만 오선 삭제
                    for row in range(top_pixel, bot_pixel + 1):
                        image[row][col] = 0  # 오선 삭제
            elif image[top_pixel - 1][col] == 0 and image[bot_pixel + 1][col] == 0:  # 다른 오선에 대해 기존 조건 충족
                for row in range(top_pixel, bot_pixel + 1):
                    image[row][col] = 0  # 오선 삭제
                    
    return image, [x[0] for x in staves]

def normalization(image, staves, standard):
    avg_distance = 0
    lines = int(len(staves) / 5)  # 보표의 개수
    for line in range(lines):
        for staff in range(4):
            staff_above = staves[line * 5 + staff]
            staff_below = staves[line * 5 + staff + 1]
            avg_distance += abs(staff_above - staff_below)  # 오선의 간격을 누적해서 더해줌
    avg_distance /= len(staves) - lines  # 오선 간의 평균 간격

    height, width = image.shape  # 이미지의 높이와 넓이
    weight = standard / avg_distance  # 기준으로 정한 오선 간격을 이용해 가중치를 구함
    new_width = int(width * weight)  # 이미지의 넓이에 가중치를 곱해줌
    new_height = int(height * weight)  # 이미지의 높이에 가중치를 곱해줌

    image = cv2.resize(image, (new_width, new_height))  # 이미지 리사이징
    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 이미지 이진화
    staves = [x * weight for x in staves]  # 오선 좌표에도 가중치를 곱해줌

    return image, staves, new_height, new_width

def extract_staff_from_images(image, output_folder):
    image_c = fs.threshold(image)  # 이미지 이진화
    mask = np.zeros(image.shape, np.uint8)  # 보표 영역만 추출하기 위해 마스크 생성

    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(image_c)  # 레이블링

    # 보표 영역 추출하여 이미지로 저장
    extracted_symbols = []  # 추출된 보표들을 저장할 리스트
    for i in range(1, cnt):
        x, y, w, h, area = stats[i]
        if w > image_c.shape[1] * 0.5:  # 보표 영역에만
            symbol = image[y:y+h, x:x+w]  # 보표 부분 이미지 추출
            extracted_symbols.append(symbol)  # 추출된 보표를 리스트에 추가

            cv2.rectangle(mask, (x, y, w, h), (255, 0, 0), -1)  # 사각형 그리기

    # 보표 추출한 이미지들을 저장할 폴더 생성 (없으면 생성)
    if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

    # 보표 추출한 이미지들을 순회하며 파일로 저장
    for i, symbol in enumerate(extracted_symbols):
        _, image_name = os.path.split(output_folder)  # output_folder의 이름을 가져옴
        symbol_filename = os.path.join(output_folder, f"{image_name}_staff_{i}.jpg")
        cv2.imwrite(symbol_filename, symbol)



# def object_detection(image, staves, origin_img, save_dir, filename):
#     lines = int(len(staves) / 5)  # 보표의 개수
#     objects = []  # 객체 정보를 저장하는 리스트

#     closing_image = fs.closing(image)
#     cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(closing_image)  # 모든 객체 검출하기
    
#     for i in range(1, cnt):

#         (x, y, w, h, area) = stats[i]
#         cv2.rectangle(image, (x, y, w, h), (255, 0, 0), 1)

#         if w >= fs.weighted(10) and h >= fs.weighted(20):  # 악보의 구성요소가 되기 위한 넓이, 높이 조건
#             center = fs.get_center(y, h)
#             for line in range(lines):
#                 area_top = staves[line * 5] - fs.weighted(50)  # 위치 조건 (상단)
#                 area_bot = staves[(line + 1) * 5 - 1] + fs.weighted(50)  # 위치 조건 (하단)

#                 if area_top <= center <= area_bot:
#                     # 검출된 객체의 자른 이미지를 생성합니다.
#                     object_image = origin_img[0:origin_img.shape[0], x-4:x + w+4]
                    
#                     # 객체의 속성을 기반으로 고유한 파일 이름을 생성합니다 (확장자 제외).
#                     object_filename = f"{filename}_object_{line}_{x}_{y}"
                    
#                     # 자른 객체 이미지를 파일로 저장합니다.
#                     object_path = os.path.join(save_dir, object_filename + ".jpg")
#                     cv2.imwrite(object_path, object_image)
                    
#                     # 객체에 대한 정보를 리스트에 추가합니다.
#                     objects.append({
#                         "line": line,
#                         "x": x,
#                         "y": y,
#                         "w": w,
#                         "h": h,
#                         "area": area,
#                         "object_path": object_path,
#                     })

#     objects.sort(key=lambda x: (x["line"], x["x"]))  # 보표 번호와 x 좌표로 객체를 정렬합니다.

#     return image, objects


def object_detection(image, staves):
    lines = int(len(staves) / 5)  # 보표의 개수
    objects = []  # 구성요소 정보가 저장될 리스트

    closing_image = fs.closing(image)
    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(closing_image)  # 모든 객체 검출하기
    for i in range(1, cnt):
        (x, y, w, h, area) = stats[i]
        if w >= fs.weighted(15) and h >= fs.weighted(40):  # 악보의 구성요소가 되기 위한 넓이, 높이 조건
            center = fs.get_center(y, h)
            for line in range(lines):
                area_top = staves[line * 5] - fs.weighted(20)  # 위치 조건 (상단)
                area_bot = staves[(line + 1) * 5 - 1] + fs.weighted(20)  # 위치 조건 (하단)
                if area_top <= center <= area_bot:
                    objects.append([line, (x, y, w, h, area)])  # 객체 리스트에 보표 번호와 객체의 정보(위치, 크기)를 추가

    objects.sort()  # 보표 번호 → x 좌표 순으로 오름차순 정렬

    return image, objects


def obj_detection_cnn(image_folder):
    image_files = glob.glob(os.path.join(image_folder, "*.jpg"))
    
    for image_file in image_files:
        # 이미지 불러오기
        image0 = cv2.imread(image_file)

        # 1. 보표 영역 추출 및 그 외 노이즈 제거
        image1 = modules.remove_noise(image0)

        # 2. 오선 제거
        image2, staves = modules.remove_staves(image1)
         # 4. 객체 검출 과정
        image4, objects = modules.object_detection(image2, staves)
    
        # 이미지 파일의 이름을 폴더로 만들기 (확장자 제외)
        image_filename = os.path.basename(image_file)
        image_filename_without_extension = os.path.splitext(image_filename)[0]

        # 폴더가 존재하지 않으면 생성
        output_folder = os.path.join(image_folder, image_filename_without_extension)
        os.makedirs(output_folder, exist_ok=True)

        # 4. 객체 검출 과정
        modules.object_analysis(image4, objects, image0, output_folder, image_filename_without_extension)

def object_analysis(image, objects, origin_img, save_dir, filename):
    for obj in objects:
        stats = obj[1]
        stems = fs.stem_detection(image, stats, 35)  # 객체 내의 모든 직선들을 검출함
        direction = None
        if len(stems) > 0:  # 직선이 1개 이상 존재함
            if stems[0][0] - stats[0] >= fs.weighted(5):  # 직선이 나중에 발견되면
                direction = True  # 정 방향 음표
            else:  # 직선이 일찍 발견되면
                direction = False  # 역 방향 음표
        obj.append(stems)  # 객체 리스트에 직선 리스트를 추가
        obj.append(direction)  # 객체 리스트에 음표 방향을 추가

    for obj in objects:
        if obj[2]:  # obj[2]에 값이 있는 경우에만 이미지 저장
            line = obj[0]
            (x, y, w, h, area) = obj[1]
            object_image = origin_img[0:origin_img.shape[0], x-4:x + w+4]

            # 객체의 속성을 기반으로 고유한 파일 이름을 생성합니다 (확장자 제외).
            object_filename = f"{filename}_object_{line}_{x}_{y}"
                        
            # 자른 객체 이미지를 파일로 저장합니다.
            object_path = os.path.join(save_dir, object_filename + ".jpg")
            cv2.imwrite(object_path, object_image)

    return image, objects