import tensorflow.keras
import numpy as np
import cv2
import serial
import time

# 아두이노와의 시리얼 통신 설정
arduino_port = 'COM8'  # 아두이노가 연결된 포트 (OS에 따라 다를 수 있습니다)
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # 아두이노가 리셋될 시간을 줌

# 모델 위치
model_filename = 'C:/Users/kimso/OneDrive/Desktop/AI_Edu/drone_jamming_arduino/drone_jamming_arduino/tm-my-image-model/model.json'

# 케라스 모델 가져오기
model = tensorflow.keras.models.load_model(model_filename)

# 카메라를 제어할 수 있는 객체
capture = cv2.VideoCapture(0)

# 카메라 길이 너비 조절
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# 이미지 처리하기
def preprocessing(frame):
    # 이미지 사이즈 조정 (티처블 머신에서 사용한 이미지 사이즈로 변경)
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    
    # 이미지 정규화
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

    # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    return frame_reshaped

# 예측용 함수
def predict(frame):
    prediction = model.predict(frame)
    return prediction

while True:
    ret, frame = capture.read()
    
    if not ret:
        print("카메라로부터 프레임을 가져올 수 없습니다.")
        break

    preprocessed = preprocessing(frame)
    prediction = predict(preprocessed)

    # 드론 클래스와 빈 하늘 클래스 비교
    if prediction[0, 0] > prediction[0, 1]:
        label = 'Drone detected'
        print('Drone detected')
        arduino.write(b'1')  # 드론이 감지되었을 때 아두이노로 '1' 전송
    else:
        label = 'No drone (Sky)'
        print('No drone (Sky)')
        arduino.write(b'0')  # 빈 하늘이 감지되었을 때 아두이노로 '0' 전송

    # 예측 결과를 화면에 표시
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("VideoFrame", frame)

    if cv2.waitKey(100) > 0: 
        break

capture.release()
cv2.destroyAllWindows()
arduino.close()