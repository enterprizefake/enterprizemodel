from flask_pymongo import PyMongo,MongoClient
import flask_pymongo
import gridfs
from pymongo import cursor
from flask_pymongo import wrappers
from sqlalchemy import false, null, true
from .fileconfig import fileConfig
from werkzeug.datastructures import FileStorage
from bson.objectid import ObjectId
from bson.json_util import dumps
import bson

# def getpathinfo(bsonobj,path):


#utils-------------------------------------------------   
def hasreaptedfolder(steps,collection_:wrappers.Collection):
    Cursor_result=collection_.find(
        {
            {".".join(steps): { '$exists': True }}
        }
    )
    if Cursor_result.count()>0:
        return (None,"repeated folder")
    
    return("success","non repeated")

def hasfolderfile(steps,collection_:wrappers.Collection,file_id):
    Cursor_result=collection_.find(
        {
            ".".join(steps)+".?files?": {
                    "$in":[file_id]
            }
            
            # ".".join(steps)+".?files?": {
            #       '$exists': True
                        
                    
            # }
            
        }
    )
    print("has folder",steps,file_id)
    if Cursor_result.count()>0:
        return ("success","right path")
    
    return(None,"false path")
    




def pathparser(rootpath:str):
    steps=rootpath.split("/")
    steps[0]='root'
    return steps


def haspath(steps,projectroot:dict):
    
    now_step=projectroot
    updatetrackroot:dict
    update_track=dict()
    updatetrackroot=update_track
    for i in steps:
        
        now_step=now_step.get(i,None)
        # print("nowstep",now_step)
        # print("fetch",i)
        if now_step==None:
            return(
                false,"no such path"
            )
        update_track[i]=dict()
        update_track=update_track[i]
    
    
          
    
    return (true,"has path")
def findpathsubfiles(steps,projectroot:dict):
    
    now_step=projectroot
    files=[]
   
    
    refs=dict()
    
    updatetrackroot:dict
    update_track=dict()
    updatetrackroot=update_track
    
    for i in steps:
        # files+=now_step.get("files",[])
        now_step_back=now_step
        
        now_step=now_step.get(i,None)
        refs['now']=now_step
        # print("nowstep",now_step)
        # print("fetch",i)
        if now_step==None:
            return(
                None,"no such path"
            )
        update_track[i]=dict()
        update_track=update_track[i]
    
    
    def walk(d):
      for k, v in d.items():
        if isinstance(v, dict):
           walk(v)
        else:
            # print("k",k)
            if k=='?files?' and isinstance(v,list):
                # print("?files",v)
                files.extend(v)
    
    
    print("nowstep:",refs['now'])
    walk(refs['now'])

    # print("walk",now_step_back)           
    
    
    return (files,"has path")
# utils------------------------------------------------end




def createProjectRootFolder(rootname,collection_:wrappers.Collection):
    result=collection_.insert_one(
        {
            "root":{
                rootname:{"?files?":[]}
            }
        }
    )
    return result
 


  
def createfolder(projectfileid,rootpath:str,foldername:str,collection_:wrappers.Collection):
    steps=rootpath.split("/")
    steps[0]='root'
    # print(steps)
    projectroot:dict
    
    projectroot=collection_.find_one(
        {
            "_id":ObjectId(projectfileid)
        }
    )
    
    
    
    
    if projectroot==None:
        return (None,"no such project")
    
    # return(type(projectroot),"test")

    
    now_step=projectroot
    
    
    
    
    updatetrackroot:dict
    update_track=dict()
    updatetrackroot=update_track
    for i in steps:
        
        now_step=now_step.get(i,None)
        # print("nowstep",now_step)
        # print("fetch",i)
        if now_step==None:
            return(
                None,"no such path"
            )
        update_track[i]=dict()
        update_track=update_track[i]
        
    
    # print("track:",update_track)
    
    steps.append(foldername)
    
    
    '''
    check folder repeated
    '''
    Cursor_result=collection_.find(
        
            {".".join(steps): { '$exists': True }}
        
    )
    if Cursor_result.count()>0:
        return (None,"repeated folder")
    
    
    
    
    collection_.update_one(
        {
          "_id":ObjectId(projectfileid)
        },
        {
            "$set":{
                ".".join(steps):{"?files?":[]}
            }
        }
    )
    return(
                None,"addfolder_success"
            )
    pass







