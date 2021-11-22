import io
from traceback import print_exc
from flask import Blueprint
from flask import jsonify
from flask import request,send_file
import gridfs

fileblueprint = Blueprint('file_blueprint', __name__)
#appblueprint注意改名xx..x(自定义)blueprint 不然大家都用appblueprint会造成重复导入
from Starter import db,mongo
from .fileconfig import fileConfig
#数据库模型导入
from database.models import Json
from flask_pymongo import wrappers

#ref
#https://www.bogotobogo.com/python/MongoDB_PyMongo/python_MongoDB_RESTAPI_with_Flask.php
#upload https://blog.csdn.net/cnhome/article/details/102294143
# https://mongodb.github.io/node-mongodb-native/2.2/api/GridFSBucket.html
@fileblueprint.route("/filetest")
def test():
    # wrappers.Collection
    try:
        C_Testb:wrappers.Collection
        C_Testb =mongo[fileConfig.dbname].get_collection(fileConfig.defaultCollection)
        
        print("-----------------------------------",mongo.db)
        C_Testb.insert_one(
            {"a":"ffffff",}  
        )
        
        res=C_Testb.find()
        print("res:",res)
        return jsonify(
            {
                "result":"sucess"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result":str(e)
            }
        )


@fileblueprint.route("/listfiles")
def listfiles():
    
    try:
        
        
        # filelists=gridfs.GridFSBucket(mongo['test'])._bucket_name
        name=gridfs.GridFSBucket(mongo[fileConfig.dbName],bucket_name=fileConfig.defaultBucket).find()
        # for i in name:
        #     i.upload_date
        return jsonify(
                {
                    "result":"sucess",
                    # "filelists":filelists,
                    "files":[{
                        "name":i.name,
                        "lenth":i.length,
                        "ch_size":i.chunk_size,
                        "con_type":i.content_type,
                        "id":str(i._id),
                        "last_date":i.upload_date,
                        "md5":i.md5,
                        "typeof":str(type(i.content_type))
        
                        
                        }for i in name],
                }
            )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result":str(e)
            }
        )

@fileblueprint.route("/uploadfile",methods=['GET','POST'])
def uploadtostore():
    from .fileutils import uploadtoMongo
    try:
        #debug
        if request.method=="GET":
            
            
            return '''
            <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        ''' 
        
        new_id=None
        uploaded_file=request.files['file']
        if uploaded_file.filename != '':
            new_id=uploadtoMongo(mongo,uploaded_file)
        
        
        

        
        return jsonify({
            "id":str(new_id),
            "result":"success"
        })
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result":str(e)
            }
        )




@fileblueprint.route('/download/<string:id>')
def downloadfromstore(id):
    from .fileutils import downloadfromMongo
    try:
        pass
        obj=downloadfromMongo(mongo,id)
        
        
        print({
                "result":obj.name
            })
        
        return send_file(io.BytesIO(obj.read(obj.length))
                         ,attachment_filename=obj.filename,mimetype=obj.content_type,
                         as_attachment=True
                         )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result":str(e)
            }
        )
        