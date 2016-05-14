import os, shutil
from bs4 import BeautifulSoup
import urllib2
import re
import json
import math

#relative data path
ratingPath = 'ratings'
linksPath = 'famous'

tagDict = {
	'park':['City Park', 'State Park', 'Community Park'],
	'nightlife':['Nightlife Spot', 'Bar'],
	'children':['Zoo', 'Other Amusement', "Children's Attraction", 'Amusement Park'],
	'nature':['Campground', 'Natural Feature', 'Scenic Point', 'Nature Reserve', 'Forest', \
	'Roadside Attraction'],
	'sports':['Other Sporting Facility', 'Ski area', 'Other Sport Stadium', 'Hiking Area', \
	'Cycling Area', 'Stadium'],
	'historic':['Military Site', 'Government Building', 'Museum', 'Native Culture', 'Other Historical', \
	'Monument', 'History Museum', 'Historic Site'],
	'art_science':['Art Museum', 'Automotive Attraction', 'Library', 'Architectural Site', \
	'Science Place', 'Art Gallery', 'Music Venue', 'Science Museum', 'Folk Art', 'Engineering Marvel'],
	'aquatic':['Fishing Spot', 'Water Sports', 'Beach'],
	'shows':['Local Theater', 'Theater', "Drive-in Movie Theater", 'Concert Hall', 'Cinema', \
	'Comedy Club', 'Show'],
	'adventure':['Offbeat Attraction', 'Other Adventure Sport']
}

#return the highest rate and most popular place, suitable places, 3 places
def getPopular(s, tags):
	path = ratingPath + os.sep + s + '.txt'
	f = open(path, 'r')
	places = json.load(f)

	ret = ['','']
	number = 0
	rate = 0.0
	rate_number = 0
	max_score = 0
	max_place = ''
	for place in places:
		tmp_score = 0
		if number < place['number']:
			ret[0], number = place['name'], place['number']
		if rate <= place['rate']:
			if rate == place['rate']:
				if rate_number < place['number']:
					ret[1], rate_number = place['name'], place['number']
			else:
				ret[1], rate = place['name'], place['rate']

		for tag in place['tags']:
			for tag1 in tagDict[tags[0]]:
				if tag == tag1:
					tmp_score += 50
			if tags[1] == '':
				pass
			else:
				for tag1 in tagDict[tags[1]]:
					if tag == tag1:
						tmp_score += 30
			if tags[2] == '':
				pass
			else:
				for tag1 in tagDict[tags[2]]:
					if tag == tag1:
						tmp_score += 20

		if tmp_score > max_score:
			max_place, max_score = place['name'], tmp_score

	ret.append(max_place)
	f.close()
	
	print ret
	print max_score
	return ret

#return the related link for getting data
def getLink(s, tags):
	#choose the last one
	places = getPopular(s, tags)
	ret = []

	path = linksPath + os.sep + s + '.txt'
	f = open(path, 'r')
	links = f.readlines()

	for place in places:
		pat = re.compile(switch(place))
		
		for link in links:
			if pat.search(link):
				ret.append(link[:-2])
				break
	f.close()
	if ret == 0:
		return None
	return ret[-1]

#return picture and description
def getData(place, tags):
	print 'data source:'
	url = getLink(place, tags)
	print url
	print '########'
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser').find('section', id='map-content-view')
	photo = BeautifulSoup(str(soup.findAll(attrs={"class":"feature-photo"})), 'html.parser')
	photo_link = photo.findAll('img')[0].attrs['src']
	reviews = BeautifulSoup(str(soup.findAll(attrs={"data-user-id":"725137"})), 'html.parser')
	description = reviews.findAll(attrs={"class":"review-text"})[0].get_text()[2:-2]
	return photo_link, description

#change the place name to link format
def switch(s):
	ret = s.lower()
	tmp = ret.split(' ')
	ret = '-'.join(tmp)
	return ret

#useless
def changeName():
	for path in os.listdir(linksPath):
		if path.endswith("Store"):
			continue
		place = path[:-6]
		f_name = place + '.txt'
		p1 = linksPath + os.sep + path
		p2 = linksPath + os.sep + f_name
		os.rename(p1, p2)
	return None


#main, test
if __name__ == '__main__':
	print '****begin****'
	tags = ['nightlife', 'art_science', '']
	#use place and tags to obtain the best place to show
	link, description = getData('orlando-fl', tags)
	print 'link: '+link
	print 'description: '+description
	print '****end****'
