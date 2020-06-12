from pickle_.models import user
from flask_login import current_user
import json
import os

class UserJson():
    def __init__(self):
        self.data=dict()
    
    def get_json(self,username):
        path=os.getcwd()
        thejson=open('{}/pickle_/JSON/{}.json'.format(path,username))  
        self.data=json.load(thejson)
        thejson.close()
        return self.data
    def _create_json(self,JSON:dict,username):
        path=os.getcwd()
        with open('{}/pickle_/JSON/{}.json'.format(path,username),'w') as thejson:
            json.dump(JSON,thejson)

    def create_json(self,username,id):
        self.data['id']=id
        self.data['username']=username
        self.data['followers']=[]
        self.data['followings']=[]
        self.data['blocked']=[]
        self.data['pinned']=[]
        self.data['chats']=[]
        path=os.getcwd()
        with open('{}/pickle_/JSON/{}.json'.format(path,username),'w') as thejson:
            json.dump(self.data,thejson)
    
    
    def addFollower(self,id):
        try:
            #adding followers
            Xuser=user.User.query.filter_by(Id=id).first()
            Xuserjson=self.get_json(Xuser.Username)
            currentJson=self.ret_data
            try:
                 Xuserjson['followers'].remove(current_user.Id)
                 currentJson['followings'].remove(id)
                 print("Hello Try")
            except:
                 Xuserjson['followers'].append(current_user.Id)
                 print("Except")
                 
                 currentJson['followings'].append(id)
                 pass
           
            #added Followers

            self._create_json(Xuserjson,Xuser.Username)
            self._create_json(currentJson,current_user.Username)
            return self.nooffollowers(Xuser.Username)
        except:
            return "Failed"
    
    def checkIfisfollowed(self,username):
        theXjson=self.get_json(username=username)
        if current_user.Id in theXjson['followers']:
            return True
        return False
    def nooffollowers(self,username):
        Xuser=self.get_json(username)
        return len(Xuser['followers'])
    def nooffollowings(self,username):
        Xuser=self.get_json(username)
        return len(Xuser['followings'])
    
    def get_followers(self):
        xjson=self.ret_data
        return xjson['followers']
    
    def get_followings(self):
        xjson=self.ret_data
        return xjson['followings']
    
    def getAllChats(self):
        xjson=self.ret_data
        return xjson['chats']
    
    def addChats(self,id):
        xjson=self.ret_data
        if xjson['chats'].count(id)>0:
            self.realignChats(id)
        else:
            xjson['chats'].append(id)
        username=user.User.query.get(id).Username
        self._create_json(xjson,current_user.Username)
        CJSON=self.get_json(username)
        if CJSON['chats'].count(current_user.Id)>0:
            try:
                CJSON['chats'].remove(current_user.Id)
            except:
                pass
        CJSON['chats'].append(current_user.Id)
        self._create_json(CJSON,username)
        print(CJSON)
    
    def removeChat(self,id):
        xjson=self.ret_data
        if xjson['chats'].count(id)==0:
            return
        xjson['chats'].remove(id)
        
        self._create_json(xjson,current_user.Username)
    
    def realignChats(self,id):
        xjson=self.ret_data
        try:
            xjson['chats'].remove(id)
        except:
            print("Except")
            pass
        xjson['chats'].insert(0,id)
        self._create_json(xjson,current_user.Username)
        return xjson['chats']
    def addPinned(self,postid):
        data=self.ret_data
        username=current_user.Username
        msg=''
        print(data)
        try:
                data['pinned'].remove(int(postid))
                msg='remove'
        except:
                 
                 data['pinned'].append(int(postid))
                 print("Except")
                 msg='added'
                 pass
            #added Followers
        self._create_json(data,username=username)
        return msg
    def getPinned(self):
        data=self.ret_data
        
        return data['pinned']

    @property
    def ret_data(self):
        path=os.getcwd()
        thejson=open('{}/pickle_/JSON/{}.json'.format(path,current_user.Username))  
        self.data=json.load(thejson)
        thejson.close()
        return self.data
    @property
    def noOFFollowers(self):
        self.data=self.ret_data
        return len(self.data['followers'])
    @property
    def noOFFollowings(self):
        self.data=self.ret_data
        return len(self.data['followings'])
    
