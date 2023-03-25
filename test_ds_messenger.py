"""Unit tests for ds_messenger"""
import ds_messenger
DSUSERVER = '168.235.86.101'


def test_send():
    """Tests send function"""
    test = ds_messenger.DirectMessenger(DSUSERVER, 'LAClippers1', 'ClipShow')
    result = test.send('We are the better LA team', 'LALakers1')
    assert result is True
    test = ds_messenger.DirectMessenger(DSUSERVER, '', '')
    result = test.send(None, None)
    assert result is False


def test_send2():
    """Tests send function unsuccesfully"""
    test = ds_messenger.DirectMessenger(DSUSERVER, 'LAClippers1', 'ClipShow')
    result = test.send(None, None)
    assert result is False


def test_new():
    """Tests retrieve new function."""
    test = ds_messenger.DirectMessenger(DSUSERVER, 'LALakers1', 'LakeShow')
    result = test.retrieve_new()
    assert isinstance(result, list) is True
    assert isinstance(result[0], ds_messenger.DirectMessage) is True
    assert result[0].message == 'We are the better LA team'
    test = ds_messenger.DirectMessenger(DSUSERVER, '', '')
    result = test.retrieve_new()
    assert result is None


def test_all():
    """Tests retrieve all function."""
    test = ds_messenger.DirectMessenger(DSUSERVER, 'LALakers1', 'LakeShow')
    result = test.retrieve_all()
    assert isinstance(result, list) is True
    assert isinstance(result[0], ds_messenger.DirectMessage) is True
    test = ds_messenger.DirectMessenger(DSUSERVER, '', '')
    result = test.retrieve_all()
    assert result is None


def test_join_error():
    """Tests join function"""
    num = 0
    try:
        test = ds_messenger.DirectMessenger(DSUSERVER, 'LALakers1', 'LakeSho')
        msg = test.client_join()
        print(msg)
    except ds_messenger.JoinError:
        num = 1
    finally:
        assert num == 1
