#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import shutil
from bs4 import BeautifulSoup
import urllib2
import re
import json

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
dict1 = {1:'park', 2: 'nightlife', 3: 'children', 4: 'nature', 
        5: 'sports',6: 'historic',7:"art_science", 8: 'aquatic',9: 'shows', 10: 'adventure'}
dict2 = {}

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
content = {'name': 'Washington-dc',
          'url': "https://roadtrippers.com/us/washington-dc/points-of-interest/the-white-house-washington",
          'photo': "https://res.cloudinary.com/roadtrippers/image/upload/v1398274359/the-white-house-29205.jpg",
          'des': "The White House is the official residence and principal workplace of the President of the United States. \
          Located at 1600 Pennsylvania Avenue NW in Washington, D.C., the house was designed by Irish-born James Hoban, and built between 1792 and 1800 of white-painted Aquia sandstone in the Neoclassical style. It has been the residence of every U.S. president since John Adams. When Thomas Jefferson moved into the house in 1801, he expanded the building outward, creating two colonnades that were meant to conceal stables and storage."
          }
#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111a.eastus.cloudapp.azure.com/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@w4111a.eastus.cloudapp.azure.com/proj1part2"
#
DATABASEURI = "postgresql://kesin:123@bigdatabase.eastus.cloudapp.azure.com/testdb"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
'''
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
'''

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args


  #
  # example of a database query
  #
  
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html")

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
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
  return url, photo_link, description

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

def choosecity(place1,place2,place3,place4,firstC, secondC, thirdC):
  p1 = []
  p2 = []
  p3 = []
  p4 = []
  if place1 != 'nope':
    if secondC and thirdC:
      cursor = g.conn.execute("SELECT number,rate, %s, %s, %s FROM bigdata where place = '%s'" %(firstC, secondC, thirdC, place1))
      for result in cursor:
        for res in result:
          p1.append(res)# can also be accessed using result[0]
      cursor.close()

    elif secondC:
      cursor = g.conn.execute("SELECT number,rate, %s, %s FROM bigdata where place = '%s'" %(firstC, secondC, place1))
      for result in cursor:
        for res in result:
          p1.append(res) # can also be accessed using result[0]
      cursor.close()

    elif thirdC:
      cursor = g.conn.execute("SELECT number,rate, %s, %s FROM bigdata where place = '%s'" %(firstC, thirdC, place1))
      for result in cursor:
        for res in result:
          p1.append(res)  # can also be accessed using result[0]
      cursor.close()
    else:
      cursor = g.conn.execute("SELECT number,rate, %s FROM bigdata where place = '%s'" %(firstC, place1))
      for result in cursor:
        for res in result:
          p1.append(res)  # can also be accessed using result[0]
      cursor.close()
  
  if place2 != 'nope':
    if secondC and thirdC:
      cursor = g.conn.execute("SELECT number,rate, %s, %s, %s FROM bigdata where place = '%s'" %(firstC, secondC, thirdC, place2))
      for result in cursor:
        for res in result:
          p2.append(res)  # can also be accessed using result[0]
      cursor.close()

    elif secondC:
      cursor = g.conn.execute("SELECT number,rate, %s, %s FROM bigdata where place = '%s'" %(firstC, secondC, place2))
      for result in cursor:
        for res in result:
          p2.append(res) # can also be accessed using result[0]
      cursor.close()

    elif thirdC:
      cursor = g.conn.execute("SELECT number,rate, %s, %s FROM bigdata where place = '%s'" %(firstC, thirdC, place2))
      for result in cursor:
        for res in result:
          p2.append(res)  # can also be accessed using result[0]
      cursor.close()
    else:
      cursor = g.conn.execute("SELECT number,rate, %s FROM bigdata where place = '%s'" %(firstC, place2))
      for result in cursor:
        for res in result:
          p2.append(res)  # can also be accessed using result[0]
      cursor.close()

  if place3 != 'nope':
    if secondC and thirdC:
      cursor = g.conn.execute("SELECT number,rate, %s, %s, %s FROM bigdata where place = '%s'" %(firstC, secondC, thirdC, place3))
      for result in cursor:
        for res in result:
          p3.append(res)  # can also be accessed using result[0]
      cursor.close()

    elif secondC:
      cursor = g.conn.execute("SELECT number,rate, %s, %s FROM bigdata where place = '%s'" %(firstC, secondC, place3))
      for result in cursor:
        for res in result:
          p3.append(res)  # can also be accessed using result[0]
      cursor.close()

    elif thirdC:
      cursor = g.conn.execute("SELECT number,rate, %s, %s FROM bigdata where place = '%s'" %(firstC, thirdC, place3))
      for result in cursor:
        for res in result:
          p3.append(res)  # can also be accessed using result[0]
      cursor.close()
    else:
      cursor = g.conn.execute("SELECT number,rate, %s FROM bigdata where place = '%s'" %(firstC, place3))
      for result in cursor:
        for res in result:
          p3.append(res) # can also be accessed using result[0]
      cursor.close()

  if place4 != 'nope':
    if secondC and thirdC:
      cursor = g.conn.execute("SELECT number,rate, %s, %s, %s FROM bigdata where place = '%s'" %(firstC, secondC, thirdC, place4))
      for result in cursor:
        for res in result:
          p4.append(res)  # can also be accessed using result[0]
      cursor.close()

    elif secondC:
      cursor = g.conn.execute("SELECT number,rate, %s, %s FROM bigdata where place = '%s'" %(firstC, secondC, place4))
      for result in cursor:
        for res in result:
          p4.append(res)  # can also be accessed using result[0]
      cursor.close()

    elif thirdC:
      cursor = g.conn.execute("SELECT number,rate, %s, %s FROM bigdata where place = '%s'" %(firstC, thirdC, place4))
      for result in cursor:
        for res in result:
          p4.append(res)  # can also be accessed using result[0]
      cursor.close()
    else:
      cursor = g.conn.execute("SELECT number,rate, %s FROM bigdata where place = '%s'" %(firstC, place4))
      for result in cursor:
        for res in result:
          p4.append(res) # can also be accessed using result[0]
      cursor.close()

  #print p1,p2,p3,p4
  return p1,p2,p3,p4

