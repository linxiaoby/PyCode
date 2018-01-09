# -*- coding: UTF-8 -*-
#读入数据
import pandas as pd
dataPath = "D:\\AllCode\Datas\\Kaggle\\Toxic\\"
train = pd.read_csv(dataPath + "train.csv\\train.csv")
test = pd.read_csv(dataPath + "test.csv\\test.csv")
test_id = test["id"]
train = train.drop(["id"], axis=1)
test = test.drop(["id"], axis=1)

train = train.iloc[:200,:] #取200条测试程序
test = test.iloc[:20, :]#取20条测试程序

fulldata = pd.concat([train, test], axis=0, ignore_index = True)
fulldata = fulldata.drop(['identity_hate', 'insult', 'obscene',
                          'severe_toxic', 'threat', 'toxic'], axis = 1)
print fulldata["comment_text"][0]

#=================================================
# -*- coding: UTF-8 -*-
#数据预处理
import re
#大写转为小写
m = fulldata.shape[0]
fulldata["comment_text"] = fulldata["comment_text"].str.lower()

#去除无用的符号用空格代替 ? , , \n .
#去除停用词
import nltk
from nltk.corpus import stopwords
for i in range(5):
    tmp = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！,.？?、~@#￥%……&*（）]",
                                         " ",str(fulldata["comment_text"][i]))
    fulldata["comment_text"][i] = ' '.join([word for word in tmp.split()
                                         if word not in (stopwords.words('english'))])
print fulldata.head()


#=================================================
#提取词干
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()

for i in range(5):
    tmp = ""
    for word in fulldata["comment_text"][i].split():
        tmp= tmp + " " + porter_stemmer.stem(word) #波特词干算法分词器
    fulldata["comment_text"][i] = tmp
print "提取词干后：",fulldata.head()

#=================================================
#向量化
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
list_fulldata = np.array(fulldata["comment_text"]).tolist() #fit_transform中必须传入可迭代的list
vectorizer = TfidfVectorizer()
vec_fulldata = vectorizer.fit_transform(list_fulldata).toarray()#非常稀疏，打印出来看到的几乎是0

#================================================
#准备train_X, test_X, train_y
m1 = train.shape[0]
train_X = vec_fulldata[:m1]
test_X = vec_fulldata[m1:]

#重新构造train_y['class']
train_y = []
collist = train.columns.values
collist = collist[1:]
for i in range(m1):
    find = False
    for col in collist:
        if train[col][i] == 1:
            find = True
            train_y.append(str(col))
            break
    if find == False: #6个类别都为0，不为1, 新增类别“unkown”
        train_y.append("unknow")

#===========================================================
train_yy = pd.DataFrame({"class":train_y})
print train_X.shape, train_yy.shape
from sklearn import svm
clf = svm.SVC(probability=True)
clf.fit(train_X, train_y)
result1 = clf.predict(test_X)
result = clf.predict_proba(test_X)
print result1
