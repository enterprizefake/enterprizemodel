# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, ForeignKey, ForeignKeyConstraint, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = 'client'

    client_name = db.Column(db.String(20), primary_key=True, nullable=False)
    client_first = db.Column(db.String(20))
    client_second = db.Column(db.String(20))
    client_third = db.Column(db.String(20))
    client_tele = db.Column(db.String(20), primary_key=True, nullable=False)
    project_id = db.Column(db.ForeignKey('project.project_id'), index=True)

    project = db.relationship('Project', primaryjoin='Client.project_id == Project.project_id', backref='clients')


class Contact(db.Model):
    __tablename__ = 'contact'

    toContactId = db.Column(db.ForeignKey('session.toContactId'), primary_key=True, nullable=False)
    employee_id = db.Column(db.ForeignKey('employee.employee_id'), primary_key=True, nullable=False, index=True)
    avatar = db.Column(db.String(200))

    employee = db.relationship('Employee', primaryjoin='Contact.employee_id == Employee.employee_id', backref='contacts')
    session = db.relationship('Session', primaryjoin='Contact.toContactId == Session.toContactId', backref='contacts')


class Employee(db.Model):
    __tablename__ = 'employee'

    employee_id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(20), nullable=False)
    employee_age = db.Column(db.Integer)
    employee_office = db.Column(db.String(20), nullable=False)
    employee_tele = db.Column(db.String(20))
    employee_capability = db.Column(db.Integer)
    employee_workattitude = db.Column(db.Integer)
    department = db.Column(db.String(20))


class User(Employee):
    __tablename__ = 'user'

    employee_id = db.Column(db.ForeignKey('employee.employee_id'), primary_key=True)
    username = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(20), nullable=False)


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
    evaluate = db.Column(db.Integer)

    employee = db.relationship('Employee', primaryjoin='EmployeeProject.employee_id == Employee.employee_id', backref='employee_projects')
    project = db.relationship('Project', primaryjoin='EmployeeProject.project_id == Project.project_id', backref='employee_projects')


class Message(db.Model):
    __tablename__ = 'message'
    __table_args__ = (
        db.ForeignKeyConstraint(['toContactId', 'employee_id'], ['contact.toContactId', 'contact.employee_id']),
        db.Index('FK_14', 'toContactId', 'employee_id')
    )

    id = db.Column(db.Integer, primary_key=True)
    toContactId = db.Column(db.Integer)
    employee_id = db.Column(db.Integer)
    status = db.Column(db.String(20))
    type = db.Column(db.String(20))
    content = db.Column(db.Text)
    sendTime = db.Column(db.BigInteger)
    fileSize = db.Column(db.String(200))
    fileName = db.Column(db.String(200))
    user_name = db.Column(db.String(20))
    avatar = db.Column(db.String(20))

    contact = db.relationship('Contact', primaryjoin='and_(Message.toContactId == Contact.toContactId, Message.employee_id == Contact.employee_id)', backref='messages')


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
    project_name = db.Column(db.String(20), nullable=False)
    project_begindate = db.Column(db.Date, nullable=False)
    project_period = db.Column(db.String(20))
    project_price = db.Column(db.Float)
    project_enddate = db.Column(db.Date)
    project_periodstage = db.Column(db.String(20))
    project_type = db.Column(db.String(20))
    project_state = db.Column(db.String(20))
    amendments = db.Column(db.Text)


class ProjectFile(db.Model):
    __tablename__ = 'project_file'
    __table_args__ = (
        db.ForeignKeyConstraint(['project_id', 'employee_id'], ['employee_project.project_id', 'employee_project.employee_id']),
        db.Index('FK_10', 'project_id', 'employee_id')
    )

    projectfile_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer)
    employee_id = db.Column(db.Integer)
    projectfile_path = db.Column(db.String(100), nullable=False)
    projectfile_time = db.Column(db.Date, nullable=False)

    project = db.relationship('EmployeeProject', primaryjoin='and_(ProjectFile.project_id == EmployeeProject.project_id, ProjectFile.employee_id == EmployeeProject.employee_id)', backref='project_files')


class Session(db.Model):
    __tablename__ = 'session'

    toContactId = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(100))
    displayName = db.Column(db.String(100))
    unread = db.Column(db.Integer)
    lastSendTime = db.Column(db.Integer)
    lastContent = db.Column(db.Text)
