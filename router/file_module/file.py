import io
import json
from traceback import print_exc
import traceback
from flask import Blueprint
from flask import jsonify
from flask import request,send_file
import gridfs
from numpy import iinfo

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
@fileblueprint.route("/mongotest")
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
                        # "typeof":str(type(i.content_type))
        
                        
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


@fileblueprint.route("/rootinfo/<string:rootid>")
def getprojectrootinfo(rootid):
    try:
        filedb=mongo[fileConfig.dbName].get_collection(fileConfig.defaultCollection)
        
        from bson.objectid import ObjectId
        pathroot=filedb.find_one(
            {
                "_id":ObjectId(rootid),
                
            }
        )
        if pathroot==None:
            return jsonify(
            {
                "info":"no such projectid",
                "result":"success"
            }
        )
        pathroot["_id"]=str(pathroot["_id"])
        
        from .folder import findpathsubfiles
        (files,info)=findpathsubfiles(["root"],pathroot)
        bucket=gridfs.GridFSBucket(mongo[fileConfig.dbName],bucket_name=fileConfig.defaultBucket)
        cursor=bucket.find(
            {
                "_id":{"$in":
                    [ ObjectId(i) for i in files]
                    # [ObjectId("55880c251df42d0466919268"), ObjectId("55bf528e69b70ae79be35006")]
                    }
            }
        )
        
        print("_____",[ ObjectId(i) for i in files])
        filemap=dict()
        from bson.json_util import dumps
        for i in cursor:
            i.close()
            obj_={
                        "name":i.name,
                        "lenth":i.length,
                        "filetype":i.content_type,
                        "fileid":str(i._id),
                        "last_date":i.upload_date,
                        "md5":i.md5,
                        "meta":i.metadata
            }
            filemap[str(i._id)]=obj_
        
        print(files,cursor.count())
        # for k,v in filemap:
        #     v['_id']=str(v['_id'])
        
        print(filemap)
        
        
        return jsonify(
            {
                "info":pathroot,
                "filemap":filemap,
                "result":"success"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result":str(e)
            }
        )



@fileblueprint.route("/uploadfilebyid",methods=['GET','POST'])
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




@fileblueprint.route('/downloadfilebyid/<string:id>')
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

@fileblueprint.route('/updatefilebyid/<string:id>',methods=['GET','POST'])
def updatetofilebyid(id):
    from .fileutils import updatetoMongo
    try:
        pass
        #debug
        if request.method=="GET":
            
            
            return '''
            <!doctype html>
        <title>Upload new File</title>
        <h1>Update new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        ''' 
        
        new_id=None
        uploaded_file=request.files['file']
        if uploaded_file.filename != '':
            new_id=updatetoMongo(mongo,id,uploaded_file)
        
        
        return jsonify(
            {
              "id":str(new_id),
             "result":"success"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result":str(e)
            }
        )

@fileblueprint.route("/deletefilebyid/<string:id>")
def deletefilebyid(id):
    from .fileutils import deletefromMongo
    try:
        state=deletefromMongo(mongo,id)
        return jsonify(
            {
              "id":str(state),
             "result":"success"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "result":str(e)
            }
        )


@fileblueprint.route("/createroot/<string:rootname>",methods=['GET'])
def testfolder(rootname):
    try:
        # print("run")
        from .folder import createProjectRootFolder
        result=createProjectRootFolder(rootname,mongo[fileConfig.dbName].get_collection(fileConfig.defaultCollection))
        return jsonify(
            {
              "root_id":str(result.inserted_id),
             "result":"success"
            }
        )
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {
                "result":str(e)
            }
        )
        
@fileblueprint.route("/createfolder",methods=['POST'])
def createnewfolder():
    import traceback
    try:
        
        json_=request.get_json()
        rootname=json_['rootname']
        foldername=json_["foldername"]
        rootid=json_["rootid"]
        from .folder import createfolder
        (obj,info)=createfolder(rootid,rootname,foldername,mongo[fileConfig.dbName].get_collection(fileConfig.defaultCollection))
        return jsonify(
            {
              "info":str(info),
            #   "type":str(obj),
             "result":"success"
            }
        )
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {
                "result":str(e)
            }
        )


@fileblueprint.route("/deletefolder",methods=['POST'])
def deletefolder():
    import traceback
    try:
        
        json_=request.get_json()
        rootname=json_['rootname']
        rootid=json_["rootid"]
        from .folder import deletefolder
        (obj,info)=deletefolder(rootid,rootname,mongo[fileConfig.dbName].get_collection(fileConfig.defaultCollection),mongo)
        return jsonify(
            {
              "info":str(info),
            #   "type":str(obj),
             "result":"success"
            }
        )
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {
                "result":str(e)
            }
        )


@fileblueprint.route("/updatefolder",methods=['POST'])
def updatefolder():
    import traceback
    try:
        
        json_=request.get_json()
        rootname=json_['rootname']
        newfoldername=json_['newfoldername']
        rootid=json_["rootid"]
        from .folder import updatefolder
        (obj,info)=updatefolder(rootid,rootname,newfoldername,mongo[fileConfig.dbName].get_collection(fileConfig.defaultCollection))
        return jsonify(
            {
              "info":str(info),
            #   "type":str(obj),
             "result":"success"
            }
        )
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {
                "result":str(e)
            }
        )

@fileblueprint.route("/filecenter/<string:operationtype>",methods=["POST"])
def operationfile(operationtype):
    json_=request.get_json()
  
    try:
        if operationtype=='delete':
            
            
            projectid=json_['rootid']
            file_id=json_['fileid']
            rootpath=json_['rootname']
            from .folder import deletefile
            (obj,info)=deletefile(projectid,rootpath,file_id,mongo[fileConfig.dbName].get_collection(fileConfig.defaultCollection)
                       ,gridfs.GridFSBucket(mongo[fileConfig.dbName],bucket_name=fileConfig.defaultBucket),mongo
                       )
            
            
            return jsonify(
            {
             "info":info,
             "result":"success"
            }
        )
        
        elif operationtype=='create':
            projectid=request.args['rootid']
            rootpath=request.args['rootname']
            
            from .folder import createfile
            
            uploaded_file=request.files['file']
            if uploaded_file.filename != '':
                
            
            
                (obj,info)=createfile(projectid,rootpath
                                    ,uploaded_file
                           ,mongo[fileConfig.dbName].get_collection(fileConfig.defaultCollection) 
                        ,mongo
                        )
            
            else:
                info="null file name"
                obj="None"
            return jsonify(
            {
             "file":obj,
             "info":info,
             "result":"success"
            })
        
        elif operationtype=='rename':
            json_=request.get_json()
            # projectid=json_['rootid']
            # rootpath=json_['rootname']
            file_id=json_['fileid']
            newname=json_['newname']
            from .folder import updatefile
            
            (obj,info)=updatefile(file_id,newname,
                                  gridfs.GridFSBucket(mongo[fileConfig.dbName],bucket_name=fileConfig.defaultBucket) 
                     
                                )
            
         
        
            return jsonify(
            {
             "info":info,
             "result":"success"
            })
            
            
        else:
            return jsonify(
            {
                "info":"no such operation",
             "result":"success"
            }
        )
        
        
     
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {
                "result":str(e)
            }
        )
