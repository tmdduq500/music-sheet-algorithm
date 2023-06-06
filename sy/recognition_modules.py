import functions_sy as fs
import cv2

# 박자표 인식
def recognize_key(image, staves, stats):
    (x, y, w, h, area) = stats
    ts_conditions = (
        staves[0] + fs.weighted(5) >= y >= staves[0] - fs.weighted(5) and  # 상단 위치 조건
        staves[4] + fs.weighted(5) >= y + h >= staves[4] - fs.weighted(5) and  # 하단 위치 조건
        staves[2] + fs.weighted(5) >= fs.get_center(y, h) >= staves[2] - fs.weighted(5) and  # 중단 위치 조건
        fs.weighted(25) >= w >= fs.weighted(10) and  # 넓이 조건
        fs.weighted(55) >= h >= fs.weighted(35)  # 높이 조건
    )

    if ts_conditions:
        return True, 1
    else:  
        return False, 0

# 음표 인식
def recognize_note(image, staff, stats, stems, direction):
    (x, y, w, h, area) = stats
    notes = []
    pitches = []
    note_condition = (
        len(stems) and
        w >= fs.weighted(10) and  # 넓이 조건
        h >= fs.weighted(35) and  # 높이 조건
        area >= fs.weighted(120)  # 픽셀 갯수 조건
    )
    if note_condition:
        for i in range(len(stems)):
            stem = stems[i]
            recognize_note_head(image, stem, direction)

    pass

def recognize_note_head(image, stem, direction):
    (x, y, w, h) = stem
    if direction:  # 정 방향 음표
        area_top = y + h - fs.weighted(7)  # 음표 머리를 탐색할 위치 (상단)
        area_bot = y + h + fs.weighted(7)  # 음표 머리를 탐색할 위치 (하단)
        area_left = x - fs.weighted(14)  # 음표 머리를 탐색할 위치 (좌측)
        area_right = x  # 음표 머리를 탐색할 위치 (우측)
    else:  # 역 방향 음표
        area_top = y - fs.weighted(7)  # 음표 머리를 탐색할 위치 (상단)
        area_bot = y + fs.weighted(7)  # 음표 머리를 탐색할 위치 (하단)
        area_left = x + w  # 음표 머리를 탐색할 위치 (좌측)
        area_right = x + w + fs.weighted(14)  # 음표 머리를 탐색할 위치 (우측)

    cv2.rectangle(image, (area_left, area_top, area_right - area_left, area_bot - area_top), (255, 0, 0), 1)

    pass
# # 보표위 음표 위치 인식->보조선 추가
# def recognize_pitch(image, staff, head_center):
#     pitch_lines = [staff[4] + fs.weighted(30) - fs.weighted(5) * i for i in range(21)]

#     for i in range(len(pitch_lines)):
#         line = pitch_lines[i]
#         if line + fs.weighted(2) >= head_center >= line - fs.weighted(2):
#             return i
        
# # 쉼표 검출
# def recognize_rest(image, staff, stats):
#     x, y, w, h, area = stats
#     rest = 0
#     center = fs.get_center(y, h)
#     rest_condition = staff[3] > center > staff[1]

#     """ 쉼표 넓이, 높이 구하기
#        if rest_condition:
#         fs.put_text(image, w, (x, y + h + fs.weighted(30)))
#         fs.put_text(image, h, (x, y + h + fs.weighted(60)))
#     """

#     if rest_condition:
#         if fs.weighted(50) >= h >= fs.weighted(40):
#             cnt = fs.count_pixels_part(image, y, y + h, x + fs.weighted(1))
#             if cnt == 2 or cnt ==1 or cnt ==3:
#                 rest = 4
#             else:
#                 rest = 16        
#         elif fs.weighted(28) >= h >= fs.weighted(25):
#             rest =8 
#         elif fs.weighted(9) >= h:
#             if staff[1] + fs.weighted(5) >= center >= staff[1]:
#                 rest = 1
#             elif staff[2] >= center >= staff[1] + fs.weighted(5):
#                 rest = 2
#         if recognize_rest_dot(image, stats):
#             rest *= -1
#         if rest:
#             fs.put_text(image, rest, (x, y + h + fs.weighted(30)))
#             fs.put_text(image, -1, (x, y + h + fs.weighted(60)))

#     return rest

# # 쉼표 점 인식
# def recognize_rest_dot(image, stats):
#     (x, y, w, h, area) = stats
#     area_top = y - fs.weighted(10)  # 쉼표 점을 탐색할 위치 (상단)
#     area_bot = y + fs.weighted(10)  # 쉼표 점을 탐색할 위치 (하단)
#     area_left = x + w  # 쉼표 점을 탐색할 위치 (좌측)
#     area_right = x + w + fs.weighted(10)  # 쉼표 점을 탐색할 위치 (우측)
#     dot_rect = (
#         area_left,
#         area_top,
#         area_right - area_left,
#         area_bot - area_top
#     )

#     pixels = fs.count_rect_pixels(image, dot_rect)

#     return pixels >= fs.weighted(10)

# def recognize_whole_note(image, staff, stats):
#     whole_note = 0
#     pitch = 0
#     (x, y, w, h, area) = stats
#     while_note_condition = (
#             fs.weighted(22) >= w >= fs.weighted(12) >= h >= fs.weighted(9)
#     )
#     if while_note_condition:
#         dot_rect = (
#             x + w,
#             y - fs.weighted(10),
#             fs.weighted(10),
#             fs.weighted(20)
#         )
#         pixels = fs.count_rect_pixels(image, dot_rect)
#         whole_note = -1 if pixels >= fs.weighted(10) else 1
#         pitch = recognize_pitch(image, staff, fs.get_center(y, h))

#         fs.put_text(image, whole_note, (x, y + h + fs.weighted(30)))
#         fs.put_text(image, pitch, (x, y + h + fs.weighted(60)))
#     return whole_note, pitch