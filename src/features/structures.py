genre_features_map = {
	'Action': 0,
	'Adult': 1,
	'Adventure': 2,
	'Animation': 3,
	'Biography': 4,
	'Comedy': 5,
	'Crime': 6,
	'Documentary': 7,
	'Drama': 8,
	'Family': 9,
	'Fantasy': 10,
	'Game-Show': 11,
	'History': 12,
	'Horror': 13,
	'Magical': 14,
	'Music': 15,
	'Musical': 16,
	'Mystery': 17,
	'News': 18,
	'Reality-TV': 19,
	'Romance': 20,
	'Sci-Fi': 21,
	'Short': 22,
	'Sport': 23,
	'Talk-Show': 24,
	'Thriller': 25,
	'War': 26,
	'Western': 27,
	'Film-Noir': 28
}

weekday_no_map = {
	'Monday': 0,
	'Tuesday': 1,
	'Wednesday': 2,
	'Thursday': 3,
	'Friday': 4,
	'Saturday': 5,
	'Sunday': 6
}

dataset_list = {
	"compressed_dataset.csv": [
		'../../../data/compressed_dataset.csv',
		[
		'Title_words_no',
		'Title_length',
		'Month',
		'Weekday',
		'Runtime',
		'Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 'History', 'Horror', 'Magical', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western', 'Film-Noir',
		'isUSHoliday',
		'remake',
		'totalActorsAwardsNo',
		'hasWriter',
		'isEnglish',
		'movie', 'series', 'episode',
		'Production',
		'Writer',
		'Director',
		'MovieTileInPlot'
		]
	],
	# "10_class_compressed_dataset.csv": [
	# 	'../../../data/compressed_dataset.csv',
	# 	[
	# 	'Title_words_no',
	# 	'Title_length',
	# 	'Month',
	# 	'Weekday',
	# 	'Runtime',
	# 	'Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 'History', 'Horror', 'Magical', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western', 'Film-Noir',
	# 	'isUSHoliday',
	# 	'remake',
	# 	'totalActorsAwardsNo',
	# 	'hasWriter',
	# 	'isEnglish',
	# 	'movie', 'series', 'episode',
	# 	'Production',
	# 	'Writer',
	# 	'Director',
	# 	'MovieTileInPlot'
	# 	]
	# ],
	# "2_class_compressed_dataset.csv": [
	# 	'../../../data/compressed_dataset.csv',
	# 	[
	# 		'Title_words_no',
	# 		'Title_length',
	# 		'Month',
	# 		'Weekday',
	# 		'Runtime',
	# 		'Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama',
	# 		'Family', 'Fantasy', 'Game-Show', 'History', 'Horror', 'Magical', 'Music', 'Musical', 'Mystery', 'News',
	# 		'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western', 'Film-Noir',
	# 		'isUSHoliday',
	# 		'remake',
	# 		'totalActorsAwardsNo',
	# 		'hasWriter',
	# 		'isEnglish',
	# 		'movie', 'series', 'episode',
	# 		'Production',
	# 		'Writer',
	# 		'Director',
	# 		'MovieTileInPlot'
	# 	]
	# ]
}