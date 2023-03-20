import ds_messenger

ip = '168.235.86.101'
port = 3021


def test_join():
    test = ds_messenger.DirectMessenger(ip, 'LALakers', 'LakeShow')
    msg = test.client_join()
    print(msg)