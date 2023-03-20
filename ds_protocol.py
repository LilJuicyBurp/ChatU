# Steven Deng
# sdeng5@uci.edu
# 47704456
import json
import socket
from collections import namedtuple

DataTuple = namedtuple('DataTuple', ['response', 'type'])

def directmessage(msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(('168.235.86.101', 3021))
        data = msg
        client.sendall(bytes(data, encoding='utf-8'))
        server_return = client.recv(4096)
        server_return = server_return.decode("utf-8")
        return server_return



def extract_json(json_msg: str) -> DataTuple:
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        type = json_obj['response']['type']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return DataTuple({'message': 'returned info can\' be read'}, 'error')
    return DataTuple(response, type)
