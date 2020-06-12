from pickle_ import app
from flask_login import current_user
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
from time import time as t
import threading as th
class ChatApplication():
    def __init__(self):
        self.pathTofbjson=app.root_path+"/JSON/.firebase/pickle-29ef6-firebase-adminsdk-byfrs-ad9ad82898.json"
        self.cred=credentials.Certificate(self.pathTofbjson)
        firebase_admin.initialize_app(self.cred,{
            'databaseURL': 'https://pickle-29ef6.firebaseio.com/'
        })
        self.ref=db.reference('Chat')
        self.etag=None
    #so this function will be called whenever a new chat or an old chat is opened and the object with the reference will be
    #passed on to the chat controller in order to continue with chat
    def open_chat(self,id2):
        id1=current_user.Id
        self.subDBf_chat="chat_ids_{}_{}".format(id1,id2)
        self.chat_path=self.ref.child(self.subDBf_chat)
        self.reciever_chat="chat_ids_{}_{}".format(id2,id1)
        self.rchat_path=self.ref.child(self.reciever_chat)
       
    #this function will give the json file of the previous chat to the browser here vue maybe used to update each chat record accordingly

    def returnPreviousChats(self):

        while True:
            try:
                return self.chat_path.get()
            except:
                continue
    
    #the function which will be thread to the controller will help to make the chat application work as real time

    def returnChats(self):
        return self.chat_path.get()
    
    '''
    next is to save Data to firebase as json. Now here is a catch that is when we are storing a data we have to store 
    in current_user's chat as well as the other users chat as well
    This will be active when a user sends a message
    '''
    def GetMessageJson(self,message,rid):
        time=datetime.now().strftime("%B %d %Y")
        day=datetime.now().strftime("%A")
        id=current_user.Id
        message=str(message).strip()
        self.chat_path.child("{}".format(int(t()))).push({
            'id':id,
            'time':time,
            'day':day,
            'message':message

        })
        self.rchat_path.child("{}".format(int(t()))).push({
            'id':id,
            'time':time,
            'day':day,
            'message':message
        })
        return self.returnChats()
    #finally delete chat

    def deleteChat(self):
        self.chat_path.delete()
    
    def checkforupdate(self):
        self.chat_path.get_if_changed()
chatApp=ChatApplication()

#this takes response and simplifies the json file 
def UserMessage(response):
    retVal=dict()
    i=0
    if response:
        for key in response:
            for k in response[key]:
                retVal[i]= {
                    "id":response[key][k]['id'],
                    "msg":response[key][k]['message']
                }
                i+=1
        return retVal
    else:
        return {}

