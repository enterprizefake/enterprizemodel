
from datetime import datetime

class SqlToDict:
    def __init__(self, data) -> None:
        self.data = data.__dict__

    def to_dict(self) :
        dict_=dict()
        for k,v in self.data.items():
             
            if(isinstance(v,str) or isinstance(v,int) or isinstance(v,float)):
                dict_[k]=v
            elif isinstance(v, datetime):
                dict_[k]=int(datetime.timestamp(v))

        return dict_