from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import *
from flask_pymongo import PyMongo,MongoClient
import traceback
import logging




app =Flask(__name__)
CORS(app,supports_credentials=True)



#配置sql地址



SQLALCHEMY_DATABASE_URI = '''mysql://enteam:123456@1.15.184.52:3306/flasktest'''
MONGODB_URI="mongodb://superuser:superadmin@1.15.184.52:27017/test?authSource=admin"


app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_DATABASE_URI
# app.config["MONGO_URI"] = MONGODB_URI

app.config["JSON_AS_ASCII"] = False
# mongo = PyMongo(app)
# mongo=PyMongo(app,uri=MONGODB_URI)
mongo=MongoClient(MONGODB_URI)
db=SQLAlchemy(app)

#导入blueprint
from template.template import appblueprint
from router.file_module.file import fileblueprint


#--------------------------------------------
#加载blueprint
app.register_blueprint(appblueprint)
app.register_blueprint(fileblueprint)


#___________________________________________


@app.route("/")
def index():
    return "index! "

if __name__=="__main__":
    try:
        app.run(debug=True,port=8086,use_reloader=True)
    except Exception :
        traceback.print_exc()
    finally:
        mongo.close()
        # print(get_trace)
        
        
    

