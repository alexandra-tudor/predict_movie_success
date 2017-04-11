from __future__ import print_function
from imdb import IMDb
import omdb
import json
from pprint import pprint
from pymongo import MongoClient

ia = IMDb()

for index in range(1, 5999998):
	the_matrix = ia.get_movie(str(index))
	title = ""
	year = ""
	try:
		title = the_matrix['title']
		year = the_matrix['year']
	except:
		print ("Data not found for index : " + str(index))

	res = omdb.request(t=title, y=int(year), r='json')
	json_content = res.content
	json_data = json.loads(json_content)

	if json_data["Response"] == "False":
		continue
	pprint(json_data)

	client = MongoClient()
	db = client.movies

	result = db.movie.insert_one(json_data)