#modules
import cv2
import numpy as np
import functions as fs

#전처리 1
#초기 이미지에서 이진화항 후 보표 영역 이미지만 추출
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