from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

from passlib.hash import sha256_crypt #Use for password hashing

from models import db
from application import app
from models import *


db.init_app(app)

@app.route("/", methods=["POST", "GET"])
def homepage():
    if request.method == "POST":
        email = request.form['inputEmail']
        password = request.form['inputPassword']

        usr = db.session.query(User).filter(User.email==email).first()
        
        if usr and sha256_crypt.verify(password, usr.password):
            session['userId'] = usr.id
            return redirect(url_for("homepage"))
        else:
            flash(f"Password or email adress are incorrect.", "info")
        
    return render_template("index.html")

@app.route("/sessionLogout")
def logout():
    session.pop("userId", None) #Delete the userId of the current user session

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
            return redirect(url_for("homepage"))
        
    return render_template("signup.html")


@app.route("/search")
def search():
    
    return render_template("search.html")


@app.route("/favorites")
def favorites():
    favorites = db.session.query(Favorite).filter(User.id==session["userId"]).all()
    
    return render_template("favorites.html", favorites=favorites)


@app.route("/addContent/<contentType>/<masterpieceId>")
@app.route("/addContent/<contentType>/<masterpieceId>/<commentContent>")
def addContent(contentType, masterpieceId, commentContent=None):
    
    if request.args.get("commentContent"):
        commentContent = request.args.get("commentContent")
        
    requests = {
            1: "db.session.add(Favorite({masterpieceId}, session['userId']))",
            2: "db.session.add(History({masterpieceId}, datetime.datetime.today().strftime('%Y-%m-%d'), session['userId']))",
            3: "db.session.add(Comment({content}, {masterpieceId}, datetime.datetime.today().strftime('%Y-%m-%d'), session['userId']))",#Fucking PROBLEME INVERSION CONTENT ET MASTERPIECE, ALORS QUE MODEL....
        }
    eval(requests[int(contentType)].format(masterpieceId=int(masterpieceId), content=str(commentContent)))
    db.session.commit()
    
    return jsonify("Content well updated.")


@app.route("/deleteContent/<contentType>/<contentId>")
def deleteContent(contentType, contentId):
    
    requests = {
            1: "db.session.query(User).filter(User.id=={}).delete()",
            2: "db.session.query(Favorite).filter(Favorite.id=={}).delete()",
            3: "db.session.query(History).filter(History.id=={}).delete()",
            4: "db.session.query(Comment).filter(Comment.id=={}).delete()",
        }
    eval(requests[int(contentType)].format(contentId))
    db.session.commit()

    return jsonify("Content well updated.")


@app.route("/admin")
def admin():
    
    users = db.session.query(User).all()
    comments = db.session.query(Comment).all()
    
    return render_template("admin.html", users=users, comments=comments)

    
if __name__ == "__main__":
    app.run(debug=True)