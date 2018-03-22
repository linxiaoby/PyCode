#计算斯皮尔曼相关系数

DATAFILE = "D:\\AllCode\\Datas\\NLP\\google_news.csv"
import pandas as pd
df = pd.read_csv(DATAFILE)
df = df.drop(["id","0", "1", "3"], axis = 1)
print (df.corr("spearman"))