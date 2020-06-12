from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from imagekitio.client import ImageKit
from flask_mail import Mail
from flask_images import Images
from flask_socketio import SocketIO
app=Flask(__name__,template_folder="../templates",static_folder='../static')

#configuration of The WEBAPP


app.config['SECRET_KEY']='c4d1ea100880c3da2eba415ebe8db3a5f6a522199ded95cf88d313205a3158db7fde'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'subhri.acharjya@gmail.com'
app.config['MAIL_PASSWORD'] = 'HyperB00l lamp clock door @ 1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


#creating flask_side applications
bcrypt=Bcrypt(app)
login=LoginManager(app)
mail=Mail(app)
images=Images(app)
socketio=SocketIO(app)


login.login_view="Login"
login.login_message_category="warning"
imagekit=ImageKit(public_key="public_F+8WfSJd5QAX4Jy62hcF6qYNg1A=",private_key="private_VMjHrVPRL1p5AYFG4ROtMyMM9K8=",url_endpoint="https://ik.imagekit.io/Pickle/")
from . import routes
from . import socketEvents









