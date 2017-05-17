import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas.tools.plotting import scatter_matrix


def print_binary_hist(df, cols, name):
	counts = pd.DataFrame(df, columns=cols)

	ax = counts.sum().plot(kind='bar')
	fig = ax.get_figure()
	fig.savefig(name)


def print_rating_hist(df, name):
	rating = df[["Title", "IMDb_Rating"]]
	rating_group = rating.groupby("IMDb_Rating")

	print (rating_group.size())

	rating_totals = rating_group.size()

	print (rating_totals)

	all_values = [[int(r[0]), r[1]] for r in rating_totals.iteritems()]
	result_values = []
	i = 1
	sum_col = 0
	for r in all_values:
		if r[0] == i:
			sum_col += r[1]
		else:
			result_values += [sum_col]
			sum_col = r[1]
			i += 1
	result_values += [sum_col]

	print (result_values)

	fig, ax = plt.subplots()

	ax.bar(range(1, 11), result_values)
	ax.set_ylabel('Number of movies')
	ax.set_xlabel('Rating')
	plt.show()
	# plt.clf()

	# ax = rating_totals.plot(kind='bar')
	# fig = ax.get_figure()
	# fig.savefig(name)


def print_correlation_matrix(df):
	corr = df.corr()
	fig, ax = plt.subplots(figsize=(47, 47))
	ax.matshow(corr)
	plt.xticks(range(len(corr.columns)), corr.columns);
	plt.yticks(range(len(corr.columns)), corr.columns);

	plt.show()


def print_scatter_matrix(df):
	axes = scatter_matrix(df[['isUSHoliday',
		  'totalActorsAwardsNo',
		  'hasWriter',
		  'isEnglish',
		  'movie', 'series',
		  'Production',
		  'Writer',
		  'Director',
		  'MovieTileInPlot',
		  # 'Year',
		  # 'Day',
		  'Plot',
		  'IMDb_Rating']], alpha=0.5, diagonal='kde')
	corr = df.corr().as_matrix()
	for i, j in zip(*plt.np.triu_indices_from(axes, k=1)):
		axes[i, j].annotate("%.3f" % corr[i, j], (0.8, 0.8), xycoords='axes fraction', ha='center', va='center')
	plt.show()
