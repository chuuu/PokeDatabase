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

import os
import ctypes  # An included library with Python install.
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response



tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


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
DATABASEURI = "postgresql://cd2925:dchchmaggie@w4111vm.eastus.cloudapp.azure.com/w4111"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


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
  #cursor = g.conn.execute("SELECT name FROM test")
  #names = []
  #for result in cursor:
  #  names.append(result['name'])  # can also be accessed using result[0]
  #cursor.close()

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
  #context = dict(data = names)


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
@app.route('/another')
def another():
  return render_template("another.html")

@app.route('/search', methods=['POST'])
def search():
  searchall = int(request.form['chooseall'])
  if searchall==0:
    return redirect('/')
  #cursor = g.conn.execute("SELECT name FROM test")
  items = []
  if searchall == 1:
    cursor = g.conn.execute("SELECT * FROM bag")
    first_item = dict (bid="Bag ID", numitems="Number of items in bag")
    items.append(first_item)
    for result in cursor:
      an_item = dict(bid=result[0], numitems=result[1])
      items.append(an_item)
      #items.append(result[0])  # can also be accessed using result[0]
      #items.append(result[1])
    cursor.close()
    context = dict(data = items)
  elif searchall==2:
    cursor = g.conn.execute("SELECT * FROM item")
    first_item = dict (iid="Item ID", itemname="Name of item", numofthisitem="How many of these items in this particular bag", bid="Bag ID")
    items.append(first_item)
    for result in cursor:
      an_item = dict(iid=result[0], itemname=result[1], numofthisitem=result[2], bid=result[3])
      items.append(an_item)
    cursor.close()
    context = dict(itemdata = items)
  elif searchall==3:
    cursor = g.conn.execute("SELECT * FROM player")
    first_item = dict (uid="User ID", ulevel="Level", gender="Gender", bid="Bag ID", regionname="Region Name", teamname="Team Name")
    items.append(first_item)
    for result in cursor:
      an_item = dict(uid=result[0], ulevel=result[1], gender=result[2], bid=result[3], regionname=result[4], teamname=result[5])
      items.append(an_item)
    cursor.close()
    context = dict(playerdata = items)
  elif searchall==4:
    cursor = g.conn.execute("SELECT * FROM pokemon")
    first_item = dict (pid="Pokemon ID", plevel="Level", familyname="Pokemon Family", pname="Pokemon Type", uid="ID of Owner Player")
    items.append(first_item)
    for result in cursor:
      an_item = dict(pid=result[0], plevel=result[1], familyname=result[2], pname=result[3], uid=result[4])
      items.append(an_item)
    cursor.close()
    context = dict(pokedata = items)
  elif searchall == 5:
    cursor = g.conn.execute("SELECT * FROM pokemonfamily")
    first_item = dict (familyname="Pokemon Family Name")
    items.append(first_item)
    for result in cursor:
      an_item = dict(familyname=result[0])
      items.append(an_item)
    cursor.close()
    context = dict(familydata = items)
  elif searchall == 6:
    cursor = g.conn.execute("SELECT * FROM region")
    first_item = dict (regionname="Name of Region", numplayers="Number of Players in this Region")
    items.append(first_item)
    for result in cursor:
      an_item = dict(regionname=result[0], numplayers=result[1])
      items.append(an_item)
    cursor.close()
    context = dict(regiondata = items)
  elif searchall == 7:
    cursor = g.conn.execute("SELECT * FROM team")
    first_item = dict (tname="Name of Team", totnumplayers="Total Number of Players in Team")
    items.append(first_item)
    for result in cursor:
      an_item = dict(tname=result[0], totnumplayers=result[1])
      items.append(an_item)
    cursor.close()
    context = dict(teamdata = items)
  return render_template("index.html", **context)


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  num = int(request.form['trying'])
  if num==0:
    return redirect('/')
  if num==1:
    try:
      bid = int(request.form['bid'])
    except ValueError:
      return redirect('/')
    try:
      numitems = int(request.form['numitems'])
    except ValueError:
      return redirect('/')
    g.conn.execute("INSERT INTO bag(bid, numitems) VALUES (%s, %s)", (bid, numitems))
  elif num==2:
    try:
      iid = int(request.form['iid'])
    except ValueError:
      return redirect('/')
    itemname = request.form['itemname']
    try:
      numofthisitem = int(request.form['numofthisitem'])
    except ValueError:
      return redirect('/')
    try:
      bid = int(request.form['bid'])
    except ValueError:
      return redirect('/')
    g.conn.execute("INSERT INTO item(iid, itemname, numofthisitem, bid) VALUES (%s, %s, %s, %s)", (iid, itemname, numofthisitem, bid))
    g.conn.execute("UPDATE bag SET numitems=numitems+(%s) WHERE bid=(%s)", (numofthisitem, bid))
  elif num==3:
    try:
      uid = int(request.form['uid'])
    except ValueError:
      return redirect('/')
    try:
      ulevel = int(request.form['ulevel'])
    except ValueError:
      return redirect('/')
    gender = request.form['gender']
    bid = uid
    regionname = request.form['regionname']
    teamname = request.form['teamname']
    g.conn.execute("INSERT INTO bag(bid, numitems) VALUES (%s, 0)", bid)
    g.conn.execute("INSERT INTO player(uid, ulevel, gender, bid, regionname, teamname) VALUES (%s, %s, %s, %s, %s, %s)", (uid, ulevel, gender, bid, regionname, teamname))
    g.conn.execute("UPDATE region SET numplayers=numplayers+1 WHERE regionname=(%s)", regionname)
    g.conn.execute("UPDATE team SET totnumplayers=totnumplayers+1 WHERE tname=(%s)", teamname)
  elif num==4:
    try:
      pid = int(request.form['pid'])
    except ValueError:
      return redirect('/')
    try:
      plevel = int(request.form['plevel'])
    except ValueError:
      return redirect('/')
    familyname = request.form['familyname']
    pname = request.form['pname']
    try:
      uid = int(request.form['uid'])
    except ValueError:
      return redirect('/')
    g.conn.execute("INSERT INTO pokemon(pid, plevel, familyname, pname, uid) VALUES (%s, %s, %s, %s, %s)", (pid, plevel, familyname, pname, uid))
  elif num==5:
    name = request.form['familyname']
    g.conn.execute("INSERT INTO pokemonfamily(familyname) VALUES (%s)", name)
  elif num==6:
    regionname = request.form['regionname']
    try:
      numplayers = int(request.form['numplayers'])
    except ValueError:
      return redirect('/')
    g.conn.execute("INSERT INTO region(regionname, numplayers) VALUES (%s, %s)", (regionname, numplayers))
  return redirect('/')

