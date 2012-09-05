import serial

class scroller(object):
  def __init__(self, serial_device):
    self.port = serial.Serial(serial_device, 9600)

  def write(self, string):
    self.port.write(string)

