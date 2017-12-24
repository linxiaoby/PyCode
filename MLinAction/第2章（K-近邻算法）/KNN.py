from numpy import *
import operator
def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    label = ['A', 'A', 'B', 'B']
    return group, label



def classify0(inX, dataSet, labels, k = 3):
    '''
    # KNN紧邻算法
    :param inX:要进行分类的向量
    :param dataSet: 已知类别标签的数据集
    :param labels:  类别标签，行数和dataSet一致
    :param k: 近邻个数， 默认为3
    :return:
    '''
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis = 1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort() #按从小到大排序下标
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def autoNorm(dataSet):
    '''
    归一化函数
    :param dataSet: 要进行归一化的数据集 array_like
    :return: normDataSet归一化后的数据集，ranges每一列的最大值与最小值的差，minVals每一列的最小值
    '''
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet =  normDataSet / tile(ranges, (m, 1))
    return normDataSet, ranges, minVals

def datingClassTest():
    '''
    约会网站实例
    :return:
    '''
    hoRatio = 0.10 #用10%的数据做测试集
    datingDateMat = np.loadtxt("D:\\AllCode\\Datas\\MLinAction\\datingTestSet2.txt")
    datingLabels = datingDateMat[:, -1]
    datingDateMat = datingDateMat[:, :-1]
    normMat, ranges, minVals = autoNorm(datingDateMat)
    m = normMat.shape[0]
    numTestVecs = int(m *hoRatio)
    errorCount = 0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs : m, :],
                                     datingLabels[numTestVecs :m], 4)
        print "the classifier came back with : %d, the real anwser is %d" %(classifierResult, datingLabels[i])
        if classifierResult != datingLabels[i]:
            errorCount += 1
    print "the error ratio is", errorCount / float(numTestVecs)
datingClassTest()