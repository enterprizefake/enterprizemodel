

from flask import Blueprint
from flask import jsonify
from flask import request
from sqlalchemy import and_
from utils.modelparser import to_pythontime,SqlToDict;
alldirectorblueprint = Blueprint('director_blueprint', __name__)
#appblueprint注意改名xx..x(自定义)blueprint 不然大家都用appblueprint会造成重复导入
from Starter import db

# https://segmentfault.com/a/1190000022883552
#数据库模型导入
from database.models import Contact, User,Project,EmployeeProject,Employee,Client,Session



@alldirectorblueprint.route("/newproject",methods=["POST"])
def newproject():
    try:
        state="yes"
        raw_json= request.get_json()
        

        
        
        
        
        json_= raw_json["project"]
        _proj=Project(
                # project_id =,
        project_name = json_["project_name"],
        project_begindate = to_pythontime(json_["project_begindate"]),
        project_period = json_["project_period"],
        project_price = json_["project_price"],
        # project_enddate = db.Column(db.Date)
        project_periodstage = json_["project_periodstage"],
        project_type = json_["project_type"],
        project_state = json_["project_state"],
        client_id=raw_json["client_id"]
    # amendments = db.Column(db.Text)
        )
        
        
        db.session.add(_proj)
        
        db.session.flush()
        if raw_json['my_office']!="老板":
            _emproj=EmployeeProject()
            _emproj.employee_id=raw_json['my_id']
            _emproj.ep_office=raw_json['my_office']
            _emproj.project_id=_proj.project_id
            
            print("projectid:",_emproj.project_id)
            db.session.add(_emproj)
        
        #新建会话
        _sess=Session()
        _sess.displayName=json_["project_name"]
        _sess.lastContent="新建聊天室"
        _sess.toContactId=_proj.project_id
        
        db.session.add(_sess)
        
        #拉入本人
        _contact=Contact()
        _contact.toContactId=_proj.project_id
        _contact.employee_id=raw_json['my_id']
        
        db.session.add(_contact)
        
        
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


@alldirectorblueprint.route("/allproject",methods=["POST"])
def myproject():
    try:
        state="yes"
        json_= request.get_json()
        employee_id=json_["my_id"]
        em_office=json_["my_office"]
        if em_office=='老板':
            _projects=db.session.query(Project,Project)\
            .filter(Project.project_id==Project.project_id)\
            .all()
        
        else:
        #查看自己id相关的项目
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
                "allproject":ret_,
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
        


@alldirectorblueprint.route("/select_employee",methods=["POST"])
def op_project():
    from sqlalchemy import exists
    try:
        state="yes"
        json_= request.get_json()
        project_id=json_["project_id"]
        
        _epee_in=db.session.query(Employee,EmployeeProject)\
        .filter(Employee.employee_id==EmployeeProject.employee_id)\
        .filter(EmployeeProject.project_id==project_id)\
        .all()
        print("run 112")
        _epee_out_raw=db.session.query(Employee)\
        .all()
        
        _epee_in_ids=[item[0].employee_id for item in _epee_in]
        _epee_out=[]
        for item in _epee_out_raw:
            if item.employee_id not in _epee_in_ids:
                _epee_out.append(item)
            

        sl_epee=[]
        avai_epee=[]
        for t in _epee_in:
            sl_epee.append({**SqlToDict(t[0],True).to_dict(),**SqlToDict(t[1],True).to_dict()})
        for t in _epee_out:
            avai_epee.append({**SqlToDict(t,True).to_dict()})
            
        

        
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
    finally:
        
        db.session.close()


@alldirectorblueprint.route("/search_client",methods=["POST"])
def search_client():
    try:
        state="yes"
        json_= request.get_json()
        value_=json_["value"]
        # _client=Client()
        _clients=db.session.query(Client).filter(
            Client.client_first==value_[0],Client.client_second==value_[1]
            ,Client.client_third==value_[2]
        ).all()
        
        customer_list=[]
        for item in _clients:
            customer_list.append(SqlToDict(item).to_dict())

        return jsonify(
            {
                "customer_list":customer_list,
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
        print("finallly")
        db.session.close()   


