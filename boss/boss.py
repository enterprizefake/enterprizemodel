import json
from traceback import print_exc
from flask import Blueprint
from flask import jsonify
from flask import request

clientblueprint=Blueprint('client_blueprint',__name__)
from Starter import db
#数据库模型导入
from database.models import Client
@clientblueprint.route('/listAllClients')
def ListAllClients():    #显示所有客户信息
    try:
        clients = Client.query.all()
        return jsonify(
            {
                "result": "success",
                "clients":[
                    {
                        "client_name":client.client_name,
                        "client_tele":client.client_tele,
                        "project_id":client.project_id
                    }for client in clients
                ]
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result":str(e)
            }
        )

@clientblueprint.route('/insert_client')
def InsertClient():    #插入新客户
    try:
        name=request.args.get("client_name")
        tele=request.args.get("client_tele")
        first=request.args.get("client_first")
        second=request.args.get("client_second")
        third=request.args.get("client_third")
        db.session.add(Client(client_name=name,client_tele=tele,client_first=first,client_second=second,client_third=third))
        db.session.commit()
        return jsonify(
            {
                "result": "success"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result": str(e)
            }
        )

@clientblueprint.route('/delete_client')
def DeleteClient():    #删除客户
    try:
        name=request.args.get("client_name")
        tele=request.args.get("client_tele")
        client=db.session.query(Client).filter_by(client_name=name,client_tele=tele).first()
        db.session.delete(client)
        db.session.commit()
        return jsonify(
            {
                "result": "success"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result": str(e)
            }
        )

@clientblueprint.route('/update_client')
def UpdateClient():
    try:

        
        return jsonify(
            {
                "result": "success"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result": str(e)
            }
        )
