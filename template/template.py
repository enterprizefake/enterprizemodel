from flask import Blueprint
from flask import jsonify
from flask import request
appblueprint = Blueprint('_blueprint', __name__)
#appblueprint注意改名xx..x(自定义)blueprint 不然大家都用appblueprint会造成重复导入
from Starter import db

#数据库模型导入
from database.models import Json




@appblueprint.route("/hellob/<name>")
def hellob(name):
    return "hellob! "+name

@appblueprint.route("/hellojson/<string:name>")
def hellojson(name):
    test={"name":name}
    return jsonify(test)

@appblueprint.route("/alljson")
def sqlall():
    all=db.session.query(Json).all()

    test={"result":[{
        "key":i.key,
        "value":i.value,
        "index":i.index
        
        }for i in all]}
    return jsonify(test)

#/insert?key=lol&value=巴卜
@appblueprint.route("/insert")
def insert():
    try:
    
        key=request.args.get("key")
        value=request.args.get("value")
        db.session.add(Json(key=key,value=value))
        db.session.commit()
        return jsonify(
            {
                "result":"success"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result":str(e)
            }
        )


@appblueprint.route("/replace/<string:key>/<string:newvalue>",methods=['GET'])
def replace(key,newvalue):
    try:
        # db.session.
        db.session.query(Json).filter(Json.key==key).update({
            Json.value:newvalue
        })
        db.session.commit()
        return jsonify(
            {
                
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result":str(e)
            }
        )