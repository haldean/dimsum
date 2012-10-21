from gevent.server import StreamServer

def make_handle(dimmer):
  def handle(socket, address):
    for line in socket.makefile():
      h, s, v = [float(x) for x in line.split(',')]
      dimmer.write_hsv(h, s, v)
  return handle

def listen(dimmer, port=9000):
  server = StreamServer(('', port), make_handle(dimmer))
  server.start()
