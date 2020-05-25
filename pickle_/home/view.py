from flask import render_template,redirect,request

def index():
    return render_template("home/index.html")