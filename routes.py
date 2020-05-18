from flask import Flask, render_template, request
#from config import Config
import sqlite3
import random

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
