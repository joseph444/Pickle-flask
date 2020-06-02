from flask import render_template,redirect,request

def index():
    return render_template("home/index.html")

def search(**kwargs):
    if kwargs:
        return render_template("home/search.html",title='Search',datas=kwargs)
    else:
        return render_template("home/search.html",title='Search')
    