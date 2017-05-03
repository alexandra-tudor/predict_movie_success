from src.db.movie_mongo import getCursor

cursor, db = getCursor()

db['movie'].remove(
	{
		"Released"  : {'$eq': 'N/A'},
		"imdbRating": {'$eq': 'N/A'},
		"Genre"     : {'$eq': 'N/A'}
	}
)