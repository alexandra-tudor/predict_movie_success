import json
from time import strptime

import pandas as pd
from datetime import datetime, timedelta
from pytrends.request import TrendReq

from src.db.movie_mongo import getCursor

google_username = ""
google_password = ""
# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq(google_username, google_password, custom_useragent='')

cursor, db = getCursor()
popularity = {}


# returns the average number of google queries from the past 4 weeks -> 4 values, for each week
def get_trends(movie_title, year, month, day):

	try:
		# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
		pytrend.build_payload(kw_list=[movie_title])
	except ValueError:
		print ("You're BANNED!!!")
		return [], [0, 0, 0, 0], 0, 0
	interest_over_time_df_web = []
	# Interest Over Time
	try:
		interest_over_time_df_web = pytrend.interest_over_time()
	except:
		print ("KeyError occurred when executing interest_over_time_df_web = pytrend.interest_over_time()")
		return [], [0, 0, 0, 0], 0, 0

	# print (interest_over_time_df_web)

	all_values = [(pd.to_datetime(r[0]).strftime("%d-%m-%Y"), r[1]) for r in interest_over_time_df_web.itertuples()]
	last_month_before_release_popularity_web = []
	sorted(all_values, key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'))
	# date_1 = datetime.strptime('' + str(day) + '-' + str(int(month)) + '-' + str(year), "%d-%m-%Y")
	# print (date_1)
	# end_date = date_1 + timedelta(days=10)
	# print (end_date)
	all_values.reverse()
	month = int(month)
	there = False
	for date, v in all_values:
		d, m, y = date.split('-')
		di = int(d)
		mi = int(m)
		yi = int(y)
		if not there:
			if yi > int(year):
				continue
			elif mi > int(month):
				continue
			elif mi == month and di > int(day):
				continue
		there = True
		last_month_before_release_popularity_web += [(date, v)]

	if len(last_month_before_release_popularity_web) == 0:
		return [], [0, 0, 0, 0], 0, 0
	last_month_before_release_popularity_web = last_month_before_release_popularity_web[3:15]

	averages = []
	i = 0
	avg_searches = 0.0
	num = 0
	q = 3
	for _, v in last_month_before_release_popularity_web:
		if i == q-1:
			if num > 0:
				averages += [avg_searches/num]
			else:
				averages += [0]
			q += 3
			avg_searches = 0.0
			num = 0
		elif i < q:
			i += 1
			avg_searches += v
			num += 1

	if num > 0:
		averages += [avg_searches/num]
	else:
		averages += [0]

	if len(averages) < 4:
		print (averages)
		return [], [0, 0, 0, 0], 0, 0

	averages.reverse()
	last_month_before_release_popularity_web.reverse()
	values_only = map(lambda x: x[1], last_month_before_release_popularity_web)
	total_avg = sum(values_only) / 12

	s = 0
	for v in range(1, len(averages)):
		s += (averages[v] - averages[v-1])/(averages[v-1] + 1)
	growth_rate = (float(s)/(len(averages)-1))

	print (averages)
	print (total_avg, growth_rate)

	return last_month_before_release_popularity_web, averages, total_avg, growth_rate


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

