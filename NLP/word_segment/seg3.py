import re, collections
def get_stats(vocab):
    pairs = collections.defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols)-1):
            pairs[symbols[i],symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, v_in, symbolD):
    v_out = {}
    bigram = ' '.join(pair)
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    symbol = ''.join(pair); symbolD.setdefault(symbol, 0)
    for word in v_in:
        w_out = p.sub(symbol, word)
        if w_out!=word:
            symbolD[symbol]+=1
        v_out[w_out] = v_in[word]
    return v_out

def read_dict(inf):
    import re
    wD = {}
    text = open(inf).read()
    text = re.sub(r'([\d]+)', '', text)#drop numbers
    sents = re.split(r"[.。!！?？；;，,\s+\n]", text)
    for sent in sents:
        if not sent:
            continue
        tmp = []
        for ch in sent:
            tmp.append(ch)
        w = ' '.join(tmp)
        wD.setdefault(w, 0)
        wD[w]+=1
    return wD

def output_dict(vocab, symbolD, outf):
    charD={}
    vL = sorted([(v, a) for a, v in vocab.items()], reverse=True)
    with open(outf, 'w') as fout:
        for v, w in vL:
            print (fout, w)
            for a in w.split():
                charD[a] = charD.get(a, 0) + 1
    return charD

def BPE_vocab(inf='data/reference.split', outf='reference.dict',num_merges = 500):
    vocab = read_dict(inf)
    symbolD={}
    for num_i in range(num_merges):
        pairs = get_stats(vocab)
        if not pairs:
            continue
        best = max(pairs, key=pairs.get)
        if ''.join(best) in symbolD:
            break
        vocab = merge_vocab(best, vocab, symbolD)
    charD = output_dict(vocab, symbolD, outf)
    return symbolD

DATA_PATH = "D:\\AllCode\\Datas\\NLP\\word-segment\\"
TRAIN_FILE = DATA_PATH + "train_plus_test.txt" #add test data into train
OUT_FILE = DATA_PATH + "out.txt"
file_name = "test.txt"
import jieba

if __name__=='__main__':
    #get BPE vocabulary
    vocab = BPE_vocab(inf = TRAIN_FILE, outf = OUT_FILE)
    # add BPE dict into jieba
    jieba.load_userdict(vocab)
    #read test data
    f = open(DATA_PATH + file_name, "r", encoding='utf8')
    lines = f.read().splitlines()
    test = []
    label = []
    cut_result = []
    #start segment
    for line in lines:
        str = line.split('\t')
        test.append(str[0])
        label.append(str[1])
        seg_list = jieba.cut(str[0])
        print(" ".join(seg_list))
