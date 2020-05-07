from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

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


@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form["inputPseudo"]
        password = request.form["inputPassword"]
        email = request.form["inputEmail"]
        
        usr = User(username, password, email)
        db.session.add(usr)
        db.session.commit() #Use everytime you make a change into your db
        return redirect(url_for("/signin"))
    else:
        return render_template("signup.html")




if __name__ == "__main__":
    app.run(debug=True)
    db.create_all() #ORM initialisation.