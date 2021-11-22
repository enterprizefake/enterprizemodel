pip install flask
pip install flask-sqlalchemy
pip install flask-sqlacodegen
pip install flask-cors
pip install flask_pymongo #11/21新增

flask-sqlacodegen "mysql://enteam:123456@1.15.184.52:3306/flusktest"  --outfile "./database/models.py" --flask #生成数据库py文件 一定cd 到此文件夹后 不然位置是错的
或者运行 codegen.bat

router 放置 template.py修改后的文件

flask请按照本文件布局
--starter.py
-------database
-------------models.py
-------router
-------------xxxxx.py#参照template.py
-------------..............
-------------xxx.py
-------template
-------------template.py


gitupdate.bat 是自动执行更新你的分支的脚本 但需要你的设置 前提是你那个发的git教程你看了 不然没用

git init的时候请 新建自己的分支