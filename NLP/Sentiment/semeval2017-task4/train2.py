#encoding:utf8

import tensorflow as tf
import pandas as pd
import numpy as np
import re
import os
from sklearn import metrics
DATA_PATH = "D:\\AllCode\\Datas\\NLP\\Sentiment\\twitter\\"
EMBEDDING_PATH = DATA_PATH + "data\\GoogleNews-vectors-negative300.bin"
def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def get_data(datapath):
    x_tmp = []
    y_tmp = []
    label_dic = {'negative': -1, 'neutral': 0, 'positive': 1}
    files = os.listdir(datapath)
    for file in files:
        if not os.path.isdir(file):
            lines = open(datapath + file, 'r', encoding='UTF8').readlines()
            for line in lines:
                twi_list = line.split('\t')
                if len(twi_list) >= 3:
                    x_tmp.append(clean_str(twi_list[2].strip()))
                    y_tmp.append(label_dic[twi_list[1]])
    x = pd.Series(np.asarray(x_tmp))
    y = pd.Series(np.asarray(y_tmp))
    return x, y



#build model
EMBEDDING_SIZE = 70
def bag_of_words_model(features, target):
  """A bag-of-words model. Note it disregards the word order in the text."""
  target = tf.one_hot(target, 15, 1, 0)
  features = tf.contrib.layers.bow_encoder(features, vocab_size=n_words, embed_dim=EMBEDDING_SIZE)
  logits = tf.contrib.layers.fully_connected(features, 15,activation_fn=None)
  loss = tf.contrib.losses.softmax_cross_entropy(logits, target)
  train_op = tf.contrib.layers.optimize_loss(loss, tf.contrib.framework.get_global_step(),optimizer='Adam', learning_rate=0.01)
  return (
      {'class': tf.argmax(logits, 1),
       'prob': tf.nn.softmax(logits)},
        loss, train_op
        )



if __name__ == '__main__':
    # prepare train and test data
    x_train, y_train = get_data(DATA_PATH + "train\\")
    x_test, y_test = get_data(DATA_PATH + "test\\")
    print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

    # process vacab
    MAX_DOCUMENT_LENGTH = 70
    vocab_processor = tf.contrib.learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    x_train = np.array(list(vocab_processor.fit_transform(x_train)))
    x_test = np.array(list(vocab_processor.transform(x_test)))
    n_words = len(vocab_processor.vocabulary_)
    print(x_train[100])

    #train and test
    classifier = tf.contrib.learn.Estimator(model_fn=bag_of_words_model)
    # Train and predict
    classifier.fit(x_train, y_train, steps=1)
    y_predicted = [p['class'] for p in
                   classifier.predict(x_test, as_iterable=True)]
    score = metrics.accuracy_score(y_test, y_predicted)
    print('Accuracy: {0:f}'.format(score))