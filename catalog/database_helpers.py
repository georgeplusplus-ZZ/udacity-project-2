#George Haralampopoulos 2019

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog import app
from catalog.database_setup import Base

import requests

def connect_to_database():
    """Connects to the database and returns an sqlalchemy session object."""
    engine = create_engine('sqlite:///nycattractions.db')
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session

def token_still_valid(access_token):
	gapi_request = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="
	gapi_request+=access_token
	resp = requests.get(gapi_request)
	if(resp.status_code == 200):
		resp_json = resp.json()
		if resp_json.get("expires_in") > 0:
			return True

	return False