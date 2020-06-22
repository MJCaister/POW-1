from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from config import Config
import sqlite3
from forms import SearchForm, LoginForm, RegistrationForm, CommentForm
import models

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///POW_Project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ajaj'

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(id):
    return models.User.query.get(int(id))

def countpows():
    count = models.Prisoner.query.filter().count()
    return count

#Home page route. Returns count info for the about page snippet
@app.route('/')
def home():
    count = countpows()
    return render_template("home.html",number=count)


#About Page route, also returns count for the about page data.
@app.route('/about')
def about():
    count = countpows()
    return render_template("about.html", number=count)


# Return a search result from the form shown on every page (page_title.html)
@app.route('/records', methods=['POST'])
def search():
    form = SearchForm()
    results = models.Prisoner.query.filter(models.Prisoner.surname.ilike('%{}%'.format(form.query.data))).all()
    if len(results) == 0:
        return render_template("results.html", val=form.query.data, results="No results.")
    else:
        #To achieve the 3 Coloums split of data, results are split through 3 lists
        results1 = results[::3]
        results2 = results[1::3]
        results3 = results[2::3]
        return render_template('results.html', title='Search Results', val=form.query.data, results1=results1, results2=results2, results3=results3)

#Set browse page
@app.route('/browse')
def browse():
    #pows = models.Prisoner.query.all()
    form = SearchForm()
    return render_template("browse.html", searchform=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

#Induvidual POW info page, catches dynamic url only if int since I'm using ids for links
@app.route('/pow/<int:val>', methods=['GET', 'POST'])
def pow(val):
    form = CommentForm()
    if form.validate_on_submit():
        comment = models.Comment(comment=form.comment.data ,userid=current_user.id, powid=val)
        db.session.add(comment)
        db.session.commit()
    comments = models.Comment.query.filter(models.Comment.powid==val).all()
    pow = models.Prisoner.query.filter_by(id=val).first_or_404()
    surname = pow.surname
    capture = pow.Capture
    count = models.Prisoner.query.filter(models.Prisoner.capture==capture.id).count()
    #grammar for prisoner page
    if isinstance(capture.date, str) == True:
        inor = "on"
        sent = "on this date"
    else:
        inor = "in"
        sent = "at this location"
    return render_template("prisoner.html", val=val, prisoner=pow, page_title=surname, inor=inor, sent=sent, count=count, form=form, comments=comments)

#This is called from the browse by letter part of website
@app.route('/results/<val>')
def results(val):
    #will have to add try except for search use
    pows = models.Prisoner.query.filter(models.Prisoner.surname.ilike('{}%'.format(val))).all()
    if len(pows) == 0:
        return render_template("results.html", val=val, results="No results.")
    else:
        #For better display of results I split the results over 3 tables. For resizing purposes it also returns all results incase screen size is too small for 3 table display
        pows1 = pows[::3]
        pows2 = pows[1::3]
        pows3 = pows[2::3]
        val = val.upper()
        return render_template("results.html",val=val, results1=pows1, results2=pows2, results3=pows3)

@app.route('/unit/<int:val>')
def unitpows(val):
    pris = models.PrisonerUnit.query.filter_by(uid=val).all()
    pows = pris.prisoner.all()
    r1 = pows[::3]
    r2 = pows[1::3]
    r3 = pows[2::3]
    return render_template("results.html", val="All Units", results1=r1, results2=r2, results3=r3)

# inject search form (flask-wtf) into all pages
#@app.context_processor
#def inject_search():
#    searchform = SearchForm()
#    return dict(searchform=searchform)

#404 error handler with custom styled page.
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(debug=True)
