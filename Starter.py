from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import *



#导入blueprint
from template.template import appblueprint






#--------------------------------------------

#配置sql地址
SQLALCHEMY_DATABASE_URI = '''mysql://enteam:123456@1.15.184.52:3306/flusktest'''
app =Flask(__name__)
CORS(app,supports_credentials=True)


#加载blueprint
app.register_blueprint(appblueprint)






#___________________________________________

app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_DATABASE_URI
app.config["JSON_AS_ASCII"] = False
db=SQLAlchemy(app)



@app.route("/")
def index():
    return "index! "

if __name__=="__main__":
    app.run(debug=True,port=8086,use_reloader=True)