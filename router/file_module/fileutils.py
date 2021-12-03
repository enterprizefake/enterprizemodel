
from flask_pymongo import PyMongo,MongoClient
import gridfs
from flask_pymongo import wrappers
from .fileconfig import fileConfig
from werkzeug.datastructures import FileStorage
from bson.objectid import ObjectId

def uploadtoMongo(mongo:MongoClient,file_:FileStorage,):
    bucket=gridfs.GridFSBucket(mongo[fileConfig.dbName],bucket_name=fileConfig.defaultBucket)
    # id=bucket.upload_from_stream(
    #     file_.filename,file_.stream,
    #     metadata={"contentType": "text/plain",
    #               "content_type": "text/plain",
                
    #               }
    
    #     # metadata=
    #     #     file_.mimetype_params.items()
        
    # )
    with  bucket.open_upload_stream(file_.filename,
                    metadata={"contentType": file_.mimetype,
                  "content_type": file_.mimetype,
                
                  }) as file_in:
        file_in.content_type=file_.mimetype
        file_in.write(file_.stream)
        file_in.close()
    print(file_.mimetype,file_.filename)
    i=file_in
    return (
        {     "name":i.name,
               "lenth":i.length,
              "ch_size":i.chunk_size,
            "con_type":i.content_type,
            "id":str(i._id),
           "last_date":i.upload_date,
          "md5":i.md5,}
    )
    pass


def downloadfromMongo(mongo:MongoClient,id:str)->gridfs.GridOut:
    """
    返回为none表示不存在文件
    """
    bucket=gridfs.GridFSBucket(mongo[fileConfig.dbName],bucket_name=fileConfig.defaultBucket)
    # bucket.download_to_stream(id)
    allname=bucket.find({"_id":ObjectId(id)})
    # bucket.open_download_stream(id)
    # obj:gridfs.GridOut
    
    obj=None
    for i in allname:
        
        obj=i
    
    return obj

def deletefromMongo(mongo:MongoClient,id:str):
    '''
    None表示无对应id
    '''
    bucket=gridfs.GridFSBucket(mongo[fileConfig.dbName],bucket_name=fileConfig.defaultBucket)
    find_=bucket.find({"_id":ObjectId(id)})
    if(find_.next()==None):
        return None
    bucket.delete(ObjectId(id))
    return id


def updatetoMongo(mongo:MongoClient,id:str,file_:FileStorage):
    
    '''
    
    '''
    bucket=gridfs.GridFSBucket(mongo[fileConfig.dbName],bucket_name=fileConfig.defaultBucket)
    find_=bucket.find({"_id":ObjectId(id)})
    if(find_.next()==None):
        return None
    
    
    '''
    uploadfile
    '''
    ret_id=None
    
    with  bucket.open_upload_stream(file_.filename,
                    metadata={"contentType": file_.mimetype,
                  "content_type": file_.mimetype,
                
                  }) as file_in:
        file_in.content_type=file_.mimetype
        file_in.write(file_.stream)
        file_in.close()

    ret_id=file_in._id
    
    
    '''
    deletefile
    '''
    bucket.delete(ObjectId(id))
    
    return ret_id









    