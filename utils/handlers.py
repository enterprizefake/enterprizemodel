

import sqlalchemy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from database.models import EmployeeOperate
def notehandler(db:SQLAlchemy,json_,what_:str):
    try:
        _epoper=EmployeeOperate()
        _epoper.employee_id=json_["my_id"]
        _epoper.operate_date=datetime.now()
        _epoper.operate_what=what_
        db.session.add(_epoper)
        db.session.commit()
        pass
    except Exception as e:
        pass
    finally:
        db.session.close()
        pass
    pass