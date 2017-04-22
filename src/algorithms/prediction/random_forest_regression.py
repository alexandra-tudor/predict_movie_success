import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import sklearn.metrics as metrics

df_train = pd.read_csv('../../../data/sample_dataset.csv', sep='\t')

vars = ['Title_words_no', 'Title_length',
		  'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
		  'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
		  'Runtime',
		  'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Magical', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western',
		  ]
train_labels = np.array(df_train[['IMDb_Rating']]).transpose()[0]

train = df_train[vars]
print (train.shape)

regressor = RandomForestRegressor(n_estimators=150, min_samples_split=2)
regressor.fit(train, train_labels)

pred_train = regressor.predict(train)
print (pred_train)
print (train_labels)
print("R-squared =", metrics.r2_score(train_labels, pred_train))

