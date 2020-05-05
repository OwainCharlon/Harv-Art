from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/TechWithTimTutorial'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)
    
    
@app.route("/")
def homepage():
    return "hello this is the homepage."


if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)