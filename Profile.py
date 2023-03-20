# Steven Deng
# sdeng5@uci.edu
# 47704456
import json
import time
from pathlib import Path
from ds_messenger import DirectMessage


class DsuFileError(Exception):
    pass


class DsuProfileError(Exception):
    pass


class Post(dict):
    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        return self._entry

    def set_time(self, time: float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''             # OPTIONAL
        self._posts = []          # OPTIONAL
        self.friends = []
        self.sent = []
        self.messages = []

    def add_post(self, post: Post) -> None:
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list[Post]:
        return self._posts

    def save_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                msg = "Error while attempting to process the DSU file."
                raise DsuFileError(msg, ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")
    
    def get_sent(self):
        return_list = []
        for i in self.sent:
            dm_obj = DirectMessage()
            dm_obj.message = i['message']
            dm_obj.recipient = i['recipient']
            dm_obj.timestamp = i['timestamp']
            return_list.append(dm_obj)
        return return_list
    
    def get_messages(self):
        return_list = []
        for i in self.messages:
            dm_obj = DirectMessage()
            dm_obj.message = i['message']
            dm_obj.recipient = i['recipient']
            dm_obj.timestamp = i['timestamp']
            return_list.append(dm_obj)
        return return_list

    def load_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for i in obj['friends']:
                    self.friends.append(i)
                for i in obj['sent']:
                    self.sent.append(i)
                for i in obj['messages']:
                    self.messages.append(i)
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
