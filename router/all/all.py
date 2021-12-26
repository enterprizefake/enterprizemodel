from flask import Blueprint
from flask import jsonify
from flask import request
from sqlalchemy import and_
from utils.modelparser import to_pythontime,SqlToDict;
allblueprint = Blueprint('all_blueprint', __name__)
#appblueprint注意改名xx..x(自定义)blueprint 不然大家都用appblueprint会造成重复导入
from Starter import db

# https://segmentfault.com/a/1190000022883552
#数据库模型导入
from database.models import User,Project,EmployeeProject,Employee,Client,Contact




@allblueprint.route("/delemployeeinproject",methods=["POST"])
def delemployeeinproject():
    try:
        state="yes"
        json_= request.get_json()
        project_id=json_["project_id"]
        employee_id=json_["employee_id"]
        
        
        
        
        db.session.query(EmployeeProject).filter(EmployeeProject.employee_id==employee_id,EmployeeProject.project_id==project_id)\
        .delete()
        db.session.query(Contact)\
        .filter(Contact.toContactId==project_id,Contact.employee_id==employee_id)\
        .delete()
        
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
    finally:
        db.session.close()


@allblueprint.route("/notes",methods=["POST"])
def notes():
    try:
        state="yes"
        json_= request.get_json()
       
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
        
    finally:
        db.session.close()

@allblueprint.route("/project",methods=["POST"])
def project():
    try:
        state="yes"
        json_= request.get_json()
        _project=json_["project"]
        _del_emps=json_["del_employees"]
        _add_emps=json_["add_employees"]
        _client_id=json_["client_id"]
        
        _project_id=_project["project_id"]
        
        #修改project 的 clientid
        db.session.query(Project)\
            .filter(Project.project_id==_project_id)\
            .update({
                Project.client_id:_client_id
            })
        
        
        
        
        for delitem in _del_emps:
            db.session.query(EmployeeProject)\
            .filter(EmployeeProject.employee_id==delitem,EmployeeProject.project_id==_project_id).delete()
            pass
        
        db.session.flush()
        for additem in _add_emps:
            _emppro=EmployeeProject()
            _emppro.project_id=_project_id
            _emppro.ep_office=additem["ep_office"]
            _emppro.employee_id=additem["employee_id"]
            print("additem:",additem)
            db.session.add(_emppro)
            pass
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
    finally:
        db.session.close()

@allblueprint.route("/project_client",methods=["POST"])
def project_client():
    try:
        state="yes"
        json_= request.get_json()
        _project_id=json_["project_id"]
        _project=db.session.query(Project).filter(Project.project_id==_project_id).first()
        if _project==None:
            raise Exception("no such project")
        _client=db.session.query(Client).filter(Client.client_id==_project.client_id).first()
        if _client==None:
            raise Exception("no such client")
        
        
        
        return jsonify(
            {
                "state":state,
                "client_name":_client.client_name,
                "client_id":_client.client_id,
                "value":[_client.client_first,_client.client_second,_client.client_third]
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
    finally:
        db.session.close()