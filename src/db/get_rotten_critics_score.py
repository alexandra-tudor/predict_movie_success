import requests
import simplejson as simplejson


def getMovieDetails(key, title):
	"""
	Get additional movie details
	"""
	if " " in title:
		parts = title.split(" ")
		title = "+".join(parts)

	link = "http://api.rottentomatoes.com/api/public/v1.0/movies.json"
	url = "%s?apikey=%s&q=%s&page_limit=1"
	url = url % (link, key, title)
	res = requests.get(url)
	js = simplejson.loads(res.content)

	for movie in js["movies"]:
		print "rated: %s" % movie["mpaa_rating"]
		print "movie synopsis: " + movie["synopsis"]
		print "critics_consensus: " + movie["critics_consensus"]

		print "Major cast:"
		for actor in movie["abridged_cast"]:
			print "%s as %s" % (actor["name"], actor["characters"][0])

		ratings = movie["ratings"]
		print "runtime: %s" % movie["runtime"]
		print "critics score: %s" % ratings["critics_score"]
		print "audience score: %s" % ratings["audience_score"]
		print "for more information: %s" % movie["links"]["alternate"]
	print "-" * 40
	print


getMovieDetails("36yrd3e6m56qskq6w8krz75p", "Harry Potter")