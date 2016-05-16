import os, shutil
from bs4 import BeautifulSoup
import re
import json

inputPath = '/Users/jotaku/Downloads/bigdata/ratings'

def start(src, dst):

	result_f = open(dst, 'w')
	exist = {}

	for path in os.listdir(src):
		if path.endswith("Store"):
			pass
		else:
			fpath = src + os.sep + path
			f = open(fpath, 'r')
			data = json.load(f)
			for i in data:
				tags = i['tags']
				for tag in tags:
					if tag in exist:
						exist[tag] += 1
					else:
						exist[tag] = 0
						print tag
			f.close()
	for tag, number in exist.iteritems():
		if number < 1000:
			continue
		result_f.write(tag+' : '+str(number))
		result_f.write('\r\n')
	result_f.close()


if __name__ == '__main__':
	start(inputPath, 'test.txt')
