from . import db,login,app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as tjw
class User(db.Model,UserMixin):
    Id=db.Column(db.Integer,primary_key=True)
    Username=db.Column(db.String(100),unique=True,nullable=False)
    Email=db.Column(db.String(120),unique=True,nullable=False)
    Password=db.Column(db.String(120),unique=True,nullable=False)
    Profile_img=db.Column(db.String(120),nullable=False,default='https://ik.imagekit.io/Pickle/user_profile_images/defaultuser1_sa94Jf9K3.png')
    Post=db.relationship('Post',backref='Author',lazy=True)
    Friends=db.Column(db.String(9999),nullable=True,default='NULL')
    isActive=db.Column(db.Boolean,nullable=False,default=False)
    theme=db.Column(db.String(100),nullable=True,default='Original')
    imgId=db.Column(db.String(100),nullable=True,default='5ed01001669a4e3c9e5d49aa')

    def __repr__(self):
        return "User ({},{},{})".format(self.Username,self.Email,self.Profile_img)
    def get_id(self):
        return self.Id
    def get_token(self,tm=1800):
        s= tjw(app.config['SECRET_KEY'],tm)
        return str(s.dumps({'user_id':self.Id}).decode('UTF-8'))
    @staticmethod
    def verify_token(token):
        s = tjw(app.config['SECRET_KEY'],1800)
        try:
            user=s.loads(token)['user_id']
            pass
        except :
            user=None
        return user
    @property
    def is_Active(self):
        return self.isActive
    
    @property
    def user_theme(self):
        return self.theme
    

#get User id

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    Id=db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(1000),nullable=False)
    Content1=db.Column(db.String(100),nullable=False)
    Content2=db.Column(db.String(1000),nullable=True)
    Content3=db.Column(db.String(1000),nullable=True)
    Image_source=db.Column(db.String(1000))
    user_id=db.Column(db.Integer,db.ForeignKey('user.Username'),nullable=False)

    def __repr__(self):
        return "Post ( {},{},{},{},{} )".format(self.Title,self.Content1,self.Content2,self.Content3,self.Image_source)
    def get_id(self):
        return self.Id