import pandas as pd
import sklearn.linear_model as LinReg
import sklearn.metrics as metrics

df_train = pd.read_csv('../../../data/sample_dataset.csv', sep='\t')

vars = ['Title_words_no', 'Title_length',
		  'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
		  'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
		  'Runtime',
		  'Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 'History', 'Horror', 'Magical', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western',
		  ]
train_labels = df_train[['IMDb_Rating']]

train = df_train[vars]
print (train.shape)

lr = LinReg.LinearRegression().fit(train, train_labels)

pred_train = lr.predict(train)
print("R-squared =", metrics.r2_score(train_labels, pred_train))