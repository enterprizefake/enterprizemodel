from io import TextIOWrapper
import io
from flask_pymongo import PyMongo,MongoClient
import gridfs
from flask_pymongo import wrappers
from matplotlib.cbook import file_requires_unicode
from .fileconfig import fileConfig
from werkzeug.datastructures import FileStorage



from io import BytesIO

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
    return file_in._id
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
    