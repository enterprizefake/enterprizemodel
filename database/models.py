# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, ForeignKeyConstraint, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = 'client'

    project_id = db.Column(db.ForeignKey('project.project_id'), index=True)
    client_name = db.Column(db.String(64), primary_key=True, nullable=False)
    client_first = db.Column(db.String(64))
    client_second = db.Column(db.String(64))
    client_third = db.Column(db.String(64))
    client_tele = db.Column(db.String(64), primary_key=True, nullable=False)

    project = db.relationship('Project', primaryjoin='Client.project_id == Project.project_id', backref='clients')


class Employee(db.Model):
    __tablename__ = 'employee'

    employee_id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(20), nullable=False)
    employee_age = db.Column(db.Integer)
    employee_office = db.Column(db.String(64), nullable=False)
    employee_tele = db.Column(db.String(32))
    employee_capability = db.Column(db.Integer)
    employee_workattitude = db.Column(db.Integer)
    department = db.Column(db.String(64))


class User(Employee):
    __tablename__ = 'user'

    username = db.Column(db.String(32), nullable=False)
    employee_id = db.Column(db.ForeignKey('employee.employee_id'), primary_key=True)
    password = db.Column(db.String(32), nullable=False)


class EmployeeMessage(db.Model):
    __tablename__ = 'employee_message'

    message_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.ForeignKey('employee.employee_id'), index=True)
    message_title = db.Column(db.String(30))
    message_content = db.Column(db.String(500))
    message_zt = db.Column(db.Integer, nullable=False)

    employee = db.relationship('Employee', primaryjoin='EmployeeMessage.employee_id == Employee.employee_id', backref='employee_messages')


class EmployeeOperate(db.Model):
    __tablename__ = 'employee_operate'

    operate_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.ForeignKey('employee.employee_id'), index=True)
    operate_date = db.Column(db.Date)
    operate_what = db.Column(db.String(200))

    employee = db.relationship('Employee', primaryjoin='EmployeeOperate.employee_id == Employee.employee_id', backref='employee_operates')


class EmployeeProject(db.Model):
    __tablename__ = 'employee_project'

    project_id = db.Column(db.ForeignKey('project.project_id'), primary_key=True, nullable=False)
    employee_id = db.Column(db.ForeignKey('employee.employee_id'), primary_key=True, nullable=False, index=True)
    ep_function = db.Column(db.String(20), nullable=False)
    ep_finish = db.Column(db.Integer)
    ep_tuanduiid = db.Column(db.String(20))
    evaluate = db.Column(db.Integer)

    employee = db.relationship('Employee', primaryjoin='EmployeeProject.employee_id == Employee.employee_id', backref='employee_projects')
    project = db.relationship('Project', primaryjoin='EmployeeProject.project_id == Project.project_id', backref='employee_projects')


class MonitorLogio(db.Model):
    __tablename__ = 'monitor_logio'

    employee_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(32))
    currenttime = db.Column(db.DateTime)
    record_id = db.Column(db.Integer, primary_key=True)


class MonitorTimer(db.Model):
    __tablename__ = 'monitor_timer'

    employee_id = db.Column(db.Integer, nullable=False)
    record_id = db.Column(db.Integer, primary_key=True)
    currentime = db.Column(db.DateTime)
    worktime = db.Column(db.Integer)


class Project(db.Model):
    __tablename__ = 'project'

    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(32), nullable=False)
    project_begindate = db.Column(db.DateTime, nullable=False)
    project_period = db.Column(db.String(32))
    project_price = db.Column(db.Float)
    project_enddate = db.Column(db.DateTime)
    project_periodstage = db.Column(db.String(32))
    project_type = db.Column(db.String(32))
    project_state = db.Column(db.String(32))
    amendments = db.Column(db.Text)


class ProjectFile(db.Model):
    __tablename__ = 'project_file'
    __table_args__ = (
        db.ForeignKeyConstraint(['project_id', 'employee_id'], ['employee_project.project_id', 'employee_project.employee_id']),
        db.Index('fk_relationship_10', 'project_id', 'employee_id')
    )

    projectfile_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer)
    employee_id = db.Column(db.Integer)
    projectfile_path = db.Column(db.String(100), nullable=False)
    projectfile_time = db.Column(db.Date, nullable=False)

    project = db.relationship('EmployeeProject', primaryjoin='and_(ProjectFile.project_id == EmployeeProject.project_id, ProjectFile.employee_id == EmployeeProject.employee_id)', backref='project_files')
