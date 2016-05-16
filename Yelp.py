#!/usr/bin/env python
#-*- coding:UTF-8 -*-
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
######################################
# input type:
# term : string  (what to search)
# location : string   (where to search)
# nums : integer   (number of return restaurants)
# return type : list
# [name, location, rating, categories]
# [string, list, float, list]
# *********
# from Yelp import Yelp
######################################

AUTH = Oauth1Authenticator(
	consumer_key='gbYB3BOZHA124isAf4DOJA',
	consumer_secret='1hC-KUCOx5auBNwvAa7SOOo_n-8',
	token='-9PnRhBDpavsYc4GuPPfNFS_HoEl71ud',
	token_secret='oo-vdlfeYrPaRHDMB6QWatKZREM'
)

client = Client(AUTH)

class Yelp(object):
	def getRestaurants(self, term, location, nums):

		params = {
		    'term': term,
		    'limit': nums,
		    'lang': 'en',
		    'sort': 2
		}

		reponse = client.search(location, **params)

		ret = []
		for item in reponse.businesses:
			category = []
			for temp in item.categories:
				category.append(temp.name)
			add = [item.name, item.location.address, item.rating, category]
			ret.append(add)

		return ret

#for test
if __name__ == '__main__':
	yelp_san = Yelp()
	list_san = yelp_san.getRestaurants('restaurants', 'Orlando', 5)
	for i in list_san:
		for j in i:
			print j

