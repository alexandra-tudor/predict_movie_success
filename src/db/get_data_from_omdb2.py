from __future__ import print_function

import json
import time

import omdb
from imdb import IMDb

from src.db.movie_mongo import connect

ia = IMDb()
db = connect()


def isNumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


with open('../../data/movies.list') as f:
	for line in f:

		if line.startswith("("):
			continue

		cols = []
		c = line.split('(')

		year = c[1].split(')')[0]
		title = c[0].replace('#', '')[:-1]

		print (title + " -- " + year)

		if not isNumber(year):
			continue

		if '-' in year:
			year = year.split('-')[0]

		if '/' in year:
			year = year.split('/')[0]

		print (year)

		if "????" == year or int(year) < 2005:
			continue

		try:
			res = omdb.request(t=title, y=int(year), r='json')
		except:
			print("Timeout! Wait and do it again")
			time.sleep(5)
			continue

		json_content = res.content.decode("utf-8")
		print (json_content)
		json_data = json.loads(json_content)

		if json_data["Response"] == "False":
			continue

		result = db.movie.insert_one(json_data)
