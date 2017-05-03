import pandas as pd


def print_hist(df, cols, name):
	counts = pd.DataFrame(df, columns=cols)
	print (counts.sum().shape)

	ax = counts.sum().plot(kind='bar')
	fig = ax.get_figure()
	fig.savefig(name)
