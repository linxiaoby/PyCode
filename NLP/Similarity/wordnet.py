from nltk.corpus import wordnet as wd

DATA_PATH = "D:\\AllCode\\Datas\\NLP\\"
DATA_FILE = DATA_PATH + "MTURK-771.csv"
RESULT_FILE = DATA_PATH + "lch_sim.csv"
import pandas as pd
data = pd.read_csv(DATA_FILE, header=None)
alist = list(data.iloc[:,0])
blist = list(data.iloc[:,1])
simlist = []
for i in range(0, len(alist)):
    asets = wd.synsets(alist[i])
    bsets = wd.synsets(blist[i])
    maxsim = -1000
    for j in range(0, len(asets)):
        for k in range(0, len(bsets)):
            sim = asets[j].lch_similarity(bsets[k])
            if(sim is not None and sim > maxsim):
                maxsim = sim

    simlist.append(maxsim)
    if (i % 10 == 0):
        print(alist[i] + " and " + blist[i] + ":" + str(maxsim))
data['mysim'] = simlist
pd.DataFrame(data).to_csv(RESULT_FILE)
