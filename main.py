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

@app.route("/favoris")
def favorites():
    return render_template("favorites.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    
    if request.method == "POST":
        email = request.form["inputEmail"]
        username = request.form["inputUsername"]
        password = request.form["inputPassword"]
        
        if db.session.query(User).filter(User.username==username).first() or db.session.query(User).filter(User.email==email).first():
            return jsonify('user already exists')
        
        else:
            db.session.add(User(username, sha256_crypt.encrypt(password), email))
            db.session.commit() #Use everytime you make a change into your db.
            return redirect(url_for("signin"))
        
    else:
        return render_template("signup.html")


@app.route("/signin", methods=["POST", "GET"])
def signin():
    
    if request.method == "POST":
        email = request.form['inputEmail']
        password = request.form['inputPassword']

        usr = db.session.query(User).filter(User.email==email).first()
        
        if usr and sha256_crypt.verify(password, usr.password):
            return jsonify({'message': 'Password is correct'}) 
        
        else:
            return jsonify({'error': 'User or password are incorrect'})

    else:
        return render_template("signin.html")




if __name__ == "__main__":
    app.run(debug=True)
    db.create_all() #DB création with ORM and models.