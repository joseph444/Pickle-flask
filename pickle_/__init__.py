from flask import Flask

app=Flask(__name__,template_folder="../templates",static_folder='../static')
app.config['SECRET_KEY']='c4d1ea100880c3da2eba415ebe8db3a5f6a522199ded95cf88d313205a3158db7fde'

from . import routes









