import numpy as np
import pandas as pd
import sklearn.metrics as metrics
from sklearn import svm

df_train = pd.read_csv('../../../data/2_class_rating_dataset.csv', sep='\t')

vars = ['Title_words_no', 'Title_length',
		  'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
		  'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
		  'Runtime',
		  'Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 'History', 'Horror', 'Magical', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western',
		  ]
train_labels = np.array(df_train[['IMDb_Rating']]).transpose()[0]
print (train_labels)

train = df_train[vars]
print (train.shape)

clf = svm.SVC(kernel='linear', C=1.0)
clf.fit(train, train_labels)

pred_train = clf.predict(train)
print (pred_train)
print (train_labels)
print("R-squared =", metrics.r2_score(train_labels, pred_train))