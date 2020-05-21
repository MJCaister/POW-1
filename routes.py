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

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/records')
def search():
    return render_template("records.html")

if __name__ == "__main__":
    app.run(debug=True)
