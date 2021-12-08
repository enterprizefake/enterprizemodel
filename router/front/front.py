
from flask import Blueprint
from flask import jsonify
from flask import request
from utils import modelparser;
from traceback import print_exc
frontprint = Blueprint('front_blueprint', __name__)
#appblueprint注意改名xx..x(自定义)blueprint 不然大家都用appblueprint会造成重复导入
from Starter import db

#数据库模型导入
from database.models import Client,Employee,User

@frontprint.route("/newclient",methods=["POST"])
def newclient():
    try:
        state="yes"
        json_= request.get_json()
        _client=Client()
        _client.client_first=json_["client_first"]
        _client.client_name=json_["client_name"]
        _client.client_second=json_["client_second"]
        _client.client_third=json_['client_third']
        _client.client_tele=json_["client_tele"]
        db.session.add(_client)
        db.session.commit()
        return jsonify(
            {
                "state":state
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "state":"no",
                "info":str(e)
            }
        )

@frontprint.route("/newemployee",methods=["POST"])
def newemployee():
    try:
        state="yes"
        json_= request.get_json()
        
        
        # _eplee=Employee(
        #     employee_name=json_["employee_name"]
        # )
    
        # _eplee.employee_name=json_["employee_name"]
        # _eplee.employee_age=json_["employee_age"]
        # _eplee.department=json_["department"]
        # _eplee.employee_tele=json_["employee_tele"]
        # _eplee.employee_office=json_["employee_office"]
        


        _usr=User()
        
        _usr.employee_name=json_["employee_name"]
        _usr.employee_age=json_["employee_age"]
        _usr.department=json_["department"]
        _usr.employee_tele=json_["employee_tele"]
        _usr.employee_office=json_["employee_office"]
        _usr.username=json_["username"]
        _usr.password=json_["password"] 
        
        # db.session.add(_eplee)
        db.session.add(_usr)
        db.session.commit()       
        return jsonify(
            {
                "state":state
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "state":"no",
                "info":str(e)
            }
        )




