import sys
import time
import subprocess
import socket

import yaml
from pywebostv.connection import WebOSClient
from pywebostv.controls import SystemControl, MediaControl
from logger import RxvLogger


class RxvLGTv:
    KEY_FILE = sys.path[0] + '/authkey.yaml'
    WEBOS_PORT = 3000

    def __init__(self, ip):
        self.ip = ip
        RxvLogger.log("TV connect ip: " + self.ip)
        self.store = {}

    def is_running(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # 2 Second Timeout
        result = sock.connect_ex((self.ip, RxvLGTv.WEBOS_PORT))
        return result == 0

    def run_os_command(self, args):
        try:
            # stdout = subprocess.PIPE lets you redirect the output
            RxvLogger.debug(' '.join(args))
            res = subprocess.Popen(args, stdout=subprocess.PIPE)
        except OSError:
            RxvLogger.error("error: popen")
            exit(-1)  # if the subprocess call failed, there's not much point in continuing

        res.wait()  # wait for process to finish; this also sets the returncode variable inside 'res'
        if res.returncode != 0:
            RxvLogger.debug("  os.wait:exit status != 0\n")
        else:
            RxvLogger.debug("os.wait:({},{})".format(res.pid, res.returncode))

            # access the output from stdout
            result = res.stdout.read()
            RxvLogger.debug("after read: {}".format(result))

        return res.returncode

    def start(self):
        RxvLogger.log("TV power on")
        trying = 0
        while trying < 10:
            self.run_os_command(['/usr/bin/kodi-send', '-a', 'CECActivateSource'])
            time.sleep(2)
            if self.is_running():
                trying = 11
            elif trying > 10:
                RxvLogger.error("Could not turn on TV")
                return
            else:
                RxvLogger.debug("Retrying connect TV")
                time.sleep(1)
        time.sleep(30)

    def register_volume_control(self, callback):
        lg = self.connect()
        media = MediaControl(lg)
        RxvLogger.debug("callback registered")
        media.subscribe_get_volume(callback)

    def power_off(self):
        self.check_and_create_store()
        lg = self.connect()
        lg_sys = SystemControl(lg)
        RxvLogger.log("TV power off")
        lg_sys.notify("RxvLG: TV will be power off!")
        time.sleep(2)
        lg_sys.power_off()
        lg.close()
        time.sleep(2)

    def connect(self):

        if not self.is_running():
            self.start()
        RxvLogger.debug("TV connect ip:" + self.ip)
        for i in range(0, 10):
            try:
                lg = WebOSClient(self.ip)
                lg.connect()
            except Exception as e:
                RxvLogger.error("Unable connect TV, retry e: " + str(e))
                time.sleep(3)
            else:
                break
        try:
            for status in lg.register(self.store):
                if status == WebOSClient.PROMPTED:
                    RxvLogger.log("Please accept the connect on the TV!")
                elif status == WebOSClient.REGISTERED:
                    RxvLogger.log("Registration successful!")
                    lg_sys = SystemControl(lg)
                    lg_sys.notify("RxvLG: Registration successful!")
            self.save_store()
            return lg
        except Exception as e:
            RxvLogger.error("Registration failed exiting!")
            RxvLogger.debug("Exception" + str(e))
            #sys.exit(1)

    def check_and_create_store(self):
        RxvLogger.debug("TV connect read key")

        try:
            with open(RxvLGTv.KEY_FILE, 'r+') as file:
                self.store = yaml.full_load(file)
        except IOError:
            self.store = {}

        RxvLogger.debug("TV connect key:" + str(self.store))
        if not self.key_correct():
            RxvLogger.log("TV connect key empty will be created")
            self.store = {}

    def save_store(self):
        RxvLogger.debug("TV connect key stored: " + str(self.store))
        with open(RxvLGTv.KEY_FILE, 'w') as file:
            yaml.dump(self.store, file)

    def setup(self):
        self.check_and_create_store()
        if not self.key_correct():
            RxvLogger.log("LG key required please accept connection on tv:")
            if not self.is_running():
                RxvLogger.log("Turning on TV and wait for boot 10s")
                self.start()
                time.sleep(10)
            self.connect()

    def key_correct(self):
        return self.store is not None and 'client_key' in self.store
