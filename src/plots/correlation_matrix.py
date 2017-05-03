import pandas as pd
import matplotlib.pyplot as plt


def print_correlation_matrix(df, size=10):
	corr = df.corr()

	fig, ax = plt.subplots(figsize=(size, size))
	plt.title('Pearson Correlation of Movie Features')
	ax.matshow(corr)
	plt.xticks(range(len(corr.columns)), corr.columns)
	plt.yticks(range(len(corr.columns)), corr.columns)

if __name__ == "__main__":
	df_train = pd.read_csv('../../../data/sample_dataset.csv', sep='\t')
	print_correlation_matrix(df_train)