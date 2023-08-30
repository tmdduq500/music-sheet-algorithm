from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import os

# 입력 폴더와 출력 폴더 지정
input_folder = r"D:\train_note\test_note\8"
output_folder = r"D:\train_note\train_note\8"


# ImageDataGenerator를 사용하여 이미지 증강 설정
datagen = ImageDataGenerator(
    rotation_range=5,  # 이미지 회전 각도 범위
    width_shift_range=0.05,  # 가로로 이동 범위
    height_shift_range=0.05,  # 세로로 이동 범위
    brightness_range=[0.5, 1.5],  # 밝기 조정 범위
    shear_range=0.05,  # 전단 각도 범위
    zoom_range=0.05,  # 확대/축소 범위
    fill_mode='nearest'  # 이미지 확대 또는 축소 시 채울 방법
)

# 입력 폴더 내의 이미지 파일 리스트 가져오기
image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

# 이미지 증강 및 저장
for filename in image_files:
    input_path = os.path.join(input_folder, filename)
    img = image.load_img(input_path)
    x = image.img_to_array(img)
    x = x.reshape((1,) + x.shape)

    i = 0
    for batch in datagen.flow(x, batch_size=100):
        augmented_image = image.array_to_img(batch[0])
        output_path = os.path.join(output_folder, f"{filename.split('.')[0]}_{i}.jpg")
        augmented_image.save(output_path)
        i += 1
        if i % 10 == 0:  # 각 이미지당 10개의 이미지를 생성하도록 수정
            break

print("이미지 증강 및 저장 완료.")
