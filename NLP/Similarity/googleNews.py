import gensim
import pandas as pd
import logging
logging.basicConfig(level = logging.DEBUG, format ='%(asctime)s  - %(levelname)s - %(message)s')
logger = logging.getLogger()
DATA_PATH = "D:\\AllCode\\Datas\\NLP\\"
def sim():
    '''
    计算相似度
    '''
    DATA_FILE = DATA_PATH + "MTURK-771.csv"
    RESULT_FILE = DATA_PATH + "google_news.csv"
    data = pd.read_csv(DATA_FILE, header=None)
    alist = list(data.iloc[:, 0])
    blist = list(data.iloc[:, 1])
    simlist = []
    logger.info("begin to calculate similarity")
    model = gensim.models.KeyedVectors.load_word2vec_format(DATA_PATH + 'GoogleNews-vectors-negative300.bin', binary=True)
    i = 0
    for i in range(len(alist)):
        sim = model.similarity(alist[i], blist[i]) #cosine similarity
        simlist.append(sim)
    data['mysim'] = simlist
    pd.DataFrame(data).to_csv(RESULT_FILE)
    logger.info("finish similarity")

if __name__ == "__main__":
    sim()