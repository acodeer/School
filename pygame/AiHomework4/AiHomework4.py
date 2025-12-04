import numpy as np
import time
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import Callback
import matplotlib.pyplot as plt




# 과제 요구사항에 따라 학습 시간 제한(10분 = 600초)을 위한 커스텀 콜백 정의
class TimeLimitCallback(Callback):
    """지정된 시간(10분)을 초과하면 학습을 중지하는 콜백"""
    def __init__(self, time_limit_seconds=600):  # 10분 = 600초
        super(TimeLimitCallback, self).__init__()
        self.time_limit = time_limit_seconds
        self.start_time = time.time()

    def on_epoch_end(self, epoch, logs=None):
        elapsed_time = time.time() - self.start_time
        
        if elapsed_time > self.time_limit:
            print(f"\n10분 초과") # 사용자가 요청한 단순화된 메시지
            self.model.stop_training = True
            return


# 1. 데이터 로드 및 전처리
cifar10 = keras.datasets.cifar10
(x_train_orig, y_train_orig), (x_test_orig, y_test_orig) = cifar10.load_data()
x_train, x_test = x_train_orig / 255.0, x_test_orig / 255.0

# 레이블 원-핫 인코딩
y_train = keras.utils.to_categorical(y_train_orig, num_classes=10)
y_test = keras.utils.to_categorical(y_test_orig, num_classes=10)

try:
    # import model1 # 신경망 1 (FCN)
    # import model2 # 신경망 2 (CNN)
     import model3 # 신경망 3 (개선 FCN)
    # import model4 # 신경망 4 (개선 CNN)
    # import model5 # 신경망 5 (Subclass CNN)
except ImportError as e:
    print(f"경고: 모델 파일 임포트 오류 - {e}. 학습을 시작하려면 필요한 모델 파일을 준비하세요.")
    
# 2. 모델 선택
model = model3.model 

model_name = model.name if hasattr(model, 'name') else "Selected Model"
EPOCHS = 400
BATCH_SIZE = 100

model.summary()


# 3. 모델 학습 및 평가
print("\n모델 학습 시작:")
time_callback = TimeLimitCallback(time_limit_seconds=600)
history = model.fit(x_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, 
                    validation_data=(x_test, y_test), 
                    callbacks=[time_callback], 
                    verbose=0) 

print("\n모델 최종 평가 (model.evaluate):")
loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy*100:.2f}%")


# 4. 최종 예측 및 수동 평가 (사용자 요청 방식)
y_new = model.predict(x_test, verbose=0)
y_label = tf.argmax(y_new, axis=1) # 예측된 정수 레이블
y_test_labels = tf.argmax(y_test, axis=1) # 실제 정답 정수 레이블

total_count = len(y_label)
correct_count = 0
# 수동으로 정답 개수 계산
for i in range(total_count):
    if y_label.numpy()[i] == y_test_labels.numpy()[i]: # 텐서 비교를 위한 .numpy() 호출
        correct_count += 1
        
print("\n[수동 검증 결과]:")
print(f"총 개수: {total_count}, 맞춘 개수: {correct_count}, 정확도: {correct_count / total_count * 100:.2f}%")


# 5. 학습 추이 그래프 생성
def plot_history(history, metric, title):
    """정확도 또는 손실 변화 그래프를 그리는 함수 (단일 모델용)"""
    try:
        plt.figure(figsize=(12, 5))
        
        # 훈련 데이터 곡선
        epochs = range(1, len(history[metric]) + 1)
        plt.plot(epochs, history[metric], label=f'Training {title}', linestyle='--')
        
        # 검증 데이터 곡선
        val_metric = f'val_{metric}'
        plt.plot(epochs, history[val_metric], label=f'Validation {title}', linestyle='-')

        plt.title(f'{title} Trend of {model_name}', fontsize=15)
        plt.xlabel('Epoch', fontsize=12)
        plt.ylabel(title, fontsize=12)
        plt.legend(loc='lower right' if title == '정확도' else 'upper right')
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"\n[그래프 생성 오류]: 그래프를 생성하는 중 오류가 발생했습니다. 환경 문제일 수 있습니다. 오류: {e}")

# 그래프 호출: history 객체를 직접 전달하도록 변경
plot_history(history.history, 'categorical_accuracy', 'Accuracy')
plot_history(history.history, 'loss', 'Loss')

