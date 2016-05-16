import os, shutil
from bs4 import BeautifulSoup
import re
import urllib2

direcInput='/Users/jotaku/Downloads/bigdata/places/'
direcOutput='/Users/jotaku/Downloads/bigdata/famous/'

def getUrl(filename):
	f = open(direcInput+filename, 'r')
	lst = f.readlines()
	for catag in lst:
		add(catag, filename)
	f.close()

def add(url, filename):
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser').find('section', id='list-groups')
	content = soup.findAll('a')
	#print soup
	#print '###########'
	#print content
	myfile = open(direcOutput+filename,'a')
	pat = re.compile(r'href="([^"]*)"')
	#pat2 = re.compile(r'https://roadtrippers.com/lists-itinerary/')
	repeated = {}
	for item in content:
		h = pat.search(str(item))
		href = h.group(1)
		ans = href
		if ans not in repeated:
			myfile.write(ans)
			myfile.write('\r\n')
			repeated[ans] = None
	myfile.close()
	return filename+'finished'

if __name__ == '__main__':
	#discard the first if statement, to run all cities.
	i = 0
	for place in os.listdir(direcInput):
		######
		#if i >= 3:
		#	break
		######
		if place.endswith('txt'):
			print i
			i+=1
			print getUrl(place)	
