from bs4 import BeautifulSoup
import re
import urllib2

def getFamous(url, localfile):
	html = urllib2.urlopen(url).read()
	#html = unicode(html, 'gb3212', 'ignore').encode('utf-8', 'ignore')
	soup = BeautifulSoup(html)
	content = soup.findAll('a')
	myfile = open(localfile,'w')
	pat = re.compile(r'href="([^"]*)"')
	pat2 = re.compile(r'https://roadtrippers.com/lists-itinerary/')
	repeated = {}
	for item in content:
		h = pat.search(str(item))
		href = h.group(1)
		if pat2.search(href):
			ans = href
			if ans not in repeated:
				myfile.write(ans)
				myfile.write('\r\n')
				repeated[ans] = None
				#print ans
	myfile.close()
	return localfile+'finished'

if __name__ == '__main__':
	f = open('aHref.txt','r')
	urls = f.readlines()
	for url in urls:
		fileName = url[28:]+'.txt'
		print getFamous(url, 'places/'+fileName)
	f.close()