import logging
import multiprocessing
import gensim
from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
logging.basicConfig(level = logging.DEBUG, format ='%(asctime)s  - %(levelname)s - %(message)s')
logger = logging.getLogger()

DATA_PATH = "D:\\AllCode\\Datas\\NLP\\"
CORPUS = DATA_PATH + "enwiki-latest-pages-articles.xml.bz2" #原始xml格式的wiki语料路径
TEXTCORPUS = DATA_PATH + "wiki.en.txt" #text语料存储路径

def xmlToText():
    '''
    原始的wiki语料是xml格式的，该函数将wiki语料写入为txt文件，一篇article为一行。
    '''
    logger.info("begin to transfer wiki xml to text ")
    wiki = WikiCorpus(CORPUS, lemmatize = False, dictionary = {})
    txtout = open(TEXTCORPUS, 'w', encoding="utf-8")
    i = 0
    for text in wiki.get_texts():
        # txtout.write(b' '.join(text).decode('utf-8') + '\n')
        txtout.write(' '.join(text) + '\n')
        i += 1
        if (i % 10000 == 0):
            logger.info("save" + str(i) + "articles")
    txtout.close()
    logger.info("finish transfer wiki xml to text ")


MODEL_NAME = DATA_PATH + "wiki.en.text.model" #model的存储名
VECTOR_NAME = DATA_PATH + "wiki.en.text.vector"
def trainModel():
    '''
    从txt的wiki语料中，训练model，然后将model存储到磁盘
    '''
    SIZE = 400
    WINDOW = 5
    # MIN_COUNT = 5
    logger.info("begin to train model")
    model = Word2Vec(LineSentence(TEXTCORPUS), size = SIZE, window = WINDOW,workers = multiprocessing.cpu_count())
    model.save(MODEL_NAME)
    model.wv.save_word2vec_format(VECTOR_NAME)
    logger.info("finish train model")


import pandas as pd
def sim():
    '''
    计算相似度
    '''
    DATA_FILE = DATA_PATH + "MTURK-771.csv"
    RESULT_FILE = DATA_PATH + "vec_sim.csv"
    data = pd.read_csv(DATA_FILE, header=None)
    alist = list(data.iloc[:, 0])
    blist = list(data.iloc[:, 1])
    simlist = []
    logger.info("begin to calculate similarity")
    model = gensim.models.KeyedVectors.load_word2vec_format(VECTOR_NAME, binary = False)
    i = 0
    for i in range(len(alist)):
        sim = model.similarity(alist[i], blist[i]) #cosine similarity
        simlist.append(sim)
    data['mysim'] = simlist
    pd.DataFrame(data).to_csv(RESULT_FILE)
    logger.info("finish similarity")

if __name__ == "__main__":
    # xmlToText()
    # trainModel()
    sim()


