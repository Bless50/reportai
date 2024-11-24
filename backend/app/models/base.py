# import the necessary function from SQLALCHEMY
# declarative_base() is used to create a base class for our database models
from sqlalchemy.ext.declarative import declarative_base

# create a base class for our database models
# this class will be used as a base class for all our database models
#it provides them  with the necessary functionality to work with the sqlachemy
Base = declarative_base()