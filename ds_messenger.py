# Steven Deng
# sdeng5@uci.edu
# 47704456
import json
import time
import socket
import ds_protocol

class JoinError(Exception):
    """Module exception for when connection fails."""

class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
		
    def send(self, message:str, recipient:str) -> bool:
        token = self.client_join()
        msg = {"token":token, "directmessage": {"entry": message,
                                                "recipient":recipient,
                                                "timestamp": time.time()}}
        json_msg = json.dumps(msg)
        json_returned = self.client_send(json_msg)
        if json_returned.response['message'] == 'Direct message sent':
            return True
        else:
            return False
		
    def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
        token = self.client_join()
        msg = {"token":token, "directmessage": 'new'}
        json_msg = json.dumps(msg)
        json_returned = self.client_send(json_msg)
        return_list = []
        for i in json_returned.response['messages']:
            dm_obj = DirectMessage()
            dm_obj.message = i['entry']
            dm_obj.recipient = i['recipient']
            dm_obj.timestamp = i['timestamp']
            return_list.append(dm_obj)
        return dm_obj
 
    def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
        token = self.client_join()
        msg = {"token":token, "directmessage": 'all'}
        json_msg = json.dumps(msg)
        json_returned = self.client_send(json_msg)
        return_list = []
        for i in json_returned.response['messages']:
            dm_obj = DirectMessage()
            dm_obj.message = i['entry']
            dm_obj.recipient = i['recipient']
            dm_obj.timestamp = i['timestamp']
            return_list.append(dm_obj)
        return dm_obj

    def client_join(self):
        json1 = {"join": {"username": str(self.username), "password": str(self.password),
                        "token": ""}}
        json2 = json.dumps(json1)
        json_returned = self.client_send(json2)
        if json_returned.type == "error":
            raise JoinError(json_returned.response["message"])
        elif json_returned.type == "ok":
            return json_returned.response['token']
        else:
            raise JoinError(json_returned.response["message"])
        
    def client_send(server_address: str, server_port: int, json_message) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server_address, server_port))
            data = json_message
            client.sendall(bytes(data, encoding='utf-8'))
            server_return = client.recv(4096)
            server_return = server_return.decode("utf-8")
            return ds_protocol.directmessage(server_return)