def calculate(p1,p2,p3,p4):
  print p1,p2,p3,p4

  tagscore1 = 0
  tagscore2 = 0
  tagscore3 = 0
  tagscore4 = 0
  if p2 == [] and p3 ==[] and p4 ==[]:
    return 1

  if p2 != [] and p3 ==[]:
    if len(p1) == 3:
      tagscore1 = float(p1[2])* 0.6
    if len(p1) == 4:
      tagscore1 = float(p1[2])* 0.6 + float(p1[3])*0.3
    if len(p1) == 5:
      tagscore1 = float(p1[2])* 0.6 + float(p1[3])*0.3 + float(p1[4])*0.1

    if len(p2) == 3:
      tagscore2 = float(p2[2])* 0.6
    if len(p2) == 4:
      tagscore2 = float(p2[2])* 0.6 + float(p2[3])*0.3
    if len(p2) == 5:
      tagscore2 = float(p2[2])* 0.6 + float(p2[3])*0.3 + float(p2[4])*0.1
    maxtag= max(tagscore1,tagscore2)
    print maxtag
    if tagscore1 > tagscore2:
      finalplace = 1
    else:
      finalplace = 2
    return finalplace

  if p2 != [] and p3 != [] and p4 == []:
    if len(p1) == 3:
      tagscore1 = float(p1[2])* 0.6
    if len(p1) == 4:
      tagscore1 = float(p1[2])* 0.6 + float(p1[3])*0.3
    if len(p1) == 5:
      tagscore1 = float(p1[2])* 0.6 + float(p1[3])*0.3 + float(p1[4])*0.1

    if len(p2) == 3:
      tagscore2 = float(p2[2])* 0.6
    if len(p2) == 4:
      tagscore2 = float(p2[2])* 0.6 + float(p2[3])*0.3
    if len(p2) == 5:
      tagscore2 = float(p2[2])* 0.6 + float(p2[3])*0.3 + float(p2[4])*0.1

    if len(p3) == 3:
      tagscore3 = float(p3[2])* 0.6
    if len(p3) == 4:
      tagscore3 = float(p3[2])* 0.6 + float(p3[3])*0.3
    if len(p3) == 5:
      tagscore3 = float(p3[2])* 0.6 + float(p3[3])*0.3 + float(p3[4])*0.1

    maxtag = max(tagscore1,tagscore2,tagscore3)
    print maxtag
    if tagscore1 == maxtag:
      return 1
    elif tagscore2 == maxtag:
      return 2
    else:
      return 3

  if p2 != [] and p3 != [] and p4 !=[]:
    if len(p1) == 3:
      tagscore1 = float(p1[2])* 0.6
    if len(p1) == 4:
      tagscore1 = float(p1[2])* 0.6 + float(p1[3])*0.3
    if len(p1) == 5:
      tagscore1 = float(p1[2])* 0.6 + float(p1[3])*0.3 + float(p1[4])*0.1

    if len(p2) == 3:
      tagscore2 = float(p2[2])* 0.6
    if len(p2) == 4:
      tagscore2 = float(p2[2])* 0.6 + float(p2[3])*0.3
    if len(p2) == 5:
      tagscore2 = float(p2[2])* 0.6 + float(p2[3])*0.3 + float(p2[4])*0.1

    if len(p3) == 3:
      tagscore3 = float(p3[2])* 0.6
    if len(p3) == 4:
      tagscore3 = float(p3[2])* 0.6 + float(p3[3])*0.3
    if len(p3) == 5:
      tagscore3 = float(p3[2])* 0.6 + float(p3[3])*0.3 + float(p3[4])*0.1

    if len(p4) == 3:
      tagscore3 = float(p4[2])* 0.6
    if len(p4) == 4:
      tagscore3 = float(p4[2])* 0.6 + float(p4[3])*0.3
    if len(p4) == 5:
      tagscore3 = float(p4[2])* 0.6 + float(p4[3])*0.3 + float(p4[4])*0.1

    maxtag = max(tagscore1,tagscore2,tagscore3)
    print maxtag
    if tagscore1 == maxtag:
      return 1
    elif tagscore2 == maxtag:
      return 2
    elif tagscore3 == maxtag:
      return 3
    else:
      return 4



