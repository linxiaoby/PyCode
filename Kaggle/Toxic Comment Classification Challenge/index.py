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



#向量化
#=================================================
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()

for i in range(5):
    tmp = ""
    for word in fulldata["comment_text"][i].split():
        tmp= tmp + " " + porter_stemmer.stem(word) #波特词干算法分词器
    fulldata["comment_text"][i] = tmp
print fulldata.head()