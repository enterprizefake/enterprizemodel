from os import *

# from flask_sqlalchemy import SQLAlchemy
from flask import Flask, json,request,jsonify,Blueprint
from flask_cors import *
from sqlalchemy.orm import session
from utils.modelparser import SqlToDict

llr = Blueprint('llr_blueprint', __name__)

from database.models import *
@llr.route("/login",methods=['POST'])
def login():
    try:
        data=db.session.query(User)
        dic={"state":"yes"}
        js=request.get_json()
        print(js)
        username,password=js['username'],js['password']
        ls=data.filter(User.username==username).all()[0]
        if(ls.password!=password):
            dic["state"]="no"
        else:
            employee_all=db.session.query(Employee)
            employee=SqlToDict(employee_all.filter(Employee.employee_id==ls.employee_id).all()[0],notype=True).to_dict()
        dic['employee']=employee
        dic['user']=js
    except Exception:
        dic["state"]="no"
    finally:
        db.session.close()
    return dic

@llr.route("/register",methods=['POST'])
def register():
    try:
        dic={"state":"yes"}
        js=request.get_json()
        if(js['type']=='注册员工'):
            print(js)
        else:
            print("gre")
        # new_employee=Employee(js)
    except Exception:
        dic["state"]="no"
    finally:
        db.session.close()
    return dic

@llr.route("/allmessages",methods=['POST'])
def allmessages():
    try:
        allSession=db.session.query(Session)
        allContact=db.session.query(Contact)
        allMessage=db.session.query(Message)
        dic={"state":"yes"}
        js=request.get_json()
        # print(js['employee_id'])
        Sessionls,Messagels=[],[]
        # print(allContact)
        Contactdata=allContact.filter(Contact.employee_id==
        js['employee_id'])
        # print(Contactdata)
        for contact in Contactdata:
            session_dict=SqlToDict(allSession.filter(Session.toContactId==contact.toContactId)[0],True).to_dict()
            session_dict['id']=session_dict.pop('toContactId')
            session_dict['index']='群聊'
            Sessionls.append(session_dict)
            # print(session_dict)
            messagels=[]
            for message in allMessage.filter(Message.toContactId==contact.toContactId):
                message_dict=SqlToDict(message,True).to_dict()
                # print(message_dict)
                message_dict['fromUser']={'id':message_dict.pop(
                    'employee_id')
                ,'displayName':message_dict.pop('user_name'),
                'avatar':message_dict.pop('avatar')}
                # print(message_dict)
                messagels.append(message_dict)
            Messagels.append( {'id':contact.toContactId,'messages':messagels} )
            # print(Messagels)
        # print(Sessionls)
        dic['Sessionls']=Sessionls
        dic['Messagels']=Messagels
        # print(Sessionls)
        # print(Messagels)
        # new_employee=Employee(js)
    except Exception:
        dic["state"]="no"
    finally:
        db.session.close()
    print(dic)
    return dic

@llr.route("/addmessage",methods=['POST'])
def addmessage():
    try:
        dic={"state":"yes"}
        js=request.get_json()
        print(js)
        mess=Message(toContactId=js['id'],content=js['content'],employee_id=
        js['employee_id'],sendTime=js['time'],user_name=js['user_name'],
        avatar=js['avatar'],type=js['type'])
        print(mess)
        db.session.add(mess)
        nowsession=db.session.query(Session).filter(Session.toContactId==js['id'])[0]
        nowsession.lastContent=js['content']
        db.session.commit()
        # print(js)
        # new_employee=Employee(js)
    except Exception:
        dic["state"]="no"
    finally:
        db.session.close()
    return dic

@llr.route("/showmessage",methods=['POST'])
def showmessage():
    try:
        all=db.session.query(Message)
        dic={"state":"yes"}
        js=request.get_json()
        print(js)
        data=all.filter(Message.id==js['id']).all()
        print(data)
        ls=[]
        for i in data:
            print(i)
            ls.append(SqlToDict(i,True).to_dict())
        # print(ls)
        dic['ls']=ls
        # print(js)
        # new_employee=Employee(js)
    except Exception:
        dic["state"]="no"
    # print(dic)
    finally:
        db.session.close()
    return dic

