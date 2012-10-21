import dimmer
import flask
import json
import scroller

def flask_app(dim, scroll):
  app = flask.Flask(__name__)

  def color_definitions():
    try:
      with open('color-defs.json', 'r') as f:
        return json.load(f)
    except (IOError, ValueError):
      return {}

  def write_color_definitions(defs):
    with open('color-defs.json', 'w') as f:
      json.dump(defs, f)

  def add_color_definition(name):
    defs = color_definitions()
    defs[name] = dim.level
    write_color_definitions(defs)

  def del_color_definition(name):
    defs = color_definitions()
    if name in defs:
      del defs[name]
      write_color_definitions(defs)

  def color_names():
    return sorted(name for name in color_definitions().iterkeys())

  @app.route('/scroll')
  def scroll_message():
    scroll.write(flask.request.args['message'])
    return flask.redirect('/')

  @app.route('/rgbapi')
  def api():
    dim.write_rgb(
        float(flask.request.args['r']),
        float(flask.request.args['g']),
        float(flask.request.args['b']))
    return flask.Response('OK', mimetype='text/plain')

  @app.route('/')
  def main():
    if 'red' in flask.request.args:
      level = lambda x: float(flask.request.args[x])
      dim.set_level(level('red'), level('green'), level('blue'))
      return flask.redirect('/')

    elif 'name' in flask.request.args:
      if 'name' in flask.request.args:
        add_color_definition(flask.request.args['name'])
      return flask.redirect('/')

    elif 'load' in flask.request.args:
      defs = color_definitions()
      preset = flask.request.args['load']
      if preset in defs:
        r, g, b = defs[flask.request.args['load']]
        dim.set_level(r, g, b)
      return flask.redirect('/')

    elif 'del' in flask.request.args:
      del_color_definition(flask.request.args['del'])
      return flask.redirect('/')
      
    r, g, b = dim.level
    return flask.render_template('main.html',
        red=r, green=g, blue=b,
        red_byte=int(256*r), green_byte=int(256*g), blue_byte=int(256*b),
        color_defs=color_names()
        )

  return app

if __name__ == '__main__':
  from gevent.wsgi import WSGIServer
  import sys
  import argparse

  parser = argparse.ArgumentParser(description='Dim some lights.')
  parser.add_argument(
      '--dimmer', type=str, help='Serial port for RGB dimmer.', default=None)
  parser.add_argument(
      '--scroller', type=str, help='Serial port for scroller.', default=None)
  parser.add_argument(
      '--port', type=int, help='Port to run web service on.', default=80)
  parser.add_argument(
      '--debug', action='store_const', const=True, default=False)
  args = parser.parse_args()

  app = flask_app(
      dimmer.dimmer(args.dimmer), scroller.scroller(args.scroller))
  if args.debug:
    app.run(debug=True)
  else:
    server = WSGIServer(('', args.port), app)
    server.serve_forever()
