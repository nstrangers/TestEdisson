import pickle
import base64


def serialize(object):
    data = base64.b64encode(pickle.dumps(object)).decode("utf-8")
    return data


def deserialize(object_in_session):
    data = pickle.loads(base64.b64decode(object_in_session.encode("utf-8")))
    return data
