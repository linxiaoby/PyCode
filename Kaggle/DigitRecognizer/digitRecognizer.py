#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.neighbors  import KNeighborsClassifier
#导入数据
dataPath = "F:\\Datas\\Kaggle\\DigitRecognizer\\"
train = pd.read_csv(dataPath + "train.csv")
test = pd.read_csv(dataPath + "test.csv")

#准备数据
ratio = 1
trainSize = train.shape[0]
testSize = test.shape[0]
train = train.iloc[:int(trainSize*ratio),:]
testData = test.iloc[:int(testSize*ratio),:]
trainLabel = train["label"]
trainData = train.drop(["label"],axis = 1)

print trainData.shape, testData.shape, trainLabel.shape

#开始训练
neigh = KNeighborsClassifier(n_neighbors = 5)
neigh.fit(trainData, trainLabel)
print "fit finished"
predictLabel = neigh.predict(testData)
print "predict finished!"

resultCsv = pd.DataFrame()
resultCsv["ImageId"] = range(1,testData.shape[0] + 1)
resultCsv["Label"] = predictLabel
resultCsv.to_csv(dataPath + "submission.csv", index=False)
print "finished!"



