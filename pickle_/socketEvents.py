from pickle_ import socketio
from flask import request
from flask_login import current_user,login_required
from pickle_.models.user import User
from .FireBaseAdmin import chatApp,UserMessage
from flask_socketio import join_room,leave_room,disconnect
from .UserFollowList import UserJson
from urllib.parse import unquote,unquote_plus
userJson=UserJson()

rooms=dict()

def Make_user_online():
    pass

@socketio.on('connect')
def connect():
    
    if not current_user.Id in rooms.keys():
        rooms[current_user.Username]=[]
        rooms[current_user.Username].append(request.sid)
        
    else:
        rooms[current_user.Username].append(request.sid)
    print(rooms)
    pass

@socketio.on('openChat')
def open_chat(id):
    name=unquote_plus(id['id'])
    print(" \t\n"*20)
    print(id)
    print("something{}somethinf".format(name))
    print(" \t\n"*20)
    id=User.query.filter(User.Username.like(name)).first().Id
    print(id)
    chatApp.open_chat(id)
    res=UserMessage(chatApp.returnChats())
    room=request.sid
    socketio.emit('opened',{'data':res},room=room)




@socketio.on('message')
def handle_message(data):
    userName=unquote_plus( data['room'])
    try:
        Rooms=rooms[data['room']]
    except :
        Rooms=None
    userId=User.query.filter_by(Username=userName).first().Id
    message=data['message']
    chatApp.open_chat(userId)
    chatApp.GetMessageJson(message,userId)
    un=User.query.get(userId).Username
    userJson.addChats(userId)
    print("Room id {}".format(Rooms))
    if Rooms:
        for Room in Rooms:
            socketio.emit('recvmsg',{'data':message,'id':current_user.Username,'un':current_user.Username},room=Room)
    print('received message: {}'.format( message))
