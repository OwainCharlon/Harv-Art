from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy


from passlib.hash import sha256_crypt #Use for password hashing

from models import *
import config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
db = SQLAlchemy()
with app.app_context():
	db.init_app(app)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/search")
def search():
    
    return render_template("search.html")

@app.route("/favorites")
def favorites():
    favorites = db.session.query(Favorite).filter(User.id==session["userId"]).all()
    
    return render_template("favorites.html", favorites=favorites)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    
    if request.method == "POST":
        email = request.form["inputEmail"]
        username = request.form["inputUsername"]
        password = request.form["inputPassword"]
        
        if db.session.query(User).filter(User.username==username).first() or db.session.query(User).filter(User.email==email).first():
            flash(f"This username or email adress is already used.", "info") #message must be display in the render
        
        else:
            db.session.add(User(username, sha256_crypt.encrypt(password), email))
            db.session.commit() #Use everytime you make a change into your db.
            flash(f"Account created with success.", "info")
            return redirect(url_for("signin"))
        
    return render_template("signup.html")


@app.route("/signin", methods=["POST", "GET"])
def signin():
    
    if request.method == "POST":
        email = request.form['inputEmail']
        password = request.form['inputPassword']

        usr = db.session.query(User).filter(User.email==email).first()
        
        if usr and sha256_crypt.verify(password, usr.password):
            session["userId"] = usr.id
            return redirect(url_for("homepage"))
        else:
            flash(f"Password or email adress are incorrect.", "info")

    return render_template("signin.html")


@app.route("/addFavorite/<masterpieceId>")
def addFavorite(masterpieceId):
    db.session.add(Favorite(masterpieceId, session["userId"]))
    db.session.commit()
    
    return jsonify("Added to your favorits.")

@app.route("/addHistory/<masterpieceId>")
def addHistory(masterpieceId):
    db.session.add(History(masterpieceId, datetime.datetime.today().strftime('%Y-%m-%d'), session["userId"]))
    db.session.commit()
    
    return jsonify("Added to your history.")

@app.route("/addComment/<content>/<masterpieceId>")
def addComment(content,masterpieceId):
    db.session.add(Comment(content, masterpieceId, datetime.datetime.today().strftime('%Y-%m-%d'), session["userId"]))
    db.session.commit()
    
    return jsonify("Comment well created.")

if __name__ == "__main__":
    app.run(debug=True)
    db.create_all() #DB création with ORM and models.