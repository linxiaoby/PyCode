import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest,chi2
def preprocess(data):
    data = data.drop(["Id", "Alley", "Utilities", "PoolQC", "Utilities"], axis=1)
    data_new = pd.DataFrame()
    for col in data.columns.values:
        if data[col].dtypes == "object" or col in ["MSSubClass", "YearBuilt", "YearRemodAdd", "GarageYrBlt","MoSold", "YrSold"]:
            col_new = data[col].fillna("Unknown")
            col_new = pd.get_dummies(col_new, prefix=col + "_")
        else:
            col_new = data[col].fillna(data[col].mean())
    #encoding
        data_new = pd.concat([data_new, col_new], axis = 1)
        SelectKBest(chi2, k=10).fit_transform()
    return data_new

df_train = pd.read_csv("..\\trainData.csv")
df_test = pd.read_csv("..\\testData.csv")
X_all = pd.concat([df_train.drop("SalePrice",axis=1),df_test])
X_all_new = preprocess(X_all)
X_train = X_all_new.iloc[:1160,:]
X_test = X_all_new.iloc[1160:,:]
y_train = df_train["SalePrice"]


print X_train.shape, X_test.shape
rfr = RandomForestRegressor(n_estimators = 100)
rfr.fit(X_train, y_train)
y_predic = rfr.predict(X_test)
result = {"Id":df_test["Id"].values, "SalePrice":y_predic}
pd.DataFrame(result).to_csv("..//answer.csv")
