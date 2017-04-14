from __future__ import print_function

import json
from pprint import pprint

import omdb
from imdb import IMDb

from src.db.movie_mongo import connect

ia = IMDb()

for index in range(294733, 5999998):
	the_matrix = ia.get_movie(str(index))
	title = ""
	year = ""
	try:
		title = the_matrix['title']
		year = the_matrix['year']
	except:
		print ("Data not found for index : " + str(index))
		continue

	res = omdb.request(t=title, y=int(year), r='json')
	json_content = res.content
	json_data = json.loads(json_content)

	if json_data["Response"] == "False":
		continue
	pprint(json_data)

	db = connect()
	result = db.movie.insert_one(json_data)