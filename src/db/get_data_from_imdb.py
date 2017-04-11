from __future__ import print_function
from imdb import IMDb
ia = IMDb()

# print the director(s) of a movie\
# entries = ia.get_top250_movies()
# for entry in entries:
# 	the_matrix = ia.get_movie(entry.getID())
# 	print the_matrix['title']
# 	print the_matrix['actors']

for index in range(1, 5999998):
	the_matrix = ia.get_movie(str(index))

	print()

	print("Title: ")
	try:
		print("[" + str(index) + "]  " + the_matrix['title'])
	except KeyError:
		print("--")

	print("Actors: ")
	try:
		actor_list = the_matrix['actors']
		print(actor_list)
	except KeyError:
		print("--")

	print("Actresses: ")
	try:
		actress_list = the_matrix['actresses']
		print(actress_list)
	except KeyError:
		print("--")

	print("Genres: ")
	try:
		genre_list = the_matrix['genres']
		print(genre_list)
	except KeyError:
		print("--")

	print("Runtime: ")
	try:
		runtime = the_matrix['runtime']
		print(runtime)
	except KeyError:
		print("--")

	print("Plot: ")
	try:
		plot = the_matrix['plot']
		print(plot)
	except KeyError:
		print("--")

	print("Cast: ")
	try:
		cast_list = the_matrix['cast']
		print(cast_list)
	except KeyError:
		print("--")

	print("Crew: ")
	try:
		crew_list = the_matrix['crew']
		print(crew_list)
	except KeyError:
		print("--")

	print("Country: ")
	try:
		country = the_matrix['country']
		print(country)
	except KeyError:
		print("--")

	print("Language: ")
	try:
		language = the_matrix['language']
		print(language)
	except KeyError:
		print("--")

	print("StoryLine: ")
	try:
		storyline = the_matrix['storyline']
		print(storyline)
	except KeyError:
		print("--")

	print("Director: ")
	try:
		director = the_matrix['director']
		print(director)
	except KeyError:
		print("--")

	print("Release: ")
	try:
		release = the_matrix['release']
		print(release)
	except KeyError:
		print("--")

	print("Year: ")
	try:
		release = the_matrix['year']
		print(release)
	except KeyError:
		print("--")

	print("Rating: ")
	try:
		release = the_matrix['rating']
		print(release)
	except KeyError:
		print("--")


# search for a person
# for person in ia.search_person('Mel Gibson'):
#     print person.personID, person['name']

# i = IMDb()
# # movie_list is a list of Movie objects, with only attributes like 'title'
# # and 'year' defined.
# movie_list = i.search_movie('lord')
# # the first movie in the list.
# first_match = movie_list[0]
# # only basic information like the title will be printed.
# print first_match.summary()
# # update the information for this movie.
# i.update(first_match)
# # a lot of information will be printed!
# print first_match.summary()
# # retrieve trivia information and print it.
# i.update(first_match, 'trivia')
# print m['trivia']
# # retrieve both 'quotes' and 'goofs' information (with a list or tuple)
# i.update(m, ['quotes', 'goofs'])
# print m['quotes']
# print m['goofs']
# # retrieve every available information.
# i.update(m, 'all')
