
from flask import Blueprint
from flask import jsonify
from flask import request
from flask_socketio import emit

from sqlalchemy import and_
from datetime import datetime
from utils.modelparser import to_pythontime,SqlToDict;

monitorblueprint = Blueprint('moniter_blueprint', __name__)
#appblueprint注意改名xx..x(自定义)blueprint 不然大家都用appblueprint会造成重复导入
from Starter import db


#数据库模型导入
from database.models import Employee, MoniterImage, MoniterSession, Session, User,MonitorLogio,MonitorTimer

timer_interval=60



    # try:
    #     state="success"
    #     json_= request.get_json()
  

    #     db.session.commit()
    #     return jsonify(
    #         {
    #             "result":state
    #         }
    #     )
    # except Exception as e:
    #     print(e)
    #     return jsonify(
    #         {
    #             "result":"fail",
    #             "info":str(e)
    #         }
    #     )    

@monitorblueprint.route("/login",methods=["POST"])
def mlogin():
    try:
        from sqlalchemy import exists
        state="success"
        json_= request.get_json()
        username=json_["user_id"]
        password=json_["password"]
        currenttime=datetime.now()
        
        
        # print(username,password)
        _users=db.session.query(User).filter(
            User.employee_id==username,User.password==password
        ).all()
        if(len(_users)==0):
        
                    return jsonify(
                    {
                        "result":"wrong name or password"
                    }
                    )
        
        _user=_users[0]
        
        _login=MonitorLogio()
        _login.employee_id=_user.employee_id
        _login.type="login"
        _login.currenttime=currenttime
        
        db.session.add(_login)
        db.session.commit()
        return jsonify(
            {
                "userid":_user.employee_id,
                "interval":timer_interval,
                "result":state
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result":"fail",
                "info":str(e)
            }
        )
    finally:
        db.session.close()

@monitorblueprint.route("/timer",methods=['POST'])
def mtimer():
    try:
        state="success"
        json_= request.get_json()
        userid=int(json_["userid"])
        currenttime=to_pythontime(json_["currenttime"])
        worktime=int(json_["worktime"])
        _timer=MonitorTimer()
        _timer.employee_id=userid
        _timer.currentime=currenttime
        _timer.worktime=worktime
        db.session.add(_timer)
        db.session.commit()
        
        return jsonify(
            {
                "result":state
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result":"fail",
                "info":str(e)
            }
        )
    finally:
        db.session.close()        


@monitorblueprint.route("/logout",methods=["POST"])
def mlogout():
    try:
        from sqlalchemy import exists
        
        state="success"
        json_= request.get_json()
        
        userid=int(json_["userid"])
        currenttime=to_pythontime(json_["currenttime"])
        begintime=to_pythontime(json_["begintime"])
        
        
        
        _records=db.session.query(User,MonitorTimer).filter(
      
                User.employee_id==MonitorTimer.employee_id,
                MonitorTimer.currentime>=begintime
        )\
        .all()
        
        _login=MonitorLogio()
        _login.employee_id=userid
        _login.type="logout"
        _login.currenttime=currenttime
        
        
        worktime=0
        totaltime=0
        for r in _records:
            _mon:MonitorTimer
            _mon=r[1]
            worktime=_mon.worktime+worktime
            totaltime=timer_interval+totaltime
        rate_=worktime/totaltime
            
            


        return jsonify(
            {
                "workrate":int(rate_*100),
                "totalworktime":totaltime,
                "result":state
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result":"fail",
                "info":str(e)
            }
        )
    finally:
        db.session.close()    






# https://stackoverflow.com/questions/43592308/how-to-wait-for-a-callback-passed-to-flask-socketios-emit
# https://github.com/miguelgrinberg/Flask-SocketIO/issues/758
from flask_socketio import Namespace



def getEmployeeList(socket,sessions):
        _all_empolyees=db.session.query(Employee,MoniterSession)\
            .outerjoin(MoniterSession,Employee.employee_id==MoniterSession.employee_id)\
            .all()
        # print(_all_empolyees)
        _view_epees=[]
        for item in _all_empolyees:
            _dic=SqlToDict(item[0]).to_dict()
            if item[1]==None:
                _dic["moniter_session_id"]=None
            else:
                _dic["moniter_session_id"]=item[1].session_id
            _view_epees.append(_dic)
        
        for session_ in sessions:
            socket.emit("message",{
            "employee_list":_view_epees,
            "cmd":"returnemployeelist"
        },room=session_)

