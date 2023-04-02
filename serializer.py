import pickle
import base64


def serializer(obj):
    data = base64.b64encode(pickle.dumps(obj)).decode("utf-8")
    return data


def deserializer(request, object_in_session):
    data = pickle.loads(base64.b64decode(request.session.get(object_in_session).encode("utf-8")))
    return data
