#-*- coding: utf-8 -*-
from flask import Blueprint
from flask import jsonify,send_file,Response,stream_with_context
from flask import request
from utils import modelparser;
formblueprint = Blueprint('from_blueprint', __name__)
#appblueprint注意改名xx..x(自定义)blueprint 不然大家都用appblueprint会造成重复导入
from Starter import db

#数据库模型导入
from database.models import Client, Project, User



@formblueprint.route("/genclient",methods=["GET"])
def genclient():
    try:
        state="yes"
        # json_= request.get_json()
        
        _clients=db.session.query(Client).all()
        _form=[]
        _form.append(",".join(["客户id","客户名称","一级单位","二级单位","三级单位","客户电话"]))
        for item in _clients:
            _form.append(
                ",".join([str(item.client_id),item.client_name,item.client_first,item.client_second,item.client_third,str(item.client_tele)])
            )
        return Response(
           stream_with_context( "\n".join(_form)),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=client.csv'})
        

    except Exception as e:
        print(e)
        return jsonify(
            {
                "state":"no",
                "info":str(e)
            }
        )
    finally:
        db.session.close()
        

@formblueprint.route("/genproject",methods=["POST","GET"])
def genproject():
    try:
        state="yes"
        
        _projects=db.session.query(Project,Client)\
        .filter(Project.client_id==Client.client_id)\
        .all()
        
        _ret_data=[]
        _ret_data.append(",".join(
            ["项目id","客户id","客户名称","项目名称","项目起始日期","项目时长","项目价格","项目结束日期","项目类型","项目状态"]
        ))
        for item_ in _projects:
            item=item_[0]
            item_2=item_[1]
            _ret_data.append(",".join([
                str(item.project_id),str(item.client_id),item_2.client_name,item.project_name,str(item.project_begindate),item.project_period,str(item.project_price),
                str(item.project_enddate),item.project_type,item.project_state
            ]))
        
        
        
        
        return Response(
            stream_with_context( "\n".join(_ret_data)),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=projects.csv'})
        
    except Exception as e:
        print(e)
        return jsonify(
            {
                "state":"no",
                "info":str(e)
            }
        )
    finally:
        db.session.close()