class MonitorSocket(Namespace):
    def __init__(self, namespace=None):
        super().__init__(namespace=namespace)
        self.moniterSRCsessions=[]
        
    def on_connect(self):
        print("connection:",request.sid)
        # self.emit("message",{"connection":"welcome!"})
        
        try:
            pass
        except Exception as e:
            print(e)
            # db.session.add()
        finally:
            db.session.close()
        pass
    def on_disconnect(self):
        print("disconnection:",request.sid)
        try:
            db.session.query(MoniterSession)\
                .filter(MoniterSession.session_id==request.sid)\
                .delete()
            db.session.commit()
            
            if request.sid in self.moniterSRCsessions:
                
                self.moniterSRCsessions.remove(request.sid)
            else:
                getEmployeeList(self,self.moniterSRCsessions)
            pass
            
        except Exception as e:
            print(e)
            pass
        finally:
            db.session.close()
        # self.disconnect(request.sid)
        
        pass
    def on_timer(self,data):
        
        print("onheartbeat")
        
        pass
    def on_clientmessage(self,data):
        print("on_clientmessage",data)
        try:
            cmd=data['cmd']
            if cmd=="register":
                _monses =MoniterSession()
                _monses.employee_id=data["my_id"]
                _monses.session_id=request.sid
                db.session.add(_monses)
                db.session.commit()
                getEmployeeList(self,self.moniterSRCsessions)
                pass
            if cmd=="moniter":
                self.moniterSRCsessions.append(request.sid)
                pass
            elif cmd=="close":
                
                pass
            elif cmd=="cmdprocesslist":
                _from_session=request.sid
                _session=db.session.query(MoniterSession)\
                    .filter(MoniterSession.employee_id==data["employee_id"]).first()
                if _session==None:
                    raise Exception("no such MoniterSession:"+data["employee_id"])
                
                _to_session=_session.session_id;
                def pl_emit_to_from(data):
  
                    data["cmd"]="returnprocesslist"
                    self.emit("message",data=data,room=_from_session)
                
                self.emit("message",{"cmd":"processlist"},room=_to_session,callback=pl_emit_to_from)
                pass
            elif cmd=="cmdscreenshot":
                _from_session=request.sid
                _session=db.session.query(MoniterSession)\
                    .filter(MoniterSession.employee_id==data["employee_id"]).first()
                if _session==None:
                    raise Exception("no such MoniterSession:"+data["employee_id"])
                
                _to_session=_session.session_id;
                
                def emit_to_from(data):
                    _monimg=MoniterImage()
                    _monimg.employee_id=data["my_id"]
                    _monimg.src_address=data["src_address"]
                    _monimg.date=datetime.now()
                    db.session.add(_monimg)
                    db.session.commit()
                    data["cmd"]="returnscreenshot"
                    self.emit("message",data=data,room=_from_session)
                
                self.emit("message",{"cmd":"screenshot"},room=_to_session,callback=emit_to_from)
                
                pass
            elif cmd=="cmdemployeelist":
                getEmployeeList(self,[request.sid])
            elif cmd=="cmdtodaytime":
                
                
                _from_session=request.sid
                _session=db.session.query(MoniterSession)\
                    .filter(MoniterSession.employee_id==data["employee_id"]).first()
                if _session==None:
                    raise Exception("no such MoniterSession:"+data["employee_id"])
                
                _to_session=_session.session_id;
                def emit_to_from(data):
                    data["cmd"]="returntodaytime"
                    self.emit("message",data=data,room=_from_session)
                
                self.emit("message",{"cmd":"todaytime"},room=_to_session,callback=emit_to_from)
                pass
         
            pass
        except Exception as e:
            self.emit("message",{"cmd":"error","info":str(e)})
            print(e)
        finally:
            db.session.close()
            
    
    
