from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(open('roadtrippers_com_best_of.html'))

content = soup.findAll('a')
myfile = open('aHref.txt','w')
pat = re.compile(r'href="([^"]*)"')
pat2 = re.compile(r'https://roadtrippers.com/us/')
for item in content:
	h = pat.search(str(item))
	href = h.group(1)
	if pat2.search(href):
		ans = href
		print ans
		myfile.write(ans)
		myfile.write('\r\n')

myfile.close()