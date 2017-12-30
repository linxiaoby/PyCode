# coding:utf-8
# Baseline MLP for MNIST dataset
import numpy
import pandas as pd
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
seed = 7
numpy.random.seed(seed)

dataPath = "F:\\Datas\\Kaggle\\DigitRecognizer\\"

#加载数据
(X_train, y_train), (X_test, y_test) = mnist.load_data()
print (X_train.shape, X_test.shape)

num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape(X_train.shape[0], num_pixels).astype('float32')
X_test = X_test.reshape(X_test.shape[0], num_pixels).astype('float32')
X_train = X_train / 255
X_test = X_test / 255

# 对输出进行one hot编码
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

# MLP模型
def baseline_model():
     model = Sequential()
     model.add(Dense(num_pixels, input_dim=num_pixels, init='normal', activation='relu'))
     model.add(Dense(num_classes, init='normal', activation='softmax'))
     model.summary()
     model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
     return model

 # 建立模型
model = baseline_model()

 # Fit
model.fit(X_train, y_train, validation_data=(X_test, y_test), nb_epoch=10, batch_size=200, verbose=2)

#Evaluation
scores = model.evaluate(X_test, y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))#输出错误率

results = model.predict(X_test, batch_size=200)

# select the indix with the maximum probability
results = numpy.argmax(results,axis = 1)

results = numpy.Series(results,name="Label")
submission = numpy.concat([pandas.Series(range(1,28001),name = "ImageId"),results],axis = 1)

submission.to_csv("cnn_mnist_datagen.csv",index=False)




