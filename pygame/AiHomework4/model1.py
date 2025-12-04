import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.callbacks import Callback

model = keras.Sequential()
model.add(Flatten(input_shape=(32, 32, 3)))
model.add(Dense(128, activation='sigmoid'))
model.add(Dense(10, activation='softmax'))

# 컴파일 설정
model.compile(optimizer=keras.optimizers.SGD(learning_rate = 0.01), 
              loss='categorical_crossentropy', 
              metrics=['categorical_accuracy'])

model.summary()