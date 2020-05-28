from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from pickle_.models import user
from pickle_ import app

class Register(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=6,max=100)])
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired(),Length(min=8,max=100)])
    confirmPassword=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField("Sign Up")

    def validate_username(self,username):
        User=user.User()
        check_user=User.query.filter_by(Username=username.data).first()
        if check_user:
            raise ValidationError('Username is Taken, Please Choose a different One')
    pass
    def validate_email(self,email):
        User=user.User()
        check_user=User.query.filter_by(Email=email.data).first()
        if check_user:
            raise ValidationError('User Already Exists')
    
    


class Login(FlaskForm):
     email=StringField("Email",validators=[DataRequired(),Email()])
     password=PasswordField("Password",validators=[DataRequired(),Length(min=8,max=100)])
     remember=BooleanField("Remember Me")
     submit=SubmitField("Log In")

     def validate_email(self,email):
        User=user.User()
        check_user=User.query.filter_by(Email=email.data).first()
        if not check_user:
            raise ValidationError("User Doesn't Exists")
     pass


class Forget(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField("Send Email")
    def validate_email(self,email):
        User=user.User()
        check_user=User.query.filter_by(Email=email.data).first()
        if not check_user:
            raise ValidationError("User Doesn't Exists")
    def validate_active(self,email):
        User=user.query.filter_by(Email=email.data).first()
        if not User.is_Active:
            raise ValidationError("User Is Not Verified")

class Reset(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8,max=100)])
    confpassword=PasswordField('Confirm',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Reset the Password')
    pass