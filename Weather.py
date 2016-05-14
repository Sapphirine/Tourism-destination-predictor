#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import urllib
import urllib2
import json
######################################
# you need woeid to get the information,
# or input the city and state to get the forecast.
# you will obtain 10 forecasts in the result list,
# and the format is : (in Json)
# 'code' : weather code
# 'text' : weather text
# 'high' & 'low' : temperature range in F
# 'day' & 'date' : day and date
# *********
# from Weather import Weather
######################################
class Weather(object):
	def getForecast(self, city, state):
		#baseurl = "https://query.yahooapis.com/v1/public/yql?"
		#yql_query = "select * from weather.forecast where woeid=2460286"
		#yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
		part1 = "https://query.yahooapis.com/v1/public/yql?q=select%20item%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22"
		part2 = "%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
		yql_url = part1 + city.lower() +"%2C%20"+ state.lower() + part2

		#print yql_url
		result = urllib2.urlopen(yql_url).read()
		data = json.loads(result)
		return data['query']['results']['channel']['item']['forecast']

#for test
if __name__ == "__main__":
	NewYorkWeather = Weather()
	result = NewYorkWeather.getForecast("orlando", "FL")
	print "forecast in " + str(len(result)) + " days :"
	print result