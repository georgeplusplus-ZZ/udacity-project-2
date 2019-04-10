#George Haralampopoulos 2019

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog.database_setup import Category, Base, Attraction, User

def add_sample_data():
            
      engine = create_engine('sqlite:///nycattractions.db')
      # Bind the engine to the metadata of the Base class so that the
      # declaratives can be accessed through a DBSession instance
      Base.metadata.bind = engine

      DBSession = sessionmaker(bind=engine)
      # A DBSession() instance establishes all conversations with the database
      # and represents a "staging zone" for all the objects loaded into the
      # database session object. Any change made against the objects in the
      # session won't be persisted into the database until you call
      # session.commit(). If you're not happy about the changes, you can
      # revert all of them back to the last commit by calling
      # session.rollback()
      session = DBSession()

      User1 = User(name="GH", email="robogeorge@udacity.com",
                   picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')

      session.add(User1)
      session.commit()

      # Menu for UrbanBurger
      museums = Category(name="museums")
      session.add(museums)
      session.commit()

      museum1 = Attraction(user_id=1, name="Museum of the Moving Image", 
                                     description="Boutique museum located in Queens that features appreciation of\
                                                  art, history, and technique of film, television, and digital media.", 
                                     image="motmi.jpg",
                                     category=museums)
      session.add(museum1)
      session.commit()

      restaurants = Category(name="restaurants")
      session.add(restaurants)
      session.commit()

      restaurant1 = Attraction(user_id=1, name="Toms Restaurant", 
                                     description="Famous Deli in Manhattan that was repeatidly fetaured in the 90's hit \
                                                  comedy television show Seinfeld, features iconic New York City deli items\
                                                  such as Pastrami sandwich and matza ball soup.", 
                                     image="seinfeld.jpg",
                                     category=restaurants)

      session.add(restaurant1)
      session.commit()

      nightlife = Category(name="nightlife")
      session.add(nightlife)
      session.commit()

      nightlife1 = Attraction(user_id=1, name="Broadway Times Square", 
                                     description="A collection of 41 professional theatres that feature showings of musicals and plays.", 
                                     image="broadway.jpg",
                                     category=nightlife)
      session.add(nightlife1)
      session.commit()

      parks = Category(name="parks")
      session.add(parks)
      session.commit()

      parks1 = Attraction(user_id=1, name="Astoria Park", 
                                     description="A park on the east river in Queens which features iconic views of the NYC skyline\
                                     and famous landmark bridges. It also houses one of the largest pool in the world which were \
                                     constructed during the 1964 olympics and used for the tryouts.", 
                                     image="astoriapark.jpg",
                                     category=parks)
      session.add(parks1)
      session.commit()

      monuments = Category(name="monuments")
      session.add(monuments)
      session.commit()

      monuments1 = Attraction(user_id=1, name="Empire State Building", 
                                     description="The most famous of all buildings in the NYC skyline. Tours are available year round for \
                                     views of the Top Deck.", 
                                     image="empirestate.jpg",
                                     category=monuments)
      session.add(monuments1)
      session.commit()


      print "Initialized database!"
