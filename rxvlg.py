import time

from tv import RxvLGTv
from amp import RxvLGYamaha
from logger import RxvLogger


class RxvLG:

    def __init__(self):
        self.running = False
        self.amplifier = RxvLGYamaha("http://192.168.0.4:80/YamahaRemoteControl/ctrl", "RX-V477")
        self.tv = RxvLGTv("192.168.0.6")
        self.tv_running = False
        self.yh_tv_running = False
        self.yh_running = False
        RxvLogger.log("Starting")
        self.tv.setup()
        if self.get_tv_running():
            self.tv.register_volume_control(self.volume_control_callback)

    def run(self):

        while True:
            self.get_yamaha_running_tv()
            self.get_tv_running()

            RxvLogger.debug("Status:" + str(self.running) + " Amplifier: " + str(self.yh_running) +
                            " Amplifier TV input: " + str(self.yh_tv_running) + " TV: " + str(self.tv_running))

            if not self.running:
                if self.yh_tv_running and self.tv_running:
                    self.running = True
                elif self.tv_running and not self.yh_running and not self.yh_tv_running:
                    self.connect_all()
                elif not self.tv_running and self.yh_tv_running:
                    self.connect_all()
            else:
                if self.tv_running and self.yh_tv_running:
                    None
                elif self.tv_running and not self.yh_running and not self.yh_tv_running:
                    self.power_off_all()
                elif not self.tv_running and self.yh_tv_running:
                    self.power_off_all()
                else:
                    self.running = False

            time.sleep(5)

    def get_yamaha_running_tv(self):
        self.yh_running = self.amplifier.is_running()
        self.yh_tv_running = (self.yh_running and self.amplifier.is_tv_enabled())
        return self.yh_tv_running

    def get_tv_running(self):
        self.tv_running = self.tv.is_running()
        return self.tv_running

    def connect_all(self):
        RxvLogger.log("Connecting...")
        if not self.yh_tv_running:
            RxvLogger.log("Starting amplifier")
            self.amplifier.start_and_connect()
            self.running = True
        elif not self.tv_running:
            RxvLogger.log("Starting TV")
            self.tv.start()
            self.running = True
        self.tv.register_volume_control(self.volume_control_callback)

    def power_off_all(self):
        RxvLogger.log("Disconnecting...")
        if self.amplifier.is_running():
            RxvLogger.log("Power off amplifier")
            self.amplifier.power_off()
            self.running = False
        elif self.tv_running:
            RxvLogger.log("Power off TV")
            self.tv.power_off()
            self.running = False

    def volume_control_callback(self, status, payload):
        RxvLogger.debug("Volume action")
        if status:
            if u'changed' in payload:
                if u'cause' in payload and payload[u'changed'] == [u'volume']:
                    if payload[u'cause'] == u'volumeDown':
                        self.amplifier.change_volume(-0.5)
                    elif payload[u'cause'] == u'volumeUp':
                        self.amplifier.change_volume(0.5)
                elif u'muted' in payload and payload[u'changed'] == [u'muted']:
                    self.amplifier.mute(payload[u'muted'])

            RxvLogger.debug(str(payload))
        else:
            RxvLogger.debug("Something went wrong.")


if __name__ == '__main__':

    rxl = RxvLG()
    rxl.run()
