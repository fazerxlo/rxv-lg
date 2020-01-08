import os


class RxvLogger:

    DEBUG_ENABLED = (os.environ.get('RXV_DEBUG') is not None)

    @staticmethod
    def log(txt):
        print(RxvLogger.__name__ + ": " + txt)

    @staticmethod
    def debug(txt):
        if RxvLogger.DEBUG_ENABLED:
            RxvLogger.log("DEBUG: " + txt)