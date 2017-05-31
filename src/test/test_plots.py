import pandas as pd
import numpy as np

from src.plots.histograms import print_binary_hist, print_rating_hist, print_correlation_matrix, print_scatter_matrix, \
	print2DPlot

df_train = pd.read_csv('../../data/trends_dataset_joined.csv', sep='\t')

vars = [
		  'IMDbID',
		  'Title', 'Title_words_no',
		  # 'Month',
		  'Weekday',
		  # 'Runtime',
		  # 'Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western',
		  'isUSHoliday',
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
		  'IMDb_Rating',
	'W1',
	'W2',
	'W3',
	'W4',
	'Total_W_AVG',
	'Growth_Rate'
	]
train_labels = np.array(df_train[['IMDb_Rating']]).transpose()[0]

train = df_train[vars]
print (train.shape)

# print_binary_hist(train, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'day_of_week.png')
# print_binary_hist(train, ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], 'month.png')
# print_binary_hist(train, ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Magical', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'], 'genres.png')
# print_rating_hist(df_train, 'rating_hist.png')
# print_correlation_matrix(train)

# print_scatter_matrix(train)

print2DPlot(train)

