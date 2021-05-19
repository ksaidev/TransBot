import time
import os
import sys
import main

def present_time():
    now = time.localtime()
    return "[%04d/%02d/%02d %02d:%02d:%02d] " \
           % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)


try:
    print(present_time() + 'Server start')
    # imp.reload(imp.import_module('main.py'))
    # exec(open('main.py').read())
    main.run()
except ConnectionResetError:
    print(present_time() + 'Connection reset')

except Exception as e:
    print(present_time() + str(e))

print(present_time() + 'Connection Reset')
time.sleep(5)
os.execv(sys.executable, ['python'] + sys.argv)
