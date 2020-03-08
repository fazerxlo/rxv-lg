import os
import sys
from datetime import datetime

class RxvLogger:

    LOG_FILE = sys.path[0] + '/rxvlg.log'
    DEBUG_ENABLED = (os.environ.get('RXV_DEBUG') is not None)



    @staticmethod
    def log(txt):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        txt = RxvLogger.__name__ + ":(" + current_time + ") " + txt
        if RxvLogger.DEBUG_ENABLED:
            print(txt)
        else:
            RxvLogger.write_to_file(txt)

    @staticmethod
    def debug(txt):
        if RxvLogger.DEBUG_ENABLED:
            RxvLogger.log("DEBUG: " + txt)

    @staticmethod
    def error(txt):
        RxvLogger.log("ERROR: " + txt)

    @staticmethod
    def write_to_file(txt):
        with open(RxvLogger.LOG_FILE, 'a+') as file:
            file.write(txt+"\n")
