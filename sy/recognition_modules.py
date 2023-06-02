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
        w >= fs.weighted(25) and  # 넓이 조건
        h >= fs.weighted(50) and  # 높이 조건
        area >= fs.weighted(300)  # 픽셀 갯수 조건
    )
    if note_condition:
        for i in range(len(stems)):
            stem = stems[i]
            head_exist, head_fill, head_center = recognize_note_head(image, stem, direction)
            if head_exist:
                tail_cnt = recognize_note_tail(image, i, stem, direction)
                note_classification = (
                    ((head_fill and tail_cnt == 0), 4),
                    ((head_fill and tail_cnt == 1), 8),
                    ((head_fill and tail_cnt == 2), 16),
                    ((head_fill and tail_cnt == 3), 32),
                )

                for j in range(len(note_classification)):
                    if note_classification[j][0]:
                        note = note_classification[j][1]
                        pitch = recognize_pitch(image, staff, head_center)
                        notes.append(note)
                        pitches.append(pitch)
                        break

    return notes, pitches

# 음표 머리 인식
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

    cnt = 0  # cnt = 끊기지 않고 이어져 있는 선의 개수를 셈
    cnt_max = 0  # cnt_max = cnt 중 가장 큰 값
    head_center = 0
    pixel_cnt = fs.count_rect_pixels(image, (area_left, area_top, area_right - area_left, area_bot - area_top))

    for row in range(area_top, area_bot):
        col, pixels = fs.get_line(image, fs.HORIZONTAL, row, area_left, area_right, 5)
        pixels += 1
        if pixels >= fs.weighted(2):
            cnt += 1
            cnt_max = max(cnt_max, pixels)
            head_center += row

    head_exist = (cnt >= 3 and pixel_cnt >= 50)
    head_fill = (cnt >= 10 and cnt_max >= 11 and pixel_cnt >= 100)
    if cnt==0:
        pass
    else:
        head_center /= cnt

    return head_exist, head_fill, head_center

# 음표 꼬리 인식
def recognize_note_tail(image, index, stem, direction):
    (x, y, w, h) = stem
    if direction:  # 정 방향 음표
        area_top = y  # 음표 꼬리를 탐색할 위치 (상단)
        area_bot = y + h - fs.weighted(15)  # 음표 꼬리를 탐색할 위치 (하단)
    else:  # 역 방향 음표
        area_top = y + fs.weighted(15)  # 음표 꼬리를 탐색할 위치 (상단)
        area_bot = y + h  # 음표 꼬리를 탐색할 위치 (하단)
    if index:
        area_col = x - fs.weighted(4)  # 음표 꼬리를 탐색할 위치 (열)
    else:
        area_col = x + w + fs.weighted(4)  # 음표 꼬리를 탐색할 위치 (열)

    cnt = fs.count_pixels_part(image, area_top, area_bot, area_col)

    return cnt

# 보표위 음표 위치 인식->보조선 추가
def recognize_pitch(image, staff, head_center):
    pitch_lines = [staff[4] + fs.weighted(30) - fs.weighted(5) * i for i in range(21)]

    for i in range(len(pitch_lines)):
        line = pitch_lines[i]
        if line + fs.weighted(2) >= head_center >= line - fs.weighted(2):
            return i
        
# 쉼표 검출
def recognize_rest(image, staff, stats):
    x, y, w, h, area = stats
    center = fs.get_center(y, h)
    rest_condition = staff[3] > center > staff[1]
    if rest_condition:
        if h >= fs.weighted(40):
            cnt = fs.count_pixels_part(image, y, y + h, x + fs.weighted(1))
            if cnt == 2 or cnt ==1 or cnt ==3:
                fs.put_text(image, "r4", (x, y + h + fs.weighted(30)))
            else:
                fs.put_text(image, "r16", (x, y + h + fs.weighted(30)))
        elif fs.weighted(28) >= h >= fs.weighted(25):
            fs.put_text(image, "r8", (x, y + h + fs.weighted(30)))
        elif fs.weighted(8) >= h:
            if staff[1] + fs.weighted(5) >= center >= staff[1]:
                fs.put_text(image, "r1", (x, y + h + fs.weighted(30)))
            elif staff[2] >= center >= staff[1] + fs.weighted(5):
                fs.put_text(image, "r2", (x, y + h + fs.weighted(30)))

    pass

# def recognize_rest(image, staff, stats):
#     x, y, w, h, area = stats
#     center = fs.get_center(y, h)
#     rest_condition = staff[3] > center > staff[1]
#     if rest_condition:
#         cnt = fs.count_pixels_part(image, y, y + h, x + fs.weighted(1))

#         fs.put_text(image, w, (x, y + h + fs.weighted(30)))
#         fs.put_text(image, h, (x, y + h + fs.weighted(60)))
#         fs.put_text(image, cnt, (x, y + h + fs.weighted(90)))

#     pass