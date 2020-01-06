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

    def run(self):

        while True:
            self.get_yamaha_running_tv()
            self.get_tv_running()

            RxvLogger.debug("Status:" + str(self.running) + " Amplifier: " + str(self.yh_running) + " TV: " + str(self.tv_running))
            if self.running is False and (self.yh_tv_running is not self.tv_running):
                self.connect_all()
            elif self.running is True and (self.yh_running is not self.tv_running):
                self.power_off_all()

            time.sleep(5)

    def get_yamaha_running_tv(self):
        self.yh_running = self.amplifier.is_running()
        self.yh_tv_running = (self.yh_running and self.amplifier.is_tv_enabled())

    def get_tv_running(self):
        self.tv_running = self.tv.is_running()

    def connect_all(self):
        RxvLogger.log("Connecting...")
        if self.yh_tv_running is False:
            RxvLogger.log("Starting amplifier")
            self.amplifier.start_and_connect()
            self.running = True
        elif self.tv_running is False:
            RxvLogger.log("Starting TV")
            self.tv.start()
            self.running = True
            self.tv.register_volume_control(self.volume_control_callback)

    def power_off_all(self):
        RxvLogger.log("Disconnecting...")
        if self.amplifier.is_running() is True:
            RxvLogger.log("Power off amplifier")
            self.amplifier.power_off()
            self.running = False
        elif self.tv_running is True:
            RxvLogger.log("Power off TV")
            self.tv.power_off()
            self.running = False

    def volume_control_callback(self, status, payload):
        if status:
            print(payload)
        else:
            print("Something went wrong.")



if __name__ == '__main__':

    rxl = RxvLG()
    rxl.run()
