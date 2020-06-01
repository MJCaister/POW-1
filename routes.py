from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
import sqlite3
from forms import SearchForm

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///POW_Project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ajaj'

db = SQLAlchemy(app)

import models

def countpows():
    count = models.Prisoner.query.filter().count()
    return count

#add function to easily get unit, rank and capture for pows

@app.route('/')
def home():
    count = countpows()
    return render_template("home.html",number=count)

@app.route('/about')
def about():
    count = countpows()
    return render_template("about.html", number=count)

#@app.route('/records')
#def search():
#    return render_template("records.html")

# Return a search result from the form shown on every page (page_title.html)
@app.route('/records', methods=['POST'])
def search():
    form = SearchForm()
    results = models.Prisoner.query.filter(models.Prisoner.surname.ilike('%{}%'.format(form.query.data))).all()
    return render_template('records.html', title='Search', results=results, query=form.query.data)

@app.route('/browse')
def browse():
    #pows = models.Prisoner.query.all()
    return render_template("browse.html")

@app.route('/pow/<int:val>')
def pow(val):
    pow = models.Prisoner.query.filter_by(id=val).first_or_404()
    unit = "test"
    surname = pow.surname
    rank = models.Rank.query.filter_by(id=pow.rank).first()
    capture = models.Capture.query.filter_by(id=pow.capture).first()
    if capture.date == "Greece":
        inor = "in"
    elif capture.date == "Crete":
        inor = "in"
    elif capture.date == "Greece/Crete":
        inor = "in"
    else:
        inor = "on"
    #unit = models.Unit.query.join(PrisonerUnit).join(Prisoner).filter((PrisonerUnit.c.pid == Prisoner.id) & (PrisonerUnit.c.uid == Unit.id)).all()
    #units = models..query().all()
    #for unit in units:
    #    for un in unit.Unit
    return render_template("prisoner.html", val=val, prisoner=pow, page_title=surname, rank=rank, capture=capture, inor=inor, unit=unit)

@app.route('/results/<val>')
def results(val):
    #will have to add try except for search use
    pows = models.Prisoner.query.filter(models.Prisoner.surname.ilike('{}%'.format(val))).all()
    #For better display of results I split the results over 3 tables. For resizing purposes it also returns all results incase screen size is too small for 3 table display
    pows1 = pows[::3]
    pows2 = pows[1::3]
    pows3 = pows[2::3]
    return render_template("results.html",val=val, prisoners1=pows1, prisoners2=pows2, prisoners3=pows3)

# inject search form (flask-wtf) into all pages
@app.context_processor
def inject_search():
    searchform = SearchForm()
    return dict(searchform=searchform)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(debug=True)
