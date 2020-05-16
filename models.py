from flask_sqlalchemy import SQLAlchemy
import datetime
from application import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        
    def __repr__(self):
    		return "<user({},{},{},{})>".format(self.id, self.username, self.password, self.email)   


class Favorite(db.Model):
    __tablename__ = "favorite"
    id = db.Column(db.Integer, primary_key=True)
    masterpiece_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    
    def __init__(self, user_id, masterpiece_id):
        self.masterpiece_id = masterpiece_id
        self.user_id = user_id
        
    def __repr__(self):
        		return "<favorite({},{},{})>".format(self.id, self.masterpiece_id, self.user_id)    


class Comment(db.Model):
    __tablename__ = "Comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    masterpiece_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    
    def __init__(self, content, date, masterpiece_id, user_id):
        self.content = content
        self.date = date
        self.masterpiece_id
        self.user_id = user_id
        
    def __repr__(self):
    		return "<comment({},{},{},{},{})>".format(self.id, self.content, self.date, self.masterpiece_id, self.user_id)


class History(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    masterpiece_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    
    def __init__(self, date, masterpiece_id, user_id):
        self.date = date
        self.masterpiece_id = masterpiece_id
        self.user_id = user_id
        
    def __repr__(self):
        return "<history({},{},{},{})>".format(self.id, self.date, self.masterpiece_id, self.user_id)    
        