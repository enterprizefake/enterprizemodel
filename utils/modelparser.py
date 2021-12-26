
from datetime import datetime,date

class SqlToDict:
    def __init__(self, data,notype=False) -> None:
        self.data = data.__dict__
        self.notype=notype

    def to_dict(self) :
        dict_=dict()
        for k,v in self.data.items():
            
            
            if(isinstance(v,str) or isinstance(v,int) or isinstance(v,float)):
                    dict_[k]=v
            elif isinstance(v, datetime):
                    dict_[k]=v.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(v, date):
                    dict_[k]=v.strftime('%Y-%m-%d')
            elif self.notype==True and v==None:
                    dict_[k]=v
        return dict_

def to_pythontime(str_):
    return datetime.strptime(str_, '%Y-%m-%d %H:%M:%S')

def tuple_merge_todict(tuple_):
        tuple_=list(tuple_)
        d={}
        for item in tuple_:
                d.update(SqlToDict(item,True).to_dict())
        return d
    