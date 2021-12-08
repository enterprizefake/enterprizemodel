

from flask import Blueprint
from flask import jsonify
from flask import request
from sqlalchemy import and_
from utils.modelparser import to_pythontime,SqlToDict;
directorblueprint = Blueprint('director_blueprint', __name__)
#appblueprint注意改名xx..x(自定义)blueprint 不然大家都用appblueprint会造成重复导入
from Starter import db

# https://segmentfault.com/a/1190000022883552
#数据库模型导入
from database.models import User,Project,EmployeeProject,Employee



@directorblueprint.route("/newproject",methods=["POST"])
def newproject():
    try:
        state="yes"
        json_= request.get_json()["project"]
        _proj=Project(
                # project_id =,
    project_name = json_["project_name"],
    project_begindate = to_pythontime(json_["project_begindate"]),
    project_period = json_["project_period"],
    # project_price = ,
    # project_enddate = db.Column(db.Date)
    project_periodstage = json_["project_periodstage"],
    project_type = json_["project_type"],
    project_state = json_["project_state"],
    # amendments = db.Column(db.Text)
        )
        
        db.session.add(_proj)
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


@directorblueprint.route("/myproject",methods=["POST"])
def myproject():
    try:
        state="yes"
        json_= request.get_json()
        employee_id=json_["employee_id"]
        _projects=db.session.query(Project,EmployeeProject)\
        .filter(Project.project_id==EmployeeProject.project_id)\
        .filter(EmployeeProject.employee_id==int(employee_id))\
        .all()
        
        ret_=[]
        for t in _projects:
            ret_.append(SqlToDict(t[0],True).to_dict())
            
        # print(_projects)
        return jsonify(
            {
                "myproeject":ret_,
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
        


@directorblueprint.route("/project",methods=["POST"])
def op_project():
    from sqlalchemy import exists
    try:
        state="yes"
        json_= request.get_json()
        project_id=json_["project_id"]
        
        _epee_in=db.session.query(Employee,EmployeeProject)\
        .filter(Employee.employee_id==EmployeeProject.employee_id)\
        .filter(EmployeeProject.project_id==int(project_id))\
        .all()
        _epee_out=db.session.query(Employee)\
        .filter(~exists().where(and_(Employee.employee_id==EmployeeProject.employee_id,EmployeeProject.project_id==int(project_id))))\
        .all()

        sl_epee=[]
        avai_epee=[]
        for t in _epee_in:
            sl_epee.append(SqlToDict(t[0],True).to_dict())
        for t in _epee_out:
            avai_epee.append(SqlToDict(t,True).to_dict())
            
        

        
        return jsonify(
            {
                "selected_employee":sl_epee,
                "available_employee":avai_epee,
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

    # try:
    #     state="yes"
    #     json_= request.get_json()
  

    #     db.session.commit()
    #     return jsonify(
    #         {
    #             "state":state
    #         }
    #     )
    # except Exception as e:
    #     print(e)
    #     return jsonify(
    #         {
    #             "state":"no",
    #             "info":str(e)
    #         }
    #     )

def search_client():
    try:
        state="yes"
        json_= request.get_json()
  

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