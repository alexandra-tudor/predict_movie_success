import re
from time import strptime

import pandas as pd
from dateutil import parser

from src.db.movie_mongo import getCursor
from src.features.complex_features import person_academy_awards
from src.features.holiday_calendar import HolidayCalendar
from src.features.structures import weekday_no_map, genre_features_map
import time

movie_producer_companies = ['Warner Bros', 'Walt Disney', 'MGM', 'Sony Pictures', 'Universal Pictures', 'Fox', 'Summit', 'DreamWorks', 'Dimension']
movie_writer = ['Quentin Tarantino', 'Charlie Kaufman', 'Paul Thomas Anderson', 'Francis Ford Coppola', 'James Cameron', 'Stanley Kubrick', 'Robert Zemeckis', 'Walt Disney', 'Ridley Scott', 'Stephen King', 'Peter Jackson', 'Akira Kurosawa', 'John Ford', 'Sergio Leone', 'Woody Allen', 'Charles Chaplin']
header = ['IMDbID',
		  'Title', 'Title_words_no', 'Title_length',
		  'Month',
		  'Weekday',
		  'Runtime',
		  'Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 'History', 'Horror', 'Magical', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western', 'Film-Noir',
		  # 'Director_average_rating_past_movies', 'Writers_average_rating_past_movies', 'Actors_average_rating_past_movies',
		  # 'Director_average_income_past_movies', 'Writers_average_income_past_movies', 'Actors_average_income_past_movies',
		  'IMDb_Rating',
		  # 'IMDb_Votes',
		  # 'BoxOffice_income',
          'isUSHoliday',
          'remake', # for some movies there are more release years e.g. 1994/2014 --> the movie from 2014 is a remake
          'totalActorsAwardsNo',
          'hasWriter',
          'isEnglish',
          'movie', 'series', 'episode',
          'Production',
          'Writer',
          'Director',
          'MovieTileInPlot',
          'Plot'
          ]

data_frame = pd.DataFrame(columns=header)
print (data_frame)

# get data from each entry in mongo database
cursor, db = getCursor()
pd_index = 0
for document in cursor:
	print ("\n")
	print ("index: " + str(pd_index))

	try:
		Title = re.sub(r'[^\x00-\x7F]+', '', document['Title']); print ("Title " + Title)
	except KeyError:
		continue

	try:
		IMDbID = document['imdbID']; print ("IMDbID " + IMDbID)
		if IMDbID == 'tt0094296':
			break
	except KeyError:
		continue

	Title_words_no = len(Title.split()); print ("Title_words_no " + str(Title_words_no))
	Title_length = len(Title); print ("Title_length " + str(Title_length))

	try:
		release_date = document['Released']; print ("Realease date: " + release_date)
	except KeyError:
		continue

	try:
		yearString = document['Year']; print ("Year: " + yearString)
		day, month, year = release_date.split()
	except KeyError:
		continue

	try:
		actors = document["Actors"]; print ("Actors: " + actors)
	except KeyError:
		continue

	if int(year) < 2004:
		print ("#########################################################################################")
		continue

	month_nr = strptime(month,'%b').tm_mon; print ("month_nr " + str(month_nr))
	month_feature = month_nr
	weekday = parser.parse(release_date).strftime('%A'); print ("weekday " + weekday)
	weekday_feature = weekday_no_map[weekday]; print ("weekday_no " + str(weekday_feature))

	try:
		Runtime = document['Runtime']; print ("Runtime " + Runtime + " " + str(Runtime).strip(','))
		genre_binary_features = [0] * len(genre_features_map.keys())
	except KeyError:
		continue

	try:
		Genre_list = document['Genre'].split(','); print ("Genre_list " + str(Genre_list))
		for g in Genre_list:
			genre_binary_features[genre_features_map[str(g).strip()]] = 1
	except KeyError:
		continue

	try:
		Language = document['Language']
	except KeyError:
		continue

	try:
		IMDb_Rating = document['imdbRating']; print ("IMDb_Rating: " + IMDb_Rating)
		holidayCalendar = HolidayCalendar()
		isUSHoliday = holidayCalendar.is_US_holiday(int(day), month_nr, int(year))
	except KeyError:
		continue

	remake = 0
	if "/" in yearString:
		remake = 1

	actors = actors.encode('utf-8').strip().split(',')
	rewards_no = 0
	for a in actors:
		rewards_no += person_academy_awards(a, int(year))

	hasWriter = 0
	try:
		if document['Writer'] != 'N/A':
			hasWriter = 1
	except KeyError:
		continue

	isEnglish = 0
	try:
		if Language == 'English':
			isEnglish = 1
	except KeyError:
		continue

	type_list = [0, 0, 0]
	try:
		if document["Type"] == 'movie':
			type_list[0] = 1
		elif document["Type"] == 'series':
			type_list[1] = 1
		elif document["Type"] == 'episode':
			type_list[2] = 1
	except KeyError:
		continue

	try:
		production = document['Production']
		movie_producer_companies_feature = 0
		for index in range(len(movie_producer_companies)):
			if movie_producer_companies[index] in production:
				movie_producer_companies_feature = index + 1
	except KeyError:
		continue

	try:
		writer = document['Writer']
		movie_writer_feature = 0
		for index in range(len(movie_writer)):
			if movie_writer[index] in writer:
				movie_writer_feature = index + 1
	except KeyError:
		continue

	try:
		director = document['Director']
		movie_director_feature = 0
		for index in range(len(movie_writer)):
			if movie_writer[index] in director:
				movie_director_feature = index + 1
	except KeyError:
		continue

	movie_title_in_plot = 0
	try:
		if Title in document['Plot']:
			movie_title_in_plot = 1
	except KeyError:
		continue

	try:
		plot = document['Plot']
	except KeyError:
		continue

	row = [str(IMDbID), str(Title), Title_words_no, Title_length]
	row += [month_feature]
	row += [weekday_feature]
	row += [int(str(Runtime).replace(",", "").split()[0])]
	row += genre_binary_features
	row += [float(str(IMDb_Rating))]
	row += [isUSHoliday]
	row += [remake]
	row += [rewards_no]
	row += [hasWriter]
	row += [isEnglish]
	row += type_list
	row += [movie_producer_companies_feature]
	row += [movie_writer_feature]
	row += [movie_director_feature]
	row += [movie_title_in_plot]
	row += [plot]

	print (row)
	print (len(row))
	print (len(header))

	data_frame.loc[pd_index] = row
	pd_index += 1
	time.sleep(2)


print (data_frame)
data_frame.drop_duplicates()
data_frame.to_csv("../../data/compressed_dataset.csv", sep='\t')
