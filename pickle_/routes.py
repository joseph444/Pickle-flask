from flask import render_template,redirect,request,flash
from pickle_ import app,bcrypt,mail,imagekit,images
from . import home
from .form import authentication,postsForm
from .models.user import User,Post,db
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message
from .exceptions import FileNotFound
from .UserFollowList import UserJson
from sqlalchemy import and_,or_,not_
from .PostLikelist import PostJSON
userJson=UserJson()
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



@app.route("/search",methods=['POST','GET'])
def search():

    if request.method=='POST':
        searchValue=request.form.get('search')
        if not searchValue:
            return " "
        else:
            if str(searchValue).rfind('%'):
                str(searchValue).replace("%","'%'")
            query="%{}%".format(searchValue)
            searchResult=dict()
            listofusers=User.query.filter(User.Username.like(query)).all()
            i=0
            for user in listofusers:
                searchResult[i]=user.ret_dict_of_values()
                i+=1
        return searchResult
    return home.view.search()


@app.route("/profile/")
def someFunction1():
    return redirect("/search")

@app.route("/profile/<id>")
def profile(id):
    if not id:
        return redirect("/search")
    else:
        
        user=User.query.filter_by(Id=id).first()
        if not user:
            flash("User Doesn't Exists",'danger')
            return redirect("/search")
        else:
            posts=Post.query.filter_by(user_id=id).order_by(Post.created_at.desc()).all()
            if not  current_user.is_authenticated:
                return render_template("account/profile.html",user=user,Theme=Theme,followers=userJson.nooffollowers(user.Username),following=userJson.nooffollowings(user.Username),posts=posts,PostJson=PostJSON)
            else:
                if int(id)==current_user.Id:
                    return redirect("/account")
                print(current_user.Id)
                return render_template("account/profile.html",user=user,Theme=Theme,isFollowed=userJson.checkIfisfollowed(user.Username),followers=userJson.nooffollowers(user.Username),following=userJson.nooffollowings(user.Username),posts=posts,PostJson=PostJSON)

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
                        return redirect("/account")
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
        userJson.create_json(user.Username,user.Id)
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

    posts=Post.query.filter_by(user_id=current_user.Id).order_by(Post.created_at.desc()).all()
    return render_template("account/index.html",title="Account",Theme=Theme,thejson=userJson,forms=postsForm.Posts(),posts=posts,PostJson=PostJSON)

@app.route("/account_post")
@login_required
def get_postS():
    id=request.args.get('id')
    if id:
        pass
    return " "
        


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
        
@app.route("/change_desc")
@login_required
def change_desc():
    desc=request.args.get("desc")
    
    current_user.Description=desc
    db.session.commit()
    return "done"

@app.route("/get_ff")
@login_required
def get_ff():
    try:
        return userJson.ret_data
    except Exception as e:
        return e


@app.route("/follow",methods=['POST','GET'])
@login_required
def follow():
    followX=request.form.get("id")
    operation=userJson.addFollower(followX)

    return "{}".format(operation)

@app.route("/get_followers",methods=['POST'])
@login_required
def get_followers():
    followerList=userJson.get_followers()
    if len(followerList)<1:
        return "0"
    Followers=dict()
    i=0
    for ids in followerList:
        user=User.query.filter_by(Id=ids).first()
        Followers[i]=user.ret_dict_of_values()
        i+=1
    return Followers

@app.route("/get_followings",methods=['POST'])
@login_required
def get_followings():
    followerList=userJson.get_followings()
    if len(followerList)<1:
        return "0"
    Followers=dict()
    i=0
    for ids in followerList:
        user=User.query.filter_by(Id=ids).first()
        Followers[i]=user.ret_dict_of_values()
        i+=1
    return Followers

@app.route("/")
@login_required
def index():
    followingIds=userJson.get_followings()
    followingIds.append(current_user.Id)
    posts=Post.query.filter(Post.user_id.in_(followingIds) ).order_by(Post.created_at.desc()).all()
    return render_template('home/index.html',newpost=postsForm.Posts(),posts=posts,PostJson=PostJSON,theme=Theme)


def save_img(Image_data,Title):
    folder_name="/Posts/{}/".format(str(current_user.Username).replace(' ','_'))
    name=str(current_user.Username).replace(' ','_')
    import secrets,os
    _,f_ext=os.path.splitext(Image_data.filename)
    name+="_"+secrets.token_hex(8)+f_ext
    tmppath=os.path.join(app.root_path,'tmp',name)
    Image_data.save(tmppath)
    f=open(tmppath,'rb')
    response=imagekit.upload_file(file=f,
            file_name=name,
            options={
                'folder':folder_name,
                'tags':['Post'],
                "is_private_file": False,
                "use_unique_file_name": True,
            })
    f.close()
    if response['error']:
                print(response['error'])
                os.remove(tmppath)
                if Image_data:
                    flash("Image was not uploaded ",'danger')
                
                return None,None
    else:

        Response=response['response']
        imgId=Response['fileId']
        url=Response['url']
        os.remove(tmppath)
        return url,imgId
                


@app.route("/post/create",methods=['POST'])
@login_required
def create_post():
    NewPost=postsForm.Posts()
    if NewPost.validate_on_submit():
        url=None
        imgId=None
        i=0
        if len(NewPost.Images.data)>0: 
            print(len(NewPost.Images.data))
            for image in NewPost.Images.data:
                if i==0:
                    url=''
                    imgId=''
                    i+=1
                Url,ImgId=save_img(image,NewPost.Title.data)
                if Url:
                    url+=Url+"|"
                    imgId+=ImgId+"|"
                else:
                    print(url)
                    break
                
           
        if NewPost.Type.data=='Recipie':
            post=Post(Title=NewPost.Title.data,Description=NewPost.Description.data,Type=NewPost.Type.data,
                            Ingredients=NewPost.Ingredients.data,Steps=NewPost.Steps.data,Image_source=url,Image_id=imgId,
                            user_id=current_user.Id
                            )
        elif NewPost.Type.data=='Rating':
               post=Post(Title=NewPost.Title.data,Description=NewPost.Description.data,Type=NewPost.Type.data,
                            FQ=NewPost.FoodQuality.data,Services=NewPost.Services.data,Cleanliness=NewPost.Cleanliness.data,
                            Behaviour=NewPost.Behaviour.data,Rating=NewPost.Rating.data,
                            Image_source=url,Image_id=imgId,
                            user_id=current_user.Id
                            )
        elif NewPost.Type.data=='Foodie':
            post=Post(Title=NewPost.Title.data,Description=NewPost.Description.data,Type=NewPost.Type.data,
                        Image_source=url,Image_id=imgId,
                        user_id=current_user.Id )
        db.session.add(post)
        db.session.commit()
        print(post.Id)
        PostJSON.create_postJson(post.Id)
        return redirect("/")
    else:
        flash("You must have messed up try to fill all the section for each type",'danger')
        return redirect("/account")

@app.route("/post/like",methods=['POST'])
@login_required
def like_post():
    postId=request.form.get('id')
    if postId:
       print()
       return PostJSON.Like(postId)
    

    return "-1"

@app.route("/post/unlike",methods=['POST'])
@login_required
def unlike_post():
    postId=request.form.get('id')
    if postId:
       print()
       return PostJSON.Unikes(postId)
    return "-1"

@app.route("/post/comment",methods=['POST'])
@login_required
def add_comment():
    comments=request.form.get('comment')
    postId=request.form.get('id')
    print(postId+comments)
    if postId:
        if comments:
            return PostJSON.addComment(postId,comments)
        return "2"
    return "-1"
    