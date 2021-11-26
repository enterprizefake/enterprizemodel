




class fileConfig:
    dbName="test"
    defaultBucket="testbucket"
    defaultCollection="Filedb"
    
    
# try:
#         state=deletefromMongo(mongo,id)
#         return jsonify(
#             {
#               "id":str(state),
#              "result":"success"
#             }
#         )
#     except Exception as e:
#         print(e)
#         return jsonify(
#             {
#                 "result":str(e)
#             }
#         )