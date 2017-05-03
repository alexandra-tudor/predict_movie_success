import pandas as pd


def print_binary_hist(df, cols, name):
	counts = pd.DataFrame(df, columns=cols)

	ax = counts.sum().plot(kind='bar')
	fig = ax.get_figure()
	fig.savefig(name)
