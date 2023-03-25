"""Module that handles communication with DPS server."""
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
    """Stores info about messages"""
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    """Contains Server interaction methods"""
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password

    def send(self, message: str, recipient: str) -> bool:
        """Sends message to contact and returns the outcome."""
        try:
            token = self.client_join()
            msg = {"token": token, "directmessage": {"entry": message,
                                                     "recipient": recipient,
                                                     "timestamp": time.time()}}
            json_msg = json.dumps(msg)
            json_returned = self.client_send(json_msg)
            if json_returned.response['message'] == 'Direct message sent':
                return True
            return False
        except JoinError:
            return False
        except ds_protocol.ProtocolError:
            return False

    def retrieve_new(self) -> list:
        """Retrieve new messages and returns a list of DM objects."""
        try:
            token = self.client_join()
            msg = {"token": token, "directmessage": 'new'}
            json_msg = json.dumps(msg)
            json_returned = self.client_send(json_msg)
            return_list = []
            for i in json_returned.response['messages']:
                dm_obj = DirectMessage()
                dm_obj.message = i['message']
                dm_obj.recipient = i['from']
                dm_obj.timestamp = i['timestamp']
                return_list.append(dm_obj)
            return return_list
        except JoinError:
            return None
        except ds_protocol.ProtocolError:
            return None

    def retrieve_all(self) -> list:
        """Retrieve all messages and returns a list of DM objects."""
        try:
            token = self.client_join()
            msg = {"token": token, "directmessage": 'all'}
            json_msg = json.dumps(msg)
            json_returned = self.client_send(json_msg)
            return_list = []
            for i in json_returned.response['messages']:
                dm_obj = DirectMessage()
                dm_obj.message = i['message']
                dm_obj.recipient = i['from']
                dm_obj.timestamp = i['timestamp']
                return_list.append(dm_obj)
            return return_list
        except JoinError:
            return None
        except ds_protocol.ProtocolError:
            return None

    def client_join(self):
        """Connects to server and returns token."""
        try:
            json1 = {"join": {"username": str(self.username),
                            "password": str(self.password),
                            "token": ""}}
            json2 = json.dumps(json1)
            json_returned = self.client_send(json2)
            if json_returned.type == "error":
                raise JoinError(json_returned.response["message"])
            if json_returned.type == "ok":
                return json_returned.response['token']
        except ds_protocol.ProtocolError:
            raise ds_protocol.ProtocolError

    def client_send(self, msg: json) -> None:
        """Sends info to server and returns decode server response"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, 3021))
                client.sendall(bytes(msg, encoding='utf-8'))
                server_return = client.recv(1000000)
                server_return = server_return.decode("utf-8")
                tupl = ds_protocol.directmessage(server_return)
                return tupl
        except ds_protocol.ProtocolError:
            raise ds_protocol.ProtocolError
