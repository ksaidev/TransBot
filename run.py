from src.bot.logging import Logging
import os
import sys
from src import main

print('')
Logging.console('Server start')
main.run()
os.execv(sys.executable, ['python'] + sys.argv)
