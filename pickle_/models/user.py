from . import db,login,app
from flask_login import UserMixin
from flask_images import resized_img_src
from itsdangerous import TimedJSONWebSignatureSerializer as tjw
from datetime import datetime
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
    Description=db.Column(db.String(4000),nullable=True)

    def __repr__(self):
        return "User ({},{},{})".format(self.Username,self.Email,self.Profile_img)
    def get_id(self):
        return self.Id
    def get_token(self,tm=1800):
        s= tjw(app.config['SECRET_KEY'],tm)
        return str(s.dumps({'user_id':self.Id}).decode('UTF-8'))
    
    def ret_dict_of_values(self):
        Dictonary=dict()
        Dictonary['Username']=self.Username
        Dictonary['Id']=self.Id
        Dictonary['Pimg']=resized_img_src( self.Profile_img,width=100,height=100,mode='fit',quality=10000)
        Dictonary['Theme']=self.theme
        return Dictonary
    
    def Profile(self):
        Dictonary=dict()
        Dictonary['Username']=self.Username
        Dictonary['Description']=self.Description
        Dictonary['Id']=self.Id
        Dictonary['Pimg']=self.Profile_img
        Dictonary['Theme']=self.theme
        return Dictonary

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
    Description=db.Column(db.String(100),nullable=False)
    Ingredients=db.Column(db.String(1000),nullable=True)
    Steps=db.Column(db.String(1000),nullable=True)
    FQ=db.Column(db.String(1000),nullable=True)
    Services=db.Column(db.String(1000),nullable=True)
    Cleanliness=db.Column(db.String(1000),nullable=True)
    Behaviour=db.Column(db.String(1000),nullable=True)
    Rating=db.Column(db.String(1000),nullable=True)
    Type=db.Column(db.String(1000),nullable=True)
    Image_source=db.Column(db.String(1000),nullable=True)
    Image_id=db.Column(db.String(1000),nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.Id'),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return "Post ( {},{} )".format(self.Title,self.Image_source,)
    def get_id(self):
        return self.Id
    
    def get_Post(self):
        post=dict()
        post['id']=self.Id
        post['Title']=self.Title
        post['Type']=self.Type
        post['Description']=self.Description
        post['created_at']=self.created_at.date()
        if self.Type=='Recipie':
            post['Ingredients']=self.Ingredients
            post['Steps']=self.Steps
        elif self.Type=='Rating':
            post['FQ']=self.FQ
            post['Services']=self.Services
            post['Cleanliness']=self.Cleanliness
            post['Behaviour']=self.Behaviour
            post['Rating']=self.Rating
        
        if self.Image_source:
            post['Img']=str(self.Image_source).split('|')[:-1]
        else:
            post['Img']=None
        userId=self.user_id
        user=User.query.filter_by(Id=userId).first()
        username=user.Username
        profImg=user.Profile_img
        post['Username']=username
        post['Id']=userId
        post['Pimg']=profImg
        return post