# rxv-lg

Sample integration project to connect LG tv (WEB OS 2) to Yamaha RX-Vxxx receiver.

## Used libraries:

- https://github.com/wuub/rxv - **Yamaha API client**
- https://github.com/supersaiyanmode/PyWebOSTV - **LG API client**
- https://github.com/trainman419/python-cec - **HDMI CEC client**

## Target:
As a result Kodi plugin will be crated

## Status:
- power on tv using **HDMI CEC** command
- power off tv using **LG API**
- receiver management using **Yamaha API**
- powering on tv will start receiver and set input to TV
- poweting on Receiver an selecting TV will power up TV
- power off TV will power off receiver if TV input were used
- power off receiver wneh TV is selected will power off TV
- volume control using TV remote
