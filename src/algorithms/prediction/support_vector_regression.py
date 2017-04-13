import pandas as pd
import numpy as np
from sklearn.svm import SVR
import sklearn.metrics as metrics

df_train = pd.read_csv('../../../data/sample_dataset.csv', sep='\t')

vars = ['Title_words_no', 'Title_length',
		  'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
		  'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
		  'Runtime',
		  'Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 'History', 'Horror', 'Magical', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western',
		  ]
train_labels = np.array(df_train[['IMDb_Rating']]).transpose()[0]

train = df_train[vars]
print (train.shape)

regressor_linear = SVR(kernel='linear', C=0.2, verbose=True)
regressor_linear.fit(train, train_labels)
pred_train = regressor_linear.predict(train)
print (pred_train)
print (train_labels)
print("R-squared linear=", metrics.r2_score(train_labels, pred_train))
print ("")

regressor_rbf = SVR(kernel='rbf', C=0.2, verbose=True)
regressor_rbf.fit(train, train_labels)
pred_train = regressor_rbf.predict(train)
print (pred_train)
print (train_labels)
print("R-squared rbf=", metrics.r2_score(train_labels, pred_train))
print ("")


regressor_poly = SVR(kernel='poly', C=0.2, degree=2, verbose=True)
regressor_poly.fit(train, train_labels)
pred_train = regressor_poly.predict(train)
print (pred_train)
print (train_labels)
print("R-squared poly=", metrics.r2_score(train_labels, pred_train))
print ("")
