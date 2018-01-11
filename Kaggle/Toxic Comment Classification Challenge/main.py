def toxicClf():
    # -*- coding: UTF-8 -*-
    # 读入数据
    import pandas as pd
    import time

    print("start: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    dataPath = "F:\\Datas\\Kaggle\\Toxic Comment Classification Challenge\\"
    train = pd.read_csv(dataPath + "train.csv\\train.csv")
    test = pd.read_csv(dataPath + "test.csv\\test.csv")
    test_id = test["id"]
    train = train.drop(["id"], axis=1)
    test = test.drop(["id"], axis=1)
    # train = train.iloc[:200,:] #取200条测试程序
    # test = test.iloc[:5, :]#取20条测试程序
    fulldata = pd.concat([train, test], axis=0, ignore_index=True)
    fulldata = fulldata.drop(['identity_hate', 'insult', 'obscene',
                              'severe_toxic', 'threat', 'toxic'], axis=1)
    print("加载数据完毕！")

    # =================================================
    # -*- coding: UTF-8 -*-
    # 数据预处理
    import re
    # 大写转为小写
    m = fulldata.shape[0]
    fulldata["comment_text"] = fulldata["comment_text"].str.lower()

    # 去除无用的符号用空格代替 ? , , \n .
    # 去除停用词
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer

    import sys
    sys.setrecursionlimit(1000000)  # 例如这里设置为一百万
    porter_stemmer = PorterStemmer()
    print("开始去除无用符号、停用词、提取词干")
    for i in range(m):
        if (i % 1000 == 0):
            print("第", i, "条去除停用词etc")

        tmp = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！,.？?、~@#￥%……&*（）]",
                     " ", str(fulldata["comment_text"][i]))  # 去除符号
        tmp1 = ' '.join([word for word in tmp.split()
                         if word not in (stopwords.words('english'))])  # 去停用词
        tmp3 = ""
        for word in tmp1.split():
            tmp3 = tmp3 + " " + porter_stemmer.stem(word)  # 波特词干算法分词器
        fulldata["comment_text"][i] = tmp3

    print("去除无用符号、停用词、提取词干完毕！")

    # =================================================
    # 提取词干
    # from nltk.stem.porter import PorterStemmer
    # porter_stemmer = PorterStemmer()
    # for i in range(m):
    #     tmp = ""
    #     for word in fulldata["comment_text"][i].split():
    #         tmp= tmp + " " + porter_stemmer.stem(word) #波特词干算法分词器
    #     fulldata["comment_text"][i] = tmp
    #
    # print ("提取词干完毕")

    # =================================================
    # 向量化
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    list_fulldata = np.array(fulldata["comment_text"]).tolist()  # fit_transform中必须传入可迭代的list
    vectorizer = TfidfVectorizer()
    vec_fulldata = vectorizer.fit_transform(list_fulldata).toarray()  # 非常稀疏，打印出来看到的几乎是0
    print("向量化完毕")

    # ================================================
    # 准备train_X, test_X, train_y
    m1 = train.shape[0]
    train_X = vec_fulldata[:m1]
    test_X = vec_fulldata[m1:]

    # 重新构造train_y['class']
    train_y = train.iloc[:, 1:]
    print("预处理结束: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # ===========================================================
    # 训练模型，预测
    print("开始训练模型")
    import skmultilearn
    from skmultilearn.problem_transform import LabelPowerset
    from sklearn.naive_bayes import GaussianNB
    clf = LabelPowerset(GaussianNB())
    clf.fit(train_X, train_y)
    print("fit is finished!", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    predicts = clf.predict_proba(test_X).toarray()

    # ===========================
    # 结果保存到文件
    # "toxic  severe_toxic  obscene  threat  insult  identity_hate"
    answer = pd.DataFrame(predicts, columns=["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"])
    answer = pd.concat([pd.DataFrame(test_id), answer], axis=1)
    answer.to_csv(dataPath + "answer.csv", index=False)
    print("all finished!", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


import sys
import threading
if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    threading.stack_size(200000000)
    thread = threading.Thread(target = toxicClf())
    thread.start()