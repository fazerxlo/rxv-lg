# rxv-lg

Sample integration project to connect LG tv (WEB OS 2) to Yamaha RX-Vxxx receiver.

## Used libraries:

- https://github.com/wuub/rxv - **Yamaha API client**
- https://github.com/supersaiyanmode/PyWebOSTV - **LG API client**
- https://kodi.tv/ - **kodi-send**

## Target:
As a result Kodi plugin will be crated

## Status:
- power on tv using **kodi-send** command
- power off tv using **LG API**
- registering app on LG TV
- store LG webOS integration key in file
- receiver management using **Yamaha API**
- turning on TV will start receiver and set input to TV
- turning on Receiver an selecting TV or HDMI input will power up TV
- power off TV will power off Receiver if TV input were used
- power off Receiver when TV or HDMI input is selected will power off TV
- Receiver volume control using TV remote
- logging output to the file
- example startup script for libreelec

## Logs

By default log file *rxvlg.log* will be crated in script directory

**DEBUG**

For debug export 

`RXV_DEBUG=True`

When debug is enabled all output with additional logs will be send to console