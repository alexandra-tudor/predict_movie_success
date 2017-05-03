from __future__ import print_function

import json
import time

import omdb
from imdb import IMDb

from src.db.movie_mongo import connect

ia = IMDb()
db = connect()

# index = 2500000-2500038
# index = 1500000-1500018
# index = 1100000-1100022
# index = 1000000-1000013
# index = 900000-900016
# index = 800000-800033
# index = 700000-700067
# index = 600000-600021
# index = 500000-500054
# index = 400000-400023
# index = 300000-300031
# index = 200000-200017
# index = 150000-150008
# index = 140000-
# index = 130000-130005
# index = 125000-128942
# index = 120000-120019
# index = 110000-110033
# index = 100000-100049
# index = 98000-98014
# index = 95000-95012
# index = 90000-90015
# index = 80000-80010
# index = 70000-70014
index = 97859 # 55000-64377 !!!!!!!!!!!!!!!
# index = 5999000-5999237
# index = 5999998-6000078
# index = 6100078-6106034
while index < 9999998:
	index += 1
	the_matrix = ia.get_movie(str(index))
	title = ""
	year = ""
	print ("\n")
	print ("Index: " + str(index))
	try:
		title = the_matrix['title']
		print (title)
		year = the_matrix['year']
		print (year)
		if int(year) < 1960:
			continue
		genre = the_matrix['genre']
		print (genre)
	except KeyError:
		print ("Data not found for index : " + str(index))
		continue

	try:
		res = omdb.request(t=title, y=int(year), r='json')
	except:
		print("Timeout! Wait and do it again")
		time.sleep(5)
		continue

	json_content = res.content
	json_data = json.loads(json_content)

	if json_data["Response"] == "False":
		continue
	# pprint(json_data)

	result = db.movie.insert_one(json_data)
	print ("\t done " + str(index))
