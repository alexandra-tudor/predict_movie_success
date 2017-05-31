import numpy as np
import pandas as pd
import sklearn.linear_model as LinReg
import sklearn.metrics as metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LassoCV

from src.features.structures import dataset_list

dataset = dataset_list["trends_dataset_joined.csv"]
print ("\n >>> Using dataset: trends_dataset_joined.csv")

df = pd.read_csv(dataset[0], sep='\t')
columns = dataset[1]

df = df[df["Total_W_AVG"] != 0]

# df = pd.get_dummies(df)

msk = np.random.rand(len(df)) < 0.75
train = df[columns][msk]
test = df[columns][~msk]

# print_rating_hist(df[msk], 'train_rating_hist.png')
# print_rating_hist(df, 'test_rating_hist.png')

train_labels = np.array(df[['IMDb_Rating']][msk]).transpose()[0]
test_labels = np.array(df[['IMDb_Rating']][~msk]).transpose()[0]

print ("Training dataset: " + str(train.shape))
print ("Testing dataset: " + str(test.shape))

predictors = [
	(RandomForestRegressor(n_estimators=150, min_samples_split=10), "Random Forest Regressor"),
	(LinReg.LinearRegression(), "Linear Regression"),
	(LassoCV(alphas=[1, 0.1, 0.001, 0.0005]), "LassoCV")
	# (SVR(kernel='linear', C=0.2), "Support Vector Regression")
	]

for predictor in predictors:
	print ("\n" + predictor[1])

	predictor[0].fit(train, train_labels)

	pred_train = predictor[0].predict(train)
	# print (pred_train)
	# print (train_labels)
	print("R-squared train =", metrics.r2_score(train_labels, pred_train))

	pred_test = predictor[0].predict(test)
	# print (pred_test)
	# print (test_labels)
	print("R-squared test =", metrics.r2_score(test_labels, pred_test))

	# print("\nF1 Score ")
	# print (f1_score(test_labels, pred_test, average="macro"))
	#
	# print("\nPrecision Score ")
	# print(precision_score(test_labels, pred_test, average="macro"))
	#
	# print("\nRecall Score ")
	# print(recall_score(test_labels, pred_test, average="macro"))
	#
	print (len(test_labels), len(pred_test))
	
	precision, recall, fscore, support = predictor[0].score(test_labels, pred_test)
	print (precision, recall, fscore, support)
