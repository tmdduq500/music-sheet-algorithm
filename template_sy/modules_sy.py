import cv2
import numpy as np
import functions_sy as fs

# 보표&노이즈 제거 
def remove_noise(image):
    image = fs.threshold(image)  # 이미지 이진화
    mask = np.zeros(image.shape, np.uint8)  # 보표 영역만 추출하기 위해 마스크 생성

    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(image)  # 레이블링
    for i in range(1, cnt):
        x, y, w, h, area = stats[i]
        if w > image.shape[1] * 0.7:  # 보표 영역에만
            cv2.rectangle(mask, (x-50, y-10, w+50, h+10), (255, 0, 0), -1)  # 사각형 그리기

    masked_image = cv2.bitwise_and(image, mask)  # 보표 영역 추출

    return masked_image

# 오선 제거
def remove_staves(image):
    height, width = image.shape
    staves = []  # 오선의 좌표들이 저장될 리스트

    for row in range(height):
        pixels = 0
        for col in range(width):
            pixels += (image[row][col] == 255)  # 한 행에 존재하는 흰색 픽셀의 개수를 셈
        if pixels >= width * 0.6:  # 이미지 넓이의 50% 이상이라면
            if len(staves) == 0 or abs(staves[-1][0] + staves[-1][1] - row) > 1:  # 첫 오선이거나 이전에 검출된 오선과 다른 오선
                staves.append([row, 0])  # 오선 추가 [오선의 y 좌표][오선 높이]
            else:  # 이전에 검출된 오선과 같은 오선
                staves[-1][1] += 1  # 높이 업데이트

    for staff in range(len(staves)):
        top_pixel = staves[staff][0]  # 오선의 최상단 y 좌표
        bot_pixel = staves[staff][0] + staves[staff][1]  # 오선의 최하단 y 좌표 (오선의 최상단 y 좌표 + 오선 높이)
        for col in range(width):
            if image[top_pixel - 1][col] == 0 and image[bot_pixel + 1][col] == 0:  # 오선 위, 아래로 픽셀이 있는지 탐색
                for row in range(top_pixel, bot_pixel + 1):
                    image[row][col] = 0  # 오선을 지움

    return image, [x[0] for x in staves]

# 오선 높이 구하기
def staff_height(staves):
    avg_distance = 0
    lines = int(len(staves) / 5)  # 보표의 개수
    for line in range(lines):
        for staff in range(4):
            staff_above = staves[line * 5 + staff]
            staff_below = staves[line * 5 + staff + 1]
            avg_distance += abs(staff_above - staff_below)  # 오선의 간격을 누적해서 더해줌
    avg_distance /= len(staves) - lines  # 오선 간의 평균 간격
    return avg_distance

# 악보 이미지 정규화
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

    return image, staves

# 객체 검출
def object_detection(image, staves):
    lines = int(len(staves) / 5)  # 보표의 개수
    objects = []  # 구성요소 정보가 저장될 리스트

    closing_image = fs.closing(image)
    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(closing_image)  # 모든 객체 검출하기
    for i in range(1, cnt):
        (x, y, w, h, area) = stats[i]
        
        # 객체 넓이 높이 확인 
        # fs.put_text(image, w, (x, y + h + 30))
        # fs.put_text(image, h, (x, y + h + 60))

        if w >= fs.weighted(10) and h >= fs.weighted(7):  # 악보의 구성요소가 되기 위한 넓이, 높이 조건
            # 객체 확인
            # cv2.rectangle(image, (x, y, w, h), (255, 0, 0), 1)
            center = fs.get_center(y, h)
            for line in range(lines):
                area_top = staves[line * 5] - fs.weighted(20)  # 위치 조건 (상단)
                area_bot = staves[(line + 1) * 5 - 1] + fs.weighted(20)  # 위치 조건 (하단)
                if area_top <= center <= area_bot:
                    objects.append([line, (x, y, w, h, area)])  # 객체 리스트에 보표 번호와 객체의 정보(위치, 크기)를 추가

    objects.sort()  # 보표 번호 → x 좌표 순으로 오름차순 정렬

    return image, objects

def template_matching(original_image, template_path):
    template = cv2.imread(template_path, cv2.IMREAD_ANYCOLOR)
    template = fs.threshold(template)
    template = cv2.resize(template, (20, 18))
    w, h = template.shape[::-1]

    img_gray = original_image.copy()
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.65
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(original_image, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 1)

    return original_image


# def template_matching(original_image, template_images):
#     img_gray = original_image.copy()
#     threshold = 0.70
#     matched_coordinates = []

#     for template_path in template_images:
#         template = cv2.imread(template_path, cv2.IMREAD_ANYCOLOR)
#         template = fs.threshold(template)
#         template = cv2.resize(template, (19, 17))
#         w, h = template.shape[::-1]

#         res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
#         loc = np.where(res >= threshold)

#         for pt in zip(*loc[::-1]):
#             cv2.rectangle(original_image, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 1)
#             matched_coordinates.append(pt)

#     # Display matched coordinates as text on the original image
#     for coord in matched_coordinates:
#         x, y = coord
#         text = f"({x}, {y})"
#         cv2.putText(original_image, text, (x-20, y+50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

#     return original_image

