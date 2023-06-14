import cv2
import os
import functions as fs

#이미지 불러오기
image=cv2.imread("C:/music-sheet-algoritm/yr/music_sheet_jpg/drum_sheet(1)_page_1.jpg", cv2.IMREAD_ANYCOLOR)

# 1. 보표 영역 추출 및 그 외 노이즈 제거
image = fs.threshold(image)  # 이미지 이진화
cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(image)  # 레이블링
#cnt는 객체수, labels는 레이블맵 행렬, stats는 객체의 정보, centroids는 무게 중심 좌표
for i in range(1, cnt): #0번 객체는 배경
    x, y, w, h, area = stats[i] #stats에는 x좌표, y좌표, 넓이, 높이, 픽셀의 개수
    cv2.rectangle(image, (x, y, w, h), (255, 0, 0), 1)  # 사각형 그리기

#이미지 띄우기
cv2.imshow('image', image)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()