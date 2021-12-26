from database.models import *
from os import *

# from flask_sqlalchemy import SQLAlchemy
from flask import Flask, json, request, jsonify, Blueprint
from flask_cors import *
from router.llr.dict import *
import datetime
SQLALCHEMY_DATABASE_URI = '''mysql://enteam:123456@1.15.184.52:3306/flasktest'''
llr = Blueprint('llr_blueprint', __name__)


@llr.route("/login", methods=['POST'])
def login():
    dic = {"state": "yes"}
    try:
        data = db.session.query(User)
        js = request.get_json()
        print(js)
        employee_id, password = js['employee_id'], js['password']
        ls = data.filter(User.employee_id == employee_id).all()[0]
        if(ls.password != password):
            dic["state"] = "no"
        else:
            employee_all = db.session.query(Employee)
            employee = to_dict(employee_all.filter(
                Employee.employee_id == ls.employee_id).all()[0])
        dic['employee'] = employee
        dic['password'] = password

        x = EmployeeOperate(operate_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), operate_what='登录',
                            employee_id=employee['employee_id'])
        db.session.add(x)
        db.session.commit()

    except Exception:
        dic["state"] = "no"
    finally:
        db.session.close()
    print(dic)
    return dic


@llr.route("/register", methods=['POST'])
def register():
    try:
        dic = {"state": "yes"}
        js = request.get_json()
        if(js['type'] == '注册员工'):
            print(js)
        else:
            print("gre")
    except Exception:
        dic["state"] = "no"
    finally:
        db.session.close()
    return dic


@llr.route("/allmessages", methods=['POST'])
def allmessages():
    dic = {"state": "yes"}
    try: 
        allSession = db.session.query(Session)
        allContact = db.session.query(Contact)
        allMessage = db.session.query(Message)
        print(allMessage.all())
        js = request.get_json()
        Sessionls, Messagels = [], []
        Contactdata = allContact.filter(Contact.employee_id ==
                                        js['employee_id'])

        for contact in Contactdata:
            session_dict = to_dict(allSession.filter(
                Session.toContactId == contact.toContactId)[0])
            session_dict['id'] = session_dict.pop('toContactId')
            session_dict['index'] = '群聊'
            Sessionls.append(session_dict)
            messagels = []
            for message in allMessage.filter(Message.toContactId == contact.toContactId):
                message_dict = to_dict(message)

                employeeid = message_dict.pop('employee_id')
                employee = to_dict(db.session.query(Employee).filter(
                    Employee.employee_id == employeeid)[0])
                message_dict['fromUser'] = {
                    'id': employeeid, 
                    'displayName': employee['employee_name'],
                    'avatar': employee['avatar']
                     }
                messagels.append(message_dict)
            Messagels.append(
                {'id': contact.toContactId, 'messages': messagels})
        dic['Sessionls'] = Sessionls
        dic['Messagels'] = Messagels
    except Exception:
        dic["state"] = "no"
    finally:
        db.session.close()
    print(dic)
    return dic

@llr.route("/addmessage", methods=['POST'])
def addmessage():
    try:
        dic = {"state": "yes"}
        js = request.get_json()
        print(js)
        mess = Message(toContactId=js['id'], content=js['content'], 
        employee_id=js['employee_id'], sendTime=js['time'], 
        type=js['type'])
        db.session.add(mess)
        nowsession = db.session.query(Session).filter(
            Session.toContactId == js['id'])[0]
        nowsession.lastContent = js['content']
        db.session.commit()
        # print(js)
        # new_employee=Employee(js)
    except Exception:
        dic["state"] = "no"
    finally:
        db.session.close()
    return dic


@llr.route("/showmessage", methods=['POST'])
def showmessage():
    try:
        all = db.session.query(Message)
        dic = {"state": "yes"}
        js = request.get_json()
        print(js)
        data = all.filter(Message.id == js['id']).all()
        print(data)
        ls = []
        for i in data:
            print(i)
            ls.append(to_dict(i))
        # print(ls)
        dic['ls'] = ls
        # print(js)
        # new_employee=Employee(js)
    except Exception:
        dic["state"] = "no"
    # print(dic)
    finally:
        db.session.close()
    return dic


@llr.route("/all/notes", methods=['POST'])
def notes():
    try:
        all = db.session.query(EmployeeOperate)
        dic = {"state": "yes"}
        js = request.get_json()
        if(js['employee_office'] == '老板'):
            data = all
        else:
            data = all.filter(EmployeeOperate.employee_id ==
                              js['employee_id']).all()
        ls = []
        for i in data:
            ls.append(to_dict(i))
        dic['ls'] = ls
    except Exception:
        dic["state"] = "no"
    finally:
        db.session.close()
    return dic


@llr.route("/all/alterpassword", methods=['POST'])
def alterpassword():
    try:
        all = db.session.query(User)
        dic = {"state": "yes"}
        js = request.get_json()
        user = all.filter(User.employee_id == js['employee_id'])[0]
        user.password = js['newpassword']
        db.session.commit()
    except Exception:
        dic["state"] = "no"
    finally:
        db.session.close()
    return dic
