import ds_messenger

ip = '168.235.86.101'

def test_join():
    test = ds_messenger.DirectMessenger(ip, 'LALakers', 'LakeShow')
    msg = test.client_join()
    print(msg)

def test_send():
    test = ds_messenger.DirectMessenger(ip, 'LAClippers', 'ClipShow')
    result = test.send('We are the better LA team', 'LALakers')
    assert result == True

def test_new():
    test = ds_messenger.DirectMessenger(ip, 'LALakers', 'LakeShow')
    result = test.retrieve_new()
    assert type(result) == list

def test_all():
    test = ds_messenger.DirectMessenger(ip, 'LALakers', 'LakeShow')
    result = test.retrieve_all()
    assert type(result) == list