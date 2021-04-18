import time
import importlib as imp

def present_time():
    now = time.localtime()
    return "[%04d/%02d/%02d %02d:%02d:%02d] " % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)


while True:
    try:
        print(present_time() + 'Server start')
        imp.reload(imp.import_module('main.py'))

    except ConnectionResetError:
        pass

    except Exception as e:
        print(present_time() + str(e))

    print(present_time() + 'Server reload')
    time.sleep(5)

