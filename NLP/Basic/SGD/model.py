# _*_ coding: utf-8 _*_

from sklearn.datasets import fetch_mldata, fetch_covtype

from sklearn.model_selection import train_test_split
import numpy as np
import logging
logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#read data and transfer to binary label
def data_process(opt):
    '''
    prepaer data
    :return:
    '''
    if opt == 1:                                    # 1 for load MNIST, else load cortype
        data = fetch_mldata('MNIST original')
    else:
        data = fetch_covtype()
    X = data['data']
    y = data['target']
    for j in range(y.shape[0]):  # transfer y to binary label
        if (y[j] % 2 == 0):
            y[j] = 0  # label 0 for even
        else:
            y[j] = 1  # label 1 for odd

    #split train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.15)
    return X_train, X_test, y_train, y_test

#sigmoid for binary classfication
def sigmoid(z):
    z = 705 if z > 705 else z       # in np.exp(z): z can't larger than 709
    z = -705 if z < -705 else z
    return  1.0/(1 + np.exp(-z))

def cal_loss(X, y, W, lmda):
    loss_sum = 0
    n = X.shape[0]
    for i in range(X.shape[0]):
        loss_sum += -np.log(sigmoid(y[i] * np.dot(W.T, X[i].T)))
        # loss_sum += np.log(1 + np.exp(-y[i] * np.dot(W.T, X[i].T))) #按照作业里的loss function写的
    loss = (loss_sum*1.0 / n) + lmda * np.linalg.norm(W)            #加上一个正则项，再取平均
    return loss

def gradient(X, y, W, lmda):
    grad_sum = 0.0
    n = X.shape[0]
    for i in range(X.shape[0]):
        grad_sum = (1 - sigmoid(y[i] * np.dot(W.T,X[i].T))) * (-y[i] * X[i]) #loss function的导数
    norm_grad = np.zeros((W.shape[0],))
    for i in range(W.shape[0]):
        norm_grad[i] = 1 if W[i] > 0 else -1
    grad = grad_sum * 1.0/n + lmda * norm_grad
    return grad

#shuffle 洗一下数据
def shuffleData(data):
    np.random.shuffle(data)
    cols = data.shape[1]
    X = data[:, 0:cols-1]
    y = data[:, cols-1:]
    return X, y

def momentum_train(X_train, y_train, batch_size, alpha, max_epochs, lmda):
    loss_list = []                              #for drawing graph
    data = np.c_[X_train,y_train]
    X, y = shuffleData(data)
    new_loss = 0
    W = np.random.uniform(size=(X_train.shape[1],))

    V = np.zeros((X_train.shape[1], ))          #argument for momentum
    beta = 0.5

    k = 0
    for epoch in range(max_epochs):
        if epoch >= 20:                         #beta is set to 0.5 until the initial learning stabilizes
            beta = 0.99                         #and then is increased to 0.9 or higher.

        while(True):
            X_batch  = X[k:k+batch_size]
            y_batch = y[k:k+batch_size]
            k += batch_size
            if(k >= X.shape[0]):                                #一次epoch之后， 再洗洗数据
                X, y = shuffleData(data)
                k = 0
                break
            grad = gradient(X_batch, y_batch, W, lmda)          #计算梯度
            V = beta * V + alpha * grad
            W = W - V                                           #更新参数
            new_loss = cal_loss(X_batch, y_batch, W, lmda)      #算算loss
        logger.info("epoch %d: loss is %f" %(epoch, new_loss))
        if epoch%100 == 0:
            loss_list.append(new_loss)
        alpha = alpha * 0.5 if alpha > 1e-4 else alpha          #learn rate decrease every epoch

    return W, new_loss,  loss_list

def adagrad_train(X_train, y_train, batch_size, alpha, max_epochs, lmda):
    loss_list = []                      #for drawing graph
    data = np.c_[X_train,y_train]
    X, y = shuffleData(data)
    new_loss = 0
    W = np.random.uniform(size=(X_train.shape[1],))

    G = np.zeros((X_train.shape[1], ))  #parameters for Adagrad
    eps = 1e-8

    k = 0
    for epoch in range(max_epochs):
        while(True):
            X_batch  = X[k:k+batch_size]
            y_batch = y[k:k+batch_size]
            k += batch_size
            if(k >= X.shape[0]):                                #一次epoch之后， 再洗洗数据
                X, y = shuffleData(data)
                k = 0
                break
            grad = gradient(X_batch, y_batch, W, lmda)          #计算梯度
            for j in range(grad.shape[0]):
                G[j] += grad[j]**2
                W[j] = W[j] - alpha * grad[j] / np.sqrt(G[j] + eps)

            new_loss = cal_loss(X_batch, y_batch, W, lmda)      #算算loss
        logger.info("epoch %d: loss is %f" %(epoch, new_loss))
        if epoch%100 == 0:
            loss_list.append(new_loss)
    return W, new_loss,  loss_list


def SGD_train(X_train, y_train, batch_size,alpha, max_epochs, lmda):
    import time
    start_time = time.time()
    data = np.c_[X_train,y_train]
    X, y = shuffleData(data)

    new_loss = 0
    W = np.random.uniform(size=(X_train.shape[1],))
    k = 0
    for epoch in range(max_epochs):
        while(True):
            X_batch  = X[k:k+batch_size]
            y_batch = y[k:k+batch_size]
            k += batch_size
            if(k >= X.shape[0]):            #一次epoch之后， 再洗洗数据
                X, y = shuffleData(data)
                k = 0
                break
            grad = gradient(X_batch, y_batch, W, lmda)          #计算梯度
            W = W - alpha * grad                           #更新参数
            new_loss = cal_loss(X_batch, y_batch, W, lmda)      #算算loss
            # print("loss:", new_loss)
        logger.info("epoch %d: loss is %f" %(epoch, new_loss))

    end_time = time.time()
    return W, new_loss,  end_time - start_time

def test(X_test, y_test, W):
    y_pred = np.zeros((X_test.shape[0], ))
    for i in range(X_test.shape[0]):
        y_pred[i] = sigmoid(np.dot(W.T, X_test[i].T))
        y_pred[i] = 1 if y_pred[i] >= 0.5 else 0
    return y_pred

if __name__ == '__main__':
                                        # 1 for load MNIST, else load cortype
    # data = fetch_mldata('MNIST original')
    data = fetch_covtype()
    X = data['data']
    y = data['target']
    for j in range(y.shape[0]):  # transfer y to binary label
        if (y[j] % 2 == 0):
            y[j] = 0  # label 0 for even
        else:
            y[j] = 1  # label 1 for odd

    #split train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.15)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
