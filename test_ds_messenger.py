import ds_messenger
import json
ip = '168.235.86.101'

def test_send():
    test = ds_messenger.DirectMessenger(ip, 'LAClippers1', 'ClipShow')
    result = test.send('We are the better LA team', 'LALakers1')
    assert result == True

def test_send2():
    test = ds_messenger.DirectMessenger(ip, 'LAClippers1', 'ClipShow')
    result = test.send(None, None)
    assert result == False

def test_new():
    test = ds_messenger.DirectMessenger(ip, 'LALakers1', 'LakeShow')
    result = test.retrieve_new()
    assert type(result) == list
    assert type(result[0]) == ds_messenger.DirectMessage
    assert result[0].message == 'We are the better LA team'

def test_all():
    test = ds_messenger.DirectMessenger(ip, 'LALakers1', 'LakeShow')
    result = test.retrieve_all()
    assert type(result) == list
    assert type(result[0]) == ds_messenger.DirectMessage

def test_join_error():
    num = 0
    try:
        test = ds_messenger.DirectMessenger(ip, 'LALakers1', 'LakeSho')
        msg = test.client_join()
        print(msg)
    except ds_messenger.JoinError:
        num = 1
    finally:
        assert num == 1
