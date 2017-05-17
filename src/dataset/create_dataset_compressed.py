import re
from time import strptime

import pandas as pd
from dateutil import parser

from src.db.movie_mongo import getCursor
from src.features.complex_features import person_academy_awards
from src.features.holiday_calendar import HolidayCalendar
from src.features.structures import weekday_no_map, genre_features_map
import time

import json
from pprint import pprint

movie_producer_companies = ['Warner Bros', 'Walt Disney', 'MGM', 'Sony Pictures', 'Universal Pictures', 'Fox', 'Summit', 'DreamWorks', 'Dimension']
movie_writer = ['Quentin Tarantino', 'Charlie Kaufman', 'Paul Thomas Anderson', 'Francis Ford Coppola', 'James Cameron', 'Stanley Kubrick', 'Robert Zemeckis', 'Walt Disney', 'Ridley Scott', 'Stephen King', 'Peter Jackson', 'Akira Kurosawa', 'John Ford', 'Sergio Leone', 'Woody Allen', 'Charles Chaplin']
header = ['IMDbID',
		  'Title', 'Title_words_no', 'Title_length',
		  'Month',
		  'Weekday',
		  'Runtime',
		  'Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 'History', 'Horror', 'Magical', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western', 'Film-Noir',
		  'IMDb_Rating',
		  'isUSHoliday',
		  'remake',
		  'totalActorsAwardsNo',
		  'hasWriter',
		  'isEnglish',
		  'movie', 'series', 'episode',
		  'Production',
		  'Writer',
		  'Director',
		  'MovieTileInPlot',
		  'Year',
		  'Day',
		  'Plot'
		  ]

data_frame = pd.DataFrame(columns=header)
print (data_frame)

"""
			"Released"      : {'$ne': 'N/A'},
			"Runtime"       : {'$ne': 'N/A'},
			"imdbRating"    : {'$ne': 'N/A'},
			"Genre"         : {'$ne': 'N/A'},
			"Plot"          : {'$ne': 'N/A'},
			"Director"      : {'$ne': 'N/A'},
			"Production"    : {'$ne': 'N/A'}
"""

def isNaN(string):
	return string == 'N/A'


# database = pd.read_json('../../data/database1_c.json', lines=True)
with open('../../data/database_cc.json') as data_file:
	# database = json.load(data_file)
	pd_index = 0
	for d in data_file:
		d = re.sub(r'[^\x00-\x7F]+', '', d)
		document = json.loads(d)
		# print (document)
		print ("\n")
		print ("index: " + str(pd_index))

		Title = re.sub(r'[^\x00-\x7F]+', '', document['Title'])
		# print ("Title " + Title)

		Title_words_no = len(Title.split())
		# print ("Title_words_no " + str(Title_words_no))

		Title_length = len(Title)
		# print ("Title_length " + str(Title_length))

		IMDbID = document['imdbID']
		# print ("imdbID " + IMDbID)

		release_date = document['Released']
		# print ("Realease date: " + release_date)
		if isNaN(release_date):
			continue

		yearString = document['Year']
		# print ("Year: " + yearString)
		if isNaN(yearString):
			continue

		day, month, year = release_date.split()

		actors = document["Actors"]
		# print ("Actors: " + actors)
		if isNaN(actors):
			continue

		if int(year) < 2004:
			print ("#########################################################################################")
			continue

		month_nr = strptime(month,'%b').tm_mon
		# print ("month_nr " + str(month_nr))

		month_feature = month_nr
		weekday = parser.parse(release_date).strftime('%A')
		# print ("weekday " + weekday)

		weekday_feature = weekday_no_map[weekday]
		# print ("weekday_no " + str(weekday_feature))

		Runtime = document['Runtime']
		if isNaN(Runtime):
			continue

		# print ("Runtime " + Runtime + " " + str(Runtime).strip(','))
		genre_binary_features = [0] * len(genre_features_map.keys())

		Genre_list = document['Genre'].split(',')
		# print ("Genre_list " + str(Genre_list))
		if isNaN(Genre_list[0]):
			continue

		for g in Genre_list:
			genre_binary_features[genre_features_map[str(g).strip()]] = 1

		Language = document['Language']
		if isNaN(Language):
			continue

		IMDb_Rating = document['imdbRating']
		# print ("IMDb_Rating: " + IMDb_Rating)
		if isNaN(IMDb_Rating):
			continue

		holidayCalendar = HolidayCalendar()
		isUSHoliday = holidayCalendar.is_US_holiday(int(day), month_nr, int(year))

		remake = 0
		if "/" in yearString:
			remake = 1

		actors = actors.encode('utf-8').strip().split(',')
		rewards_no = 0
		for a in actors:
			rewards_no += person_academy_awards(a, int(year))

		hasWriter = 0
		if document['Writer'] != 'N/A':
			hasWriter = 1

		isEnglish = 0
		if Language == 'English':
			isEnglish = 1

		type_list = [0, 0, 0]
		if document["Type"] == 'movie':
			type_list[0] = 1
		elif document["Type"] == 'series':
			type_list[1] = 1
		elif document["Type"] == 'episode':
			type_list[2] = 1
		# print ("Type ", document["Type"])

		production = ""
		try:
			production = document['Production']
		except KeyError:
			print ("---------------------- No production -------------------------")
		# print ('Production', production)
		movie_producer_companies_feature = 0
		for index in range(len(movie_producer_companies)):
			if movie_producer_companies[index] in production:
				movie_producer_companies_feature = index + 1

		writer = document['Writer']
		# print ('Writer', writer)
		movie_writer_feature = 0
		for index in range(len(movie_writer)):
			if movie_writer[index] in writer:
				movie_writer_feature = index + 1

		director = document['Director']
		# print ('Director', director)
		movie_director_feature = 0
		for index in range(len(movie_writer)):
			if movie_writer[index] in director:
				movie_director_feature = index + 1

		movie_title_in_plot = 0
		if Title in document['Plot']:
			movie_title_in_plot = 1

		plot = document['Plot']
		if isNaN(plot):
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
		row += [yearString]
		row += [day]
		row += [plot]

		print (row)
		# print (len(row))
		# print (len(header))

		data_frame.loc[pd_index] = row
		pd_index += 1

print (data_frame)
data_frame.drop_duplicates()
data_frame.to_csv("../../data/compressed_dataset2.csv", sep='\t')
