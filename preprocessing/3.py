import pandas as pd
import numpy as np
from sklearn import neighbors
pd.DataFrame

class Solution:
    def standardScale(self,df):
        df_new = df.drop("ID",axis=1)
        for col in df_new.columns.values:
            df_new[col] = (df_new[col] - df_new[col].mean())/df_new[col].std()
        df_new['ID'] = df['ID']
        return pd.DataFrame(np.around(df_new, decimals=3))

    def missingValue(self, df):
        return df.fillna(0)

    def discretization(self, df):
        df_new = df.drop("ID", axis = 1)
        for col in df_new.columns:
            factor = pd.cut(df[col].values.astype(float).ravel(), [-np.inf, 0, np.inf], labels=['1', '2'])
            df_new[col] = pd.Series(factor)
        df_new['ID'] = df['ID']
        return df_new


data = pd.read_csv("D:\AllCode\PyCode\\train.csv")
sol = Solution()
data_new = sol.discretization(data)
print data_new