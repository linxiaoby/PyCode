#encoding:utf-8
import jieba
DATAPATH = "D:\\AllCode\\Datas\\NLP\\word-segment\\"
file_name = "test.txt"
f = open(DATAPATH + file_name, "r", encoding='utf8')
lines = f.read().splitlines()
test = []
label = []
cut_result = []
for line in lines:
    str = line.split('\t')
    test.append(str[0])
    label.append(str[1])
    seg_list = jieba.cut(str[0])
    print (" ".join(seg_list))
