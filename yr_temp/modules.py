#modules
import cv2
import numpy as np
import functions as fs

#전처리 1
#초기 이미지에서 이진화한 후 보표 영역 이미지만 추출
def remove_noise(image):
    # 보표 영역 추출 및 그 외 노이즈 제거
    image = fs.threshold(image)  # 이미지 이진화
    mask = np.zeros(image.shape, np.uint8)# 보표 영역만 추출하기 위해 마스크 생성
        #연결된 모든 객체를 인식해서 이미지에 사각형 그리기
    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(image)  # 레이블링
    for i in range(1, cnt):
        x, y, w, h, area = stats[i]
        if w > image.shape[1] * 0.5:  # 인식된 객체의 가로 길이가 이미지 가로 길이의 50% 이상인 경우/보표 영역에만
            cv2.rectangle(mask, (x, y, w, h), (255, 0, 0), -1)  # 사각형 그리기    
    masked_image = cv2.bitwise_and(image, mask)
    
    return masked_image

#전처리 2
#오선 제거
def remove_staves(image):
    height, width = image.shape # 이전 처리된 이미지의 가로, 세로 길이 정보
    staves = []  # 오선의 좌표, 높이들이 저장될 리스트

    # 한 줄(행)에 해당하는 픽셀 개수를 확인하고 히스토그램 이미지에 개수만큼 채우기
    for row in range(height):
        pixels = 0 # 픽셀 개수 변수
        for col in range(width): # 여기까지 for 문을 통해 전체 이미지를 훑기
            pixels += (image[row][col] == 255)  # 한 행에 존재하는 픽셀의 개수를 셈
        if pixels >= width * 0.5:  # 픽셀의 개수가 전체 이미지 넓이의 50% 이상이라면-> 오선이라면 오선에 관한 정보 정리
            if len(staves) == 0 or abs(staves[-1][0] + staves[-1][1] - row) >= 1:  # 첫 오선이거나 이전에 검출된 오선과 다른 오선
                staves.append([row, 1])  # 오선 추가 [오선의 y 좌표][오선 높이]
            else:  # 이전에 검출된 오선과 같은 오선
                staves[-1][1] += 1  # 리스트의 마지막에서 2번째 요소인 [오선 높이]에 +1
        # 여기까지 오선에 관한 정보 정리
        
    #오선의 위, 아래를 탐색한 후 픽셀이 존재하지 않으면 오선을 지우는 코드
    for staff in range(len(staves)):
        top_pixel = staves[staff][0]  # 오선의 최상단 y 좌표
        bot_pixel = staves[staff][0] + staves[staff][1] - 1  # 오선의 최하단 y 좌표 (오선의 최상단 y 좌표 + 오선 높이)
        for col in range(width):
            if image[top_pixel - 1][col] == 0 and image[bot_pixel + 1][col] == 0:  # 오선 위, 아래로 픽셀이 있는지 탐색
                for row in range(top_pixel, bot_pixel + 1):
                    image[row][col] = 0  # 오선을 지움
    return image, [x[0] for x in staves]    

#전처리 3
#이미지 정규화
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