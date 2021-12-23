# 环境配置 install.txt 
**或者运行 install.bat**
pip install flask
pip install flask-sqlalchemy
pip install flask-sqlacodegen
pip install flask-cors
pip install flask_pymongo #11/21新增
pip install flask-socketio #12/9新增
pip install gevent-websocket
pip install eventlet

# 数据库生成
flask-sqlacodegen "mysql://enteam:123456@1.15.184.52:3306/flasktest1"  --outfile "./database/models.py" --flask #生成数据库py文件 一定cd 到此文件夹后 不然位置是错的

**或者运行 codegen.bat**

router 放置 template.py修改后的文件

# 文件布局
flask请按照本文件布局
--starter.py
-------database
-------------models.py
-------router
-------------xxxxx.py 参照template.py
-------------..............
-------------xxx.py
-------template
-------------template.py
-------utils #models转化python dict


gitupdate.bat 是自动执行更新你的分支的脚本 但需要你的设置 前提是你那个发的git教程你看了 不然没用

git init的时候请 新建自己的分支

#开发问题
详见dev_issues分支(如sql问题)


### 12/5新增
app.register_blueprint(restapi, url_prefix='/webservice')#增加前缀 比如 /mytest变成 /webservice/mytest
### 12/6新增
models转化python dict 见utils.modelparser
###code自动
https://snippet-generator.app/?description=xxxblueprint&tabtrigger=xxxbl&snippet=&mode=vscode
