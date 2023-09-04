from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import json
import numpy as np
import glob

# 모델을 로드합니다.
model = load_model('D:/note_deep_learning/DrumNote_CNN_Model.keras')

# 클래스 정보를 로드합니다.
with open('D:/note_deep_learning/class_indices.json', 'r') as f:
    class_indices = json.load(f)

# 이미지 파일이 있는 디렉토리 경로
image_directory = 'D:/note_deep_learning/test/'

# 이미지 파일 목록 가져오기
image_files = glob.glob(image_directory + '*.jpg')  # 필요한 이미지 확장자에 따라 수정

# 예측된 클래스 이름을 저장할 리스트 생성
predicted_class_names = []

# 각 이미지에 대한 예측 수행
for image_file in image_files:
    # 이미지 로드 및 전처리
    test_image = image.load_img(image_file, target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)

    # 예측 수행
    result = model.predict(test_image)

    # 예측 결과 확인
    predicted_class_index = np.argmax(result)
    predicted_class_name = [key for key, value in class_indices.items() if value == predicted_class_index][0]

    # 예측된 클래스 이름을 리스트에 추가
    predicted_class_names.append(predicted_class_name)

# 모든 이미지에 대한 예측된 클래스 이름이 담긴 리스트 출력
print(predicted_class_names)
