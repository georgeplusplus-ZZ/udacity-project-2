#George Haralampopoulos 2019
#sets up database for our nyc attraction application using sqlalchemy

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.dialects.mysql import FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import sys
import datetime

Base = declarative_base()

def get_date():
	"""Helper function to populate datetime field for a table"""
	return datetime.datetime.now()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    picture = Column(String(250))


class Category(Base):
	__tablename__ = 'category'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)


class Attraction(Base):
	__tablename__ = 'Attraction'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	image = Column(String(250))
	description = Column(String(250))
	created_at = Column(Date, default=get_date())
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship(User)
    