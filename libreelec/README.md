#LIBREELEC installation

Libreelec is the first multimedia OS that support my Raspberry pi 4

##Install required Python modules 

As a simple/safe mediacenter it is the very basic setup of tools and system is in read only mode:
- no way to install packages
- no way from cosle to install  python packages in system path

Enable ssh and login https://wiki.libreelec.tv/accessing_libreelec

Download pip installer:

`curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`

Install 

`python get-pip.py --user`

Add pip to path:

`export PATH=$PATH:/storage/.local/bin`

Install dependencies 

- rxv:
`pip install rxv --user`

- PyWebOSTV (unfortunately we cannot compile binaries of modules and we have to do some hacks)

`pip install PyWebOSTV --user --no-deps`

- PyWebOSTV used dependencies:

`pip install pyaml ws4py future --user`

###Run program

Copy sources to sample folder

`mkdir /storage/rxvlg`

Run program

`python /storage/rxvlg/rxvlg.py`

###Run program on startup

You can use startup Libreelec functionality 

You can use sample `autostart.sh` script

`cp /storage/rxvlg/libreelec/autostart.sh /storage/.config/`

It is recomended to terminate program before shutdown/reboot

You can use sample `shutdown.sh` script

`cp /storage/rxvlg/libreelec/shutdown.sh /storage/.config/`


