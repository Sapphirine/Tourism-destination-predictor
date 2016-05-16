Yelp.py : use yelp api
Weather.py : use Yahoo weather api

getPlaceList.py : get all travel cities links and save in aHref.txt
source : roadtrippers.com_best_of.html

getFamous.py : get all cities category links and save in the places dir
source : aHref.txt

getFamous1.py : get all cities famous links and save in the famous dir
source : places dir

getReviews.py : get all ratings and reviews in one places and save in the file with the place name
source : famous dir

getRatings.py : change the html format to json format and save in the ratings file
source : reviews

countTags.py : count different tags for statistics
source : ratings

analysis.py : get the tag data and analyze the popularity
source : ratings

getData.py : get the photo and description from local data set
source : ratings & famous