def deletefolder(projectfileid,rootpath:str,collection_:wrappers.Collection,mongo:flask_pymongo.MongoClient):
    projectroot:dict
    
    projectroot=collection_.find_one(
        {
            "_id":ObjectId(projectfileid)
        }
    )
    
    if projectroot==None:
        return (None,"no such project_id")
    
    steps=pathparser(rootpath)
    (result,info)=haspath(steps,projectroot)
    if result==false:
        return(None,"no such path")
    
    
    '''
    recursive delete file needs function
    '''
   
    
    
    (files,info)=findpathsubfiles(steps,projectroot)
    
    print("steps",steps)
    print("projectroot",projectroot)
    print("files:",files)
    
    
    from .fileutils import deletefromMongo
    if files!=None:
        for file_id in files:
            deletefromMongo(mongo,file_id)
    
    
    
    collection_.update_one(
        {
          "_id":ObjectId(projectfileid)
        },
        {
            "$unset":{
                 ".".join(steps):""
            }
        }
    )
    return(
                None,"deletefolder_success"
            )


def updatefolder(projectfileid,rootpath:str,newfoldername:str,collection_:wrappers.Collection):
    projectroot:dict
    
    projectroot=collection_.find_one(
        {
            "_id":ObjectId(projectfileid)
        }
    )
    
    if projectroot==None:
        return (None,"no such project_id")
    
    steps=pathparser(rootpath)
    (result,info)=haspath(steps,projectroot)
    if result==false:
        return(None,"no such path")
    
    
    
    collection_.update_one(
        {
          "_id":ObjectId(projectfileid)
        },
        {
            "$rename":{
                 ".".join(steps):(".".join(steps[0:-1])+'.'+newfoldername)
            }
        }
    )
    return(
                None,"updatefolder_success"
            )



from werkzeug.datastructures import FileStorage
def createfile(projectfileid,rootpath:str,file_:FileStorage,collection_:wrappers.Collection,mongo:flask_pymongo.MongoClient):
    
    projectroot:dict
    
    projectroot=collection_.find_one(
        {
            "_id":ObjectId(projectfileid)
        }
    )
    
    if projectroot==None:
        return (None,"no such project_id")
    
    steps=pathparser(rootpath)
    (result,info)=haspath(steps,projectroot)
    if result==false:
        return(None,"no such path")
    
    
    from .fileutils import uploadtoMongo
    
    file_id=uploadtoMongo(mongo,file_)
    
    
    
    collection_.update_one(
        {
          "_id":ObjectId(projectfileid)
        },
        {
            "$push":{
                 ".".join(steps)+".?files?":str(file_id['id'])
            }
        }
    )
    return(
                file_id,"createfile_success"
            )
    
    
    pass


def updatefile(file_id:str,file_name:str,bucket_:gridfs.GridFSBucket):
    '''
    更新名称
    (True,"success")
    '''
    
    Cursor_=bucket_.find({
        "_id":ObjectId(file_id)
    })
    if Cursor_.count()==0:
        return (None,"no such file")
    
    bucket_.rename(ObjectId(file_id),file_name)
        
    
    return (True,"updatefile_success")
        
    
    
    
    
    pass

def deletefile(projectfileid,rootpath:str,file_id:str,collection_:wrappers.Collection,bucket_:gridfs.GridFSBucket
               ,mongo:flask_pymongo.MongoClient
               ):
    '''
    删除文件
    '''
    
    Cursor_=bucket_.find({
        "_id":ObjectId(file_id)
    })
    if Cursor_.count()==0:
        return (None,"no such file")
    
    
   
    projectroot:dict
    
    projectroot=collection_.find_one(
        {
            "_id":ObjectId(projectfileid)
        }
    )
    
    if projectroot==None:
        return (None,"no such project_id")
    
    steps=pathparser(rootpath)
    (result,info)=haspath(steps,projectroot)
    if result==false:
        return(None,"no such path")
    
    (obj,info)=hasfolderfile(steps,collection_,file_id)
    if obj==None:
        return(None,"no such file with path")
    
    from .fileutils import deletefromMongo
    result= deletefromMongo(mongo,file_id)
    if result==None:
        return(None,"deletefile_fail")
    
    
    collection_.update_one(
        {
          "_id":ObjectId(projectfileid)
        },
        {
            "$pull":{
                 ".".join(steps)+".?files?":str(file_id)
            }
        }
    )
    
    
    return(None,"deletefile_success")
    
    
    pass
    
    
    


