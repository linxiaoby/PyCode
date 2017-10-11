#Ecoding:utf-8
import pandas as pd
import numpy as np
from sklearn import preprocessing
import seaborn as sns #这个包用来干嘛

#导入数据
wine = pd.read_csv("F:\\wine.csv")
# print wine.head()
# print wine['Alcohol'] #取前5行

#0-1标准化
minmax_scale = preprocessing.MinMaxScaler().fit(wine[['Alcohol','Malic acid']])
df_minmax = minmax_scale.transform(wine[['Alcohol','Malic acid']])

#z-score 标准化
std_scale = preprocessing.StandardScaler().fit(wine[['Alcohol','Malic acid']]);
df_std = std_scale.transform(wine[['Alcohol','Malic acid']]);
print ('Min-value after 0-1 scaling:\nAlcohol={:.2f},Malic acid={:.2f}'.
       format(df_minmax[:,0].min(),df_minmax[:,1].min()))
print ('Max-value after 0-1 scaling:\nAlcohol={:.2f},Malic acid={:.2f}'.
       format(df_minmax[:,0].max(),df_minmax[:,1].max()))
print '\n++++++++++++++++++++++++++++++\n'
print ('Mean after z-score scaling:\nAlcohol={:.2f},Malic acid={:.2f}'.
       format(df_std[:,0].mean(),df_std[:,1].mean()))
print ('\nStandard deviation after z-score scaling:\nAlcohol={:.2f},Malic acid={:.2f}'.
       format(df_std[:,0].std(),df_std[:,1].std()))