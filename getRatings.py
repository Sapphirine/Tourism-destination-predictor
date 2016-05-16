import os, shutil
from bs4 import BeautifulSoup
import re
import json

inputPath = '/Users/jotaku/Downloads/bigdata/reviews'
outputPath = '/Users/jotaku/Downloads/bigdata/ratings'

#begin the algorithm
def start(src, dst):
	i = 0
	for path in os.listdir(src):
		#### for test
		#i += 1
		#print path
		#if i > 2:
		#	break
		#### limitted to two dirs
		filepath = src + os.sep + path
		if os.path.isdir(filepath):
			saveRatings(filepath, dst, path)


#go into every files
def saveRatings(src, dst, city):

	result_path = dst + os.sep + city + '.txt'
	result_file = open(result_path, 'w')

	ans = []

	for f in os.listdir(src):
		if f.endswith("Store"):
			pass
		else:
			f_path = src + os.sep + f
			data = getRatings(f_path)
			ans.append(data)

	json.dump(ans, result_file)
	result_file.close()

#return ratings and numbers
def getRatings(src):
	f = open(src, 'r')
	data = f.readlines()
	dct = {}

	#get place name
	name = getText(data[0])
	dct['name'] = name[:-1]
	
	#get rate and numbers
	rate = getText(data[1])
	number = getText(data[2])

	if int(number) == 0:
		dct['rate'] = 0.0
	else:
		dct['rate'] = float(rate)
	
	dct['number'] = int(number)

	#get tags
	tags = []
	for l in data:
		if l[:10] == '<li><span>':
			tags.append(getText(l)[:-1])
	dct['tags'] = tags

	return dct

#get tags
def getTags(s):
	soup = BeautifulSoup(s, 'html.parser')
	ret = []
	tags = soup.findAll('span')

	for tag in tags:
		ret.append(getText(tag))
	
	return ret


#get text from html format
def getText(s):
	soup = BeautifulSoup(s, 'html.parser')
	ret = soup.get_text()
	return ret

if __name__ == '__main__':
	start(inputPath, outputPath)
	print "end"
	'''
	f = open('test.txt', 'r')
	h = json.load(f)
	print h
	print h[0]
	f.close()
	###
	f = open('test.txt', 'w')
	s1 = {'1':'a', '2':'b', '3':'c'}
	s2 = {'1':'a', '2':'b', '3':'c', '4':'d'}
	ans = [s1, s2]
	json.dump(ans, f)
	f.close()
	'''

