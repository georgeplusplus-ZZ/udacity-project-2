from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import flash
from flask import abort
from flask import session as login_session

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Attraction

import os
import random
import string

# Globals
app = Flask(__name__, static_url_path='/static')

engine = create_engine('sqlite:///nycattractions.db', connect_args={'check_same_thread':False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind= engine)
session = DBSession()

@app.route('/')
@app.route('/home')
def homepageContent():
	items = session.query(Attraction).order_by(Attraction.created_at).limit(5).all()
	return render_template('home.html', items= items)

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/view/<string:attraction_type>')
def attractionContent(attraction_type):
	attractions = session.query(Attraction).filter(Attraction.category.has(name= attraction_type.lower())).all()
	if not len(attractions):
		abort(404)
	return render_template('attractions.html', attractions= attractions)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)