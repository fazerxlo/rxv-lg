import re
import rxv
from logger import RxvLogger


class RxvLGYamaha:
    def __init__(self, url, name):
        RxvLogger.log("Yamaha connect ip: " + url)
        self.rv = rxv.RXV(url, name)

    def is_running(self):
        RxvLogger.debug("Yamaha running?: " + str(self.rv.on))
        return self.rv.on

    def is_tv_enabled(self):
        RxvLogger.debug("Yamaha input?: " + self.rv.input)
        return re.search(r"^((AV)|(HDMI))\d+$", self.rv.input) is not None

    def start_and_connect(self):
        RxvLogger.log("Yamaha power on")
        self.rv.on = True
        self.rv.input = 'AV1'

    def power_off(self):
        RxvLogger.log("Yamaha power off")
        self.rv.on = False

    def change_volume(self, value):
        vol = self.rv.volume
        RxvLogger.debug("Volume change: " + str(vol + value))
        self.rv.volume = vol + value

    def mute(self, state):
        RxvLogger.debug("Mute change change: " + str(state))
        self.rv.mute = state
