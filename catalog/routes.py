#George Haralampopoulos 2019
#Main routes to display and change content

from werkzeug.utils import secure_filename

from sqlalchemy.orm.exc import NoResultFound

from flask import render_template
from flask import url_for
from flask import jsonify
from flask import abort
from flask import session as login_session
from flask import flash
from flask import redirect
from flask import request

from catalog import app
from catalog.database_setup import Category, Attraction, User
from catalog.database_helpers import connect_to_database
from catalog.database_helpers import token_still_valid
from catalog.auth import get_user_id

import os
import random
import string


@app.route('/')
@app.route('/home')
def homepage():
	session = connect_to_database()
	items = session.query(Attraction).order_by(Attraction.created_at).limit(5).all()
	session.close()
	return render_template('home.html', items= items)

@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/view/<string:attraction_type>')
def categoryContent(attraction_type):
	session = connect_to_database()
	attractions = session.query(Attraction).filter(Attraction.category.has(name= attraction_type.lower())).all()
	if not attractions:
		session.close()
		abort(404)
	session.close()
	return render_template('attractions.html', attractions= attractions, category_type=attraction_type)

@app.route('/user/<string:user_name>')
def profileContent(user_name):
	if not login_session.get('username'):
		flash("You must log in to view this content." , "info")
		return redirect(url_for('homepage'))
	if not token_still_valid(login_session.get('access_token')):
		# clear session since session is no longer active
		login_session.clear()
		flash("Login expired. Please login again to view your content." , "info")
		return redirect(url_for('homepage'))
	if user_name != login_session['username']:
		flash("This is not your login screen!" , "error")
		return redirect(url_for('homepage'))
	
	session = connect_to_database()
	user_id = get_user_id(login_session['email'])
	attractions = session.query(Attraction).filter_by(user_id= user_id).all()
	session.close()
	category_type = ''
	if attractions:
		category_type = get_category_type(attractions[0])
	return render_template('attractions.html', attractions= attractions, category_type=category_type)

@app.route('/view/<string:attraction_type>/<int:attraction_id>')
def attractionContent(attraction_type, attraction_id):
	session = connect_to_database()
	attraction = session.query(Attraction).filter_by(id=attraction_id).one()
	if not attraction:
		session.close()
		abort(404)
	content_creator = session.query(User).filter_by(id=attraction.user_id).one()
	session.close()

	if content_creator.id == get_user_id(login_session.get('email')):
		return render_template('content.html', content=attraction, content_creator=content_creator, category=attraction_type)

	return render_template('publiccontent.html', content=attraction, content_creator=content_creator)

# Delete an attraction item
@app.route('/view/<string:attraction_type>/<int:attraction_id>/delete', methods=['POST'])
def deleteContent(attraction_type, attraction_id):
    if not login_session.get('username'):
    	flash("Must be logged in to do that", "error")
        return redirect(url_for('homepage'))

    session = connect_to_database()
    itemToDelete = session.query(Attraction).filter_by(id=attraction_id).one()
    session.close()
    if login_session['user_id'] != itemToDelete.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete this item to this category. Please create your own attraction in order to delete items.');}</script><body onload='myFunction()''>"
    
    session.delete(itemToDelete)
    session.commit()
    flash(('Menu Item "%s" Successfully Deleted') % itemToDelete.name, "success")
    return redirect(url_for('homepage'))

@app.route('/view/<string:user_name>/<int:attraction_id>/edit', methods=['POST'])
def editContent(user_name, attraction_id):
	if not login_session.get('username'):
		flash("Must be logged in to do that", "error")
		return redirect(url_for('homepage'))
	if user_name != login_session['username']:
		flash("This is not your login screen!" , "error")
		return redirect(url_for('homepage'))

	session = connect_to_database()
	editedAttraction = session.query(Attraction).filter_by(id=attraction_id).one()
	edited = False
	if request.form['name']:
		edited = True
		editedAttraction.name = request.form['name']
	if request.form['description']:
		edited = True
		editedAttraction.description = request.form['description']
	session.commit()
	session.close()

	if edited:
		flash(('Successfully Edited to %s' % request.form['name']), "success")
		return redirect(url_for('profileContent', user_name=user_name))

	flash("Form was not edited successfully, try again if you believe this is in error", "info")
	return redirect(url_for('profileContent', user_name=user_name))

@app.route('/user/<string:user_name>/add', methods=['GET', 'POST'])
def addContent(user_name):
	if request.method == 'GET':
		if not login_session.get('username'):
			flash("You must log in to view this content." , "info")
			return redirect(url_for('homepage'))
		if not token_still_valid(login_session.get('access_token')):
			# clear session since session is no longer active
			login_session.clear()
			flash("Login expired. Please login again to view your content." , "info")
			return redirect(url_for('homepage'))
		if user_name != login_session['username']:
			flash("This is not your login screen!" , "error")
			return redirect(url_for('homepage'))

		session = connect_to_database()
		user = session.query(User).filter_by(id=login_session.get('user_id')).one()
		session.close()
		allowed_formats = ',. '.join(app.config['ALLOWED_EXTENSIONS'])
		return render_template('add.html', user=user, allowed_formats=allowed_formats)

	elif request.method == 'POST':

		validForm = True
		# Check form for errors.
		if 'picture' not in request.files:
			flash('An image is required for uploading an attraction.', "error")
			validForm = False
		if not request.form['name']:
			flash('Missing Name field. You must give your attraction a Name.', "error")
			validForm = False
		if not request.form['description']:
			flash('Missing Description field. You must give your attraction a Description.', "error")
			validForm = False

		if not validForm:
			return redirect(url_for('addContent', user_name=user_name))

		file = request.files['picture']

		# Need to add handling for same file names.
		if file.filename == '':
			flash('Missing file name. You must have a name for your file.', "error")

		session = connect_to_database()
		user = session.query(User).filter_by(id=login_session.get('user_id')).one()

		try:
			newItem = Attraction(name=request.form['name'], 
								 category_id=get_category_id(request.form['category'].lower()), 
								 description=request.form['description'], 
								 user_id=user.id,
								 image= file.filename)
		except ValueError as e:
			flash('Failed to add content: %s ' % e.message, "error")
			return redirect(url_for('addContent', user_name=user_name))

		session.add(newItem)
		session.commit()
		session.close()
		flash(('Successfully Added %s' % request.form['name']), "success")
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return redirect(url_for('addContent', user_name=user_name))
	else:
		abort(404)

# Handler for 404 response
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Helper functions
def get_category_type(attraction):
	return attraction.category.name

def get_category_id(category_type):
	session = connect_to_database()
	try:
		category = session.query(Category).filter_by(name=category_type).one()
		session.close()
		return category.id
	except NoResultFound:
		session.close()
		raise ValueError('Could not find the category type %s!' % category_type)
