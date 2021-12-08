from flask import Blueprint
from flask import jsonify
from flask import request
from sqlalchemy import and_
from utils.modelparser import to_pythontime,SqlToDict;
monitorblueprint = Blueprint('moniter_blueprint', __name__)
#appblueprint注意改名xx..x(自定义)blueprint 不然大家都用appblueprint会造成重复导入
from Starter import db

#数据库模型导入
from database.models import User

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
    #             "result":"no",
    #             "info":str(e)
    #         }
    #     )    

    
def mlogin():
    try:
        from sqlalchemy import exists
        state="success"
        json_= request.get_json()
        username=json_["user"]
        password=json_["password"]
        currenttime=to_pythontime(json_["currentime"])
        _users=db.session.query(User).filter(
            exists().where(and_(User.employee_name==username,User.password==password))
        ).all()
        if(len(_users)==0):
        
                    return jsonify(
                    {
                        "result":"wrong name or password"
                    }
                    )
        
        _user=_users[0]
        return jsonify(
            {
                "userid":_user.employee_id,
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

def mtimer():
    try:
        state="success"
        json_= request.get_json()
        userid=int(json_["userid"])
        currenttime=to_pythontime(json_["currentime"])
        worktime=int(json_["worktime"])


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


    