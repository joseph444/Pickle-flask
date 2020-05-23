from flask import render_template,redirect,request
from pickle import app
from home import routes
@app.route("/")
def index():
    return render_template('home/index.html')