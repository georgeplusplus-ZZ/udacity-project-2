#George Haralampopoulos 2019

from sqlalchemy import create_engine
from catalog.database_setup import Base

from catalog.sample_data import add_sample_data

	
if __name__ == '__main__':
	engine = create_engine('sqlite:///nycattractions.db')
	Base.metadata.create_all(engine)
	add_sample_data()