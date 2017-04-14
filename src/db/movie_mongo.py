from pymongo import MongoClient

def connect():
	client = MongoClient()
	db = client.movies

	return db

def getCursor():
	client = MongoClient()
	db = client.movies
	collection = db['movie']
	cursor = collection.find(
		{
			"Released"  : {'$ne': 'N/A'},
			"Runtime"   : {'$ne': 'N/A'},
			"imdbRating": {'$ne': 'N/A'},
			"Genre"     : {'$ne': 'N/A'}
		}
	)

	return cursor