import json
import datetime
from traceback import print_exc
from flask import Blueprint
from flask import jsonify
from flask import request

bossblueprint=Blueprint('boss_blueprint',__name__)
from Starter import db
#数据库模型导入
from database.models import Employee,User,Client,EmployeeOperate,Contact,Project,Session

@bossblueprint.route('/allemployee',methods=["POST"])
def ListallEmployee():    #显示所有员工信息
    try:
        now_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')   #获取当前时间
        my_office=request.get_json()['my_office']   #操作人的职务
        my_name=request.get_json()['my_name']   #操作人的姓名
        my_id=request.get_json()['my_id']
        what=my_office+my_name+'查看了所有员工信息'   #记录操作日志
        operate=EmployeeOperate(employee_id=my_id,operate_date=now_time,operate_what=what)
        db.session.add(operate)
        db.session.commit()
        employees=Employee.query.all()   #获取所有员工信息
        return jsonify(
            {
                "allemployee":[
                    {
                        'department':employee.department,
                        'employee_age':employee.employee_age,
                        'employee_capability':employee.employee_capability,
                        'employee_id':employee.employee_id,
                        'employee_name':employee.employee_name,
                        'employee_office':employee.employee_office,
                        'employee_tele':employee.employee_tele,
                        'employee_workattitude':employee.employee_workattitude
                    }for employee in employees
                ]
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "state":str(e)
            }
        )
    finally:
        db.session.close()


@bossblueprint.route('/delemployee',methods=["POST"])
def DeleteEmployee():    #删除员工
    try:
        employee_id=request.get_json()['employee_id']    #获取要删除的员工id
        # print(employee_id)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间
        my_office = request.get_json()['my_office']  # 操作人的职务
        my_name = request.get_json()['my_name']  # 操作人的姓名
        my_id = request.get_json()['my_id']
        user = db.session.query(User).filter_by(employee_id=employee_id).first()
        employee=db.session.query(Employee).filter_by(employee_id=employee_id).first()
        what = my_office + my_name + '解雇了'+employee.employee_office+employee.employee_name  # 记录操作日志
        operate = EmployeeOperate(employee_id=my_id, operate_date=now_time,operate_what=what)
        db.session.add(operate)
        contacts=db.session.query(Contact).filter_by(employee_id=employee_id).all()
        for contact in contacts:   #将这个员工从他所参加的所有项目中移除
            db.session.delete(contact)
        db.session.delete(user)      #公司里删除此员工相关信息
        db.session.commit()
        return jsonify(
            {
                "state":"yes"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "state": "no",
                "info":str(e)
            }
        )
    finally:
        db.session.close()

@bossblueprint.route('/alteremployee',methods=["POST"])
def AlterEmployee():    #修改员工信息
    try:
        json_=request.get_json()
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间
        my_office = json_['my_office']  # 操作人的职务
        my_name = json_['my_name']  # 操作人的姓名
        my_id = json_['my_id']
        employee = db.session.query(Employee).filter_by(employee_id=json_['employee_id']).first()
        what=my_office+my_name+'修改了'+employee.employee_office+employee.employee_name+'的信息'
        operate = EmployeeOperate(employee_id=my_id, operate_date=now_time, operate_what=what)
        db.session.add(operate)
        db.session.query(Employee).filter(Employee.employee_id==json_['employee_id']).update({
            Employee.employee_office:json_['employee_office'],
            Employee.employee_age:json_['employee_age'],
            Employee.employee_workattitude:json_['employee_workattitude'],
            Employee.employee_tele:json_['employee_tele'],
            Employee.employee_name:json_['employee_name'],
            Employee.employee_capability:json_['employee_capability'],
            Employee.department:json_['department']
        })
        db.session.commit()
        return jsonify(
            {
                "state": "yes"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "state": "no",
                "info": str(e)
            }
        )
    finally:
        db.session.close()

