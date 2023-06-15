import cv2
import numpy as np
import os
import modules_sy as modules_sy
import functions_sy as fs

def find_templates(image_path, template_folder):
    image = cv2.imread(image_path, cv2.IMREAD_ANYCOLOR)
    # 악보 이미지 로드
    #전처리 1. 보표 영역 추출 및 그 외 노이즈 제거
    masked_image = modules_sy.remove_noise(image)
    removed_image, staves = modules_sy.remove_staves(masked_image)
    normalized_image, staves = modules_sy.normalization(removed_image, staves, 14)
    
    # 결과를 저장할 리스트 생성
    results = []

    # 템플릿 폴더 내의 이미지 파일들 가져오기
    template_files = os.listdir(template_folder)

    for template_file in template_files:
        # 템플릿 이미지 경로
        template_path = os.path.join(template_folder, template_file)

        # 템플릿 이미지 로드
        template = cv2.imread(template_path, cv2.IMREAD_ANYCOLOR)
        template = fs.threshold(template)

        # 템플릿 매칭 수행
        result = cv2.matchTemplate(normalized_image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 매칭 결과를 리스트에 추가
        results.append({
            'template_file': template_file,
            'max_val': max_val,
            'max_loc': max_loc
        })

    # 매칭 결과 정렬
    results = sorted(results, key=lambda x: x['max_val'], reverse=True)

    # 결과 출력
    for result in results:
        template_file = result['template_file']
        max_val = result['max_val']
        max_loc = result['max_loc']

        # 템플릿 이미지 로드 (원본 이미지와 동일한 차원을 가지도록)
        template = cv2.imread(os.path.join(template_folder, template_file), cv2.IMREAD_ANYCOLOR)
        template = fs.threshold(template)

        # 일치하는 영역의 좌상단과 우하단 좌표 계산
        template_width, template_height = template.shape[1], template.shape[0]
        top_left = max_loc
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

        # 원본 이미지에 일치하는 영역 표시
        cv2.rectangle(normalized_image, top_left, bottom_right, (125, 125, 0), 2)


        # 매칭된 영역의 이미지 표시
        cv2.imshow('Matched Template: ' + template_file, template)

        print('Template:', template_file)
        print('Max Value:', max_val)
        print('Max Location:', max_loc)
        print('---')

    # 전체 이미지에 대한 결과 출력
    cv2.imshow('Result', normalized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 악보 이미지 경로
image_path = "D:\\music-sheet-algoritm\\sy\\music_sheet_jpg\\7.jpg"

# 템플릿 이미지들이 있는 폴더 경로
template_folder = "D:\\music-sheet-algoritm\\sy\\note&rest_image\\"

# 템플릿 매칭 수행 및 결과 출력
find_templates(image_path, template_folder)