#프로그램 8.3
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.callbacks import Callback

model = keras.Sequential()

# 1. CIFAR-10 Input shape
model.add(Input(shape=(32, 32, 3)))

# 2. Convolution layers
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# 3. Flatten + Dense
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.summary()

# 4. compile 수정 (categorical_crossentropy가 일반적)
model.compile(
    optimizer=keras.optimizers.SGD(learning_rate=0.1),
    loss='categorical_crossentropy',
    metrics=['categorical_accuracy']
)
