import os
from sqlalchemy import Column, String, create_engine, DateTime, Date, Integer, cast
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()



actor_movie = db.Table("Actor_Movie",
    db.Column('actor_id', db.Integer, db.ForeignKey('Actor.id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('Movie.id'))
)

'''
Actor
'''
class Actor(db.Model):  
  __tablename__ = 'Actor'

  id = Column(db.Integer, primary_key=True)
  first_name = Column(String)
  last_name = Column(String)
  gender = Column(String(11))
  date_of_birth = Column(DateTime)
  age = Column(Integer)
  
  db.UniqueConstraint(first_name, last_name, date_of_birth)

  def create(self):
    db.session.add(self)
    db.session.commit()
    return self
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def __init__(self, first_name, last_name, gender, date_of_birth, age):
    self.first_name = first_name
    self.last_name = last_name
    self.gender = gender
    self.date_of_birth = date_of_birth
    self.age = age

  def format(self):
    return {
      'id': self.id,
      'firstName': self.first_name,
      'lastName': self.last_name,
      'gender': self.gender,
      'dateOfBirth': self.date_of_birth,
      'age': self.age
      }

'''
Movie
'''
class Movie(db.Model):  
  __tablename__ = 'Movie'

  id = Column(db.Integer, primary_key=True)
  title = Column(String)
  genre = Column(String)
  rating = Column(String(11))
  release_date= Column(Date)
  cast = db.relationship('Actor', secondary=actor_movie)
  db.UniqueConstraint(title, release_date)

  def create(self):
    db.session.add(self)
    db.session.commit()
    return self
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def __init__(self, title, genre, rating, release_date):
    self.title = title
    self.genre = genre
    self.rating = rating
    self.release_date = release_date

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'genre': self.genre,
      'rating': self.rating,
      'releaseDate': self.release_date,
      'cast': [ actor.first_name + " " + actor.last_name for actor in self.cast]
      }




