import os
import json
import glob
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def run_drum_note_cnn():
    # 모델을 로드합니다.
    model = load_model('D:/music-sheet-algoritm/note_deep_learning/DrumNote_CNN_Model.keras')

    # 클래스 정보를 로드합니다.
    with open('D:/music-sheet-algoritm/note_deep_learning/class_indices.json', 'r') as f:
        class_indices = json.load(f)

    # 최상위 폴더 경로
    top_folder = 'D:/music-sheet-algoritm/note_deep_learning/drum_sheet'

    # 각 상위 폴더의 예측 결과를 저장할 딕셔너리 초기화
    all_folder_predictions = {}

    def image_prediction(prediction_list, image_files):
        # 각 이미지에 대한 예측 수행 및 결과 저장
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

            # 예측 결과를 리스트에 추가
            prediction_list.append(predicted_class_name)
        return prediction_list

    # 각 하위 폴더의 예측 결과를 저장합니다.
    for root, dirs, files in os.walk(top_folder):
        for subdir in dirs:
            if subdir.startswith('test_') and subdir.count('_') == 1:  # 상위 폴더 검사
                parent_folder = os.path.join(root, subdir)

                # 이미지 폴더가 이미 존재하는 경우 처리 건너뛰기
                predictions_txt_path = os.path.join(parent_folder, f"{os.path.basename(parent_folder)}_predictions.txt")
                if os.path.exists(predictions_txt_path):
                    print(f"Predictions already exist for folder '{os.path.basename(parent_folder)}'. Skipping processing for this folder.")
                    continue

                # 하위 폴더 내의 하위 폴더 목록 가져오기
                subdirs = [d for d in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, d))]

                # 예측 결과 저장 리스트 초기화
                predictions = []

                # 각 하위 폴더의 예측 결과를 저장합니다.
                for subdir_name in subdirs:
                    subdir_path = os.path.join(parent_folder, subdir_name)

                    # 이미지 파일 목록 가져오기
                    image_files = glob.glob(os.path.join(subdir_path, '*.jpg'))

                    # 하위 폴더의 예측 결과 저장 리스트 초기화
                    subdir_predictions = []

                    subdir_predictions = image_prediction(subdir_predictions, image_files)

                    # 예측 결과를 띄워쓰기로 구분된 문자열로 만듭니다.
                    subdir_predictions_text = " ".join(subdir_predictions)

                    # 각 하위 폴더의 예측 결과를 상위 폴더의 예측 결과에 추가
                    predictions.append(subdir_predictions_text)

                # 상위 폴더의 예측 결과를 하나의 문자열로 합치기
                all_predictions_text = "\n".join(predictions)

                # 상위 폴더의 예측 결과를 저장
                all_folder_predictions[parent_folder] = all_predictions_text

                # 상위 폴더에 예측 결과 저장
                txt_filename = os.path.join(parent_folder, f"{os.path.basename(parent_folder)}_predictions.txt")
                with open(txt_filename, 'w') as txt_file:
                    txt_file.write(all_predictions_text)

    # 각 최하위 폴더의 예측 결과를 합친 후 상위 폴더에 저장
    for root, dirs, files in os.walk(top_folder):
        for subdir in dirs:
            if subdir.startswith('test_') and subdir.count('_') == 3:  # 최하위 폴더 검사
                test_folder = os.path.join(root, subdir)

                # 이미지 파일 목록 가져오기
                image_files = glob.glob(os.path.join(test_folder, '*.jpg'))

                # 예측 결과 저장 리스트 초기화
                predictions = []

                predictions = image_prediction(predictions, image_files)

                # 예측 결과를 띄워쓰기로 구분된 문자열로 만듭니다.
                predictions_text = " ".join(predictions)

                # 각 하위 폴더의 예측 결과를 해당 폴더에 저장
                txt_filename = os.path.join(test_folder, f"{subdir}_predictions.txt")
                with open(txt_filename, 'w') as txt_file:
                    txt_file.write(predictions_text)


if __name__ == "__main__":
    run_drum_note_cnn()