dimsum
======

Home automation for dimmers and RGB lights. This is designed to run on a
dedicated computer (I run it on a Raspberry Pi) connected to an Arduino running
the RgbSerial sketch. Requires flask, gevent and Python 2.x. To run, use  
  
    python dimsum.py --dimmer /dev/dimmer-serial-port
