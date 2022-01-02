import datetime
from flask import Blueprint
from flask import jsonify
from flask import request
from numpy import delete

from utils import modelparser;
fileviewblueprint = Blueprint('fileview_blueprint', __name__)
#appblueprint注意改名xx..x(自定义)blueprint 不然大家都用appblueprint会造成重复导入
from Starter import db

#数据库模型导入
from database.models import Employee, Project, ProjectFile, User

@fileviewblueprint.route("/projectrelationfiles",methods=["POST"])
def getpersonfiles():
    try:
        state="yes"
        json_= request.get_json()
        _project_id=json_["project_id"]
        _ep_id=json_["my_id"]
        _ep_office=json_["my_office"]
        
        
        if _ep_office=="老板":
            pass
            _db_files=db.session.query(ProjectFile,Project,Employee)\
                .filter(ProjectFile.project_id==Project.project_id,ProjectFile.employee_id==Employee.employee_id)\
                .filter(ProjectFile.project_id==_project_id).all()
        elif _ep_office[-2:]=="主管":
            _db_files=db.session.query(ProjectFile,Project,Employee)\
                .filter(ProjectFile.project_id==Project.project_id,ProjectFile.employee_id==Employee.employee_id)\
                .filter(ProjectFile.project_id==_project_id).all()
            pass
        else :
            _db_files=db.session.query(ProjectFile,Project,Employee)\
                .filter(ProjectFile.project_id==Project.project_id,ProjectFile.employee_id==Employee.employee_id)\
                .filter(ProjectFile.project_id==_project_id,ProjectFile.employee_id==_ep_id).all()
        _files=[]
        
        for item in _db_files:
            _files.append(modelparser.tuple_merge_todict(item))
        
        
        return jsonify(
            {
                "filelist":_files,
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
        
        
@fileviewblueprint.route("/projectnewfiles",methods=["POST"])
def projectnewfiles():
    try:
        state="yes"
        json_= request.get_json()
        
        print("json:",json_)
        _project_id=json_["project_id"]
        _ep_id=json_["my_id"]
        _ep_office=json_["my_office"]   
        _projectfile_id=json_["projectfile_id"]
        _projf=ProjectFile()
        _projf.project_id=_project_id
        _projf.employee_id=_ep_id
        _projf.projectfile_id=_projectfile_id
        _projf.projectfile_time=datetime.datetime.now()
        db.session.add(_projf)
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


@fileviewblueprint.route("/unlinkprojectfiles",methods=["POST"])
def unlinkprojectfiles():
    try:
        state="yes"
        json_= request.get_json()
        
        
        _project_id=json_["project_id"]
        _ep_id=json_["my_id"]
        _ep_office=json_["my_office"]   
        _projectfile_id=json_["projectfile_id"]
        
        db.session.query(ProjectFile)\
            .filter(ProjectFile.projectfile_id==_projectfile_id)\
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