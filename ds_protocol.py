"""Protcol for communicating with DSP server"""
# Steven Deng
# sdeng5@uci.edu
# 47704456
import json
from collections import namedtuple


class ProtocolError(Exception):
    """Module specific error"""


DataTuple = namedtuple('DataTuple', ['response', 'type'])


def directmessage(json_msg: str) -> DataTuple:
    """Deciphers DSP server return."""
    try:
        json_obj = json.loads(json_msg)
        msg = json_obj['response']
        typ = json_obj['response']['type']
    except json.JSONDecodeError:
        raise ProtocolError
    except TypeError:
        raise ProtocolError
    return DataTuple(msg, typ)
