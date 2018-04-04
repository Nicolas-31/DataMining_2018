import pickle
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, add
from keras.layers import Conv2D, MaxPooling2D
import keras
import numpy as np

batch_size = 25
num_classes = 2
epochs = 10
(x_train, y_train),(x_test, y_test) = pickle.load(open('female.p', 'rb'))
#(x_train, y_train),(x_test, y_test) = pickle.load(open('male.p', 'rb'))

def reshape(x):
    x = np.asarray(x)
    x = x.astype('float32')
    return x/255

x_train = reshape(x_train)
x_test = reshape(x_test)
y_train = np.asarray(y_train)
y_test = np.asarray(y_test)
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Conv2D(8, 3, activation='relu', input_shape=np.shape(x_train)[1:]))
model.add(Conv2D(16, 3, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(24, 3, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, 3, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dropout(0.25))
model.add(Dense(128,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='sigmoid'))
model.summary()
model.compile(
        loss=keras.losses.categorical_crossentropy,
        optimizer=keras.optimizers.Adadelta(),
        metrics=['accuracy'])
model.fit(x_train,y_train,batch_size=batch_size,epochs=epochs,verbose=2,validation_data=(x_test,y_test))
score = model.evaluate(x_test,y_test,verbose=2)
