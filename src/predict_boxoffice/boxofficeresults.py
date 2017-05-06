import requests
from bs4 import BeautifulSoup
import pickle
import time
from pprint import pprint
from collections import defaultdict
import re
import os
from imdb import IMDb


class DatasetGenerator:

	def __init__(self):

		pass

	def returnSoup(self, urllist):
		soups = []
		for url in urllist:
			response = requests.get(url)
			while response.status_code != 200:
				time.sleep(2)
				response = requests.get(url)
			#print response.status_code, url
			soup = BeautifulSoup(response.text, "lxml")
			soups.append(soup)
		return soups

	def makeData(self, soups):
		releasegross = []
		movienames = []
		releasedate =[]
		studio = []
		for soup in soups:
			#print soup.find_all('table')[3].find_all('tr')
			#print "\n\n\n"
			tablelength = len(soup.find_all('table')[3].find_all('tr'))
			#print tablelength
			for i in range(2, tablelength):
			#for i in range(tablelength):
				#print soup.find_all('table')[3].find_all('tr')[i].find_all('td')
				try:
					releasegross_it = soup.find_all('table')[3].find_all('tr')[i].find_all('td')[5].text
					movienames_it = soup.find_all('table')[3].find_all('tr')[i].find_all('td')[1].text
					releasedate_it = soup.find_all('table')[3].find_all('tr')[i].find_all('td')[0].text
					studio_it = soup.find_all('table')[3].find_all('tr')[i].find_all('td')[2].text
				except Exception as e:
					continue

				releasegross.append(releasegross_it)
				movienames.append(movienames_it)
				releasedate.append(releasedate_it)
				studio.append(studio_it)

		boxoffice ={}
		for i, item in enumerate(movienames):
			if (item[0] != "$"):
				boxoffice[item] = zip(studio, releasegross, releasedate)[i]
		return boxoffice


	def get_urls(self, ctype):

		if (ctype == "boxoffice"):
			links = []
			for i in range(2000, 2017):
				url = 'http://www.boxofficemojo.com/yearly/chart/?view=releasedate&view2=domestic&yr='+str(i)+'&p=.htm'
				links.append(url)
			return links

		elif (ctype == "oscar"):
			links = []
			for i in range(2000, 2017):
				url = 'http://www.boxofficemojo.com/oscar/chart/?yr='+str(i)+'&view=allcategories&p=.htm'
				links.append(url)
			return links


	def getBestPicture(self, links):
		bestpicture = defaultdict(list)
		for link in links:
			date = link[45:49]
			response = requests.get(link)
			while response.status_code != 200:
				time.sleep(2)
				response = requests.get(link)
			soup = BeautifulSoup(response.text, "lxml")
			for siblings in soup.table.next_sibling.next_sibling.table.tr.next_siblings:
				bestpicture[date].append(siblings.b.text.encode('ascii','ignore'))
			bestpicture[date] = bestpicture[date][:-2]
		return bestpicture

	def getBestDirector(self, links):
		bestdirector = defaultdict(list)
		for link in links:
			date = link[45:49]
			response = requests.get(link)
			while response.status_code != 200:
				time.sleep(2)
				response = requests.get(link)
			soup = BeautifulSoup(response.text, "lxml")
			for items in soup.find_all('table')[3].find_all('tr')[1:-2]:
				bestdirector[date].append(items.find_all('td')[1].text.encode('ascii','ignore'))
		return bestdirector


	def getBestActor(self, links):
		bestactor = defaultdict(list)
		for link in links:
			date = link[45:49]
			response = requests.get(link)
			while response.status_code != 200:
				time.sleep(2)
				response = requests.get(link)
			soup = BeautifulSoup(response.text, "lxml")
			for items in soup.find_all('table')[4].find_all('tr')[1:-2]:
				bestactor[date].append(items.find_all('td')[1].text.encode('ascii','ignore'))
		return bestactor


	def getBestActress(self, links):
		bestactress = defaultdict(list)
		for link in links:
			date = link[45:49]
			response = requests.get(link)
			while response.status_code != 200:
				time.sleep(2)
				response = requests.get(link)
			soup = BeautifulSoup(response.text, "lxml")
			for items in soup.find_all('table')[5].find_all('tr')[1:-2]:
				bestactress[date].append(items.find_all('td')[1].text.encode('ascii','ignore'))
		return bestactress

	def getBoxOfficeData(self):
		urllist = self.get_urls("boxoffice")

		soups = self.returnSoup(urllist)
		boxoffice = self.makeData(soups)

		#pprint(boxoffice)

		with open('boxofficedata.pkl', 'w') as picklefile:
			pickle.dump(boxoffice, picklefile)

	def getOscarsData(self):

		links = self.get_urls("oscar")

		bestpicture = self.getBestPicture(links)
		bestdirector = self.getBestDirector(links)
		bestactor = self.getBestActor(links)
		bestactress = self.getBestActress(links)

		pprint(bestpicture)
		print "\n\n\n"
		pprint(bestdirector)
		print "\n\n\n"
		pprint(bestactor)
		print "\n\n\n"
		pprint(bestactress)

		with open('bestpicture.pkl', 'w') as picklefile:
			pickle.dump(bestpicture, picklefile)


		with open('bestdirector.pkl', 'w') as picklefile:
			pickle.dump(bestdirector, picklefile)


		with open('bestactor.pkl', 'w') as picklefile:
			pickle.dump(bestactor, picklefile)


		with open('bestactress.pkl', 'w') as picklefile:
			pickle.dump(bestactress, picklefile)

	def screensData(self):
		urllist = self.get_urls("boxoffice")
		soups = self.returnSoup(urllist)

		screens = []
		movienames = []
		for soup in soups:
			#print soup.find_all('table')[3].find_all('tr')
			#print "\n\n\n"
			tablelength = len(soup.find_all('table')[3].find_all('tr'))
			#print tablelength
			for i in range(2, tablelength):
			#for i in range(tablelength):
				#print soup.find_all('table')[3].find_all('tr')[i].find_all('td')
				try:
					movienames_it = soup.find_all('table')[3].find_all('tr')[i].find_all('td')[1].text
					screen_it = soup.find_all('table')[3].find_all('tr')[i].find_all('td')[4].text
				except Exception as e:
					continue

				movienames.append(movienames_it)
				screens.append(screen_it)

		the = {}
		for i, item in enumerate(movienames):
			if (item[0] != "$"):
				the[item] = screens[i]

		with open('screens.pkl', 'w') as picklefile:
			pickle.dump(the, picklefile)

	def getBudgetData(self):

		urllist = ["http://www.the-numbers.com/movie/budgets/all"]
		soups = []

		for url in urllist:
			response = requests.get(url)
			while response.status_code != 200:
				time.sleep(2)
				response = requests.get(url)
			#print response.status_code, url
			soup = BeautifulSoup(response.text, "lxml")
			soups.append(soup)

		for soup in soups:
			tablelength = len(soup.find_all('table')[0].find_all('tr'))
			budget_dict = {}
			for i in range(1, tablelength):
				try:
					name = soup.find_all('table')[0].find_all('tr')[i].find_all('td')[2].text
					budget = soup.find_all('table')[0].find_all('tr')[i].find_all('td')[3].text

					budget_dict[name] = budget
				except Exception as e:
					#print "error at index", i
					continue

		with open('budget.pkl', 'w') as picklefile:
			pickle.dump(budget_dict, picklefile)


		#with open("budget.pkl", 'r') as picklefile:
		#	budget = pickle.load(picklefile)

	def getBoxOfficeBudget(self):

		with open("boxofficedata.pkl", 'rb') as picklefile:
			boxoffice = pickle.load(picklefile)

		with open("budget.pkl", 'r') as picklefile:
			budget = pickle.load(picklefile)

		movies = boxoffice.keys()
		movie_budgets = budget.keys()

		budget_dict = {}
		for movie in movies:
			if movie in movie_budgets:
				budget_dict[movie] = budget[movie]
			else:
				budget_dict[movie] = "N/A"

		with open('budget_boxoffice.pkl', 'w') as picklefile:
			pickle.dump(budget_dict, picklefile)

		return budget_dict

	def IMDB_Data(self):

		ia = IMDb()

		#Read in box office data

		with open("boxofficedata.pkl", 'rb') as picklefile:
			boxoffice = pickle.load(picklefile)

		movies = boxoffice.keys()
		print len(movies)

		#with open("genre.pkl", 'r') as picklefile:
		#		genre = pickle.load(picklefile)
		genre = {}
		#print set(movies)
		#print "********"
		#print set(genre.keys())
		#movies = set(movies) - set(genre.keys())
		#print set(genre.keys())

		print len(movies)
		'''
		for movie in movies:
			try:
				if not ia.search_movie(movie):
					genre[movie] = 'N/A'
					print(movie, "not found")
				else:
					firstmatch = ia.search_movie(movie)[0]
					ia.update(firstmatch)
					if firstmatch.has_key('genres') == 1:
						genre[movie] = firstmatch['genres']
						print(movie, "genre found")
					else:
						genre[movie] = 'N/A'
						print(movie, 'genre not found')
			except Exception as e:
				print "some error at movie ", movie

		with open('genre.pkl', 'w') as picklefile:
			pickle.dump(genre, picklefile)
		'''

		'''getting director, cast, and runtime data'''

		#with open("director.pkl", 'r') as picklefile:
		#	director = pickle.load(picklefile)

		#with open("cast.pkl", 'r') as picklefile:
		#	cast = pickle.load(picklefile)

		#with open("runtime.pkl", 'r') as picklefile:
		#	runtime = pickle.load(picklefile)

		director = {}
		cast = {}
		runtime = {}

		#print movies
		for movie in movies:
			try:
				if not ia.search_movie(movie):
					print(movie, "not found")
					director[movie] = 'N/A'
					cast[movie] = 'N/A'
					runtime[movie] = 'N/A'
				else:
					print(movie)
					firstmatch = ia.search_movie(movie)[0]
					ia.update(firstmatch)
					if firstmatch.has_key('director') == 1:
						director[movie] = firstmatch['director'][0]['name']
					elif firstmatch.has_key('director') == 0:
						director[movie] = 'N/A'
					if firstmatch.has_key('cast') == 1:
						for item in firstmatch['cast']:
							try:
								cast[movie].append(item['name'])
							except:
								cast[movie] = [item['name']]
					elif firstmatch.has_key('cast') == 0:
						cast[movie] = 'N/A'
					if firstmatch.has_key('runtime') == 1:
						for item in firstmatch['runtime']:
							try:
								runtime[movie].append(item)
							except:
								runtime[movie] = [item]
					elif firstmatch.has_key('runtime') == 0:
						runtime[movie] = 'N/A'
					#print director[movie], " --- ", cast[movie], " +++ ",  runtime[movie]
			except Exception as e:
				raise e



		with open('director.pkl', 'w') as picklefile:
			pickle.dump(director, picklefile)

		with open('cast.pkl', 'w') as picklefile:
			pickle.dump(cast, picklefile)

		with open('runtime.pkl', 'w') as picklefile:
			pickle.dump(runtime, picklefile)

class MovieSuccessPredictor:


	def __init__(self):

		pass



dg = DatasetGenerator()

#dg.getBoxOfficeData()
#dg.getOscarsData()

#dg.IMDB_Data()

bd = dg.getBoxOfficeBudget()