@bossblueprint.route('/allclient',methods=["POST"])
def ListallClient():    #显示所有客户信息
    try:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间
        my_office = request.get_json()['my_office']  # 操作人的职务
        my_name = request.get_json()['my_name']  # 操作人的姓名
        my_id = request.get_json()['my_id']
        what = my_office + my_name + '查看了所有客户信息'  # 记录操作日志
        operate = EmployeeOperate(employee_id=my_id, operate_date=now_time, operate_what=what)
        db.session.add(operate)
        db.session.commit()
        clients = Client.query.all()
        client_projects={}    #储存每个客户的项目
        for c in clients:
            projects=db.session.query(Project).filter_by(client_id=c.client_id).all()   #查询客户的项目
            a=[]
            for p in projects:
                d={}.fromkeys(['project_name','project_period','project_state'])
                d['project_name']=p.project_name
                d['project_period']=p.project_period
                d['project_state']=p.project_state
                a.append(d)
            client_projects[c.client_id]=a
        #print(client_projects)
        return jsonify(
            {
                "customer_list":[
                    {
                        'client_id':client.client_id,
                        'projects':client_projects[client.client_id],
                        'client_name':client.client_name,
                        'client_first':client.client_first,
                        'client_second':client.client_second,
                        'client_third':client.client_third,
                        'client_tele':client.client_tele
                    }for client in clients
                ]
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "state":str(e)
            }
        )
    finally:
        db.session.close()

@bossblueprint.route('/delclient',methods=["POST"])
def DeleteClient():   #删除客户
    try:
        client_id=request.get_json()['client_id']     #获取要删除的客户id
        # print(client_id)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间
        my_office = request.get_json()['my_office']  # 操作人的职务
        my_name = request.get_json()['my_name']  # 操作人的姓名
        my_id = request.get_json()['my_id']
        client = db.session.query(Client).filter_by(client_id=client_id).first()
        what = my_office + my_name + '删除了客户' + client.client_name+'的信息'  # 记录操作日志
        operate = EmployeeOperate(employee_id=my_id, operate_date=now_time, operate_what=what)
        db.session.add(operate)
        db.session.delete(client)
        db.session.commit()
        return jsonify(
            {
                "state": "yes"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "state": "no",
                "info": str(e)
            }
        )
    finally:
        db.session.close()

@bossblueprint.route('/alterclient',methods=["POST"])
def AlterClient():    #修改客户信息
    try:
        json_=request.get_json()
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间
        my_office = json_['my_office']  # 操作人的职务
        my_name = json_['my_name']  # 操作人的姓名
        my_id = json_['my_id']
        client = db.session.query(Client).filter_by(client_id=json_['client_id']).first()
        what=my_office+my_name+'修改了客户'+client.client_name+'的信息'
        operate = EmployeeOperate(employee_id=my_id, operate_date=now_time, operate_what=what)
        db.session.add(operate)
        db.session.query(Client).filter(Client.client_id==json_['client_id']).update({
            Client.client_name:json_['client_name'],
            Client.client_tele:json_['client_tele'],
            Client.client_first:json_['client_first'],
            Client.client_second:json_['client_second'],
            Client.client_third:json_['client_third']
        })
        db.session.commit()
        return jsonify(
            {
                "state": "yes"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "state": "no",
                "info": str(e)
            }
        )
    finally:
        db.session.close()

@bossblueprint.route('/delproject',methods=["POST"])
def DelProject():    #删除项目
    try:
        json_ = request.get_json()
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间
        my_office = json_['my_office']  # 操作人的职务
        my_name = json_['my_name']  # 操作人的姓名
        my_id = json_['my_id']
        project=db.session.query(Project).filter_by(project_id=json_['project_id']).first()     #查询要删除的项目
        what = my_office + my_name + '删除了项目' + project.project_name
        operate = EmployeeOperate(employee_id=my_id, operate_date=now_time, operate_what=what)
        db.session.add(operate)
        db.session.delete(project)
        contacts=db.session.query(Contact).filter_by(toContactId=json_['project_id']).all()
        if contacts!=[]:
            for contact in contacts:   #清空项目群聊里的员工
                db.session.delete(contact)
        session=db.session.query(Session).filter_by(toContactId=json_['project_id']).first()
        db.session.delete(session)   #删除该项目的群聊
        db.session.commit()
        return jsonify(
            {
                "state": "yes"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "state": "no",
                "info": str(e)
            }
        )
    finally:
        db.session.close()