from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo
class Register(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=6,max=100)])
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired(),Length(min=8,max=100)])
    confirmPassword=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField("Sign Up")
    pass

class Login(FlaskForm):
     email=StringField("Email",validators=[DataRequired(),Email()])
     password=PasswordField("Password",validators=[DataRequired(),Length(min=8,max=100)])
     remember=BooleanField("Remember Me")
     submit=SubmitField("Log In")
     pass