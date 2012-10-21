import SocketServer

class SocketApiServer(SocketServer.StreamRequestHandler):
  def handle(self):
    for line in self.rfile:
      h, s, v = [float(x) for x in line.split(',')]
      self.dimmer.write_hsv(h, s, v)

def listen(dimmer, port=9000):
  SocketApiServer.dimmer = dimmer
  server = SocketServer.TCPServer(('', port), SocketApiServer)
  server.serve_forever()
