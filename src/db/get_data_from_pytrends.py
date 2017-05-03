import json
from time import strptime

import pandas as pd
from pytrends.request import TrendReq

from src.db.movie_mongo import getCursor

google_username = ""
google_password = ""
# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq(google_username, google_password, custom_useragent='My PyTrends Script')

cursor, db = getCursor()
popularity = {}


# returns the average number of google queries from the past 4 weeks -> 4 values, for each week
def get_trends(movie_title, year, month, day):
	start_time_frame = (str(year) + '-' + format(month - 1, '02') + '-' + str(day)).encode('utf-8')
	end_time_frame = (str(year) + '-' + format(month, '02') + '-' + str(day)).encode('utf-8')
	time_frame = (start_time_frame + ' ' + end_time_frame).encode('utf-8')

	# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
	pytrend.build_payload(kw_list=[movie_title], gprop='web', timeframe=time_frame)

	interest_over_time_df_web = []
	# Interest Over Time
	try:
		interest_over_time_df_web = pytrend.interest_over_time()
	except KeyError:
		print ("KeyError occurred when executing interest_over_time_df_web = pytrend.interest_over_time()")

	print (interest_over_time_df_web)

	last_month_before_release_popularity_web = [(pd.to_datetime(r[0]).strftime("%d-%m-%Y"), r[1]) for r in interest_over_time_df_web.itertuples()]

	averages = []
	for i in range(3):
		avg_searches = 0.0
		num = 0
		for _,v in last_month_before_release_popularity_web:
			avg_searches += v
			num += 1
		averages += [avg_searches/num]

	return last_month_before_release_popularity_web, averages


def get_pytrends_data():
	for document in cursor:
		title = document['Title']
		release_date = document['Released']
		print ("")
		print ("Title : " + title + " ; Release: ", release_date)
		day, month, year = release_date.split()
		month_nr = strptime(month,'%b').tm_mon

		start_time_frame = (year + '-' + format(month_nr-1, '02') + '-' + day).encode('utf-8')
		end_time_frame = (year + '-' + format(month_nr, '02') + '-' + day).encode('utf-8')
		time_frame = (start_time_frame + ' ' + end_time_frame).encode('utf-8')
		# print (time_frame)
		# print (start_time_frame, end_time_frame)

		# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
		pytrend.build_payload(kw_list=[title], gprop='web')

		# Interest Over Time
		try:
			interest_over_time_df_web = pytrend.interest_over_time()
		except KeyError:
			print ("KeyError occurred when executing interest_over_time_df_web = pytrend.interest_over_time()")
			continue

		# print (interest_over_time_df_web)

		last_month_before_release_popularity_web = [(pd.to_datetime(r[0]).strftime("%d-%m-%Y"), r[1]) for r in interest_over_time_df_web.itertuples()]
		# print (last_month_before_release_popularity_web)

		try:
			pytrend.build_payload(kw_list=[title], gprop='youtube')
		except ValueError:
			print ("ValueError occurred when executing pytrend.build_payload(kw_list=[title], gprop='youtube')")
			continue

		try:
			interest_over_time_df_youtube = pytrend.interest_over_time()
		except KeyError:
			print ("KeyError occurred when executing interest_over_time_df_youtube = pytrend.interest_over_time()")
			continue

		# print (interest_over_time_df_youtube)

		try:
			last_month_before_release_popularity_youtube = [(pd.to_datetime(r[0]).strftime("%d-%m-%Y"), r[1]) for r in interest_over_time_df_youtube.itertuples()]
		except ValueError:
			print ("ValueError occurred when executing last_month_before_release_popularity_youtube = [(pd.to_datetime(r[0]).strftime(\"%d-%m-%Y\"), r[1]) for r in interest_over_time_df_youtube.itertuples()]")
			continue

		# print (last_month_before_release_popularity_youtube)
		popularity[title] = {'last_month_before_release_popularity_web': last_month_before_release_popularity_web, 'last_month_before_release_popularity_youtube': last_month_before_release_popularity_youtube, 'release_date':release_date}

	with open('../../data/google_trends_popularity.json', 'w+') as outfile:
		json.dump(popularity, outfile)

