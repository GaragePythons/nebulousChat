import pickle

def serialize(object):
    return pickle.dumps(object)

def unserialize(string):
    return pickle.loads(string)
