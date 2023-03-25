"""Unit tests for ds_protocol module."""
import json
import ds_protocol


def test_case_1():
    """Tests all and new requests."""
    msg = {"response": {"type": "ok",
                        "messages": [{"message": "Hello User 1!",
                                      "from": "markb",
                                      "timestamp": "1603167689.3928561"},
                                     {"message": "Bzzzzz",
                                      "from": "thebeemoviescript",
                                      "timestamp": "1603167689.3928561"}]}}
    test = ds_protocol.directmessage(json.dumps(msg))
    assert test.type == 'ok'
    assert test.response == {"type": "ok",
                             "messages": [{"message": "Hello User 1!",
                                           "from": "markb",
                                           "timestamp": "1603167689.3928561"},
                                          {"message": "Bzzzzz",
                                           "from": "thebeemoviescript",
                                           "timestamp": "1603167689.3928561"}]}


def test_case_2():
    """Tests direct message request."""
    msg = {"response": {"type": "ok", "message": "Direct message sent"}}
    test = ds_protocol.directmessage(json.dumps(msg))
    assert test.type == 'ok'
    assert test.response == {"type": "ok", "message": "Direct message sent"}


def test_case_3():
    """Tests json.JSONDecodeError."""
    num = 0
    try:
        msg = '"response": {"type": "ok", "message": "Direct message sent"}'
        test = ds_protocol.directmessage(msg)
    except ds_protocol.ProtocolError:
        num += 1
    assert num == 1


def test_case_4():
    """Tests json.JSONDecodeError."""
    num = 0
    try:
        msg = ["response", {"type": "ok", "message": "Direct message sent"}]
        test = ds_protocol.directmessage(json.dumps(msg))
    except ds_protocol.ProtocolError:
        num += 1
    assert num == 1
