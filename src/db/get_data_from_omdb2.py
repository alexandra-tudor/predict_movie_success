from __future__ import print_function

import json
import time

import omdb
from imdb import IMDb

from src.db.movie_mongo import connect

ia = IMDb()
db = connect()

with open('../../data/movies.list') as f:
	for line in f:
		cols = line.split()
		year = cols[-1]
		title = cols[0].replace('#', '')

		print (title + " -- " + year)

		if '-' in year:
			year = year.split('-')[0]

		print (year)

		if "????" == year or int(year) < 2005:
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

		print (json_data)

		result = db.movie.insert_one(json_data)
