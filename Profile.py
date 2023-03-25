"""Profile class which stores user information."""
# Steven Deng
# sdeng5@uci.edu
# 47704456
import json
from pathlib import Path
from ds_messenger import DirectMessage


class DsuFileError(Exception):
    """Custom exception to show file error"""



class DsuProfileError(Exception):
    """Custom exception to show profile error"""



class Profile:
    """Stores User information."""
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.friends = []
        self.sent = []
        self.messages = []

    def save_profile(self, path: str) -> None:
        """Saves Profile information into file"""
        path_ = Path(path)

        if path_.exists() and path_.suffix == '.dsu':
            try:
                with open(path_, 'w', encoding='utf-8') as file:
                    json.dump(self.__dict__, file)
            except Exception as ex:
                msg = "Error while attempting to process the DSU file."
                raise DsuFileError(msg, ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def get_sent(self):
        """Returns all sent messages of DM objects"""
        return_list = []
        for i in self.sent:
            dm_obj = DirectMessage()
            dm_obj.message = i['message']
            dm_obj.recipient = i['recipient']
            dm_obj.timestamp = i['timestamp']
            return_list.append(dm_obj)
        return return_list

    def get_messages(self):
        """Returns all messages of DM objects"""
        return_list = []
        for i in self.messages:
            dm_obj = DirectMessage()
            dm_obj.message = i['message']
            dm_obj.recipient = i['recipient']
            dm_obj.timestamp = i['timestamp']
            return_list.append(dm_obj)
        return return_list

    def load_profile(self, path: str) -> None:
        """Loads file info into attributes."""
        path_ = Path(path)

        if path_.exists() and path_.suffix == '.dsu':
            try:
                with open(path_, 'r', encoding='utf-8') as file:
                    obj = json.load(file)
                    self.username = obj['username']
                    self.password = obj['password']
                    self.dsuserver = obj['dsuserver']
                    for i in obj['friends']:
                        self.friends.append(i)
                    for i in obj['sent']:
                        self.sent.append(i)
                    for i in obj['messages']:
                        self.messages.append(i)
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
