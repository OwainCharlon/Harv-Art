from flask_sqlalchemy import SQLAlchemy
import datetime

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        
    #def __repr__(self):
     #   return "<Chronic_diseases(pathology_id=%s, is_chronic=%d)>" % (
        #    self.pathology_id, self.is_chronic)
        
class Favorite(db.Model):
    __tablename__ = "Favorite"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    masterpiece_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
    
    def __init__(self, masterpiece_id, date, user_id):
        self.masterpiece_id = masterpiece_id
        self.date = date
        self.user_id = user_id
        

class History(db.Model):
    __tablename__ = "History"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    masterpiece_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
    
    def __init__(self, masterpiece_id, date, user_id):
        self.masterpiece_id = masterpiece_id
        self.date = date
        self.user_id = user_id
        
        
class Comment(db.Model):
    __tablename__ = "Comment"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    masterpiece_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
    
    def __init__(self, content, masterpiece_id, date, user_id):
        self.content = content
        self.masterpiece_id = masterpiece_id
        self.date = date
        self.user_id = user_id
