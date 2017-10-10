import pandas as pd
from sklearn import preprocessing
import numpy as np
class Solution:
    def standardScale(self,dataframe_x):
        # print  dataframe_x
        std_scale = preprocessing.StandardScaler().fit(dataframe_x[['CT', 'FA', 'WT', 'SP']])
        dataframe_x_new = std_scale.transform(dataframe_x[['CT', 'FA', 'WT', 'SP']])
        print std_scale
        # dataframe_x_new = np.around(dataframe_x_new, decimals=3)
        # print pd.DataFrame(dataframe_x_new, columns=['CT', 'FA', 'WT', 'SP'])
        return

data = pd.read_csv("F:\\datasets\\train_x.csv")
print data.head()
sol = Solution()
data_new = sol.standardScale(data)
print data_new