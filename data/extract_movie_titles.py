import urllib
import urllib2
from bs4 import BeautifulSoup

with open('movie_titles.txt') as file:
	data = file.read()

data = data.split("\n")

titles = []
for line in data:
	if line and line[0] == '"':
		titles.append(line.split(":")[1].strip().replace('"', ''))

trailers = []
fh = open("trailers.txt", "w")

for idx, title in enumerate(titles[1223:]):
	print idx, title
	textToSearch = 'trailer ' + title
	#print textToSearch
	query = urllib.quote(textToSearch)
	url = "https://www.youtube.com/results?search_query=" + query
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, "lxml")
	for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
		trailer = title + ':https://www.youtube.com' + vid['href'] + '\n'
		trailers.append(trailer)
		fh.write(trailer)
		#print 'https://www.youtube.com' + vid['href']
		break

#for trailer in trailers:
#	fh.write(trailer)





