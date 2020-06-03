from pickle_.models.user import Post,User
from pickle_ import app
from flask_login import current_user
import json
import os,secrets,datetime
import threading as th

class Postjson():
    def __init__(self):
        self.post=dict()
        pass
    def __path__(self,id):
        filename='{}.json'.format(id)
        folder=os.path.join(app.root_path,"JSON/POSTS/",filename)
        return folder

    def create_postJson(self,postId):
        self.post['Likes']=[]
        self.post['Unlikes']=[]
        self.post['Comment']=[]
        with open(self.__path__(postId),'w') as f:
            json.dump(self.post,f)
        pass

    def __ret_post(self,id):
            Json=open(self.__path__(id))
            post=json.load(Json)
            return post

    def __save_json(self,data:dict,id):
        with open(self.__path__(id),'w') as f:
            json.dump(data,f)
            pass

    '''
    This method is for Adding/deleteng user from a particular posts Unlists additional checking will be implemented during the request time
    Where it will be checked that if the current_user belongs to the followers list or not
    '''
    def Unikes(self,id):
        try:
            data=self.__ret_post(id)
        except Exception as e:
            return str(e)
        msg=''
        try:
            data['Unlikes'].remove(current_user.Id)
            msg='removed'
        except:
            data['Unlikes'].append(current_user.Id)
            msg='added'
            try:
                data['Likes'].remove(current_user.Id)
                msg=msg+'removed'
            except:
                pass
        self.__save_json(data,id)
        return msg
    

    '''This One is to add/Remove User from Like post list'''
    def Like(self,id):
        try:
            data=self.__ret_post(id)
        except Exception as e:
            return str(e)
        msg=''
        try:
            data['Likes'].remove(current_user.Id)
            msg='removed'
        except:
            data['Likes'].append(current_user.Id)
            msg='added'
            try:
                data['Unlikes'].remove(current_user.Id)
                msg=msg+'removed'
            except:
                pass
        print(data)
        self.__save_json(data,id)
        return msg
        
    def addComment(self,id,comment):
        try:
            data=self.__ret_post(id)
        except Exception as e:
            return str(e)
        msg='added'
        time=datetime.datetime.now()
        time=time.strftime("%m/%d/%Y, %H:%M:%S")
        data['Comment'].append({'user_id':current_user.Id,'comment':comment,'time':time})
        print(data['Comment'])
        self.__save_json(data,id)
        return msg
    
    def deleteComment(self,id,comment,time,usrid):
        try:
            data=self.__ret_post(id)
        except Exception as e:
            return str(e)
        required=dict()
        required['user_id']=userid
        required['comment']=comment
        required['time']=time
        try:
            data['Comment'].remove(required)
        except:
            return {"error":'Data Not Found'}
        
        self.__save_json(data,id)
        return "Deleted"
    
    def getComments(self, id):
        try:
            data=self.__ret_post(id)
        except Exception as e:
            return None
        response=dict()
        i=0
        for comments in data['Comments']:
            userId=comments['user_id']
            comment=comments['comment']
            time=comments['time'].date()
            user=User.query.get(userId).first()
            userDt=user.ret_dict_of_values()
            R=dict()
            R['user']=userDt
            R['comment']=comment
            R['time']=time
            response[i]=R
            i+=1
        
        return response
    def getNoofLikes(self,id):
        try:
            data=self.__ret_post(id)
        except Exception as e:
            return {"error":e}
        
        return {"nooflikes":len(data['Likes'])}
        pass
    def getNoofDislikes(self,id):
        try:
            data=self.__ret_post(id)
        except Exception as e:
            return {"error":e}
        
        return {"nooflikes":len(data['Unlikes'])}
        pass
    def getNoofComments(self,id):
        try:
            data=self.__ret_post(id)
        except Exception as e:
            return {"error":e}
        
        return {"nooflikes":len(data['Comment'])}
        pass
    def getLikeList(self,id):
        try:
            data=self.__ret_post(id)
        except Exception as e:
            return {"error":e}
        response=dict()
        i=0
        for ids in data['Likes']:
            post=Post.query.get(ids).first()
            response[i]=post.ret_dict_of_values()
        return response
        pass
    def getDislikeList(self,id):
        try:
            data=self.__ret_post(id)
        except Exception as e:
            return {"error":e}
        response=dict()
        i=0
        for ids in data['Unlikes']:
            post=Post.query.get(ids).first()
            response[i]=post.ret_dict_of_values()
        return response



PostJSON=Postjson()