@app.route('/seeuid', methods=['POST'])
def seeuid():
  iden = request.form['seeuid']
  items = []
  cursor = g.conn.execute("SELECT * FROM pokemon WHERE uid=(%s)", iden)
  first_item = dict (pid="Pokemon ID", plevel="Level", familyname="Pokemon Family", pname="Pokemon Type", uid="ID of Owner Player")
  items.append(first_item)
  for result in cursor:
    an_item = dict(pid=result[0], plevel=result[1], familyname=result[2], pname=result[3], uid=result[4])
    items.append(an_item)
  cursor.close()
  context = dict(seepokedata = items)
  return render_template("index.html", **context)

@app.route('/seeinfouid', methods=['POST'])
def seeinfouid():
  iden = request.form['seeuid']
  items = []
  cursor = g.conn.execute("SELECT * FROM player WHERE uid=(%s)", iden)
  first_item = dict (uid="User ID", ulevel="Level", gender="Gender", bid="Bag ID", regionname="Region Name", teamname="Team Name")
  items.append(first_item)
  for result in cursor:
    an_item = dict(uid=result[0], ulevel=result[1], gender=result[2], bid=result[3], regionname=result[4], teamname=result[5])
    items.append(an_item)
  cursor.close()
  context = dict(seeinfodata = items)  
  return render_template("index.html", **context)

@app.route('/seepokename', methods=['POST'])
def seepokename():
  iden = request.form['seepokename']
  items = []
  cursor = g.conn.execute("SELECT distinct familyname FROM pokemon where pname=(%s)", iden)
  for result in cursor:
    items.append(result[0])
  cursor.close()
  context = dict(seefamilydata = items)
  return render_template("index.html", **context)

@app.route('/seefamily', methods=['POST'])
def seefamily():
  iden = request.form['seefamily']
  items = []
  cursor = g.conn.execute("SELECT distinct pname FROM pokemon where familyname=(%s)", iden)
  for result in cursor:
    items.append(result[0])
  cursor.close()
  context = dict(seethisfamilydata = items)
  return render_template("index.html", **context)

@app.route('/seeregion', methods=['POST'])
def seeregion():
  iden = request.form['seeregion']
  items = []
  cursor = g.conn.execute("SELECT * FROM player where regionname=(%s)", iden)
  first_item = dict (uid="User ID", ulevel="Level", gender="Gender", bid="Bag ID", regionname="Region Name", teamname="Team Name")
  items.append(first_item)
  for result in cursor:
    an_item = dict(uid=result[0], ulevel=result[1], gender=result[2], bid=result[3], regionname=result[4], teamname=result[5])
    items.append(an_item)
  cursor.close()
  context = dict(seeapirdata = items)
  return render_template("index.html", **context)

@app.route('/seeteam', methods=['POST'])
def seeteam():
  iden = request.form['seeteam']
  items = []
  cursor = g.conn.execute("SELECT * FROM player where teamname=(%s)", iden)
  first_item = dict (uid="User ID", ulevel="Level", gender="Gender", bid="Bag ID", regionname="Region Name", teamname="Team Name")
  items.append(first_item)
  for result in cursor:
    an_item = dict(uid=result[0], ulevel=result[1], gender=result[2], bid=result[3], regionname=result[4], teamname=result[5])
    items.append(an_item)
  cursor.close()
  context = dict(seeapitdata = items)
  return render_template("index.html", **context)

@app.route('/modify', methods=['POST'])
def modify():
  try:
    pid = int(request.form['pidmodify'])
  except ValueError:
    return redirect('/')
  try:
    plevel = int(request.form['plevelmodify'])
  except ValueError:
    return redirect('/')
  familyname = request.form['familynamemodify']
  pname = request.form['pnamemodify']
  try:
    uid = int(request.form['uidmodify'])
  except ValueError:
    return redirect('/')
  g.conn.execute("UPDATE pokemon SET plevel=(%s), familyname=(%s), pname=(%s), uid=(%s) WHERE pid=(%s)", (plevel, familyname, pname, uid, pid))
  return redirect('/')


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
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
