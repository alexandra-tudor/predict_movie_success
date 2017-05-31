import numpy as np
import pandas as pd
import sklearn.metrics as metrics
from sklearn import svm
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_recall_fscore_support as score

from src.features.structures import dataset_list

dataset = dataset_list["2_class_rating_dataset.csv"]
print ("\n >>> Using dataset: " + "2_class_rating_dataset.csv")

df = pd.read_csv(dataset[0], sep='\t')
columns = dataset[1]

df = df[df["Total_W_AVG"] != 0]

df['IMDb_Rating'] = map(lambda x: int(x), df['IMDb_Rating'])

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
	(svm.SVC(kernel='linear', C=1.0), "SVM linear"),
	(svm.SVC(kernel='rbf', C=1.0), "SVM rbf"),
	(KNeighborsClassifier(3),"KNN"),
    (GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True), "GaussianProcess"),
    (DecisionTreeClassifier(max_depth=5), "DecisionTree"),
    (RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1), "RandomForest"),
    (MLPClassifier(alpha=1), "MLP"),
    (AdaBoostClassifier(),"AdaBoost"),
    (GaussianNB(),"GaussianNB"),
    (QuadraticDiscriminantAnalysis(), "QuadraticDiscriminant")
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

	print("\nF1 Score ")
	print (f1_score(test_labels, pred_test, average="macro"))

	print("\nPrecision Score ")
	print(precision_score(test_labels, pred_test, average="macro"))

	print("\nRecall Score ")
	print(recall_score(test_labels, pred_test, average="macro"))

	precision, recall, fscore, support = score(test_labels, pred_test)
	print (precision, recall, fscore, support)
