#7.7프로그램 개선
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Flatten, Dense, Dropout # Dropout 임포트
from tensorflow.keras import regularizers # regularizers 임포트
from tensorflow.keras.callbacks import Callback

model = keras.Sequential()
model.add(Flatten(input_shape=(32, 32, 3)))

# --- 🚨 규제 강도를 낮추어 10분 내 수렴을 유도 ---

# L2 정규화는 제거하거나 0.0001로 낮춥니다.
model.add(Dense(512, activation = 'relu'))
model.add(Dropout(0.2)) # 0.4 -> 0.2로 강도 완화

model.add(Dense(256, activation = 'relu'))
model.add(Dropout(0.15)) # 0.4 -> 0.2로 강도 완화

model.add(Dense(128, activation = 'relu'))
model.add(Dropout(0.1)) # 0.3 -> 0.2로 강도 완화

# 출력 레이어
model.add(Dense(10, activation = 'softmax'))

# --- 재조정 끝 ---

model.compile(optimizer=keras.optimizers.Adam(learning_rate = 0.003), 
               loss='categorical_crossentropy',
                metrics=['categorical_accuracy'])
model.summary()