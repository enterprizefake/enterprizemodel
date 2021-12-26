
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
from database.models import User,MonitorLogio,MonitorTimer

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
        username=json_["user"]
        password=json_["password"]
        currenttime=to_pythontime(json_["currenttime"])
        
        
        # print(username,password)
        _users=db.session.query(User).filter(
            User.username==username,User.password==password
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



class MonitorSocket(Namespace):
    def on_connect(self):
        # print("connection:",request.sid)
        self.emit("message",{"connection":"welcome!"})
        
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
        # self.disconnect(request.sid)
        
        pass
    def on_timer(self,data):
        
        print("onheartbeat")
        
        pass
    def on_clientmessage(self,data):
        try:
            pass
        except Exception as e:
            cmd=data['cmd']
            if cmd=="register":
                pass
            elif cmd=="close":
                pass
            elif cmd=="processlist":
                pass
            elif cmd=="screenshot":
                pass
        finally:
            db.session.close()
            
    
    
