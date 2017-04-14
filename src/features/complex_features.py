import pandas as pd

def get_director_average_rating_past_movies(director_name, movie_release_date):
	pass


def get_writers_average_rating_past_movies(writers, movie_release_date):
	pass


def get_actors_average_rating_past_movies(actors, movie_release_date):
	pass


def person_academy_awards(person_name, movie_release_year):
	h = ['Year', 'Ceremony', 'Award', 'Winner', 'Name', 'Film']

	data = pd.read_csv("../../data/academyawards.csv")

	# no of academy awards for person_name, before movie_release_year
	filtered_data = data[(data.Name == person_name)]

	awards_no = 0

	row_iterator = filtered_data.iterrows()

	for i, row in row_iterator:
		print (row['Year'])
		print (row['Name'])

		year = max(map(lambda x: int(x), row['Year'].split('/')))

		if year < movie_release_year:
			awards_no += 1

	return awards_no