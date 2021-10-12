from dotenv import load_dotenv
import os
from os import environ as env
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

load_dotenv()
database_name = env['Production_Database']
host_path = env['Host_Path']
username = env['DB_User']
password = env['DB_Password']

database_path = "postgres://" + username + ":" + password + "@{}/{}".format(host_path, database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = 'JustAKey'
    app.config['SESSION_TYPE'] = 'filesystem'
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Game
'''
class Game(db.Model):
    __tablename__ = 'games'

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    title = Column(db.String, nullable=False)
    type = Column(db.String)
    genre = Column(db.String, nullable=False)
    category = Column(db.String)
    description = Column(db.String)

    def __init__(self, title, type, genre, category, description):
        self.title = title
        self.type = type
        self.genre = genre
        self.category = category
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'genre': self.genre,
            'category': self.category,
            'description': self.description
        }

'''
Review
'''
class Review(db.Model):
    __tablename__ = 'reviews'

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = Column(db.Integer, db.ForeignKey(Game.id), nullable=False) #Game ID to reference the game in games table.
    rating = Column(db.Integer)
    reviewer = Column(db.String)
    review = Column(db.String)

    def __init__(self, game_id, rating, reviewer, review):
        self.game_id = game_id
        self.rating = rating
        self.reviewer = reviewer
        self.review = review

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'rating': self.rating,
            'reviewer': self.reviewer,
            'review': self.review
        }
