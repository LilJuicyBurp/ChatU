# Steven Deng
# sdeng5@uci.edu
# 47704456
import json
import socket
from collections import namedtuple

DataTuple = namedtuple('DataTuple', ['response', 'type'])

def directmessage(json_msg: str) -> DataTuple:
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        type = json_obj['response']['type']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return DataTuple({'message': 'returned info can\' be read'}, 'error')
    return DataTuple(response, type)
