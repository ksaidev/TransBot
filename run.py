import time
import os
import sys
from src.script import main

def present_time():
    now = time.localtime()
    return "[%04d/%02d/%02d %02d:%02d:%02d] " \
           % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)


print(present_time() + 'Server start')
main.run()
time.sleep(2)
os.execv(sys.executable, ['python'] + sys.argv)
