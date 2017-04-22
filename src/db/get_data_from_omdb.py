from __future__ import print_function

import json
from pprint import pprint

import omdb
from imdb import IMDb
from requests import HTTPError

import time

from src.db.movie_mongo import connect

ia = IMDb()
db = connect()

index = 349317
while index < 5999998:
	the_matrix = ia.get_movie(str(index))
	title = ""
	year = ""
	try:
		title = the_matrix['title']
		year = the_matrix['year']
	except:
		print ("Data not found for index : " + str(index))
		index += 1
		continue

	try:
		res = omdb.request(t=title, y=int(year), r='json')
		json_content = res.content
		json_data = json.loads(json_content)

		if json_data["Response"] == "False":
			continue
		pprint(json_data)

		result = db.movie.insert_one(json_data)

		index += 1
	except HTTPError:
		print ("Timeout! Wait and do it again")
		time.sleep(50)
		continue
