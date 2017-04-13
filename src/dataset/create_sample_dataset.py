"""
IMDbID,
Title, Title_words_no, Title_length,
January, February, March, April, May, June, July, August, September, October, November, December,
Monday, Tuesday, Wednesday, Thursday Friday, Saturday, Sunday,
Runtime,
Action, Adventure, Animation, Comedy, Crime, Drama, Fantasy, Historical, Horror, Magical, Romance, Thriller, Western,
Director_average_rating_past_movies, Writers_average_rating_past_movies, Actors_average_rating_past_movies,
Director_average_income_past_movies, Writers_average_income_past_movies, Actors_average_income_past_movies,
Language,
Country,
Rating, Votes, BoxOffice_income
"""

import pandas as pd
import re
from pymongo import MongoClient
from time import strptime
from dateutil import parser

header = ['IMDbID',
		  'Title', 'Title_words_no', 'Title_length',
		  'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
		  'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
		  'Runtime',
		  'Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 'History', 'Horror', 'Magical', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western',
		  # 'Director_average_rating_past_movies', 'Writers_average_rating_past_movies', 'Actors_average_rating_past_movies',
		  # 'Director_average_income_past_movies', 'Writers_average_income_past_movies', 'Actors_average_income_past_movies',
		  # 'Language',
		  # 'Country',
		  'IMDb_Rating',
		  # 'IMDb_Votes',
		  # 'BoxOffice_income'
          ]

data_frame = pd.DataFrame(columns=header)
print (data_frame)

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
	'Western': 27
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

# get data from each entry in mongo database
client = MongoClient()
db = client.movies
collection = db['movie']
cursor = collection.find(
	{
		"Released": {'$ne':'N/A'},
		"Runtime": {'$ne':'N/A'},
		"imdbRating": {'$ne':'N/A'},
		"Genre": {'$ne':'N/A'}
	}
)

index = 0
for document in cursor:
	print ("")
	Title = re.sub(r'[^\x00-\x7F]+', '', document['Title']); print ("Title " + Title)
	IMDbID = document['imdbID']; print ("IMDbID " + IMDbID)
	Title_words_no = len(Title.split()); print ("Title_words_no " + str(Title_words_no))
	Title_length = len(Title); print ("Title_length " + str(Title_length))
	release_date = document['Released']; print ("Realease date: " + release_date)
	day, month, year = release_date.split()

	if int(year) < 1900:
		continue

	month_nr = strptime(month,'%b').tm_mon; print ("month_nr " + str(month_nr))
	month_binary_features = [0] * 12
	month_binary_features[month_nr-1] = 1; print ("month_binary_features " + str(month_binary_features))
	weekday_binary_features = [0] * 7
	weekday = parser.parse(release_date).strftime('%A'); print ("weekday " + weekday)
	weekday_no = weekday_no_map[weekday]; print ("weekday_no " + str(weekday_no))
	weekday_binary_features[weekday_no] = 1; print ("weekday_binary_features " + str(weekday_binary_features))
	Runtime = document['Runtime']; print ("Runtime " + Runtime)
	genre_binary_features = [0] * len(genre_features_map.keys())
	Genre_list = document['Genre'].split(','); print ("Genre_list " + str(Genre_list))
	for g in Genre_list:
		genre_binary_features[genre_features_map[str(g).strip()]] = 1

	# Director_average_rating_past_movies
	# Writers_average_rating_past_movies
	# Actors_average_rating_past_movies
	# Director_average_income_past_movies
	# Writers_average_income_past_movies
	# Actors_average_income_past_movies

	# Language = document['Language']
	# Country = document['Country']
	IMDb_Rating = document['imdbRating']; print ("IMDb_Rating: " + IMDb_Rating)
	# IMDb_Votes  = document['imdbVotes']
	# BoxOffice_income = document['BoxOffice']

	row = [str(IMDbID), str(Title), Title_words_no, Title_length]
	row += month_binary_features
	row += weekday_binary_features
	row += [int(str(Runtime).split()[0])]
	row += genre_binary_features
	row += [float(str(IMDb_Rating))]

	print (row)

	data_frame.loc[index] = row
	index += 1

print (data_frame)
data_frame.to_csv("../../data/sample_dataset.csv", sep='\t')
