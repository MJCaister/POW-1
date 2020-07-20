from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from config import Config
import sqlite3
from forms import SearchForm, LoginForm, RegistrationForm, CommentForm, DeleteForm
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
    form = SearchForm()
    return render_template("browse.html", searchform=form)

#login page
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

# register account page
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

#logout page. redirects to home
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

#Induvidual POW info page, catches dynamic url only if int since I'm using ids for links
@app.route('/pow/<int:val>', methods=['GET', 'POST'])
def pow(val):
    form = CommentForm()
    deleteform = DeleteForm()
    if form.validate_on_submit() and form.comment.data:
        comment = models.Comment(comment=form.comment.data ,userid=current_user.id, powid=val)
        db.session.add(comment)
        db.session.commit()
    #elif deleteform.validate_on_submit():
    #    return redirect('/about')
    comments = models.Comment.query.filter(models.Comment.powid==val).all()
    pow = models.Prisoner.query.filter_by(id=val).first_or_404()
    surname = pow.surname
    capture = pow.Capture
    firstnames = pow.first_names
    if firstnames == None:
        firstnames = pow.initial
    count = models.Prisoner.query.filter(models.Prisoner.capture==capture.id).count()
    #grammar for prisoner page
    if isinstance(capture.date, str) == True:
        inor = "on"
        sent = "on this date"
    else:
        inor = "in"
        sent = "at this location"
    return render_template("prisoner.html", val=val, prisoner=pow, first_names = firstnames, inor=inor, sent=sent, count=count, form=form, comments=comments)

@app.route('/delete/<int:user>/<int:com>')
def delcomment(user, com):
    if current_user.is_authenticated and current_user.id == user:
        pow = models.Comment.query.filter(models.Comment.id==com).first_or_404()
        comment = db.session.query(models.Comment).filter(models.Comment.id==com).first_or_404()
        db.session.delete(comment)
        db.session.commit()
        return redirect('/pow/{}'.format(pow.powid))
    else:
        abort(404)

@app.route('/rank/<int:val>')
def displayranks(val):
    pows = models.Prisoner.query.filter(models.Prisoner.rank==val).all()
    rank = models.Rank.query.filter(models.Rank.id==val).first_or_404()
    pows1 = pows[::3]
    pows2 = pows[1::3]
    pows3 = pows[2::3]
    return render_template('results.html', results1=pows1, results2=pows2, results3=pows3, val=rank.name)


#Browse Prisoners by Capture Date/location
@app.route('/capture/<int:val>')
def displaycaptures(val):
    pows = models.Prisoner.query.filter(models.Prisoner.capture==val).all()
    capture = models.Capture.query.filter(models.Capture.id==val).first_or_404()
    pows1 = pows[::3]
    pows2 = pows[1::3]
    pows3 = pows[2::3]
    return render_template('results.html', results1=pows1, results2=pows2, results3=pows3, val=capture.date)

#Browse Prisoners by Each Unit
@app.route('/unit/<int:val>/')
def unitpows(val):
    prisoners = models.PrisonerUnit.query.filter(models.PrisonerUnit.uid==val).all()
    print(prisoners)
    pows = []
    for x in prisoners:
        pows.append(x.prisoner)
    r1 = pows[::3]
    r2 = pows[1::3]
    r3 = pows[2::3]
    return render_template("results.html", val="All Units", results1=r1, results2=r2, results3=r3)

@app.route('/unit/<int:val1>/<int:val2>/')
def unitspows(val1, val2):
    p1 = models.PrisonerUnit.query.filter(models.PrisonerUnit.id==val1).all()
    p2 = models.PrisonerUnit.query.filter(models.PrisonerUnit.id==val2).all()
    pow1 = []
    pow2 = []
    for x in p1:
        pow1.append(x.prisoner)
    for y in p2:
        pow1.append(y.prisoner)
    print(pow1)
    pows = []
    for prisoner in pow1:
        if prisoner in pow2:
            pows.append(prisoner)
    r1 = pows[::3]
    r2 = pows[1::3]
    r3 = pows[2::3]
    return render_template("results.html", val="two unit", results1=r1, results2=r2, results3=r3)

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

#404 error handler with custom styled page.
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(debug=True)
