import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy import render_er

Base = declarative_base()

# class Person(Base):
#     __tablename__ = 'person'
#     # Here we define columns for the table person
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)

# class Address(Base):
#     __tablename__ = 'address'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     street_name = Column(String(250))
#     street_number = Column(String(250))
#     post_code = Column(String(250), nullable=False)
#     person_id = Column(Integer, ForeignKey('person.id'))
#     person = relationship(Person)

#     def to_dict(self):
#         return {}

class Followers(Base):
    __tablename__ = 'followers'
    follower_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    followed_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    about = Column(String(250), nullable=False)
    phone = Column(Integer, nullable=False)
    email = Column(String(50), nullable=False)

    post = relationship("Post", back_populates="parent")
    comment = relationship("Comment", back_populates="parent")
    followed = relationship("User",
        secondary = Followers,
        primaryjoin = (Followers.follower_id == id),
        secondaryjoin = (Followers.followed_id == id),
        backref = relationship("Followers", backref="parent"),
        lazy = 'dynamic')
    

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    link = Column(String(250), nullable=False)
    description = Column(Text, nullable=False)
    user_id= Column(Integer, ForeignKey("user.id"))

    comment = relationship("Comment", back_populates="parent")
    tag = relationship("Tag", back_populates="parent")

    user = relationship("User", back_populates="children")

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime)

    user = relationship("User", back_populates="children")
    post = relationship("Post", back_populates="children")

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    description = Column(String(250), nullable=False) 

    post = relationship("Post", back_populates="children")

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e