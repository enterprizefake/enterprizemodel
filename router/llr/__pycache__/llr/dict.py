def to_dict(data):
    dic=data.__dict__
    dic.pop('_sa_instance_state')
    return dic