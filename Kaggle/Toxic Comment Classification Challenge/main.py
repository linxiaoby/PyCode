def toxicClf():
    # -*- coding: UTF-8 -*-
    # 读入数据
    import pandas as pd
    import time

    print("start: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    dataPath = "D:\\AllCode\\Datas\\Kaggle\\Toxic\\"
    train = pd.read_csv(dataPath + "train.csv\\train.csv")
    print (train.shape)
    test = pd.read_csv(dataPath + "test.csv\\test.csv")
    test_id = test["id"]
    train = train.drop(["id"], axis=1)
    test = test.drop(["id"], axis=1)
    train = train.iloc[:200,:] #取200条测试程序
    test = test.iloc[:5, :]#取20条测试程序
    fulldata = pd.concat([train, test], axis=0, ignore_index=True)
    fulldata = fulldata.drop(['identity_hate', 'insult', 'obscene',
                              'severe_toxic', 'threat', 'toxic'], axis=1)
    print("加载数据完毕！")

    # =================================================
    # -*- coding: UTF-8 -*-
    # 数据预处理
    # 去除无用的符号用空格代替 ? , , \n .
    # 去除停用词
    import re
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    print(type(stopwords.words('english')))
    porter_stemmer = PorterStemmer()
    print("开始去除无用符号、提取词干")
    m = fulldata.shape[0]
    for i in range(m):
        if (i % 1000 == 0):
            print("第", i, "条去除停用词etc")

        tmp = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！,.？?、~@#￥%……&*（）]",
                     " ", str(fulldata["comment_text"][i]))  # 去除符号
        tmp1 = ""
        for word in tmp.split():
            tmp1 = tmp1 + " " + porter_stemmer.stem(word)  # 波特词干算法分词器
        fulldata["comment_text"][i] = tmp1

    print("去除无用符号、提取词干完毕！")


    # =================================================
    # 向量化
    import numpy as np
    from sklearn.feature_extraction import text

    #构造停用词文件
    sk_stop_words = text.ENGLISH_STOP_WORDS
    nltk_stop_words = stopwords.words('english')
    my_stop_words = list(set(sk_stop_words).union(set(nltk_stop_words))) #sklearn的停用词和nltk的停用词合并，组成一个更大的停用词集

    list_fulldata = np.array(fulldata["comment_text"]).tolist()  # fit_transform中必须传入可迭代的list
    vectorizer = text.TfidfVectorizer(max_df = 0.98, stop_words = set(my_stop_words), lowercase = True)
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