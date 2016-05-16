import os, shutil
from bs4 import BeautifulSoup
import re
import urllib2
import types

direcInput='/Users/jotaku/Downloads/bigdata/famous/'
direcOutput='/Users/jotaku/Downloads/bigdata/reviews/'

#go through all the famous places
def getUrl(filename):
	f = open(direcInput+filename, 'r')
	lst = f.readlines()
	visited = {}
	pat = [r'shopping', r'accommodation', r'camping-rv', r'food-drink']
	for catag in lst:
		if re.search(pat[0], catag) or re.search(pat[1], catag) \
		or re.search(pat[2], catag) or re.search(pat[3], catag):
			continue
		if catag not in visited:
			visited[catag] = None
			print catag[25:]
			print add(catag, filename)
	print len(visited)
	f.close()
	return "finished"

#write down the reviews for every link
def add(url, filename):
	if ' ' in url:
		return "skip"
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser').find('section', id='map-content-view')
	name = soup.findAll(attrs={"itemprop":"name"})
	ratings = soup.findAll(attrs={"itemprop":"ratingValue"})
	if len(ratings) == 0:
		count = []
	else:
		count = soup.findAll(attrs={"itemprop":"ratingCount"})
	reviews = soup.findAll(attrs={"class":"review-text"})
	tag = soup.findAll(attrs={"class":"category-list"})
	
	#print reviews
	#print '###########'
	openPath = direcOutput + filename[:-6] + '/' + changeSlash(url[25:])
	f= open(openPath,'w')

	f.write(str(name[0]))
	f.write('\r\n')

	if len(ratings) == 0:
		f.write('No_ratings')
		f.write('\r\n')
	else:
		f.write(str(ratings[0]))
		f.write('\r\n')

	if len(count) == 0:
		f.write('0')
		f.write('\r\n')
	else:
		f.write(str(count[0]))
		f.write('\r\n')

	if len(tag) == 0:
		f.write('No_tags')
		f.write('\r\n')
	else:
		f.write(str(tag[0]))
		f.write('\r\n')

	for review in reviews:
		f.write(str(review))
		f.write('\r\n')

	f.close()
	return 'finished'

#build the dir for the reviews
def makeDir(dire):
	newPath = direcOutput + dire
	if not os.path.isdir(newPath):
		os.makedirs(newPath)

#delete the slash in the filename
def changeSlash(s):
	ret = ''
	for i in range(len(s)):
		if s[i] != '/':
			ret += s[i]
		else:
			ret += '-'
	ret = ret[:-2]
	ret += '.txt'
	return ret

#to run all, delete the first if statement
if __name__ == '__main__':
	i = 0
	for famous in os.listdir(direcInput):
		######
		#if i >= 1:
		#	break
		######
		if famous.endswith('txt'):
			print i
			i+=1
			print famous[:-6]
			makeDir(famous[:-6])
			print getUrl(famous)