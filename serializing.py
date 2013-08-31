import pickle

def serialize(thing):
    return pickle.dumps(thing)

def unserialize(string):
    return pickle.loads(string)
