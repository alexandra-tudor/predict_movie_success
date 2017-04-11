import pandas as pd
import math as mat
from sklearn import preprocessing
import sklearn.linear_model as LinReg
import sklearn.metrics as metrics

df_train = pd.read_csv('../../../data/imdb_test.csv')

vars = ['ratingCount']
train_labels = df_train[['imdbRating']]

train = df_train[vars]
print (train.shape)

lr = LinReg.LinearRegression().fit(train, train_labels)

pred_train = lr.predict(train)
print("R-squared =", metrics.r2_score(train_labels, pred_train))
