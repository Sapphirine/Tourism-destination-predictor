import os, shutil
import json
import csv
import math
import types

inputPath = '/Users/jotaku/Downloads/bigdata/ratings'

tagDict = {'Local Theater':'shows', 'Campground':'nature', 'Art Museum':'art_science', \
'Other Sporting Facility':'sports', 'Military Site':'historic', 'Nightlife Spot':'nightlife', \
'City Park':'park', 'Ski area':'sports', 'Automotive Attraction':'art_science', \
'Library':'art_science', 'Other Sport Stadium':'sports', 'State Park':'park', \
'Architectural Site':'art_science', 'Bar':'nightlife', 'Government Building':'historic', \
'Museum':'historic', 'Theater':'shows', 'Science Place':'art_science', \
'Native Culture':'historic', 'Art Gallery':'art_science', 'Music Venue':'art_science', \
"Drive-in Movie Theater":'shows', 'Natural Feature':'nature', 'Offbeat Attraction':'adventure', \
'Other Historical':'historic', 'Scenic Point':'nature', 'Concert Hall':'shows', \
'Zoo':'children', 'Other Amusement':'adventure', 'Nature Reserve':'nature', \
'Cinema':'shows', 'Hiking Area':'sports', 'Forest':'nature', 'Fishing Spot':'aquatic', \
'Water Sports':'aquatic', 'Beach':'aquatic', 'Comedy Club':'shows', 'Community Park':'park', \
'Other Adventure Sport':'adventure', 'Show':'shows', 'Roadside Attraction':'nature', \
'Cycling Area':'sports', 'Science Museum':'art_science', "Children's Attraction":'children', \
'Stadium':'sports', 'Folk Art':'art_science', 'Amusement Park':'children', 'Monument':'historic', \
'History Museum':'historic', 'Historic Site':'historic', 'Engineering Marvel':'art_science'}

def start(src, dst):
	csvfile = file(dst, 'w')
	writer = csv.writer(csvfile)
	writer.writerow(['place', 'number', 'rate', 'park', \
		'nightlife', 'children', 'nature', 'sports', 'historic', \
		'art_science', 'aquatic', 'shows', 'adventure'])


	for path in os.listdir(src):
		if path.endswith("Store"):
			pass
		else:
			ans = [path[:-4]]
			fpath = src + os.sep + path
			f = open(fpath, 'r')
			data = json.load(f)
			rates = getRatings(data)
			ans.append(rates[-1])
			ans.append(rates[0])

			tagdata = getTags(data)
			for i in tagdata:
				ans.append(round(i, 2))

			writer.writerow(ans)
			f.close()

	csvfile.close()

#get the average rate and rate numbers
def getRatings(dct):
	suma = 0.0
	num = 0
	for i in dct:
		num += i['number']
		suma += i['number'] * i['rate']

	return [round(suma/num, 2), num]

#get tags presentages
def getTags(dct):
	cnt = [0]*10
	tagNumDict = {'park':0, 'nightlife':1, 'children':2, 'nature':3, \
				'sports':4, 'historic':5, 'art_science':6, \
				'aquatic':7, 'shows':8, 'adventure':9}
	for i in dct:
		tags = i['tags']
		num = i['number']
		for tag in tags:
			if tag in tagDict:
				cnt[tagNumDict[tagDict[tag]]] += math.log((num+1),2)

	print cnt

	return cnt


#main
if __name__ == '__main__':
	start(inputPath, 'test.csv')
