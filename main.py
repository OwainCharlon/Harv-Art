from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

from passlib.hash import sha256_crypt  # Use for password hashing

from models import db
from application import app
from models import *

import urllib3
import json
import pymysql

http = urllib3.PoolManager()
db.init_app(app)


@app.route("/", methods=["POST", "GET"])
def homepage():
    if request.method == "POST":
        email = request.form['inputEmail']
        password = request.form['inputPassword']

        usr = db.session.query(User).filter(User.email == email).first()

        if usr and sha256_crypt.verify(password, usr.password):
            session['userId'] = usr.id
            return redirect(url_for("homepage"))
        else:
            flash(f"Password or email adress are incorrect.", "info")

    return render_template("index.html")


@app.route("/logout")
def logout():
    # Delete the userId of the current user session
    session.pop("userId", None)

    return redirect(url_for("homepage"))


@app.route("/signup", methods=["POST", "GET"])
def signup():

    if request.method == "POST":
        email = request.form["inputEmail"]
        username = request.form["inputUsername"]
        password = request.form["inputPassword"]

        if db.session.query(User).filter(User.username == username).first() or db.session.query(User).filter(User.email == email).first():
            flash(f"This username or email adress is already used.",
                  "info")  # message must be display in the render

        else:
            db.session.add(
                User(username, sha256_crypt.encrypt(password), email))
            # Use everytime you make a change into your db.
            db.session.commit()
            flash(f"Account created with success.", "info")
            return redirect(url_for("homepage"))

    return render_template("signup.html")


@app.route("/favorites")
def favorites():
    favorites = db.session.query(Favorite).filter(
        User.id == session["userId"]).all()

    return render_template("favorites.html", favorites=favorites)

@app.route("/history")
def history():
    history = db.session.query(History).filter(
        User.id == session["userId"]).all()

    return render_template("history.html", history=history)

@app.route("/addContent/<contentType>/<actualmasterpieceId>")
@app.route("/addContent/<contentType>/<actualmasterpieceId>/<commentContent>")
def addContent(contentType, actualmasterpieceId, commentContent=None):

    if session['userId']:
        
        isExisting = {
            1: """db.session.query(Favorite).filter(Favorite.masterpiece_id == {masterpieceId}).filter(Favorite.user_id == session['userId']).first()""",
            2: """db.session.query(History).filter(History.masterpiece_id == {masterpieceId}).filter(History.user_id == session['userId']).first()""",
            3: """None"""
        }

        if eval(isExisting[int(contentType)].format(masterpieceId=int(actualmasterpieceId))) is None:
            if request.args.get("commentContent"):
                commentContent = request.args.get("commentContent")
        
            requests = {
                1: """db.session.add(Favorite({masterpieceId}, session['userId']))""",
                2: """db.session.add(History(datetime.datetime.today().strftime('%Y-%m-%d'),{masterpieceId}, session['userId']))""",
                3: """db.session.add(Comment("{content}", datetime.datetime.today().strftime('%Y-%m-%d'), {masterpieceId}, session['userId']))""",
            }
            eval(requests[int(contentType)].format(content=str(commentContent), masterpieceId=int(actualmasterpieceId)))
            db.session.commit()
    else:
        pass

    return jsonify("Content well updated.")


@app.route("/deleteContent/<contentType>/<contentId>")
def deleteContent(contentType, contentId):

    requests = {
        1: "db.session.query(User).filter(User.id=={}).delete()",
        2: "db.session.query(Favorite).filter(Favorite.masterpiece_id=={}).delete()",
        3: "db.session.query(History).filter(History.id=={}).delete()",
        4: "db.session.query(Comment).filter(Comment.id=={}).delete()",
    }
    eval(requests[int(contentType)].format(int(contentId)))
    db.session.commit()

    return jsonify("Content well updated.")


@app.route("/getComments/<masterpieceId>") 
def getComments(masterpieceId):

    comments = db.session.query(Comment, User.username).join(
        User, Comment.user_id == User.id).filter(Comment.masterpiece_id == masterpieceId).all()
    if comments:
        commentArray = [str(comment[0].content) + '@@' + str(comment[0].date) + '@@' + str(comment[1]) for comment in comments]
    else:
        commentArray = ["Aucun commentaire" + '@@' + "" + '@@' + ""]
    return jsonify(commentArray)


@app.route("/isFavorite/<masterpieceId>")
def isFavorite(masterpieceId):
    
    isFavorite = "Not in favorite" if db.session.query(Favorite).filter(Favorite.masterpiece_id == masterpieceId).filter(Favorite.user_id == session['userId']).first() is None else "In favorite"
    return jsonify(isFavorite)

@app.route("/admin")
def admin():

    users = db.session.query(User).all()
    comments = db.session.query(Comment).all()

    return render_template("admin.html", users=users, comments=comments)


def fetch_all(ressource):
    tab = []
    page = 0
    pages = 1
    while(page <= pages):
        page += 1
        response = http.request('GET', 'https://api.harvardartmuseums.org/'+ressource,
                                fields={
                                    'apikey': 'b6782a10-8def-11ea-877a-6df674fda82b',
                                    'sort': 'name',
                                    'page': page,
                                    'size': 100
                                })
        content = json.loads(response.data)
        pages = content['info']['pages']
        for record in content['records']:
            tab.append([record['id'], record['name']])
    return tab


@app.route('/search')
def search():
    forms_data = []
    forms_data.append(['culture', fetch_all('culture')])
    forms_data.append(['century', fetch_all('century')])
    forms_data.append(['period', fetch_all('period')])
    forms_data.append(['technique', fetch_all('technique')])
    forms_data.append(['worktype', fetch_all('worktype')])
    return render_template('choose.html', forms_data=forms_data)


@app.route("/customfetch", methods=['POST'])
def customfetch():
    culture = request.form.get('culture')
    century = request.form.get('century')
    period = request.form.get('period')
    technique = request.form.get('technique')
    worktype = request.form.get('worktype')
    keyword = request.form.get('keyword')
    fields = {
        'apikey': 'b6782a10-8def-11ea-877a-6df674fda82b',
        'hasimage': 1,
        'size': 10
    }
    if culture:
        fields['culture'] = culture
    if century:
        fields['century'] = century
    if period:
        fields['period'] = period
    if technique:
        fields['technique'] = technique
    if worktype:
        fields['worktype'] = worktype
    if keyword:
        fields['keyword'] = keyword
    session['fields'] = fields
    response = http.request(
        'GET', 'https://api.harvardartmuseums.org/object', fields)
    content = json.loads(response.data)
    return render_template('art.html', content=content)


@app.route("/page", methods=['POST'])
def page():
    fields = session['fields']
    fields['page'] = request.form.get('page')
    response = http.request(
        'GET', 'https://api.harvardartmuseums.org/object', fields)
    content = json.loads(response.data)
    return render_template('art.html', content=content)

@app.route("/test")
def test():
    alreadyExists = {
            1: """db.session.query(Favorite).filter(Favorite.masterpiece_id == 229759 ).filter(Favorite.user_id == session['userId']).first()""",
            2: """db.session.query(History).filter(History.id == ).first()""",
            3: """None"""
        }
        
    isExisting = eval(alreadyExists[3])
        
    return render_template('test.html', isExisting=isExisting)
    
if __name__ == "__main__":
    app.run(debug=True)
