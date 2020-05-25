from . import db
class User(db.Model):
    Id=db.Column(db.Integer,primary_key=True)
    Username=db.Column(db.String(100),unique=True,nullable=False)
    Email=db.Column(db.String(120),unique=True,nullable=False)
    Password=db.Column(db.String(120),unique=True,nullable=False)
    Profile_img=db.Column(db.String(120),nullable=False,default='defaultProfile.jpeg')
    Post=db.relationship('Post',backref='Author',lazy=True)
    Friends=db.Column(db.String(9999),default="{}")
    

    def __repr__(self):
        return "User ({},{},{})".format(self.Username,self.Email,self.Profile_img)


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
    