@app.route('/another')
def another():
  return render_template("another.html")

@app.route('/submit', methods=['POST'])
def submit():
  print request.form
  place1 = request.form['Place1']
  place2 = request.form['Place2']
  place3 = request.form['Place3']
  place4 = request.form['Place4']
  comfort = request.form['Comfort']

  start = request.form['Check-in']
  end = request.form['Check-out']

  tag1 = request.form['tag1']
  tag2 = request.form['tag2']
  tag3 = request.form['tag3']

  firstC = dict1[int(tag1)]
  secondC = None
  thirdC = None
  if tag2 != 'nope':
    secondC = dict1[int(tag2)]
  if tag3 != 'nope':
    thirdC = dict1[int(tag3)]

  dict2[1] = place1
  dict2[2] = place2
  dict2[3] = place3
  dict2[4] = place4
  print firstC, secondC, thirdC
  print place1,place2,place3,place4

  p1,p2,p3,p4 = choosecity(place1,place2,place3,place4,firstC, secondC, thirdC)
  
  placenumber = calculate(p1,p2,p3,p4)
  finalplace = dict2[placenumber]
  print finalplace

  if secondC == None:
    secondC = ''
  if thirdC == None:
    thirdC = ''

  tags = [firstC, secondC, thirdC]
  print tags

  url,link, description = getData(finalplace, tags)
  print 'link: '+link
  print 'description: '+description
  print '****end****'
  content['url'] = url
  content['photo'] = link
  content['des'] = description
  content['name'] = finalplace
  
  #print content
  return redirect('/')
# Example of adding new data to the database



@app.route('/hottours')
def hottours():
  return render_template('index-1.html')

@app.route('/special_offer')
def special():
  print content
  return render_template('index-2x.html',**content)

@app.route('/background')
def back():
  return render_template('index-2.html')

@app.route('/contact')
def contact():
  return render_template('index-4.html')
@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8080, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """
    debug = True
    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()