# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, ForeignKey, ForeignKeyConstraint, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = 'client'

    client_id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(50, 'utf8mb4_bin'))
    client_first = db.Column(db.String(50, 'utf8mb4_bin'))
    client_second = db.Column(db.String(50, 'utf8mb4_bin'))
    client_third = db.Column(db.String(50, 'utf8mb4_bin'))
    client_tele = db.Column(db.String(50, 'utf8mb4_bin'))


class Contact(db.Model):
    __tablename__ = 'contact'

    toContactId = db.Column(db.ForeignKey('session.toContactId'), primary_key=True, nullable=False)
    employee_id = db.Column(db.ForeignKey('employee.employee_id'), primary_key=True, nullable=False, index=True)
    empty = db.Column(db.Integer)

    employee = db.relationship('Employee', primaryjoin='Contact.employee_id == Employee.employee_id', backref='contacts')
    session = db.relationship('Session', primaryjoin='Contact.toContactId == Session.toContactId', backref='contacts')


class Employee(db.Model):
    __tablename__ = 'employee'

    employee_id = db.Column(db.String(50, 'utf8mb4_bin'), primary_key=True)
    employee_name = db.Column(db.String(50, 'utf8mb4_bin'), nullable=False)
    employee_age = db.Column(db.Integer)
    employee_office = db.Column(db.String(50, 'utf8mb4_bin'), nullable=False)
    employee_tele = db.Column(db.String(50, 'utf8mb4_bin'))
    employee_capability = db.Column(db.Integer)
    employee_workattitude = db.Column(db.Integer)
    department = db.Column(db.String(50, 'utf8mb4_bin'))
    avatar = db.Column(db.Text(collation='utf8mb4_croatian_ci'))


class User(Employee):
    __tablename__ = 'user'

    employee_id = db.Column(db.ForeignKey('employee.employee_id'), primary_key=True)
    password = db.Column(db.String(50, 'utf8mb4_bin'), nullable=False)


class EmployeeOperate(db.Model):
    __tablename__ = 'employee_operate'

    operate_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.ForeignKey('employee.employee_id'), index=True)
    operate_date = db.Column(db.String(30, 'utf8mb4_bin'))
    operate_what = db.Column(db.String(200, 'utf8mb4_bin'))

    employee = db.relationship('Employee', primaryjoin='EmployeeOperate.employee_id == Employee.employee_id', backref='employee_operates')


class EmployeeProject(db.Model):
    __tablename__ = 'employee_project'

    employee_id = db.Column(db.ForeignKey('employee.employee_id'), primary_key=True, nullable=False)
    project_id = db.Column(db.ForeignKey('project.project_id'), primary_key=True, nullable=False, index=True)
    ep_office = db.Column(db.String(20, 'utf8mb4_bin'))
    evaluate = db.Column(db.Integer)

    employee = db.relationship('Employee', primaryjoin='EmployeeProject.employee_id == Employee.employee_id', backref='employee_projects')
    project = db.relationship('Project', primaryjoin='EmployeeProject.project_id == Project.project_id', backref='employee_projects')


class Message(db.Model):
    __tablename__ = 'message'
    __table_args__ = (
        db.ForeignKeyConstraint(['toContactId', 'employee_id'], ['contact.toContactId', 'contact.employee_id']),
        db.Index('FK_R14', 'toContactId', 'employee_id')
    )

    id = db.Column(db.Integer, primary_key=True)
    toContactId = db.Column(db.Integer)
    employee_id = db.Column(db.String(50, 'utf8mb4_bin'))
    status = db.Column(db.String(50, 'utf8mb4_bin'))
    type = db.Column(db.String(50, 'utf8mb4_bin'))
    content = db.Column(db.Text(collation='utf8mb4_bin'))
    sendTime = db.Column(db.BigInteger)
    fileSize = db.Column(db.String(200, 'utf8mb4_bin'))
    fileName = db.Column(db.String(200, 'utf8mb4_bin'))

    contact = db.relationship('Contact', primaryjoin='and_(Message.toContactId == Contact.toContactId, Message.employee_id == Contact.employee_id)', backref='messages')


class MoniterImage(db.Model):
    __tablename__ = 'moniter_image'

    employee_id = db.Column(db.ForeignKey('employee.employee_id'), nullable=False, index=True)
    src_id = db.Column(db.Integer, primary_key=True)
    src_address = db.Column(db.String(90, 'utf8mb4_bin'))
    date = db.Column(db.DateTime)

    employee = db.relationship('Employee', primaryjoin='MoniterImage.employee_id == Employee.employee_id', backref='moniter_images')


class MoniterSession(db.Model):
    __tablename__ = 'moniter_session'

    session_id = db.Column(db.String(64, 'utf8mb4_bin'), primary_key=True, nullable=False)
    employee_id = db.Column(db.ForeignKey('employee.employee_id'), primary_key=True, nullable=False, index=True)

    employee = db.relationship('Employee', primaryjoin='MoniterSession.employee_id == Employee.employee_id', backref='moniter_sessions')


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
    client_id = db.Column(db.ForeignKey('client.client_id'), index=True)
    project_name = db.Column(db.String(50, 'utf8mb4_bin'), nullable=False)
    project_begindate = db.Column(db.Date, nullable=False)
    project_period = db.Column(db.String(50, 'utf8mb4_bin'))
    project_price = db.Column(db.Float)
    project_enddate = db.Column(db.Date)
    project_periodstage = db.Column(db.String(50, 'utf8mb4_bin'))
    project_type = db.Column(db.String(50))
    project_state = db.Column(db.String(50, 'utf8mb4_bin'))
    amendments = db.Column(db.Text(collation='utf8mb4_bin'))

    client = db.relationship('Client', primaryjoin='Project.client_id == Client.client_id', backref='projects')


class ProjectFile(db.Model):
    __tablename__ = 'project_file'
    __table_args__ = (
        db.ForeignKeyConstraint(['employee_id', 'project_id'], ['employee_project.employee_id', 'employee_project.project_id']),
        db.Index('FK_Relationship_10', 'employee_id', 'project_id')
    )

    projectfile_id = db.Column(db.String(64, 'utf8mb4_bin'), primary_key=True)
    employee_id = db.Column(db.String(50, 'utf8mb4_bin'))
    project_id = db.Column(db.Integer)
    projectfile_path = db.Column(db.String(100, 'utf8mb4_bin'))
    projectfile_time = db.Column(db.Date, nullable=False)

    employee = db.relationship('EmployeeProject', primaryjoin='and_(ProjectFile.employee_id == EmployeeProject.employee_id, ProjectFile.project_id == EmployeeProject.project_id)', backref='project_files')


class Session(db.Model):
    __tablename__ = 'session'

    toContactId = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.Text(collation='utf8mb4_bin'))
    displayName = db.Column(db.String(100, 'utf8mb4_bin'))
    unread = db.Column(db.Integer)
    lastSendTime = db.Column(db.Integer)
    lastContent = db.Column(db.Text(collation='utf8mb4_bin'))
