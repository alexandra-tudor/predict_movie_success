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

import re
from time import strptime

import pandas as pd
from dateutil import parser

from src.db.get_data_from_pytrends import get_trends
from src.db.movie_mongo import getCursor
from src.features.complex_features import person_academy_awards
from src.features.holiday_calendar import HolidayCalendar
from src.features.structures import weekday_no_map, genre_features_map

header = ['IMDbID',
		  'Title', 'Title_words_no', 'Title_length',
		  'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
		  'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
		  'Runtime',
		  'Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 'History', 'Horror', 'Magical', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western', 'Film-Noir',
		  # 'Director_average_rating_past_movies', 'Writers_average_rating_past_movies', 'Actors_average_rating_past_movies',
		  # 'Director_average_income_past_movies', 'Writers_average_income_past_movies', 'Actors_average_income_past_movies',
		  # 'Language',
		  # 'Country',
		  'IMDb_Rating',
		  # 'IMDb_Votes',
		  # 'BoxOffice_income',
          'isUSHoliday',
          'remake', # for some movies there are more release years e.g. 1994/2014 --> the movie from 2014 is a remake
          'totalActorsAwardsNo',
          'trendsWeek1', 'trendsWeek2', 'trendsWeek3', 'trendsWeek4'
          ]

data_frame = pd.DataFrame(columns=header)
print (data_frame)

# get data from each entry in mongo database
cursor, db = getCursor()
index = 0
for document in cursor:
	print ("")
	print ("index: " + str(index))
	if index == 94296:
		index += 1
		continue

	Title = re.sub(r'[^\x00-\x7F]+', '', document['Title']); print ("Title " + Title)
	IMDbID = document['imdbID']; print ("IMDbID " + IMDbID)
	Title_words_no = len(Title.split()); print ("Title_words_no " + str(Title_words_no))
	Title_length = len(Title); print ("Title_length " + str(Title_length))
	release_date = document['Released']; print ("Realease date: " + release_date)
	yearString = document['Year']; print ("Year: " + yearString)
	day, month, year = release_date.split()
	actors = document["Actors"]; print ("Actors: " + actors)

	# google trends has data since 2004
	if int(year) < 2005:
		continue

	month_nr = strptime(month,'%b').tm_mon; print ("month_nr " + str(month_nr))
	month_binary_features = [0] * 12
	month_binary_features[month_nr-1] = 1; print ("month_binary_features " + str(month_binary_features))
	weekday_binary_features = [0] * 7
	weekday = parser.parse(release_date).strftime('%A'); print ("weekday " + weekday)
	weekday_no = weekday_no_map[weekday]; print ("weekday_no " + str(weekday_no))
	weekday_binary_features[weekday_no] = 1; print ("weekday_binary_features " + str(weekday_binary_features))
	Runtime = document['Runtime']; print ("Runtime " + Runtime + " " + str(Runtime).strip(','))
	genre_binary_features = [0] * len(genre_features_map.keys()); print ("Genres: " + str(len(genre_features_map.keys())))
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
	holidayCalendar = HolidayCalendar()
	isUSHoliday = int(holidayCalendar.is_US_holiday(int(day), month_nr, int(year)))

	remake = 0
	if "/" in yearString:
		remake = 1

	actors = actors.encode('utf-8').strip().split(',')
	rewards_no = 0
	for a in actors:
		rewards_no += person_academy_awards(a, int(year))

	trends_data, avgs = get_trends(Title, int(year), month_nr, int(day))

	row = [str(IMDbID), str(Title), Title_words_no, Title_length]
	row += month_binary_features
	row += weekday_binary_features
	row += [int(str(Runtime).replace(",", "").split()[0])]
	row += genre_binary_features
	row += [float(str(IMDb_Rating))]
	row += [isUSHoliday]
	row += [remake]
	row += [rewards_no]
	print (avgs)
	row += [avgs[0], avgs[1], avgs[2], avgs[3]]

	print (row)

	data_frame.loc[index] = row
	index += 1

print (data_frame)
data_frame.drop_duplicates()
data_frame.to_csv("../../data/trends_dataset.csv", sep='\t')
