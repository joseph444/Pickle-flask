from flask import render_template,redirect,request,flash
from pickle_ import app,bcrypt,mail,imagekit
from . import home
from .form import authentication
from .models.user import User,Post,db
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message
from .exceptions import FileNotFound

class Themes():
    def __init__(self):
        self.themes={
                
                'Original':'nevablue',
                'Spicy':'spicy-',
                'Veggies':'veg-',
                'Fruity':'fruits-',
                'Chilled':'cold-',
                'Candy':'candy-',
                'Chocolate':'choco-',
                'Bread and Butter':'bread-',
                'Popsickle':'pop-',
                'Sushi':'rice-',
                
            }
    
    def get_theme(self,key):
        try:
            return self.themes[key]
        except:
            return None
    def allTheme(self):
        return self.themes
Theme=Themes()

#normal pages which can be seen without logging in

@app.route("/")
def index():
    return home.view.index()




#user authentication section

@app.route("/login",methods=['GET','POST'])
def Login():
    next_page=request.args.get('next')
    if not current_user.is_authenticated:
        form=authentication.Login()
        if form.validate_on_submit():
            user=User.query.filter_by(Email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.Password,form.password.data):
                if user.is_Active:
                    login_user(user,remember=form.remember.data)
                    if next_page:
                        return redirect(next_page)
                    
                    else:
                        return redirect("/")
                else:
                    flash("You have to verify your email first",'warning')
            else:
                flash("Check Your Email or Password",'danger')
    
        return render_template("authentication/login.html",title='Login',form=form,bg='heavyrain')
    else:
        return redirect("/")


@app.route("/register",methods=['GET','POST'])
def register():
    if not current_user.is_authenticated:
        form=authentication.Register()
        if form.validate_on_submit():
            hs_password=bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user=User(Username=form.username.data,Email=form.email.data,Password=hs_password,Friends="")
            db.session.add(user)
            db.session.commit()
            url=request.base_url
            token=user.get_token()
            body="The Click below to activate your account , link will be disabled after 30 min {}/{}".format(url,token)
            msg=Message(subject='Activation Message',recipients= [form.email.data],body=body,sender=app.config['MAIL_USERNAME'])
            try:
                mail.send(msg)
                flash('Registration Successfull for {}. Your Activation Mail has been sent'.format(form.username.data),'success')
                pass
            except:
                flash("Sorry we are facing some smtp problems",'danger')
            return redirect("/login")
        return render_template("authentication/register.html",title='Register',form=form,bg='.heavyrain')
    else:
        return redirect("/")

@app.route("/register/<tokken>")
def activate_user(tokken):
    id=User.verify_token(tokken)
    if id:
        user=User.query.filter_by(Id=id).first()
        user.isActive=True
        db.session.commit()
        flash("Email is now verified",'success')
        return redirect("/login")
    else:
        flash("Invalid Tokken",'danger')
        return redirect("/login")

@app.route("/forget_password",methods=['GET','POST'])
def forget_password():
    if not current_user.is_authenticated:
        form=authentication.Forget()
        if form.validate_on_submit():
            url=request.base_url
            user=User.query.filter_by(Email=form.email.data).first()
            tokken=user.get_token()
            body="The Click below to change the password , link will be disabled after 10 min  {}/{}".format(url,tokken)
            msg=Message(subject='Activation Message',recipients= [form.email.data],body=body,sender=app.config['MAIL_USERNAME'])
            try:
                mail.send(msg)
                flash("The password reset link has been sent please check your email",'success')
                pass
            except:
                flash("Sorry we are facing some smtp problems",'danger')
            
        return render_template("authentication/forget.html",form=form,title="Forget Password")
        pass
    else:
        return redirect("/")

@app.route("/forget_password/<token>",methods=['GET','POST'])
def reset(token):
    id=User.verify_token(token)
    if id:
        form=authentication.Reset()
        if form.validate_on_submit():
            user=User.query.filter_by(Id=id).first()
            hs_pass=bcrypt.generate_password_hash(form.password.data)
            user.Password=hs_pass
            db.session.commit()
            flash("Password reset is successfull")
            return redirect("/login")
            pass
        else:
            return render_template("authentication/reset.html",form=form,title='Reset Password')
            pass
    else:
        return redirect('/login')

@app.route("/logout",methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect("/")


'''@TODO create a feature to reset password from inside
'''

# This is the section where all the things will be login required like searrching, sending friend request, chatting, etc

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    return render_template("account/index.html",title="Account",Theme=Theme)


@app.route("/change_theme")
@login_required
def change_theme():
    try:
        newThme=request.args.get('theme')
        current_user.theme=newThme
        db.session.commit()
    except Exception as e:
        print(e)
        return e
    
    return "{}".format(request.args.get('theme'))

@app.route("/change_img",methods=['POST'])
@login_required
def change_img():
    defaultId="5ed01001669a4e3c9e5d49aa"
    allowed_Types=['jpg','png','jpeg','gif','pjpeg','exif','bmp','pgm','webp','bpg','ico']
    if 'newimg' in request.files:
        file=request.files['newimg']
        if file.filename=='':
            return "No File Selected"
        filename=str(file.filename)
        if not ('.' in filename and filename.rsplit(".",maxsplit=1)[1] in allowed_Types):
            return "You can Only Upload a Image file. .{} not allowed ".format(filename.rsplit(".",maxsplit=1)[1])
        print(current_user.Profile_img)
        try:
            folderName="/user_profile_images/{}/".format(current_user.Username)
            folderName=folderName.replace(" ","_")
            if(current_user.imgId!=defaultId):
                imagekit.delete_file(current_user.imgId)
                
            response=imagekit.upload_file(file=file,
                    file_name= "{}.{}".format(current_user.Username,filename.rsplit(".",maxsplit=1)[1]),
                    options= {
                        'folder':folderName,
                        'tags':['profile picture'],
                        "is_private_file": False,
                        "use_unique_file_name": True,
                        })
            if response['error']:
                print(response['error'])
                raise FileNotFound
            else:
                Response=response['response']
                imgId=Response['fileId']
                url=Response['url']
                current_user.Profile_img=url
                current_user.imgId=imgId
                db.session.commit()
        except Exception as e:
            return "{}".format(e)
        return "1"
    else:
        for x in request.files:
            print(x)
        return 'Some Error Occured'
        
    