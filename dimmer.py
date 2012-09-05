import serial

class dimmer(object):
  def __init__(self, serial_device):
    if serial_device:
      self.port = serial.Serial(serial_device, 9600)
    else:
      import sys
      self.port = sys.stdout
    self.levels = 0, 0, 0

  def set_level(self, r, g, b):
    def write_rgb(r, g, b):
      level = lambda x: int(255 * x)
      outstr = '%d %d %d\n' % (level(r), level(g), level(b))
      self.port.write(outstr)
      
    steps = 100
    sr, sg, sb = self.levels
    step_size = lambda sx, x: float(x - sx) / float(steps)
    step_r, step_g, step_b = \
        step_size(sr, r), step_size(sg, g), step_size(sb, b)

    for x in range(steps):
      write_rgb(sr + x * step_r, sg + x * step_g, sb + x * step_b)
    write_rgb(r, g, b)
    self.levels = (r, g, b)

  @property
  def level(self):
    return self.levels

  def zero(self):
    self.set_level(0, 0, 0)
