import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import sklearn.linear_model as LinReg
from sklearn.svm import SVR
import sklearn.metrics as metrics

from src.features.structures import dataset_list
from src.plots.histograms import print_rating_hist

for dataset in dataset_list.keys():
	print ("\n >>> Using dataset: " + dataset)

	df = pd.read_csv(dataset_list[dataset][0], sep='\t')
	columns = dataset_list[dataset][1]

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
		# (SVR(kernel='linear', C=0.2), "Support Vector Regression")
		]

	for predictor in predictors:
		print ("\n" + predictor[1])

		predictor[0].fit(train, train_labels)

		pred_train = predictor[0].predict(train)
		print (pred_train)
		print (train_labels)
		print("R-squared train =", metrics.r2_score(train_labels, pred_train))

		pred_test = predictor[0].predict(test)
		print (pred_test)
		print (test_labels)
		print("R-squared test =", metrics.r2_score(test_labels, pred_test))
