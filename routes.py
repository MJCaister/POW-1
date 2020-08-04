from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from config import Config
import sqlite3
from flask_mail import Mail
from myemail import send_password_reset_email, send_update_email
import os

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///POW_Project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ajaj'
app.config['MAIL_SERVER'] = 'smtp.gmail.com' or os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = 587 or int(os.environ.get('MAIL_PORT') or 25)
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '16284@burnside.school.nz' or os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = 'hihi8003' or os.environ.get('MAIL_PASSWORD')
app.config['ADMINS'] = ['16284@burnside.school.nz']

db = SQLAlchemy(app)
mail = Mail(app)
login = LoginManager(app)
login.login_view = 'login'


from forms import SearchForm, LoginForm, RegistrationForm, CommentForm, DeleteForm, ContactForm, PasswordUpdate, EmailUpdate, DelAccountForm, ResetPasswordRequestForm, ResetPasswordForm
import models



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

@app.route('/rank')
def ranks():
    ranks = models.Rank.query.filter().all()
    r1 = ranks[::3]
    r2 = ranks[1::3]
    r3 = ranks[2::3]
    return render_template("ranks.html", ranks=ranks, search="All Ranks", r1=r1, r2=r2, r3=r3)

@app.route('/unit')
def units():
    units = models.Unit.query.filter().all()
    u1 = units[::3]
    u2 = units[1::3]
    u3 = units[2::3]
    return render_template("units.html", search="All Units", u1=u1, u2=u2, u3=u3)

@app.route('/capture')
def capture():
    capture = models.Capture.query.filter().all()
    c1 = capture[::3]
    c2 = capture[1::3]
    c3 = capture[2::3]
    return render_template("capture.html", capture=capture, search="All Capture Dates and Locations", c1=c1, c2=c2, c3=c3)
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
        return redirect('/user/{}'.format(form.username.data))
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


#updates the user's password in the database
@app.route('/update_password', methods=['GET', 'POST'])
@login_required
def updatepass():
    passwordform = PasswordUpdate()
    if passwordform.validate_on_submit():
        if current_user.check_password(passwordform.currentpassword.data):
            user = db.session.query(models.User).filter_by(username=current_user.username).first_or_404()
            user.password_hash = generate_password_hash(passwordform.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Password has been updated!')
            logout_user()
            return redirect(url_for('login'))
    return render_template('updatepass.html', passwordform=passwordform)

@app.route('/update_email', methods=['GET', 'POST'])
@login_required
def updateemail():
    emailform = EmailUpdate()
    if emailform.validate_on_submit():
        if current_user.check_password(emailform.password.data) and current_user.email==emailform.currentemail.data:
            user = db.session.query(models.User).filter_by(username=current_user.username).first_or_404()
            user.email = emailform.email.data
            db.session.add(user)
            db.session.commit()
            logout_user()
            return redirect(url_for('login'))
    return render_template('updateemail.html', emailform=emailform)

#logout page. redirects to home
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def deleteaccount():
    user = db.session.query(models.User).filter_by(username=current_user.username).first_or_404()
    delaccount = DelAccountForm()
    if delaccount.validate_on_submit() and check_password_hash(current_user.password_hash, delaccount.password.data):
        db.session.delete(user)
        db.session.commit()
        flash('Your account has been deleted.')
        return redirect('/')
    else:
        return render_template('deleteaccount.html', delaccount=delaccount)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect('/')
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('requestreset.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect('/')
    user = models.User.verify_reset_password_token(token)
    if not user:
        return redirect('/')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.query(models.User).filter_by(id=user.id).update({models.User.password_hash:user.password_hash})
        db.session.commit()
        flash('Your password has been reset.')
        return redirect('/')
    return render_template('resetpassword.html', form=form)

#Induvidual POW info page, catches dynamic url only if int since I'm using ids for links
@app.route('/pow/<int:val>', methods=['GET', 'POST'])
def pow(val):
    form = CommentForm()
    deleteform = DeleteForm()
    if form.validate_on_submit() and form.comment.data:
        comment = models.Comment(comment=form.comment.data ,userid=current_user.id, powid=val)
        db.session.add(comment)
        db.session.commit()
        tuser = models.UserPrisoner.query.filter_by(powid=val).all()
        if tuser:
            for user in tuser:
                print(user)
                send_update_email(user)
    comments = models.Comment.query.filter(models.Comment.powid==val).all()
    track = models.UserPrisoner.query.filter(models.UserPrisoner.powid==val).first()
    pow = models.Prisoner.query.filter_by(id=val).first_or_404()
    capture = pow.Capture
    count = models.Prisoner.query.filter(models.Prisoner.capture==capture.id).count()
    #grammar for prisoner page
    if isinstance(capture.date, str) == True:
        inor = "on"
        sent = "on this date"
    else:
        inor = "in"
        sent = "at this location"
    return render_template("prisoner.html", val=val, prisoner=pow, inor=inor, sent=sent, count=count, form=form, comments=comments, tracked=track)

@app.route('/track/<int:pow>/<int:user>')
@login_required
def trackprisoner(pow, user):
    track = models.UserPrisoner(powid=pow, userid=user)
    db.session.add(track)
    db.session.commit()
    return redirect('/pow/{}'.format(pow))

@app.route('/delete/<int:user>/<int:com>')
@login_required
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
    return render_template('results.html', results1=pows1, results2=pows2, results3=pows3, val=rank.name, val2=rank.initial)


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
@app.route('/unit/<int:val>')
def unitpows(val):
    prisoners = models.PrisonerUnit.query.filter(models.PrisonerUnit.uid==val).all()
    count = len(prisoners)
    unit = models.Unit.query.filter_by(id=val).first_or_404()
    print(prisoners)
    pows = []
    for x in prisoners:
        pows.append(x.prisoner)
    r1 = pows[::3]
    r2 = pows[1::3]
    r3 = pows[2::3]
    return render_template("results.html", count= count, val=unit.fullname, results1=r1, results2=r2, results3=r3)

@app.route('/unit/<int:val1>/<int:val2>')
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
        count = len(pows)
        #For better display of results I split the results over 3 tables. For resizing purposes it also returns all results incase screen size is too small for 3 table display
        pows1 = pows[::3]
        pows2 = pows[1::3]
        pows3 = pows[2::3]
        val = val.upper()
        return render_template("results.html",val=val, count=count, results1=pows1, results2=pows2, results3=pows3)

@app.route('/user/<username>')
@login_required
def user(username):
    user = models.User.query.filter_by(username=username).first_or_404()
    comments = models.Comment.query.filter_by(userid=user.id)
    tracked = models.UserPrisoner.query.filter_by(userid=user.id)
    return render_template("user.html", user=user, comments=comments, tracked=tracked)

@app.context_processor
def inject_search():
    form = ContactForm()
    return dict(contactform=form)

#404 error handler with custom styled page.
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
