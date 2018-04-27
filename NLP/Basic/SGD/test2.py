# _*_ coding: utf-8 _*_

from sklearn.datasets import fetch_mldata
from sklearn.model_selection import train_test_split
import numpy as np

#get mnist data and transfer to binary label
def data_process():
    '''
    prepaer data
    :return:
    '''
    mnist = fetch_mldata('MNIST original')
    X = mnist['data']
    y = mnist['target']
    for j in range(y.shape[0]):  # transfer y to binary label
        if (y[j] % 2 == 0):
            y[j] = 1  # label 1 for even
        else:
            y[j] = -1  # label -1 for odd

    #split train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.15)
    return X_train, X_test, y_train, y_test

#sigmod for binary classfication
def sigmod(z):
    tmp =  1/(1 + np.exp(-z))   #sigmod
    if tmp < 0.5:
        return -1
    else :
        return 1

#这个loss可能算得不对
def cal_loss(X, y, W, lmda):
    loss_sum = 0
    n = X.shape[0]
    for i in range(X.shape[0]):
        loss_sum += np.log(1 + np.exp(-y[i] * np.dot(W.T, X[i].T))) #按照作业里的loss function写的
    loss = (loss_sum*1.0 / n) + lmda * np.linalg.norm(W)            #加上一个正则项，再取平均
    return loss

#mini-batch SGD, 计算grad
def gradient(X, y, W, lmda):
    grad_sum = 0
    n = X.shape[0]
    for i in range(X.shape[0]):
        grad_sum += (-y[i]*X[i]) /(1 + np.exp(y[i] * np.dot(W.T,X[i].T))) #loss function的导数
    grad = grad_sum /n + lmda
    return grad

#shuffle 洗一下数据
def shuffleData(data):
    np.random.shuffle(data)
    cols = data.shape[1]
    X = data[:, 0:cols-1]
    y = data[:, cols-1:]
    return X, y

def train(X_train, y_train, batch_size, learn_rate):
    import time
    # 迭代阀值，当两次迭代损失函数之差小于该阀值时停止迭代
    start_time = time.time()
    epsilon = 1e-5            #迭代阈值
    max_steps = 10000

    data = np.c_[X_train,y_train]
    X, y = shuffleData(data)

    old_loss = 0
    new_loss = 0
    W = np.random.rand(X_train.shape[1],)
    lmda = 0.004                    #norm
    k = 0
    for step in range(max_steps):
        print("step %d :"%step)
        X_batch  = X[k:k+batch_size]
        y_batch = y[k:k+batch_size]
        k += batch_size
        if(k >= X.shape[0]):            #一次epoch之后， 再洗洗数据
            X, y = shuffleData(data)
            k = 0
            continue
        grad = gradient(X_batch, y_batch, W, lmda)          #计算梯度
        W = W - learn_rate * grad                           #更新参数
        new_loss = cal_loss(X_batch, y_batch, W, lmda)      #算算loss
        print("loss:", new_loss)
        if(abs(new_loss - old_loss) < epsilon):             #两次loss间的差如果足够小，就可以停了
            break
        old_loss = new_loss

    end_time = time.time()
    return W, new_loss,  end_time - start_time

def test(X_test, y_test, W):
    fx = -np.dot(W.T, X_test.T).T

    for i in range(fx.shape[0]):
        fx[i] = sigmod(fx[i])
    y_pred = fx
    return y_pred


from sklearn import metrics
BATCH_SIZE = 100    #batch size
LEARN_RATE = 0.01   #learning rate
LMDA = 0.004        #norm weight
if __name__ == '__main__':
    # prepare data
    X_train, X_test, y_train, y_test = data_process()
    print(X_train.shape, y_train.shape)

    #train
    W,loss, time = train(X_train, y_train, BATCH_SIZE, LEARN_RATE)
    print("\ndonedonedonedonedone!")
    print("loss is %f" %loss)

    #test
    y_pred = test(X_test, y_test, W)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    recall = metrics.recall_score(y_test, y_pred)
    f1 = metrics.f1_score(y_test, y_pred)
    print("accuracy is %f, recall is %f, f1 value is %f" %(accuracy, recall, f1))