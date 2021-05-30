from src.script.logging import Logging
import os
import sys
from src.script import main

print('')
Logging.console('Server start')
main.run()
os.execv(sys.executable, ['python'] + sys.argv)
