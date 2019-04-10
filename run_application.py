#George Haralampopoulos 2019

from catalog import app

import argparse


def parse_args():
	parser = argparse.ArgumentParser(description='Runtime for Explore NYC Flask Web Application.')
	parser.add_argument('--gapi_id', required=True, 
									  help=' Enter the full path of your client id provided \
									  by Google API. Example: \
									  <your-client-id-here>.apps.googleusercontent.com')
	parser.add_argument('--debug', action='store_true')
	args = parser.parse_args()
	return args

if __name__ == '__main__':

	args = parse_args()

	app.config['DATABASE_URL'] = 'sqlite:///nycattractions.db'
	app.config['UPLOAD_FOLDER'] = '/vagrant/catalog/catalog/static'
	app.config['OAUTH_SECRETS_LOCATION'] = '' # default location
	app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg'])
	app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 # 1MB
	app.config['GAPI_CLIENT_ID'] = args.gapi_id
	app.secret_key = 'super_secret_key' 
	if args.debug:
		app.debug = True
	app.run(host='0.0.0.0', port=5000)
