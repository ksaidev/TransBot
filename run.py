import time

def present_time():
    now = time.localtime()
    return "[%04d/%02d/%02d %02d:%02d:%02d] " % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)


while True:
    try:
        print(present_time() + 'Server start')
        import Main

    except ConnectionResetError:
        pass

    except Exception as e:
        print(present_time() + str(e))

    print(present_time() + 'Connection Reset')
    time.sleep(5)

