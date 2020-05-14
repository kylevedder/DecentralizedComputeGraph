import pickle

def serialize(data):
  if data is not None:
    return pickle.dumps(data)
  return None

def deserialize(data):
  if data is not None and data != b'':
    return pickle.loads(data)
  return None