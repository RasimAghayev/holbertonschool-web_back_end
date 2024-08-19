""" 0. User model
"""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

# Initialize the base class for declarative models
Base = declarative_base()


class User(Base):
    """ User class
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)


# Example of creating an engine and creating the table
# engine = create_engine('sqlite:///example.db')
# Base.metadata.create_all(engine)
