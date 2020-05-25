from flask import render_template,redirect,request,flash
from pickle_ import app
from . import home
from .form import authentication
from .models.user import User,Post
@app.route("/")
def index():
    return home.view.index()

@app.route("/login",methods=['GET','POST'])
def Login():
    form=authentication.Login()
    if form.validate_on_submit():
        flash('Login Successfull for {}'.format(form.email.data),'success')
        return redirect("/")
   
    return render_template("authentication/login.html",title='Login',form=form,bg='bg-snow')


@app.route("/register",methods=['GET','POST'])
def register():
    form=authentication.Register()
    if form.validate_on_submit():
        flash('Registration Successfull for {}'.format(form.username.data),'success')
        return redirect("/")
    return render_template("authentication/register.html",title='Register',form=form,bg='bg-snow')